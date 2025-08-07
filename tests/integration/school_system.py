"""
🎓 SCHOOL SYSTEM - Simulacra Rancher Education Module
=====================================================

7 Themed Schools with Passive Learning, LP Decay, and Specialization Mechanics
"""

import json
import time
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple
import sqlite3
import os

class SchoolType(Enum):
    """7 themed schools tied to major gameplay systems"""
    CRAFTING = "crafting"
    ARENA = "arena"
    GATHERING = "gathering"
    BREEDING = "breeding"
    ECONOMY = "economy"
    MOD_INFLUENCE = "mod_influence"
    GAMBLING = "gambling"

@dataclass
class SchoolLevel:
    """Individual school level tracking"""
    school_type: SchoolType
    level: int = 0
    learning_points: int = 0
    last_activity: float = 0.0
    decay_start: float = 0.0
    total_time_spent: int = 0
    trivia_answered: int = 0
    bonus_points_earned: int = 0

@dataclass
class PlayerEducation:
    """Complete player education profile"""
    player_id: str
    total_level: int = 0
    schools: Dict[SchoolType, SchoolLevel] = None
    retired: bool = False
    retirement_date: Optional[str] = None
    retirement_rank: Optional[int] = None
    comeback_attempts: int = 0
    
    def __post_init__(self):
        if self.schools is None:
            self.schools = {}
            for school_type in SchoolType:
                self.schools[school_type] = SchoolLevel(school_type=school_type)

class SchoolSystem:
    """Complete school system with passive learning and decay"""
    
    def __init__(self, db_path: str = "data/school_system.db"):
        self.db_path = db_path
        self.initialize_database()
        
        # School configurations
        self.school_configs = {
            SchoolType.CRAFTING: {
                "name": "⚒️ Crafting School",
                "description": "Master the art of creating powerful items",
                "success_rate_bonus": 0.01,  # +1% per level
                "lp_per_minute": 1,
                "decay_rate": 0.1,  # LP lost per hour when inactive
                "max_level": 100,
                "trivia_questions": [
                    "What material is best for fire-resistant armor?",
                    "How do you craft a legendary weapon?",
                    "What's the optimal temperature for smelting?",
                    "Which gem enhances crafting success?",
                    "How do you repair damaged equipment?"
                ]
            },
            SchoolType.ARENA: {
                "name": "⚔️ Arena School",
                "description": "Learn combat techniques and battle strategies",
                "success_rate_bonus": 0.01,
                "lp_per_minute": 1,
                "decay_rate": 0.15,
                "max_level": 100,
                "trivia_questions": [
                    "What's the best counter to a charging opponent?",
                    "How do you break through heavy armor?",
                    "What's the optimal stance for defense?",
                    "Which weapon has the longest reach?",
                    "How do you recover from a knockdown?"
                ]
            },
            SchoolType.GATHERING: {
                "name": "🛠️ Resource Gathering School",
                "description": "Master resource collection and exploration",
                "success_rate_bonus": 0.01,
                "lp_per_minute": 1,
                "decay_rate": 0.08,
                "max_level": 100,
                "trivia_questions": [
                    "Where do you find rare minerals?",
                    "How do you identify valuable resources?",
                    "What tools are best for deep mining?",
                    "How do you avoid cave-ins?",
                    "Which areas have the richest deposits?"
                ]
            },
            SchoolType.BREEDING: {
                "name": "🧪 Breeding School",
                "description": "Study simulacra genetics and breeding techniques",
                "success_rate_bonus": 0.01,
                "lp_per_minute": 1,
                "decay_rate": 0.12,
                "max_level": 100,
                "trivia_questions": [
                    "How do you identify genetic traits?",
                    "What determines offspring quality?",
                    "How do you prevent genetic defects?",
                    "Which breeding pairs produce the best results?",
                    "How do you maintain genetic diversity?"
                ]
            },
            SchoolType.ECONOMY: {
                "name": "💹 Economy School",
                "description": "Master trade, markets, and economic strategies",
                "success_rate_bonus": 0.01,
                "lp_per_minute": 1,
                "decay_rate": 0.1,
                "max_level": 100,
                "trivia_questions": [
                    "How do you identify market trends?",
                    "What's the best time to buy low?",
                    "How do you maximize profit margins?",
                    "Which commodities are most stable?",
                    "How do you hedge against losses?"
                ]
            },
            SchoolType.MOD_INFLUENCE: {
                "name": "🎭 Mod/Influence School",
                "description": "Learn to create and influence game modifications",
                "success_rate_bonus": 0.01,
                "lp_per_minute": 1,
                "decay_rate": 0.2,
                "max_level": 100,
                "trivia_questions": [
                    "How do you balance mod effects?",
                    "What makes a mod popular?",
                    "How do you test mod stability?",
                    "Which mods have the most impact?",
                    "How do you maintain mod compatibility?"
                ]
            },
            SchoolType.GAMBLING: {
                "name": "🎰 Gambling School",
                "description": "Master probability, risk assessment, and betting strategies",
                "success_rate_bonus": 0.01,
                "lp_per_minute": 1,
                "decay_rate": 0.25,
                "max_level": 100,
                "trivia_questions": [
                    "How do you calculate expected value?",
                    "What's the optimal bet sizing strategy?",
                    "How do you manage risk vs reward?",
                    "Which games have the best odds?",
                    "How do you avoid the gambler's fallacy?"
                ]
            }
        }
        
        # Leaderboard tracking
        self.leaderboards = {
            "global_rp": [],
            "battles_won": [],
            "longest_simulacra": [],
            "items_crafted": [],
            "gambling_wins": [],
            "school_levels": []
        }

    def initialize_database(self):
        """Initialize SQLite database for school system"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Player education profiles
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS player_education (
                    player_id TEXT PRIMARY KEY,
                    total_level INTEGER DEFAULT 0,
                    retired BOOLEAN DEFAULT FALSE,
                    retirement_date TEXT,
                    retirement_rank INTEGER,
                    comeback_attempts INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Individual school levels
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS school_levels (
                    player_id TEXT,
                    school_type TEXT,
                    level INTEGER DEFAULT 0,
                    learning_points INTEGER DEFAULT 0,
                    last_activity REAL DEFAULT 0,
                    decay_start REAL DEFAULT 0,
                    total_time_spent INTEGER DEFAULT 0,
                    trivia_answered INTEGER DEFAULT 0,
                    bonus_points_earned INTEGER DEFAULT 0,
                    PRIMARY KEY (player_id, school_type),
                    FOREIGN KEY (player_id) REFERENCES player_education (player_id)
                )
            """)
            
            # Leaderboards
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leaderboards (
                    leaderboard_type TEXT,
                    player_id TEXT,
                    score REAL,
                    rank INTEGER,
                    timestamp REAL,
                    PRIMARY KEY (leaderboard_type, player_id)
                )
            """)
            
            # School trivia questions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trivia_questions (
                    school_type TEXT,
                    question TEXT,
                    answer TEXT,
                    difficulty INTEGER DEFAULT 1,
                    PRIMARY KEY (school_type, question)
                )
            """)
            
            conn.commit()

    def get_or_create_player(self, player_id: str) -> PlayerEducation:
        """Get or create a player's education profile"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if player exists
            cursor.execute("SELECT * FROM player_education WHERE player_id = ?", (player_id,))
            result = cursor.fetchone()
            
            if result:
                # Load existing player
                player = PlayerEducation(
                    player_id=player_id,
                    total_level=result[1],
                    retired=bool(result[2]),
                    retirement_date=result[3],
                    retirement_rank=result[4],
                    comeback_attempts=result[5]
                )
                
                # Load school levels
                cursor.execute("SELECT * FROM school_levels WHERE player_id = ?", (player_id,))
                for row in cursor.fetchall():
                    school_type = SchoolType(row[1])
                    player.schools[school_type] = SchoolLevel(
                        school_type=school_type,
                        level=row[2],
                        learning_points=row[3],
                        last_activity=row[4],
                        decay_start=row[5],
                        total_time_spent=row[6],
                        trivia_answered=row[7],
                        bonus_points_earned=row[8]
                    )
                
                return player
            else:
                # Create new player
                player = PlayerEducation(player_id=player_id)
                cursor.execute("""
                    INSERT INTO player_education (player_id, total_level)
                    VALUES (?, 0)
                """, (player_id,))
                
                # Initialize all schools
                for school_type in SchoolType:
                    cursor.execute("""
                        INSERT INTO school_levels (player_id, school_type, level, learning_points)
                        VALUES (?, ?, 0, 0)
                    """, (player_id, school_type.value))
                
                conn.commit()
                return player

    def attend_school(self, player_id: str, school_type: SchoolType, minutes: int = 1) -> Dict:
        """Player attends a school and gains learning points"""
        player = self.get_or_create_player(player_id)
        school_level = player.schools[school_type]
        config = self.school_configs[school_type]
        
        current_time = time.time()
        
        # Calculate LP gained
        lp_gained = config["lp_per_minute"] * minutes
        
        # Update school level
        school_level.learning_points += lp_gained
        school_level.last_activity = current_time
        school_level.total_time_spent += minutes
        
        # Check for level up
        old_level = school_level.level
        new_level = min(school_level.learning_points // 100, config["max_level"])
        school_level.level = new_level
        
        # Update total level
        old_total = player.total_level
        player.total_level = sum(school.level for school in player.schools.values())
        
        # Save to database
        self._save_player_education(player)
        
        return {
            "player_id": player_id,
            "school": config["name"],
            "lp_gained": lp_gained,
            "total_lp": school_level.learning_points,
            "old_level": old_level,
            "new_level": new_level,
            "leveled_up": new_level > old_level,
            "total_level": player.total_level,
            "total_level_gained": player.total_level - old_total
        }

    def process_decay(self, player_id: str) -> Dict:
        """Process LP decay for inactive schools"""
        player = self.get_or_create_player(player_id)
        current_time = time.time()
        decay_report = {}
        
        for school_type, school_level in player.schools.items():
            config = self.school_configs[school_type]
            
            # Check if school is inactive (more than 1 hour since last activity)
            if current_time - school_level.last_activity > 3600:  # 1 hour
                if school_level.decay_start == 0:
                    school_level.decay_start = current_time
                
                # Calculate decay
                hours_inactive = (current_time - school_level.decay_start) / 3600
                lp_lost = int(config["decay_rate"] * hours_inactive)
                
                if lp_lost > 0:
                    old_lp = school_level.learning_points
                    school_level.learning_points = max(0, school_level.learning_points - lp_lost)
                    lp_actually_lost = old_lp - school_level.learning_points
                    
                    # Check for level down
                    old_level = school_level.level
                    new_level = min(school_level.learning_points // 100, config["max_level"])
                    school_level.level = new_level
                    
                    if lp_actually_lost > 0:
                        decay_report[school_type.value] = {
                            "lp_lost": lp_actually_lost,
                            "old_level": old_level,
                            "new_level": new_level,
                            "leveled_down": new_level < old_level
                        }
        
        # Update total level
        player.total_level = sum(school.level for school in player.schools.values())
        
        # Save changes
        self._save_player_education(player)
        
        return decay_report

    def answer_trivia(self, player_id: str, school_type: SchoolType, answer: str) -> Dict:
        """Player answers school trivia for bonus LP"""
        player = self.get_or_create_player(player_id)
        school_level = player.schools[school_type]
        config = self.school_configs[school_type]
        
        # Simple trivia system (in real implementation, would have actual Q&A)
        is_correct = random.random() < 0.7  # 70% success rate
        
        if is_correct:
            # Bonus LP for correct answer
            bonus_lp = 10 + (school_level.level * 2)  # More bonus at higher levels
            school_level.learning_points += bonus_lp
            school_level.trivia_answered += 1
            school_level.bonus_points_earned += bonus_lp
            
            # Check for level up
            old_level = school_level.level
            new_level = min(school_level.learning_points // 100, config["max_level"])
            school_level.level = new_level
            
            # Update total level
            old_total = player.total_level
            player.total_level = sum(school.level for school in player.schools.values())
            
            # Save changes
            self._save_player_education(player)
            
            return {
                "correct": True,
                "bonus_lp": bonus_lp,
                "new_level": new_level,
                "leveled_up": new_level > old_level,
                "total_level_gained": player.total_level - old_total
            }
        else:
            return {
                "correct": False,
                "bonus_lp": 0,
                "message": "Incorrect answer. Try again!"
            }

    def get_success_rate_bonus(self, player_id: str, school_type: SchoolType) -> float:
        """Get success rate bonus from school level"""
        player = self.get_or_create_player(player_id)
        school_level = player.schools[school_type]
        config = self.school_configs[school_type]
        
        return school_level.level * config["success_rate_bonus"]

    def retire_player(self, player_id: str) -> Dict:
        """Retire a player from leaderboards"""
        player = self.get_or_create_player(player_id)
        
        if player.retired:
            return {"error": "Player already retired"}
        
        # Get current rank before retirement
        current_rank = self._get_player_rank(player_id, "global_rp")
        
        player.retired = True
        player.retirement_date = datetime.now().isoformat()
        player.retirement_rank = current_rank
        
        # Save to database
        self._save_player_education(player)
        
        return {
            "player_id": player_id,
            "retired": True,
            "retirement_date": player.retirement_date,
            "retirement_rank": current_rank,
            "total_level": player.total_level
        }

    def unretire_player(self, player_id: str) -> Dict:
        """Unretire a player (resets all progress)"""
        player = self.get_or_create_player(player_id)
        
        if not player.retired:
            return {"error": "Player not retired"}
        
        # Reset all progress
        for school_level in player.schools.values():
            school_level.level = 0
            school_level.learning_points = 0
            school_level.total_time_spent = 0
            school_level.trivia_answered = 0
            school_level.bonus_points_earned = 0
        
        player.total_level = 0
        player.retired = False
        player.retirement_date = None
        player.retirement_rank = None
        player.comeback_attempts += 1
        
        # Save to database
        self._save_player_education(player)
        
        return {
            "player_id": player_id,
            "unretired": True,
            "comeback_attempts": player.comeback_attempts,
            "message": "All progress reset. Starting fresh!"
        }

    def get_leaderboard(self, leaderboard_type: str, limit: int = 10) -> List[Dict]:
        """Get leaderboard rankings"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT player_id, score, rank, timestamp
                FROM leaderboards 
                WHERE leaderboard_type = ?
                ORDER BY rank ASC
                LIMIT ?
            """, (leaderboard_type, limit))
            
            return [
                {
                    "rank": row[2],
                    "player_id": row[0],
                    "score": row[1],
                    "timestamp": row[3]
                }
                for row in cursor.fetchall()
            ]

    def update_leaderboard(self, leaderboard_type: str, player_id: str, score: float):
        """Update leaderboard score"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get current rank
            cursor.execute("""
                SELECT COUNT(*) + 1 FROM leaderboards 
                WHERE leaderboard_type = ? AND score > ?
            """, (leaderboard_type, score))
            
            new_rank = cursor.fetchone()[0]
            
            # Update or insert
            cursor.execute("""
                INSERT OR REPLACE INTO leaderboards (leaderboard_type, player_id, score, rank, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (leaderboard_type, player_id, score, new_rank, time.time()))
            
            conn.commit()

    def get_player_education_summary(self, player_id: str) -> Dict:
        """Get comprehensive education summary for a player"""
        player = self.get_or_create_player(player_id)
        
        school_summaries = {}
        for school_type, school_level in player.schools.items():
            config = self.school_configs[school_type]
            school_summaries[school_type.value] = {
                "name": config["name"],
                "level": school_level.level,
                "learning_points": school_level.learning_points,
                "success_rate_bonus": self.get_success_rate_bonus(player_id, school_type),
                "total_time_spent": school_level.total_time_spent,
                "trivia_answered": school_level.trivia_answered,
                "bonus_points_earned": school_level.bonus_points_earned,
                "max_level": config["max_level"]
            }
        
        return {
            "player_id": player_id,
            "total_level": player.total_level,
            "retired": player.retired,
            "retirement_date": player.retirement_date,
            "retirement_rank": player.retirement_rank,
            "comeback_attempts": player.comeback_attempts,
            "schools": school_summaries,
            "specialization": self._get_specialization(player),
            "role_strategy": self._get_role_strategy(player)
        }

    def _get_specialization(self, player: PlayerEducation) -> str:
        """Determine player's specialization"""
        max_level = max(school.level for school in player.schools.values())
        max_schools = [school_type for school_type, school in player.schools.items() 
                      if school.level == max_level]
        
        if max_level >= 80:
            if len(max_schools) == 1:
                return f"Specialist ({max_schools[0].value.capitalize()})"
            else:
                return f"Multi-Specialist ({len(max_schools)} schools)"
        elif max_level >= 50:
            return "Advanced Generalist"
        else:
            return "Generalist"

    def _get_role_strategy(self, player: PlayerEducation) -> str:
        """Determine player's role strategy"""
        total_level = player.total_level
        max_level = max(school.level for school in player.schools.values())
        
        if max_level >= 90:
            return "Deep Mastery"
        elif total_level >= 300:
            return "Balanced Expert"
        elif total_level >= 150:
            return "Skilled Generalist"
        else:
            return "Learning Phase"

    def _get_player_rank(self, player_id: str, leaderboard_type: str) -> Optional[int]:
        """Get player's current rank on a leaderboard"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT rank FROM leaderboards 
                WHERE leaderboard_type = ? AND player_id = ?
            """, (leaderboard_type, player_id))
            
            result = cursor.fetchone()
            return result[0] if result else None

    def _save_player_education(self, player: PlayerEducation):
        """Save player education data to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Update player education
            cursor.execute("""
                UPDATE player_education 
                SET total_level = ?, retired = ?, retirement_date = ?, 
                    retirement_rank = ?, comeback_attempts = ?
                WHERE player_id = ?
            """, (player.total_level, player.retired, player.retirement_date,
                  player.retirement_rank, player.comeback_attempts, player.player_id))
            
            # Update school levels
            for school_type, school_level in player.schools.items():
                cursor.execute("""
                    UPDATE school_levels 
                    SET level = ?, learning_points = ?, last_activity = ?,
                        decay_start = ?, total_time_spent = ?, trivia_answered = ?,
                        bonus_points_earned = ?
                    WHERE player_id = ? AND school_type = ?
                """, (school_level.level, school_level.learning_points, school_level.last_activity,
                      school_level.decay_start, school_level.total_time_spent, school_level.trivia_answered,
                      school_level.bonus_points_earned, player.player_id, school_type.value))
            
            conn.commit()

# Example usage and testing
if __name__ == "__main__":
    school_system = SchoolSystem()
    
    # Test player education
    player_id = "test_player_123"
    
    # Attend schools
    result = school_system.attend_school(player_id, SchoolType.CRAFTING, 60)
    print(f"🎓 {result}")
    
    # Answer trivia
    trivia_result = school_system.answer_trivia(player_id, SchoolType.CRAFTING, "iron")
    print(f"🧠 {trivia_result}")
    
    # Get summary
    summary = school_system.get_player_education_summary(player_id)
    print(f"📊 {summary}")
    
    # Process decay
    decay_result = school_system.process_decay(player_id)
    print(f"�� {decay_result}") 
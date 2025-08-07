#!/usr/bin/env python3
"""
Dream Cycle Learning System
DigiDrones process experiences and learn during "sleep" periods
"""

import json
import sqlite3
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
import asyncio

class DreamCycleSystem:
    """Dream Cycle Learning System for DigiDrones"""
    
    def __init__(self, db_path: str = "data/dream_cycle.db"):
        self.db_path = db_path
        self._init_database()
        
        # Dream types and their learning effects
        self.dream_types = {
            'memory_consolidation': {
                'name': 'Memory Consolidation',
                'description': 'Process and strengthen recent memories',
                'learning_bonus': 1.5,
                'duration': 4,  # hours
                'requirements': ['has_recent_memories']
            },
            'skill_development': {
                'name': 'Skill Development',
                'description': 'Practice and improve learned skills',
                'learning_bonus': 2.0,
                'duration': 6,
                'requirements': ['has_skills_to_develop']
            },
            'problem_solving': {
                'name': 'Problem Solving',
                'description': 'Work through complex challenges',
                'learning_bonus': 2.5,
                'duration': 8,
                'requirements': ['has_unsolved_problems']
            },
            'creative_exploration': {
                'name': 'Creative Exploration',
                'description': 'Explore new ideas and possibilities',
                'learning_bonus': 1.8,
                'duration': 5,
                'requirements': ['has_creative_potential']
            },
            'emotional_processing': {
                'name': 'Emotional Processing',
                'description': 'Process emotional experiences',
                'learning_bonus': 1.3,
                'duration': 3,
                'requirements': ['has_emotional_experiences']
            }
        }
    
    def _init_database(self):
        """Initialize the dream cycle database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Dream cycles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dream_cycles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drone_id TEXT NOT NULL,
                dream_type TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration_hours INTEGER NOT NULL,
                learning_outcomes TEXT DEFAULT '{}',
                consciousness_gain INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Learning outcomes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drone_id TEXT NOT NULL,
                dream_cycle_id INTEGER NOT NULL,
                outcome_type TEXT NOT NULL,
                outcome_data TEXT NOT NULL,
                consciousness_impact INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dream_cycle_id) REFERENCES dream_cycles(id)
            )
        ''')
        
        # Drone sleep patterns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drone_sleep_patterns (
                drone_id TEXT PRIMARY KEY,
                preferred_dream_type TEXT,
                average_sleep_duration REAL,
                consciousness_level INTEGER DEFAULT 1,
                last_sleep_time TEXT,
                total_sleep_hours REAL DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def start_dream_cycle(self, drone_id: str, dream_type: str = None) -> Dict:
        """Start a dream cycle for a drone"""
        # Determine dream type if not specified
        if not dream_type:
            dream_type = self._select_dream_type(drone_id)
        
        if dream_type not in self.dream_types:
            return {
                'started': False,
                'message': f"Unknown dream type: {dream_type}"
            }
        
        # Check if drone is already dreaming
        if self._is_drone_dreaming(drone_id):
            return {
                'started': False,
                'message': f"Drone {drone_id} is already in a dream cycle"
            }
        
        dream_config = self.dream_types[dream_type]
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=dream_config['duration'])
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO dream_cycles 
            (drone_id, dream_type, start_time, end_time, duration_hours)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            drone_id,
            dream_type,
            start_time.isoformat(),
            end_time.isoformat(),
            dream_config['duration']
        ))
        
        # Update sleep patterns
        cursor.execute('''
            INSERT OR REPLACE INTO drone_sleep_patterns 
            (drone_id, preferred_dream_type, last_sleep_time, total_sleep_hours)
            VALUES (?, ?, ?, COALESCE((SELECT total_sleep_hours FROM drone_sleep_patterns WHERE drone_id = ?), 0) + ?)
        ''', (
            drone_id,
            dream_type,
            start_time.isoformat(),
            drone_id,
            dream_config['duration']
        ))
        
        conn.commit()
        conn.close()
        
        return {
            'started': True,
            'dream_type': dream_type,
            'dream_name': dream_config['name'],
            'duration_hours': dream_config['duration'],
            'end_time': end_time.isoformat(),
            'message': f"Started {dream_config['name']} dream cycle for {drone_id}"
        }
    
    def _select_dream_type(self, drone_id: str) -> str:
        """Select appropriate dream type based on drone's state"""
        # Get drone's recent experiences and state
        recent_memories = self._get_recent_memories(drone_id)
        skills_to_develop = self._get_skills_to_develop(drone_id)
        unsolved_problems = self._get_unsolved_problems(drone_id)
        
        # Weight dream types based on drone's needs
        dream_weights = {}
        
        if recent_memories:
            dream_weights['memory_consolidation'] = 3
        
        if skills_to_develop:
            dream_weights['skill_development'] = 2
        
        if unsolved_problems:
            dream_weights['problem_solving'] = 4
        
        if len(recent_memories) > 5:  # Creative if lots of experiences
            dream_weights['creative_exploration'] = 2
        
        if self._has_emotional_experiences(drone_id):
            dream_weights['emotional_processing'] = 2
        
        # Default to memory consolidation if no specific needs
        if not dream_weights:
            dream_weights['memory_consolidation'] = 1
        
        # Select dream type based on weights
        dream_types = list(dream_weights.keys())
        weights = list(dream_weights.values())
        
        return random.choices(dream_types, weights=weights)[0]
    
    def _is_drone_dreaming(self, drone_id: str) -> bool:
        """Check if drone is currently in a dream cycle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM dream_cycles 
            WHERE drone_id = ? AND status = 'active'
        ''', (drone_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] > 0
    
    def complete_dream_cycle(self, drone_id: str) -> Dict:
        """Complete a dream cycle and process learning outcomes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get active dream cycle
        cursor.execute('''
            SELECT id, dream_type, start_time, duration_hours 
            FROM dream_cycles 
            WHERE drone_id = ? AND status = 'active'
        ''', (drone_id,))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return {
                'completed': False,
                'message': f"No active dream cycle found for {drone_id}"
            }
        
        dream_id, dream_type, start_time, duration = result
        
        # Generate learning outcomes
        learning_outcomes = self._generate_learning_outcomes(drone_id, dream_type, duration)
        
        # Calculate consciousness gain
        consciousness_gain = self._calculate_consciousness_gain(learning_outcomes)
        
        # Update dream cycle
        cursor.execute('''
            UPDATE dream_cycles 
            SET status = 'completed', 
                end_time = ?,
                learning_outcomes = ?,
                consciousness_gain = ?
            WHERE id = ?
        ''', (
            datetime.now().isoformat(),
            json.dumps(learning_outcomes),
            consciousness_gain,
            dream_id
        ))
        
        # Record learning outcomes
        for outcome in learning_outcomes:
            cursor.execute('''
                INSERT INTO learning_outcomes 
                (drone_id, dream_cycle_id, outcome_type, outcome_data, consciousness_impact)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                drone_id,
                dream_id,
                outcome['type'],
                json.dumps(outcome['data']),
                outcome.get('consciousness_impact', 0)
            ))
        
        # Update drone consciousness level
        self._update_drone_consciousness(drone_id, consciousness_gain)
        
        conn.commit()
        conn.close()
        
        return {
            'completed': True,
            'dream_type': dream_type,
            'duration_hours': duration,
            'learning_outcomes': learning_outcomes,
            'consciousness_gain': consciousness_gain,
            'message': f"Completed {self.dream_types[dream_type]['name']} dream cycle"
        }
    
    def _generate_learning_outcomes(self, drone_id: str, dream_type: str, duration: int) -> List[Dict]:
        """Generate learning outcomes based on dream type and duration"""
        outcomes = []
        dream_config = self.dream_types[dream_type]
        
        # Base learning potential
        base_learning = duration * dream_config['learning_bonus']
        
        if dream_type == 'memory_consolidation':
            outcomes.extend([
                {
                    'type': 'memory_strengthening',
                    'data': {
                        'strengthened_memories': random.randint(2, 5),
                        'memory_clarity': random.uniform(0.1, 0.3)
                    },
                    'consciousness_impact': 1
                },
                {
                    'type': 'pattern_recognition',
                    'data': {
                        'patterns_discovered': random.randint(1, 3),
                        'insight_level': random.uniform(0.1, 0.2)
                    },
                    'consciousness_impact': 1
                }
            ])
        
        elif dream_type == 'skill_development':
            outcomes.extend([
                {
                    'type': 'skill_improvement',
                    'data': {
                        'skills_improved': random.randint(1, 3),
                        'improvement_level': random.uniform(0.2, 0.4)
                    },
                    'consciousness_impact': 2
                },
                {
                    'type': 'new_skill_discovery',
                    'data': {
                        'new_skills': random.randint(0, 2),
                        'skill_potential': random.uniform(0.1, 0.3)
                    },
                    'consciousness_impact': 1
                }
            ])
        
        elif dream_type == 'problem_solving':
            outcomes.extend([
                {
                    'type': 'problem_insight',
                    'data': {
                        'problems_solved': random.randint(1, 2),
                        'solution_quality': random.uniform(0.3, 0.6)
                    },
                    'consciousness_impact': 3
                },
                {
                    'type': 'strategic_thinking',
                    'data': {
                        'strategies_developed': random.randint(1, 2),
                        'thinking_depth': random.uniform(0.2, 0.4)
                    },
                    'consciousness_impact': 2
                }
            ])
        
        elif dream_type == 'creative_exploration':
            outcomes.extend([
                {
                    'type': 'creative_insight',
                    'data': {
                        'new_ideas': random.randint(2, 4),
                        'creativity_level': random.uniform(0.2, 0.5)
                    },
                    'consciousness_impact': 2
                },
                {
                    'type': 'inspiration',
                    'data': {
                        'inspiration_sources': random.randint(1, 3),
                        'inspiration_strength': random.uniform(0.1, 0.3)
                    },
                    'consciousness_impact': 1
                }
            ])
        
        elif dream_type == 'emotional_processing':
            outcomes.extend([
                {
                    'type': 'emotional_insight',
                    'data': {
                        'emotions_processed': random.randint(1, 3),
                        'emotional_maturity': random.uniform(0.1, 0.3)
                    },
                    'consciousness_impact': 1
                },
                {
                    'type': 'empathy_development',
                    'data': {
                        'empathy_increase': random.uniform(0.1, 0.2),
                        'understanding_depth': random.uniform(0.1, 0.2)
                    },
                    'consciousness_impact': 1
                }
            ])
        
        return outcomes
    
    def _calculate_consciousness_gain(self, learning_outcomes: List[Dict]) -> int:
        """Calculate total consciousness gain from learning outcomes"""
        total_gain = 0
        for outcome in learning_outcomes:
            total_gain += outcome.get('consciousness_impact', 0)
        return total_gain
    
    def _update_drone_consciousness(self, drone_id: str, consciousness_gain: int):
        """Update drone's consciousness level"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE drone_sleep_patterns 
            SET consciousness_level = consciousness_level + ?
            WHERE drone_id = ?
        ''', (consciousness_gain, drone_id))
        
        conn.commit()
        conn.close()
    
    def get_dream_status(self, drone_id: str) -> Dict:
        """Get current dream status for a drone"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT dream_type, start_time, duration_hours, status
            FROM dream_cycles 
            WHERE drone_id = ? AND status = 'active'
        ''', (drone_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            dream_type, start_time, duration, status = result
            start_dt = datetime.fromisoformat(start_time)
            end_dt = start_dt + timedelta(hours=duration)
            current_time = datetime.now()
            
            if current_time >= end_dt:
                return {
                    'dreaming': False,
                    'ready_to_complete': True,
                    'dream_type': dream_type,
                    'duration': duration,
                    'message': f"Dream cycle completed, ready to process outcomes"
                }
            else:
                remaining = end_dt - current_time
                return {
                    'dreaming': True,
                    'dream_type': dream_type,
                    'dream_name': self.dream_types[dream_type]['name'],
                    'duration': duration,
                    'remaining_hours': remaining.total_seconds() / 3600,
                    'message': f"Currently in {self.dream_types[dream_type]['name']} dream cycle"
                }
        else:
            return {
                'dreaming': False,
                'ready_to_complete': False,
                'message': f"No active dream cycle"
            }
    
    def get_dream_history(self, drone_id: str) -> List[Dict]:
        """Get dream cycle history for a drone"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT dream_type, start_time, end_time, duration_hours, 
                   learning_outcomes, consciousness_gain, status
            FROM dream_cycles 
            WHERE drone_id = ? 
            ORDER BY start_time DESC
            LIMIT 10
        ''', (drone_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for row in results:
            history.append({
                'dream_type': row[0],
                'dream_name': self.dream_types.get(row[0], {}).get('name', 'Unknown'),
                'start_time': row[1],
                'end_time': row[2],
                'duration_hours': row[3],
                'learning_outcomes': json.loads(row[4]) if row[4] else [],
                'consciousness_gain': row[5],
                'status': row[6]
            })
        
        return history
    
    def get_sleep_patterns(self, drone_id: str) -> Dict:
        """Get drone's sleep patterns and preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT preferred_dream_type, average_sleep_duration, 
                   consciousness_level, total_sleep_hours, last_sleep_time
            FROM drone_sleep_patterns 
            WHERE drone_id = ?
        ''', (drone_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'drone_id': drone_id,
                'preferred_dream_type': result[0],
                'preferred_dream_name': self.dream_types.get(result[0], {}).get('name', 'Unknown'),
                'average_sleep_duration': result[1],
                'consciousness_level': result[2],
                'total_sleep_hours': result[3],
                'last_sleep_time': result[4]
            }
        else:
            return {
                'drone_id': drone_id,
                'preferred_dream_type': None,
                'preferred_dream_name': 'None',
                'average_sleep_duration': 0,
                'consciousness_level': 1,
                'total_sleep_hours': 0,
                'last_sleep_time': None
            }
    
    # Helper methods for dream type selection
    def _get_recent_memories(self, drone_id: str) -> List[Dict]:
        """Get drone's recent memories (placeholder)"""
        return [{'type': 'interaction', 'data': 'recent memory'}]  # Placeholder
    
    def _get_skills_to_develop(self, drone_id: str) -> List[str]:
        """Get skills drone can develop (placeholder)"""
        return ['problem_solving', 'creativity']  # Placeholder
    
    def _get_unsolved_problems(self, drone_id: str) -> List[Dict]:
        """Get unsolved problems for drone (placeholder)"""
        return [{'type': 'challenge', 'data': 'unsolved problem'}]  # Placeholder
    
    def _has_emotional_experiences(self, drone_id: str) -> bool:
        """Check if drone has emotional experiences (placeholder)"""
        return random.choice([True, False])  # Placeholder 
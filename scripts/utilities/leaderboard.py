#!/usr/bin/env python3
"""
Exclusive Leaderboard System
Top 10 only display to create FOMO and competitive engagement
"""

import json
import sqlite3
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class LeaderboardEntry:
    discord_id: str
    username: str
    ticks_survived: int
    drones_used: int
    rp_earned: int
    record_date: datetime
    server_id: str = None
    
    def to_dict(self) -> Dict:
        return {
            'discord_id': self.discord_id,
            'username': self.username,
            'ticks_survived': self.ticks_survived,
            'drones_used': self.drones_used,
            'rp_earned': self.rp_earned,
            'record_date': self.record_date.isoformat(),
            'server_id': self.server_id
        }

class ExclusiveLeaderboard:
    """Exclusive Leaderboard System - Top 10 Only"""
    
    def __init__(self, db_path: str = "data/leaderboard.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the leaderboard database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create leaderboard table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_id TEXT NOT NULL,
                username TEXT NOT NULL,
                ticks_survived INTEGER NOT NULL,
                drones_used INTEGER NOT NULL,
                rp_earned INTEGER NOT NULL,
                record_date TEXT NOT NULL,
                server_id TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_ticks_survived 
            ON leaderboard(ticks_survived DESC)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_discord_id 
            ON leaderboard(discord_id)
        ''')
        
        conn.commit()
        conn.close()
    
    def submit_record(self, entry: LeaderboardEntry) -> Dict:
        """Submit a new leaderboard record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if this is a new record for the user
        cursor.execute('''
            SELECT ticks_survived FROM leaderboard 
            WHERE discord_id = ? 
            ORDER BY ticks_survived DESC 
            LIMIT 1
        ''', (entry.discord_id,))
        
        existing_record = cursor.fetchone()
        is_new_record = True
        
        if existing_record:
            existing_ticks = existing_record[0]
            if entry.ticks_survived <= existing_ticks:
                is_new_record = False
        
        # Insert new record
        cursor.execute('''
            INSERT INTO leaderboard 
            (discord_id, username, ticks_survived, drones_used, rp_earned, record_date, server_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry.discord_id,
            entry.username,
            entry.ticks_survived,
            entry.drones_used,
            entry.rp_earned,
            entry.record_date.isoformat(),
            entry.server_id
        ))
        
        # Get current ranking
        ranking = self._get_player_ranking(entry.discord_id)
        
        conn.commit()
        conn.close()
        
        return {
            'submitted': True,
            'is_new_record': is_new_record,
            'ranking': ranking,
            'in_top_10': ranking <= 10 if ranking else False
        }
    
    def get_top_10(self, server_id: str = None) -> List[Dict]:
        """Get top 10 leaderboard entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if server_id:
            cursor.execute('''
                SELECT discord_id, username, ticks_survived, drones_used, rp_earned, record_date
                FROM leaderboard 
                WHERE server_id = ?
                ORDER BY ticks_survived DESC 
                LIMIT 10
            ''', (server_id,))
        else:
            cursor.execute('''
                SELECT discord_id, username, ticks_survived, drones_used, rp_earned, record_date
                FROM leaderboard 
                ORDER BY ticks_survived DESC 
                LIMIT 10
            ''')
        
        results = cursor.fetchall()
        conn.close()
        
        leaderboard = []
        for i, row in enumerate(results, 1):
            leaderboard.append({
                'rank': i,
                'discord_id': row[0],
                'username': row[1],
                'ticks_survived': row[2],
                'drones_used': row[3],
                'rp_earned': row[4],
                'record_date': datetime.fromisoformat(row[5]).strftime('%Y-%m-%d')
            })
        
        return leaderboard
    
    def get_player_stats(self, discord_id: str, server_id: str = None) -> Dict:
        """Get detailed stats for a player"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if server_id:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_runs,
                    MAX(ticks_survived) as best_run,
                    AVG(ticks_survived) as avg_run,
                    SUM(rp_earned) as total_rp,
                    MAX(record_date) as last_run
                FROM leaderboard 
                WHERE discord_id = ? AND server_id = ?
            ''', (discord_id, server_id))
        else:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_runs,
                    MAX(ticks_survived) as best_run,
                    AVG(ticks_survived) as avg_run,
                    SUM(rp_earned) as total_rp,
                    MAX(record_date) as last_run
                FROM leaderboard 
                WHERE discord_id = ?
            ''', (discord_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result or result[0] == 0:
            return {
                'total_runs': 0,
                'best_run': 0,
                'avg_run': 0,
                'total_rp': 0,
                'last_run': None,
                'ranking': None
            }
        
        ranking = self._get_player_ranking(discord_id, server_id)
        
        return {
            'total_runs': result[0],
            'best_run': result[1],
            'avg_run': round(result[2], 1) if result[2] else 0,
            'total_rp': result[3],
            'last_run': datetime.fromisoformat(result[4]).strftime('%Y-%m-%d') if result[4] else None,
            'ranking': ranking,
            'in_top_10': ranking <= 10 if ranking else False
        }
    
    def _get_player_ranking(self, discord_id: str, server_id: str = None) -> Optional[int]:
        """Get player's current ranking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get player's best run
        if server_id:
            cursor.execute('''
                SELECT MAX(ticks_survived) FROM leaderboard 
                WHERE discord_id = ? AND server_id = ?
            ''', (discord_id, server_id))
        else:
            cursor.execute('''
                SELECT MAX(ticks_survived) FROM leaderboard 
                WHERE discord_id = ?
            ''', (discord_id,))
        
        player_best = cursor.fetchone()[0]
        
        if not player_best:
            conn.close()
            return None
        
        # Count how many players have better scores
        if server_id:
            cursor.execute('''
                SELECT COUNT(*) FROM leaderboard 
                WHERE ticks_survived > ? AND server_id = ?
            ''', (player_best, server_id))
        else:
            cursor.execute('''
                SELECT COUNT(*) FROM leaderboard 
                WHERE ticks_survived > ?
            ''', (player_best,))
        
        better_players = cursor.fetchone()[0]
        ranking = better_players + 1
        
        conn.close()
        return ranking
    
    def get_leaderboard_display(self, server_id: str = None) -> str:
        """Generate formatted leaderboard display"""
        top_10 = self.get_top_10(server_id)
        
        if not top_10:
            return "🏆 **DIGIRANCHER SURVIVAL LEADERBOARD** 🏆\n" + \
                   "==========================================\n" + \
                   "No records yet! Be the first to survive!"
        
        display = "🏆 **DIGIRANCHER SURVIVAL LEADERBOARD** 🏆\n"
        display += "==========================================\n"
        
        for entry in top_10:
            rank_emoji = self._get_rank_emoji(entry['rank'])
            display += f"{rank_emoji} **{entry['username']}** {entry['ticks_survived']} ticks ({entry['record_date']})\n"
        
        display += "\n❓ Your ranking: Hidden (not in top 10)\n"
        display += "💡 Keep trying to break into the leaderboard!"
        
        return display
    
    def _get_rank_emoji(self, rank: int) -> str:
        """Get emoji for rank position"""
        emojis = {
            1: "🥇",
            2: "🥈", 
            3: "🥉",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣",
            10: "🔟"
        }
        return emojis.get(rank, f"{rank}.")
    
    def get_player_ranking_message(self, discord_id: str, server_id: str = None) -> str:
        """Get personalized ranking message for player"""
        stats = self.get_player_stats(discord_id, server_id)
        
        if stats['total_runs'] == 0:
            return "❓ **Your Ranking**: No records yet\n" + \
                   "💡 Start your first simulation to get ranked!"
        
        if stats['in_top_10']:
            return f"🏆 **Your Ranking**: #{stats['ranking']}\n" + \
                   f"🎯 Best Run: {stats['best_run']} ticks\n" + \
                   f"📊 Total Runs: {stats['total_runs']}\n" + \
                   f"💰 Total RP Earned: {stats['total_rp']}"
        else:
            return f"❓ **Your Ranking**: Hidden (not in top 10)\n" + \
                   f"🎯 Best Run: {stats['best_run']} ticks\n" + \
                   f"📊 Total Runs: {stats['total_runs']}\n" + \
                   f"💰 Total RP Earned: {stats['total_rp']}\n" + \
                   f"💡 Keep trying to break into the top 10!"
    
    def get_achievements(self, discord_id: str, server_id: str = None) -> List[Dict]:
        """Get player achievements"""
        stats = self.get_player_stats(discord_id, server_id)
        achievements = []
        
        if stats['total_runs'] >= 1:
            achievements.append({
                'name': 'First Steps',
                'description': 'Complete your first simulation',
                'unlocked': True
            })
        
        if stats['total_runs'] >= 10:
            achievements.append({
                'name': 'Dedicated Survivor',
                'description': 'Complete 10 simulations',
                'unlocked': True
            })
        
        if stats['best_run'] >= 100:
            achievements.append({
                'name': 'Century Survivor',
                'description': 'Survive 100 ticks in one run',
                'unlocked': True
            })
        
        if stats['best_run'] >= 500:
            achievements.append({
                'name': 'Legendary Survivor',
                'description': 'Survive 500 ticks in one run',
                'unlocked': True
            })
        
        if stats['in_top_10']:
            achievements.append({
                'name': 'Top 10 Elite',
                'description': 'Break into the top 10 leaderboard',
                'unlocked': True
            })
        
        if stats['ranking'] == 1:
            achievements.append({
                'name': 'Champion',
                'description': 'Achieve #1 on the leaderboard',
                'unlocked': True
            })
        
        return achievements
    
    def get_global_stats(self) -> Dict:
        """Get global leaderboard statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT discord_id) as total_players,
                COUNT(*) as total_runs,
                MAX(ticks_survived) as best_record,
                AVG(ticks_survived) as avg_record,
                SUM(rp_earned) as total_rp_earned
            FROM leaderboard
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total_players': result[0],
            'total_runs': result[1],
            'best_record': result[2],
            'avg_record': round(result[3], 1) if result[3] else 0,
            'total_rp_earned': result[4]
        }
    
    def cleanup_old_records(self, days_to_keep: int = 30):
        """Clean up old leaderboard records"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM leaderboard 
            WHERE record_date < ?
        ''', (cutoff_date.isoformat(),))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count 
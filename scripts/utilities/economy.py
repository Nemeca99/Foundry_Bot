#!/usr/bin/env python3
"""
Enhanced Economy System with Entropy Compression and Global Multiplier
====================================================================
"""

import json
import time
import random
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import sqlite3
import os


@dataclass
class EconomyTransaction:
    """Detailed transaction logging"""

    user_id: str
    amount: int
    transaction_type: str  # "earn" or "spend"
    reason: str
    timestamp: float
    global_multiplier: float
    entropy_cost: int = 0
    success_rate_bonus: float = 0.0


class EnhancedEconomySystem:
    """Enhanced economy with entropy compression and global multiplier"""

    def __init__(self, db_path: str = "data/economy.db"):
        self.db_path = db_path
        self.initialize_database()

        # Global multiplier system
        self.global_multiplier = 1.0
        self.drones_alive = 0
        self.active_players = 0
        self.drones_ever_died = 1  # Prevent division by zero

        # Entropy compression settings
        self.base_costs = {
            "hunt": 50,
            "mod": 100,
            "economy": 75,
            "fight": 25,
            "school_attendance": 10,
            "trivia_answer": 5,
        }

    def initialize_database(self):
        """Initialize SQLite database for economy system"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # User RP balances
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_balances (
                    user_id TEXT PRIMARY KEY,
                    rp_balance INTEGER DEFAULT 0,
                    total_earned INTEGER DEFAULT 0,
                    total_spent INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Transaction history
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    amount INTEGER,
                    transaction_type TEXT,
                    reason TEXT,
                    timestamp REAL,
                    global_multiplier REAL,
                    entropy_cost INTEGER DEFAULT 0,
                    success_rate_bonus REAL DEFAULT 0.0
                )
            """
            )

            # Global multiplier tracking
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS global_multiplier (
                    id INTEGER PRIMARY KEY,
                    multiplier REAL DEFAULT 1.0,
                    drones_alive INTEGER DEFAULT 0,
                    active_players INTEGER DEFAULT 0,
                    drones_ever_died INTEGER DEFAULT 1,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()

    def update_global_multiplier(
        self, drones_alive: int, active_players: int, drones_ever_died: int
    ):
        """Update global multiplier based on game state"""
        self.drones_alive = drones_alive
        self.active_players = active_players
        self.drones_ever_died = max(1, drones_ever_died)  # Prevent division by zero

        # Calculate multiplier: (drones_alive * active_players) / drones_ever_died
        raw_multiplier = (
            self.drones_alive * self.active_players
        ) / self.drones_ever_died

        # Apply caps: 0.1x minimum, 3.0x maximum
        self.global_multiplier = max(0.1, min(3.0, raw_multiplier))

        # Save to database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO global_multiplier 
                (id, multiplier, drones_alive, active_players, drones_ever_died, last_updated)
                VALUES (1, ?, ?, ?, ?, ?)
            """,
                (
                    self.global_multiplier,
                    self.drones_alive,
                    self.active_players,
                    self.drones_ever_died,
                    datetime.now().isoformat(),
                ),
            )
            conn.commit()

    def get_current_multiplier(self) -> float:
        """Get current global multiplier"""
        return self.global_multiplier

    def calculate_entropy_cost(
        self, activity_type: str, ticks_requested: int, success_rate_bonus: float = 0.0
    ) -> int:
        """Calculate entropy compression cost for multi-tick activities"""
        base_cost = self.base_costs.get(activity_type, 50)

        # Apply success rate bonus to base cost
        modified_base_cost = int(base_cost * (1 + success_rate_bonus))

        # Apply global multiplier FIRST
        global_modified_cost = int(modified_base_cost * self.global_multiplier)

        # Ensure minimum cost of 1 RP
        if global_modified_cost < 1:
            global_modified_cost = 1

        if ticks_requested <= 1:
            return global_modified_cost

        # Entropy compression: (base_cost * 2) * ticks_requested
        base_over_cost = global_modified_cost * 2
        compression_cost = base_over_cost * ticks_requested

        return int(compression_cost)

    def earn_rp(
        self,
        user_id: str,
        amount: int,
        reason: str = "Activity",
        success_rate_bonus: float = 0.0,
    ) -> int:
        """Earn RP with global multiplier and success rate bonus"""
        # Apply success rate bonus to earned amount
        bonus_amount = int(amount * success_rate_bonus)
        total_earned = amount + bonus_amount

        # Apply global multiplier
        final_amount = int(total_earned * self.global_multiplier)

        # Get current balance
        current_balance = self.get_user_rp(user_id)
        new_balance = current_balance + final_amount

        # Update database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Update user balance
            cursor.execute(
                """
                INSERT OR REPLACE INTO user_balances 
                (user_id, rp_balance, total_earned, last_updated)
                VALUES (?, ?, ?, ?)
            """,
                (user_id, new_balance, final_amount, datetime.now().isoformat()),
            )

            # Log transaction
            transaction = EconomyTransaction(
                user_id=user_id,
                amount=final_amount,
                transaction_type="earn",
                reason=reason,
                timestamp=time.time(),
                global_multiplier=self.global_multiplier,
                success_rate_bonus=success_rate_bonus,
            )

            cursor.execute(
                """
                INSERT INTO transactions 
                (user_id, amount, transaction_type, reason, timestamp, global_multiplier, success_rate_bonus)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    transaction.user_id,
                    transaction.amount,
                    transaction.transaction_type,
                    transaction.reason,
                    transaction.timestamp,
                    transaction.global_multiplier,
                    transaction.success_rate_bonus,
                ),
            )

            conn.commit()

        return final_amount

    def spend_rp(self, user_id: str, amount: int, reason: str = "Activity") -> bool:
        """Spend RP with entropy compression"""
        current_balance = self.get_user_rp(user_id)

        if current_balance < amount:
            return False

        new_balance = current_balance - amount

        # Update database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Update user balance
            cursor.execute(
                """
                UPDATE user_balances 
                SET rp_balance = ?, total_spent = total_spent + ?, last_updated = ?
                WHERE user_id = ?
            """,
                (new_balance, amount, datetime.now().isoformat(), user_id),
            )

            # Log transaction
            transaction = EconomyTransaction(
                user_id=user_id,
                amount=amount,
                transaction_type="spend",
                reason=reason,
                timestamp=time.time(),
                global_multiplier=self.global_multiplier,
            )

            cursor.execute(
                """
                INSERT INTO transactions 
                (user_id, amount, transaction_type, reason, timestamp, global_multiplier)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    transaction.user_id,
                    transaction.amount,
                    transaction.transaction_type,
                    transaction.reason,
                    transaction.timestamp,
                    transaction.global_multiplier,
                ),
            )

            conn.commit()

        return True

    def get_user_rp(self, user_id: str) -> int:
        """Get user's current RP balance"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT rp_balance FROM user_balances WHERE user_id = ?", (user_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else 0

    def check_daily_bonus(self, user_id: str) -> Optional[int]:
        """Check and award daily RP bonus"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Check if user already got bonus today
            cursor.execute(
                """
                SELECT last_updated FROM user_balances WHERE user_id = ?
            """,
                (user_id,),
            )
            result = cursor.fetchone()

            if result:
                last_updated = datetime.fromisoformat(result[0])
                today = datetime.now().date()

                if last_updated.date() < today:
                    # Award daily bonus
                    bonus_amount = 100  # Base daily bonus
                    final_bonus = int(bonus_amount * self.global_multiplier)

                    self.earn_rp(user_id, final_bonus, "Daily Bonus")
                    return final_bonus

            return None

    def get_transaction_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get user's transaction history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT amount, transaction_type, reason, timestamp, global_multiplier, success_rate_bonus
                FROM transactions 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """,
                (user_id, limit),
            )

            return [
                {
                    "amount": row[0],
                    "type": row[1],
                    "reason": row[2],
                    "timestamp": row[3],
                    "global_multiplier": row[4],
                    "success_rate_bonus": row[5],
                }
                for row in cursor.fetchall()
            ]

    def get_economy_summary(self) -> Dict:
        """Get comprehensive economy summary"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total users with RP
            cursor.execute("SELECT COUNT(*) FROM user_balances")
            total_users = cursor.fetchone()[0]

            # Total RP in circulation
            cursor.execute("SELECT SUM(rp_balance) FROM user_balances")
            total_rp = cursor.fetchone()[0] or 0

            # Total earned/spent
            cursor.execute(
                "SELECT SUM(total_earned), SUM(total_spent) FROM user_balances"
            )
            result = cursor.fetchone()
            total_earned = result[0] or 0
            total_spent = result[1] or 0

            return {
                "global_multiplier": self.global_multiplier,
                "drones_alive": self.drones_alive,
                "active_players": self.active_players,
                "drones_ever_died": self.drones_ever_died,
                "total_users": total_users,
                "total_rp_circulation": total_rp,
                "total_rp_earned": total_earned,
                "total_rp_spent": total_spent,
                "economy_health": (
                    "healthy" if total_earned > total_spent else "declining"
                ),
            }

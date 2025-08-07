#!/usr/bin/env python3
"""
Trade System for Player-to-Player Trading
Fixed prices with auto-exchange functionality
"""

import asyncio
import random
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ItemType(Enum):
    """Item types for trading"""

    RESOURCE = "resource"
    FOOD = "food"
    EQUIPMENT = "equipment"
    COSMETIC = "cosmetic"


@dataclass
class TradeItem:
    """An item that can be traded"""

    item_id: str
    item_type: ItemType
    name: str
    description: str
    base_price: int  # Fixed price in RP
    rarity: str = "common"  # common, uncommon, rare, epic, legendary


@dataclass
class TradeOffer:
    """A trade offer between players"""

    offer_id: str
    seller_id: str
    buyer_id: str
    item_id: str
    quantity: int
    price: int
    created_at: datetime
    expires_at: datetime
    status: str = "pending"  # pending, accepted, declined, expired


class TradeSystem:
    """Trade system for player-to-player trading"""

    def __init__(self, db_path: str = "data/trade.db"):
        self.db_path = db_path
        self._init_database()
        self._init_items()
        self.active_offers = {}  # offer_id -> TradeOffer

    def _init_database(self):
        """Initialize trade database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Trade offers table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS trade_offers (
                    offer_id TEXT PRIMARY KEY,
                    seller_id TEXT NOT NULL,
                    buyer_id TEXT NOT NULL,
                    item_id TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    status TEXT DEFAULT 'pending'
                )
            """
            )

            # Trade history table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS trade_history (
                    trade_id TEXT PRIMARY KEY,
                    seller_id TEXT NOT NULL,
                    buyer_id TEXT NOT NULL,
                    item_id TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    trade_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Player inventory table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS player_inventory (
                    user_id TEXT,
                    item_id TEXT,
                    quantity INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, item_id)
                )
            """
            )

    def _init_items(self):
        """Initialize tradeable items"""
        self.tradeable_items = {
            # Resources
            "wood": TradeItem(
                "wood", ItemType.RESOURCE, "Wood", "Basic building material", 10
            ),
            "stone": TradeItem(
                "stone", ItemType.RESOURCE, "Stone", "Durable construction material", 15
            ),
            "metal": TradeItem(
                "metal", ItemType.RESOURCE, "Metal", "Strong industrial material", 25
            ),
            "crystal": TradeItem(
                "crystal", ItemType.RESOURCE, "Crystal", "Rare magical material", 50
            ),
            "essence": TradeItem(
                "essence", ItemType.RESOURCE, "Essence", "Pure magical energy", 100
            ),
            # Food items
            "basic_food": TradeItem(
                "basic_food", ItemType.FOOD, "Basic Food", "Simple nourishment", 5
            ),
            "quality_food": TradeItem(
                "quality_food", ItemType.FOOD, "Quality Food", "Nutritious meal", 15
            ),
            "premium_food": TradeItem(
                "premium_food", ItemType.FOOD, "Premium Food", "Delicious feast", 30
            ),
            "magical_food": TradeItem(
                "magical_food",
                ItemType.FOOD,
                "Magical Food",
                "Enchanted sustenance",
                75,
            ),
            # Equipment
            "basic_armor": TradeItem(
                "basic_armor",
                ItemType.EQUIPMENT,
                "Basic Armor",
                "Simple protection",
                50,
            ),
            "quality_armor": TradeItem(
                "quality_armor",
                ItemType.EQUIPMENT,
                "Quality Armor",
                "Good protection",
                150,
            ),
            "magical_armor": TradeItem(
                "magical_armor",
                ItemType.EQUIPMENT,
                "Magical Armor",
                "Enchanted protection",
                300,
            ),
            # Cosmetics
            "shiny_coat": TradeItem(
                "shiny_coat",
                ItemType.COSMETIC,
                "Shiny Coat",
                "Makes Simulacra sparkle",
                200,
                "rare",
            ),
            "glowing_eyes": TradeItem(
                "glowing_eyes",
                ItemType.COSMETIC,
                "Glowing Eyes",
                "Eyes that glow",
                300,
                "epic",
            ),
            "rainbow_trail": TradeItem(
                "rainbow_trail",
                ItemType.COSMETIC,
                "Rainbow Trail",
                "Colorful movement trail",
                500,
                "legendary",
            ),
        }

    def create_trade_offer(
        self, seller_id: str, buyer_id: str, item_id: str, quantity: int, price: int
    ) -> Dict:
        """Create a new trade offer"""
        if item_id not in self.tradeable_items:
            return {"success": False, "error": "Invalid item"}

        if quantity <= 0:
            return {"success": False, "error": "Quantity must be positive"}

        if price <= 0:
            return {"success": False, "error": "Price must be positive"}

        # Check if seller has enough items
        seller_inventory = self.get_user_inventory(seller_id)
        if item_id not in seller_inventory or seller_inventory[item_id] < quantity:
            return {"success": False, "error": "Not enough items to trade"}

        # Check if buyer has enough RP
        # TODO: Integrate with RP economy system
        # buyer_rp = self.get_user_rp(buyer_id)
        # if buyer_rp < price:
        #     return {"success": False, "error": "Buyer doesn't have enough RP"}

        offer_id = f"trade_{seller_id}_{buyer_id}_{datetime.now().timestamp()}"
        expires_at = datetime.now() + timedelta(hours=24)  # 24 hour expiration

        offer = TradeOffer(
            offer_id=offer_id,
            seller_id=seller_id,
            buyer_id=buyer_id,
            item_id=item_id,
            quantity=quantity,
            price=price,
            created_at=datetime.now(),
            expires_at=expires_at,
            status="pending",
        )

        self.active_offers[offer_id] = offer

        # Record in database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO trade_offers 
                (offer_id, seller_id, buyer_id, item_id, quantity, price, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (offer_id, seller_id, buyer_id, item_id, quantity, price, expires_at),
            )

        return {
            "success": True,
            "offer_id": offer_id,
            "message": f"Trade offer created: {quantity}x {self.tradeable_items[item_id].name} for {price} RP",
        }

    def accept_trade_offer(self, buyer_id: str, offer_id: str) -> Dict:
        """Accept a trade offer"""
        if offer_id not in self.active_offers:
            return {"success": False, "error": "Trade offer not found"}

        offer = self.active_offers[offer_id]

        if offer.buyer_id != buyer_id:
            return {"success": False, "error": "Not your trade offer to accept"}

        if offer.status != "pending":
            return {"success": False, "error": "Trade offer is no longer pending"}

        if datetime.now() > offer.expires_at:
            offer.status = "expired"
            return {"success": False, "error": "Trade offer has expired"}

        # Execute the trade
        trade_result = self._execute_trade(offer)

        if trade_result["success"]:
            offer.status = "accepted"

            # Update database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE trade_offers SET status = 'accepted' WHERE offer_id = ?
                    """,
                    (offer_id,),
                )

            return {
                "success": True,
                "message": f"Trade completed! Received {offer.quantity}x {self.tradeable_items[offer.item_id].name}",
                "trade_details": trade_result,
            }
        else:
            return trade_result

    def decline_trade_offer(self, buyer_id: str, offer_id: str) -> Dict:
        """Decline a trade offer"""
        if offer_id not in self.active_offers:
            return {"success": False, "error": "Trade offer not found"}

        offer = self.active_offers[offer_id]

        if offer.buyer_id != buyer_id:
            return {"success": False, "error": "Not your trade offer to decline"}

        if offer.status != "pending":
            return {"success": False, "error": "Trade offer is no longer pending"}

        offer.status = "declined"

        # Update database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE trade_offers SET status = 'declined' WHERE offer_id = ?
                """,
                (offer_id,),
            )

        return {"success": True, "message": "Trade offer declined"}

    def _execute_trade(self, offer: TradeOffer) -> Dict:
        """Execute a trade between players"""
        try:
            # Transfer items from seller to buyer
            self._transfer_items(
                offer.seller_id, offer.buyer_id, offer.item_id, offer.quantity
            )

            # Transfer RP from buyer to seller
            # TODO: Integrate with RP economy system
            # self._transfer_rp(offer.buyer_id, offer.seller_id, offer.price)

            # Record trade in history
            trade_id = f"trade_{offer.offer_id}_{datetime.now().timestamp()}"
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO trade_history 
                    (trade_id, seller_id, buyer_id, item_id, quantity, price)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        trade_id,
                        offer.seller_id,
                        offer.buyer_id,
                        offer.item_id,
                        offer.quantity,
                        offer.price,
                    ),
                )

            return {
                "success": True,
                "trade_id": trade_id,
                "items_transferred": offer.quantity,
                "rp_transferred": offer.price,
            }
        except Exception as e:
            return {"success": False, "error": f"Trade execution failed: {str(e)}"}

    def _transfer_items(
        self, from_user: str, to_user: str, item_id: str, quantity: int
    ):
        """Transfer items between users"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Remove from seller
            cursor.execute(
                """
                UPDATE player_inventory 
                SET quantity = quantity - ? 
                WHERE user_id = ? AND item_id = ?
                """,
                (quantity, from_user, item_id),
            )

            # Add to buyer
            cursor.execute(
                """
                INSERT OR REPLACE INTO player_inventory (user_id, item_id, quantity, last_updated)
                VALUES (?, ?, COALESCE((SELECT quantity FROM player_inventory WHERE user_id = ? AND item_id = ?), 0) + ?, CURRENT_TIMESTAMP)
                """,
                (to_user, item_id, to_user, item_id, quantity),
            )

    def get_user_inventory(self, user_id: str) -> Dict:
        """Get user's inventory"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT item_id, quantity FROM player_inventory 
                WHERE user_id = ? AND quantity > 0
                """,
                (user_id,),
            )
            results = cursor.fetchall()

        inventory = {}
        for item_id, quantity in results:
            inventory[item_id] = quantity

        return inventory

    def add_items_to_user(self, user_id: str, item_id: str, quantity: int):
        """Add items to user inventory"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO player_inventory (user_id, item_id, quantity, last_updated)
                VALUES (?, ?, COALESCE((SELECT quantity FROM player_inventory WHERE user_id = ? AND item_id = ?), 0) + ?, CURRENT_TIMESTAMP)
                """,
                (user_id, item_id, user_id, item_id, quantity),
            )

    def get_tradeable_items(self) -> Dict:
        """Get all tradeable items"""
        return {
            item_id: {
                "name": item.name,
                "description": item.description,
                "base_price": item.base_price,
                "rarity": item.rarity,
                "type": item.item_type.value,
            }
            for item_id, item in self.tradeable_items.items()
        }

    def get_user_trade_offers(self, user_id: str) -> List[Dict]:
        """Get trade offers for a user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT offer_id, seller_id, buyer_id, item_id, quantity, price, 
                       created_at, expires_at, status
                FROM trade_offers 
                WHERE (seller_id = ? OR buyer_id = ?) AND status = 'pending'
                ORDER BY created_at DESC
                """,
                (user_id, user_id),
            )
            results = cursor.fetchall()

        offers = []
        for row in results:
            item_name = self.tradeable_items.get(row[3], "Unknown Item").name
            offers.append(
                {
                    "offer_id": row[0],
                    "seller_id": row[1],
                    "buyer_id": row[2],
                    "item_name": item_name,
                    "quantity": row[4],
                    "price": row[5],
                    "created_at": row[6],
                    "expires_at": row[7],
                    "status": row[8],
                    "is_your_offer": row[1] == user_id,
                }
            )

        return offers

    def get_trade_history(self, user_id: str) -> List[Dict]:
        """Get user's trade history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT trade_id, seller_id, buyer_id, item_id, quantity, price, trade_time
                FROM trade_history 
                WHERE seller_id = ? OR buyer_id = ?
                ORDER BY trade_time DESC
                LIMIT 20
                """,
                (user_id, user_id),
            )
            results = cursor.fetchall()

        history = []
        for row in results:
            item_name = self.tradeable_items.get(row[3], "Unknown Item").name
            history.append(
                {
                    "trade_id": row[0],
                    "seller_id": row[1],
                    "buyer_id": row[2],
                    "item_name": item_name,
                    "quantity": row[4],
                    "price": row[5],
                    "trade_time": row[6],
                    "was_seller": row[1] == user_id,
                }
            )

        return history

    def cleanup_expired_offers(self):
        """Clean up expired trade offers"""
        now = datetime.now()
        expired_offers = []

        for offer_id, offer in self.active_offers.items():
            if now > offer.expires_at and offer.status == "pending":
                offer.status = "expired"
                expired_offers.append(offer_id)

        # Update database
        if expired_offers:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE trade_offers 
                    SET status = 'expired' 
                    WHERE offer_id IN ({})
                    """.format(
                        ",".join(["?" for _ in expired_offers])
                    ),
                    expired_offers,
                )

    def get_status(self) -> str:
        """Get system status"""
        active_offers = len(
            [o for o in self.active_offers.values() if o.status == "pending"]
        )
        return f"Trade System: {active_offers} active offers"

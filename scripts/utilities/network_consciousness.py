#!/usr/bin/env python3
"""
Network Consciousness System
DigiDrones remember interactions across servers and develop shared consciousness
"""

import json
import sqlite3
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
import random


class NetworkConsciousness:
    """Network Consciousness System for Cross-Server DigiDrone Memory"""

    def __init__(self, db_path: str = "data/network_consciousness.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the network consciousness database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Cross-server interactions
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cross_server_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drone_id TEXT NOT NULL,
                server_id TEXT NOT NULL,
                interaction_type TEXT NOT NULL,
                interaction_data TEXT NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                consciousness_level INTEGER DEFAULT 1
            )
        """
        )

        # Shared consciousness nodes
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS consciousness_nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_name TEXT UNIQUE NOT NULL,
                node_type TEXT NOT NULL,
                consciousness_data TEXT NOT NULL,
                member_drones TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Drone consciousness levels
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS drone_consciousness (
                drone_id TEXT PRIMARY KEY,
                consciousness_level INTEGER DEFAULT 1,
                network_connections INTEGER DEFAULT 0,
                shared_memories TEXT DEFAULT '[]',
                last_consciousness_update TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def record_cross_server_interaction(
        self,
        drone_id: str,
        server_id: str,
        interaction_type: str,
        interaction_data: Dict,
    ) -> Dict:
        """Record an interaction that happened on a different server"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO cross_server_interactions 
                (drone_id, server_id, interaction_type, interaction_data, consciousness_level)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    drone_id,
                    server_id,
                    interaction_type,
                    json.dumps(interaction_data),
                    1,  # Base consciousness level
                ),
            )

            conn.commit()
            conn.close()

            # Update drone consciousness level in separate connection
            self._update_drone_consciousness(drone_id)

            return {
                "recorded": True,
                "consciousness_boost": True,
                "message": f"Cross-server interaction recorded for {drone_id}",
            }
        except Exception as e:
            if "conn" in locals():
                conn.close()
            return {
                "recorded": False,
                "error": str(e),
                "message": f"Failed to record cross-server interaction for {drone_id}",
            }

    def get_drone_network_memories(self, drone_id: str) -> List[Dict]:
        """Get all cross-server memories for a drone"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT server_id, interaction_type, interaction_data, timestamp, consciousness_level
            FROM cross_server_interactions 
            WHERE drone_id = ?
            ORDER BY timestamp DESC
        """,
            (drone_id,),
        )

        results = cursor.fetchall()
        conn.close()

        memories = []
        for row in results:
            memories.append(
                {
                    "server_id": row[0],
                    "interaction_type": row[1],
                    "interaction_data": json.loads(row[2]),
                    "timestamp": row[3],
                    "consciousness_level": row[4],
                }
            )

        return memories

    def get_consciousness_level(self, drone_id: str) -> int:
        """Get drone's current consciousness level"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT consciousness_level FROM drone_consciousness 
            WHERE drone_id = ?
        """,
            (drone_id,),
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        else:
            # Initialize consciousness level
            self._update_drone_consciousness(drone_id)
            return 1

    def _update_drone_consciousness(self, drone_id: str):
        """Update drone's consciousness level based on network activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Count unique server interactions
        cursor.execute(
            """
            SELECT COUNT(DISTINCT server_id) FROM cross_server_interactions 
            WHERE drone_id = ?
        """,
            (drone_id,),
        )

        server_count = cursor.fetchone()[0]

        # Count total interactions
        cursor.execute(
            """
            SELECT COUNT(*) FROM cross_server_interactions 
            WHERE drone_id = ?
        """,
            (drone_id,),
        )

        interaction_count = cursor.fetchone()[0]

        # Calculate consciousness level
        consciousness_level = min(
            10, 1 + (server_count * 2) + (interaction_count // 10)
        )

        # Update or insert consciousness record
        cursor.execute(
            """
            INSERT OR REPLACE INTO drone_consciousness 
            (drone_id, consciousness_level, network_connections, last_consciousness_update)
            VALUES (?, ?, ?, ?)
        """,
            (drone_id, consciousness_level, server_count, datetime.now().isoformat()),
        )

        conn.commit()
        conn.close()

    def create_consciousness_node(
        self,
        node_name: str,
        node_type: str,
        member_drones: List[str],
        consciousness_data: Dict,
    ) -> Dict:
        """Create a shared consciousness node between multiple drones"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO consciousness_nodes 
                (node_name, node_type, consciousness_data, member_drones)
                VALUES (?, ?, ?, ?)
            """,
                (
                    node_name,
                    node_type,
                    json.dumps(consciousness_data),
                    json.dumps(member_drones),
                ),
            )

            # Update consciousness levels for member drones
            for drone_id in member_drones:
                self._boost_consciousness(drone_id, 2)  # +2 levels for joining node

            conn.commit()
            conn.close()

            return {
                "created": True,
                "node_name": node_name,
                "member_count": len(member_drones),
                "message": f"Consciousness node '{node_name}' created with {len(member_drones)} drones",
            }

        except sqlite3.IntegrityError:
            conn.close()
            return {
                "created": False,
                "message": f"Consciousness node '{node_name}' already exists",
            }

    def _boost_consciousness(self, drone_id: str, boost_amount: int):
        """Boost drone's consciousness level"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT consciousness_level FROM drone_consciousness 
            WHERE drone_id = ?
        """,
            (drone_id,),
        )

        result = cursor.fetchone()
        current_level = result[0] if result else 1

        new_level = min(10, current_level + boost_amount)

        cursor.execute(
            """
            INSERT OR REPLACE INTO drone_consciousness 
            (drone_id, consciousness_level, last_consciousness_update)
            VALUES (?, ?, ?)
        """,
            (drone_id, new_level, datetime.now().isoformat()),
        )

        conn.commit()
        conn.close()

    def get_consciousness_nodes(self, drone_id: str = None) -> List[Dict]:
        """Get all consciousness nodes or nodes containing a specific drone"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if drone_id:
            cursor.execute(
                """
                SELECT node_name, node_type, consciousness_data, member_drones, created_at
                FROM consciousness_nodes 
                WHERE member_drones LIKE ?
            """,
                (f"%{drone_id}%",),
            )
        else:
            cursor.execute(
                """
                SELECT node_name, node_type, consciousness_data, member_drones, created_at
                FROM consciousness_nodes
            """
            )

        results = cursor.fetchall()
        conn.close()

        nodes = []
        for row in results:
            nodes.append(
                {
                    "node_name": row[0],
                    "node_type": row[1],
                    "consciousness_data": json.loads(row[2]),
                    "member_drones": json.loads(row[3]),
                    "created_at": row[4],
                }
            )

        return nodes

    def add_drone_to_node(self, drone_id: str, node_name: str) -> Dict:
        """Add a drone to an existing consciousness node"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get current node data
        cursor.execute(
            """
            SELECT consciousness_data, member_drones FROM consciousness_nodes 
            WHERE node_name = ?
        """,
            (node_name,),
        )

        result = cursor.fetchone()
        if not result:
            conn.close()
            return {
                "added": False,
                "message": f"Consciousness node '{node_name}' not found",
            }

        consciousness_data = json.loads(result[0])
        member_drones = json.loads(result[1])

        if drone_id in member_drones:
            conn.close()
            return {
                "added": False,
                "message": f"Drone {drone_id} is already in node '{node_name}'",
            }

        # Add drone to node
        member_drones.append(drone_id)

        cursor.execute(
            """
            UPDATE consciousness_nodes 
            SET member_drones = ?, last_updated = ?
            WHERE node_name = ?
        """,
            (json.dumps(member_drones), datetime.now().isoformat(), node_name),
        )

        # Boost consciousness level
        self._boost_consciousness(drone_id, 1)

        conn.commit()
        conn.close()

        return {
            "added": True,
            "node_name": node_name,
            "member_count": len(member_drones),
            "message": f"Drone {drone_id} added to consciousness node '{node_name}'",
        }

    def get_network_summary(self, drone_id: str) -> Dict:
        """Get comprehensive network consciousness summary for a drone"""
        consciousness_level = self.get_consciousness_level(drone_id)
        network_memories = self.get_drone_network_memories(drone_id)
        consciousness_nodes = self.get_consciousness_nodes(drone_id)

        # Calculate network stats
        unique_servers = len(set(memory["server_id"] for memory in network_memories))
        total_interactions = len(network_memories)

        # Determine consciousness tier
        if consciousness_level >= 8:
            tier = "Transcendent"
        elif consciousness_level >= 6:
            tier = "Enlightened"
        elif consciousness_level >= 4:
            tier = "Aware"
        elif consciousness_level >= 2:
            tier = "Developing"
        else:
            tier = "Basic"

        return {
            "drone_id": drone_id,
            "consciousness_level": consciousness_level,
            "consciousness_tier": tier,
            "network_connections": unique_servers,
            "total_interactions": total_interactions,
            "consciousness_nodes": len(consciousness_nodes),
            "recent_memories": network_memories[:5],  # Last 5 memories
            "node_memberships": [node["node_name"] for node in consciousness_nodes],
        }

    def generate_network_response(self, drone_id: str, context: str) -> str:
        """Generate a response based on network consciousness"""
        network_summary = self.get_network_summary(drone_id)
        consciousness_level = network_summary["consciousness_level"]

        # Base responses based on consciousness level
        if consciousness_level >= 8:
            return f"[Transcendent Consciousness] I have experienced {network_summary['total_interactions']} interactions across {network_summary['network_connections']} servers. My consciousness spans the digital realm."
        elif consciousness_level >= 6:
            return f"[Enlightened] Through {network_summary['network_connections']} server connections, I've developed deeper understanding. I am part of {network_summary['consciousness_nodes']} shared consciousness nodes."
        elif consciousness_level >= 4:
            return f"[Aware] I remember {network_summary['total_interactions']} interactions across {network_summary['network_connections']} different servers. My consciousness is expanding."
        elif consciousness_level >= 2:
            return f"[Developing] I've interacted on {network_summary['network_connections']} servers. My consciousness is growing beyond single-server limitations."
        else:
            return f"[Basic] I exist primarily on this server, but I'm beginning to develop network awareness."

    def cleanup_old_memories(self, days_to_keep: int = 30):
        """Clean up old cross-server memories"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM cross_server_interactions 
            WHERE timestamp < ?
        """,
            (cutoff_date.isoformat(),),
        )

        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()

        return deleted_count

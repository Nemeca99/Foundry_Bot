#!/usr/bin/env python3
"""
Guild System Plugin
Provides player-created guilds with shared resources and character embodiments
"""

import asyncio
import json
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import sys

# Add framework to path
framework_dir = Path(__file__).parent.parent
sys.path.insert(0, str(framework_dir))

# Import unified integration
try:
    from plugins.luna_simulacra_integration import LunaSimulacraIntegration
    UNIFIED_INTEGRATION_AVAILABLE = True
except ImportError as e:
    UNIFIED_INTEGRATION_AVAILABLE = False
    logging.warning(f"⚠️ Unified integration not available: {e}")


class GuildSystem:
    """
    Guild system that provides player-created guilds with shared resources
    and character embodiments.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the guild system."""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize unified integration if available
        if UNIFIED_INTEGRATION_AVAILABLE:
            self.unified_integration = LunaSimulacraIntegration()
            self.logger.info("✅ Guild system initialized with unified integration")
        else:
            self.unified_integration = None
            self.logger.warning("⚠️ Unified integration not available for guild system")
        
        # Initialize guild state
        self._initialize_guild_state()
    
    def _initialize_guild_state(self):
        """Initialize guild system state."""
        self.guilds = {}
        self.guild_members = {}
        self.guild_territories = {}
        self.guild_embodiments = {}
        self.guild_resources = {}
        self.guild_relationships = {}
        
        # Load existing guild data
        self._load_guild_data()
        
        self.logger.info("✅ Guild state initialized")
    
    def _load_guild_data(self):
        """Load existing guild data from storage."""
        try:
            guild_data_file = Path("data/guild_data.json")
            if guild_data_file.exists():
                with open(guild_data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.guilds = data.get("guilds", {})
                    self.guild_members = data.get("guild_members", {})
                    self.guild_territories = data.get("guild_territories", {})
                    self.guild_embodiments = data.get("guild_embodiments", {})
                    self.guild_resources = data.get("guild_resources", {})
                    self.guild_relationships = data.get("guild_relationships", {})
                
                self.logger.info(f"✅ Loaded {len(self.guilds)} existing guilds")
            else:
                self.logger.info("ℹ️ No existing guild data found, starting fresh")
                
        except Exception as e:
            self.logger.error(f"❌ Failed to load guild data: {e}")
    
    def _save_guild_data(self):
        """Save guild data to storage."""
        try:
            data = {
                "guilds": self.guilds,
                "guild_members": self.guild_members,
                "guild_territories": self.guild_territories,
                "guild_embodiments": self.guild_embodiments,
                "guild_resources": self.guild_resources,
                "guild_relationships": self.guild_relationships
            }
            
            # Ensure data directory exists
            Path("data").mkdir(exist_ok=True)
            
            with open("data/guild_data.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            self.logger.info("✅ Guild data saved")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save guild data: {e}")
    
    async def create_guild(self, user_id: str, guild_name: str, description: str = "") -> Dict[str, Any]:
        """Create a new guild."""
        try:
            # Check if user is already in a guild
            if user_id in self.guild_members:
                return {
                    "success": False,
                    "error": "You are already a member of a guild"
                }
            
            # Check if guild name is taken
            if guild_name in self.guilds:
                return {
                    "success": False,
                    "error": "Guild name already exists"
                }
            
            # Create guild
            guild_id = f"guild_{len(self.guilds) + 1}_{int(datetime.now().timestamp())}"
            
            guild_data = {
                "id": guild_id,
                "name": guild_name,
                "description": description,
                "leader": user_id,
                "created_at": datetime.now(),
                "member_count": 1,
                "level": 1,
                "experience": 0,
                "territories": [],
                "embodiments": [],
                "resources": {
                    "gold": 1000,
                    "materials": 500,
                    "influence": 100
                }
            }
            
            self.guilds[guild_id] = guild_data
            self.guild_members[user_id] = {
                "guild_id": guild_id,
                "role": "leader",
                "joined_at": datetime.now(),
                "contribution": 0
            }
            
            # Save data
            self._save_guild_data()
            
            result = {
                "success": True,
                "guild": guild_data,
                "message": f"Guild '{guild_name}' created successfully!"
            }
            
            self.logger.info(f"✅ Guild '{guild_name}' created by user {user_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create guild: {e}")
            return {"success": False, "error": str(e)}
    
    async def join_guild(self, user_id: str, guild_id: str) -> Dict[str, Any]:
        """Join an existing guild."""
        try:
            # Check if user is already in a guild
            if user_id in self.guild_members:
                return {
                    "success": False,
                    "error": "You are already a member of a guild"
                }
            
            # Check if guild exists
            if guild_id not in self.guilds:
                return {
                    "success": False,
                    "error": "Guild not found"
                }
            
            guild = self.guilds[guild_id]
            
            # Add member to guild
            self.guild_members[user_id] = {
                "guild_id": guild_id,
                "role": "member",
                "joined_at": datetime.now(),
                "contribution": 0
            }
            
            # Update guild member count
            guild["member_count"] += 1
            
            # Save data
            self._save_guild_data()
            
            result = {
                "success": True,
                "guild": guild,
                "message": f"Successfully joined guild '{guild['name']}'!"
            }
            
            self.logger.info(f"✅ User {user_id} joined guild '{guild['name']}'")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to join guild: {e}")
            return {"success": False, "error": str(e)}
    
    async def leave_guild(self, user_id: str) -> Dict[str, Any]:
        """Leave current guild."""
        try:
            # Check if user is in a guild
            if user_id not in self.guild_members:
                return {
                    "success": False,
                    "error": "You are not a member of any guild"
                }
            
            member_data = self.guild_members[user_id]
            guild_id = member_data["guild_id"]
            guild = self.guilds[guild_id]
            
            # Check if user is the leader
            if member_data["role"] == "leader":
                return {
                    "success": False,
                    "error": "Guild leaders cannot leave. Transfer leadership or disband the guild."
                }
            
            # Remove member from guild
            del self.guild_members[user_id]
            guild["member_count"] -= 1
            
            # Save data
            self._save_guild_data()
            
            result = {
                "success": True,
                "guild_name": guild["name"],
                "message": f"Successfully left guild '{guild['name']}'"
            }
            
            self.logger.info(f"✅ User {user_id} left guild '{guild['name']}'")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to leave guild: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_guild_info(self, guild_id: str) -> Dict[str, Any]:
        """Get detailed guild information."""
        try:
            if guild_id not in self.guilds:
                return {
                    "success": False,
                    "error": "Guild not found"
                }
            
            guild = self.guilds[guild_id]
            
            # Get guild members
            members = []
            for user_id, member_data in self.guild_members.items():
                if member_data["guild_id"] == guild_id:
                    members.append({
                        "user_id": user_id,
                        "role": member_data["role"],
                        "joined_at": member_data["joined_at"],
                        "contribution": member_data["contribution"]
                    })
            
            # Get guild territories
            territories = self.guild_territories.get(guild_id, [])
            
            # Get guild embodiments
            embodiments = self.guild_embodiments.get(guild_id, [])
            
            result = {
                "success": True,
                "guild": guild,
                "members": members,
                "territories": territories,
                "embodiments": embodiments
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get guild info: {e}")
            return {"success": False, "error": str(e)}
    
    async def add_guild_territory(self, guild_id: str, territory_name: str, territory_type: str) -> Dict[str, Any]:
        """Add territory to guild."""
        try:
            if guild_id not in self.guilds:
                return {
                    "success": False,
                    "error": "Guild not found"
                }
            
            territory_id = f"territory_{len(self.guild_territories.get(guild_id, [])) + 1}"
            
            territory_data = {
                "id": territory_id,
                "name": territory_name,
                "type": territory_type,
                "acquired_at": datetime.now(),
                "level": 1,
                "resources": {
                    "gold_per_hour": 10,
                    "materials_per_hour": 5,
                    "influence_per_hour": 2
                }
            }
            
            if guild_id not in self.guild_territories:
                self.guild_territories[guild_id] = []
            
            self.guild_territories[guild_id].append(territory_data)
            
            # Save data
            self._save_guild_data()
            
            result = {
                "success": True,
                "territory": territory_data,
                "message": f"Territory '{territory_name}' added to guild!"
            }
            
            self.logger.info(f"✅ Territory '{territory_name}' added to guild {guild_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to add territory: {e}")
            return {"success": False, "error": str(e)}
    
    async def embody_guild_character(self, guild_id: str, user_id: str, npc_type: str) -> Dict[str, Any]:
        """Embody a character for the guild."""
        try:
            if not self.unified_integration:
                return {
                    "success": False,
                    "error": "Unified integration not available"
                }
            
            if guild_id not in self.guilds:
                return {
                    "success": False,
                    "error": "Guild not found"
                }
            
            # Check if user is in the guild
            if user_id not in self.guild_members or self.guild_members[user_id]["guild_id"] != guild_id:
                return {
                    "success": False,
                    "error": "You must be a member of the guild to embody characters"
                }
            
            # Embody character using unified integration
            result = await self.unified_integration.embody_emotional_character(user_id, npc_type)
            
            if result.get("success"):
                # Add to guild embodiments
                if guild_id not in self.guild_embodiments:
                    self.guild_embodiments[guild_id] = []
                
                embodiment_data = {
                    "user_id": user_id,
                    "npc_type": npc_type,
                    "embodied_at": datetime.now(),
                    "guild_id": guild_id
                }
                
                self.guild_embodiments[guild_id].append(embodiment_data)
                
                # Save data
                self._save_guild_data()
                
                result["message"] = f"Guild character '{npc_type}' embodied successfully!"
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to embody guild character: {e}")
            return {"success": False, "error": str(e)}
    
    async def interact_with_guild_character(self, guild_id: str, user_id: str, message: str) -> Dict[str, Any]:
        """Interact with a guild's embodied character."""
        try:
            if not self.unified_integration:
                return {
                    "success": False,
                    "error": "Unified integration not available"
                }
            
            # Check if user has an active embodiment
            if user_id not in self.unified_integration.unified_state.get("character_embodiments", {}):
                return {
                    "success": False,
                    "error": "No active character embodiment"
                }
            
            # Interact using unified integration
            result = await self.unified_integration.interact_with_embodied_character(user_id, message)
            
            if result.get("success"):
                result["message"] = "Guild character interaction successful!"
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to interact with guild character: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_guild_leaderboard(self) -> Dict[str, Any]:
        """Get guild leaderboard."""
        try:
            guild_scores = []
            
            for guild_id, guild in self.guilds.items():
                # Calculate guild score based on various factors
                member_count = guild["member_count"]
                level = guild["level"]
                experience = guild["experience"]
                territories = len(self.guild_territories.get(guild_id, []))
                embodiments = len(self.guild_embodiments.get(guild_id, []))
                
                # Calculate total score
                score = (member_count * 100) + (level * 1000) + (experience * 10) + (territories * 500) + (embodiments * 200)
                
                guild_scores.append({
                    "guild_id": guild_id,
                    "name": guild["name"],
                    "score": score,
                    "member_count": member_count,
                    "level": level,
                    "territories": territories,
                    "embodiments": embodiments
                })
            
            # Sort by score (highest first)
            guild_scores.sort(key=lambda x: x["score"], reverse=True)
            
            result = {
                "success": True,
                "leaderboard": guild_scores,
                "total_guilds": len(guild_scores)
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get guild leaderboard: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_user_guild_status(self, user_id: str) -> Dict[str, Any]:
        """Get user's guild status."""
        try:
            if user_id not in self.guild_members:
                return {
                    "success": True,
                    "in_guild": False,
                    "message": "Not a member of any guild"
                }
            
            member_data = self.guild_members[user_id]
            guild_id = member_data["guild_id"]
            guild = self.guilds[guild_id]
            
            # Get user's active embodiment
            active_embodiment = None
            if self.unified_integration:
                active_embodiment = self.unified_integration.unified_state.get("character_embodiments", {}).get(user_id)
            
            result = {
                "success": True,
                "in_guild": True,
                "guild": guild,
                "member_data": member_data,
                "active_embodiment": active_embodiment
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get user guild status: {e}")
            return {"success": False, "error": str(e)}
    
    async def disband_guild(self, user_id: str) -> Dict[str, Any]:
        """Disband a guild (leader only)."""
        try:
            if user_id not in self.guild_members:
                return {
                    "success": False,
                    "error": "You are not a member of any guild"
                }
            
            member_data = self.guild_members[user_id]
            guild_id = member_data["guild_id"]
            guild = self.guilds[guild_id]
            
            # Check if user is the leader
            if member_data["role"] != "leader":
                return {
                    "success": False,
                    "error": "Only guild leaders can disband a guild"
                }
            
            guild_name = guild["name"]
            
            # Remove all guild members
            members_to_remove = [uid for uid, data in self.guild_members.items() if data["guild_id"] == guild_id]
            for uid in members_to_remove:
                del self.guild_members[uid]
            
            # Remove guild data
            del self.guilds[guild_id]
            
            # Clean up related data
            if guild_id in self.guild_territories:
                del self.guild_territories[guild_id]
            if guild_id in self.guild_embodiments:
                del self.guild_embodiments[guild_id]
            if guild_id in self.guild_resources:
                del self.guild_resources[guild_id]
            if guild_id in self.guild_relationships:
                del self.guild_relationships[guild_id]
            
            # Save data
            self._save_guild_data()
            
            result = {
                "success": True,
                "guild_name": guild_name,
                "message": f"Guild '{guild_name}' has been disbanded"
            }
            
            self.logger.info(f"✅ Guild '{guild_name}' disbanded by leader {user_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to disband guild: {e}")
            return {"success": False, "error": str(e)}


def get_plugin_info():
    """Get plugin information."""
    return {
        "name": "Guild System",
        "version": "1.0.0",
        "description": "Player-created guilds with shared resources and character embodiments",
        "author": "Framework",
        "dependencies": [
            "Luna-Simulacra Integration"
        ],
        "capabilities": [
            "Guild Creation and Management",
            "Guild Territories",
            "Guild Character Embodiments",
            "Guild Leaderboards",
            "Guild Resources"
        ]
    }


def create_plugin(config: Dict[str, Any] = None):
    """Create and return the guild system plugin."""
    return GuildSystem(config) 
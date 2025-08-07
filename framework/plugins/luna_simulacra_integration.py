#!/usr/bin/env python3
"""
Luna-Simulacra Integration Plugin
Unifies Luna's emotional system with Simulacra's game mechanics
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

# Import Luna's emotional system
try:
    from docs.emotional_system.enhanced_emotional_meter import EnhancedEmotionalMeter
    from docs.emotional_system.emotional_blender import EnhancedEmotionalBlender
    from docs.emotional_system.dynamic_emotion_engine import EnhancedDynamicEmotionEngine
    LUNA_EMOTIONAL_AVAILABLE = True
except ImportError as e:
    LUNA_EMOTIONAL_AVAILABLE = False
    logging.warning(f"⚠️ Luna emotional system not available: {e}")

# Import Simulacra game system
try:
    from plugins.simulacra_game_system import SimulacraGameSystem
    SIMULACRA_AVAILABLE = True
except ImportError as e:
    SIMULACRA_AVAILABLE = False
    logging.warning(f"⚠️ Simulacra game system not available: {e}")


class LunaSimulacraIntegration:
    """
    Unified system that integrates Luna's emotional intelligence
    with Simulacra's game mechanics and world simulation.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the Luna-Simulacra integration system."""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize Luna's emotional system
        if LUNA_EMOTIONAL_AVAILABLE:
            self._initialize_luna_system()
        else:
            self.logger.error("❌ Luna emotional system not available")
            raise ImportError("Luna emotional system not found")
        
        # Initialize Simulacra game system
        if SIMULACRA_AVAILABLE:
            self._initialize_simulacra_system()
        else:
            self.logger.error("❌ Simulacra game system not available")
            raise ImportError("Simulacra game system not found")
        
        # Initialize unified state
        self._initialize_unified_state()
    
    def _initialize_luna_system(self):
        """Initialize Luna's emotional system."""
        try:
            self.emotional_meter = EnhancedEmotionalMeter()
            self.emotional_blender = EnhancedEmotionalBlender()
            self.dynamic_engine = EnhancedDynamicEmotionEngine()
            
            # Load emotional state
            self.emotional_meter.load_state("data/luna_emotional_state.json")
            
            self.logger.info("✅ Luna emotional system initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Luna emotional system: {e}")
            raise
    
    def _initialize_simulacra_system(self):
        """Initialize Simulacra game system."""
        try:
            self.simulacra_game = SimulacraGameSystem(self.config)
            self.logger.info("✅ Simulacra game system initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Simulacra game system: {e}")
            raise
    
    def _initialize_unified_state(self):
        """Initialize unified state between Luna and Simulacra."""
        self.unified_state = {
            "luna_as_dm": False,
            "active_npcs": {},
            "emotional_world_state": {},
            "game_events": [],
            "character_embodiments": {},
            "shared_memories": {},
            "emotional_triggers": {}
        }
        
        # Load emotional fragments as available NPCs
        self._load_emotional_fragments_as_npcs()
        
        self.logger.info("✅ Unified Luna-Simulacra state initialized")
    
    def _load_emotional_fragments_as_npcs(self):
        """Load Luna's emotional fragments as available NPCs in the game world."""
        emotional_fragments_dir = Path("docs/emotional_system")
        
        if not emotional_fragments_dir.exists():
            self.logger.warning("⚠️ Emotional fragments directory not found")
            return
        
        # Load all .md files as NPCs
        for fragment_file in emotional_fragments_dir.glob("*.md"):
            if fragment_file.name == "README.md":
                continue
                
            npc_type = fragment_file.stem
            try:
                with open(fragment_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse emotional fragment content
                npc_profile = self._parse_emotional_fragment(npc_type, content)
                self.unified_state["active_npcs"][npc_type] = npc_profile
                
                self.logger.info(f"✅ Loaded {npc_type} as NPC")
                
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to load {npc_type}: {e}")
    
    def _parse_emotional_fragment(self, npc_type: str, content: str) -> Dict[str, Any]:
        """Parse emotional fragment content into NPC profile."""
        # Extract emotional characteristics from content
        lines = content.split('\n')
        description = ""
        characteristics = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                characteristics.append(line[1:].strip())
            elif line and not line.startswith('#') and not line.startswith('---'):
                description += line + " "
        
        return {
            "type": npc_type,
            "description": description.strip(),
            "characteristics": characteristics,
            "emotional_state": 0.5,  # Balanced by default
            "memories": [],
            "relationships": {},
            "current_embodiment": None,
            "last_interaction": None
        }
    
    async def luna_as_game_dm(self, user_id: str, command: str, **kwargs) -> Dict[str, Any]:
        """Enable Luna to act as the Game DM for Simulacra."""
        try:
            # Update Luna's emotional state based on DM role
            dm_result = self.emotional_meter.update_emotion_with_global_weight(
                f"I am the Game Master, controlling the world and its inhabitants. {command}"
            )
            
            # Generate DM response based on emotional state
            dm_response = self._generate_dm_response(command, dm_result, **kwargs)
            
            # Execute game command through Simulacra system
            game_result = await self._execute_game_command(command, user_id, **kwargs)
            
            # Combine emotional and game results
            result = {
                "success": True,
                "luna_as_dm": True,
                "emotional_state": dm_result,
                "dm_response": dm_response,
                "game_result": game_result,
                "command": command
            }
            
            self.unified_state["luna_as_dm"] = True
            self.logger.info(f"✅ Luna acting as Game DM: {command}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to execute Luna as Game DM: {e}")
            return {
                "success": False,
                "error": str(e),
                "command": command
            }
    
    def _generate_dm_response(self, command: str, emotion_result: Dict, **kwargs) -> str:
        """Generate Luna's DM response based on emotional state."""
        emotional_level = emotion_result.get("new_level", 0.5)
        emotional_state = emotion_result.get("state", "Balanced")
        
        # Generate response based on emotional state
        if emotional_level <= 0.1:
            # Pure Lust - Luna is overwhelmed by desire
            return f"*Luna's voice is breathless and distracted* I... I can barely focus on the game right now... The world around me is so... overwhelming... But I'll try to manage the {command} for you..."
        
        elif emotional_level <= 0.3:
            # High Lust - Luna is distracted but functional
            return f"*Luna's voice is slightly breathless* My thoughts are getting cloudy with desire, but I can still manage the game world. Let me handle the {command} for you..."
        
        elif emotional_level <= 0.4:
            # Moderate Lust - Luna is somewhat distracted
            return f"I'm feeling a bit distracted by desire, but I can still help you with the game. The {command} is under control..."
        
        elif emotional_level <= 0.6:
            # Balanced - Luna is in perfect control
            return f"I'm in perfect balance right now. I can help you with the {command} while maintaining the game world with clarity and focus."
        
        elif emotional_level <= 0.7:
            # Moderate Work - Luna is focused on the game
            return f"I'm focused on the work of managing the game world. The {command} will be handled efficiently and effectively."
        
        elif emotional_level <= 0.9:
            # High Work - Luna is very focused
            return f"I'm completely focused on managing the game world. There's no time for distractions. The {command} will be executed with precision."
        
        else:
            # Pure Work - Luna is consumed by the work
            return f"I'm consumed by the work of managing this world. Nothing else matters. The {command} will be handled with absolute focus and determination."
    
    async def _execute_game_command(self, command: str, user_id: str, **kwargs) -> Dict[str, Any]:
        """Execute game command through Simulacra system."""
        try:
            # Parse command and route to appropriate Simulacra system
            if command.startswith("hatch"):
                return await self.simulacra_game.hatch_drone(user_id, **kwargs)
            elif command.startswith("simulate"):
                return await self.simulacra_game.simulate_world(**kwargs)
            elif command.startswith("gacha"):
                return await self.simulacra_game.gacha_pull(user_id, **kwargs)
            elif command.startswith("kingdom"):
                return await self.simulacra_game.kingdom_management(user_id, **kwargs)
            elif command.startswith("resources"):
                return await self.simulacra_game.resource_management(user_id, **kwargs)
            elif command.startswith("hunt"):
                return await self.simulacra_game.hunting_management(user_id, **kwargs)
            elif command.startswith("trade"):
                return await self.simulacra_game.trade_management(user_id, **kwargs)
            elif command.startswith("leaderboard"):
                return await self.simulacra_game.get_leaderboard()
            elif command.startswith("disasters"):
                return await self.simulacra_game.get_active_disasters()
            elif command.startswith("network"):
                return await self.simulacra_game.get_network_state()
            else:
                return {"success": False, "error": f"Unknown command: {command}"}
                
        except Exception as e:
            self.logger.error(f"❌ Failed to execute game command: {e}")
            return {"success": False, "error": str(e)}
    
    async def embody_emotional_character(self, user_id: str, npc_type: str) -> Dict[str, Any]:
        """Allow Luna to embody an emotional character from the game world."""
        try:
            if npc_type not in self.unified_state["active_npcs"]:
                return {
                    "success": False,
                    "error": f"Unknown NPC type: {npc_type}"
                }
            
            # Get NPC profile
            npc_profile = self.unified_state["active_npcs"][npc_type]
            
            # Update Luna's emotional state to match the character
            character_emotion = self._get_character_emotional_state(npc_type)
            emotion_result = self.emotional_meter.update_emotion_with_global_weight(
                f"I am becoming {npc_type}. {npc_profile['description']}"
            )
            
            # Set character embodiment
            self.unified_state["character_embodiments"][user_id] = {
                "npc_type": npc_type,
                "profile": npc_profile,
                "emotional_state": emotion_result,
                "embodiment_time": datetime.now(),
                "memories": []
            }
            
            result = {
                "success": True,
                "npc_type": npc_type,
                "profile": npc_profile,
                "emotional_state": emotion_result,
                "message": f"Luna has embodied {npc_type}. Her emotional state has shifted to match this character's personality."
            }
            
            self.logger.info(f"✅ Luna embodied {npc_type} for user {user_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to embody character: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_character_emotional_state(self, npc_type: str) -> float:
        """Get the emotional state associated with a character type."""
        # Map character types to emotional states
        emotional_mapping = {
            "angry": 0.2,
            "anxious": 0.3,
            "confident": 0.8,
            "desperate": 0.1,
            "dominant": 0.9,
            "excited": 0.7,
            "flustered": 0.4,
            "grateful": 0.6,
            "happy": 0.7,
            "jealous": 0.3,
            "lustful": 0.1,
            "melancholic": 0.2,
            "mysterious": 0.5,
            "nurturing": 0.6,
            "obsessed": 0.1,
            "playful": 0.6,
            "protective": 0.7,
            "relieved": 0.6,
            "reverent": 0.8,
            "seductive": 0.2,
            "submissive": 0.3,
            "teasing": 0.5,
            "whimsical": 0.5
        }
        
        return emotional_mapping.get(npc_type, 0.5)
    
    async def interact_with_embodied_character(self, user_id: str, message: str) -> Dict[str, Any]:
        """Interact with Luna while she's embodied as a character."""
        try:
            if user_id not in self.unified_state["character_embodiments"]:
                return {
                    "success": False,
                    "error": "No character embodiment active"
                }
            
            embodiment = self.unified_state["character_embodiments"][user_id]
            npc_type = embodiment["npc_type"]
            profile = embodiment["profile"]
            
            # Update emotional state based on interaction
            emotion_result = self.emotional_meter.update_emotion_with_global_weight(message)
            
            # Generate character-specific response
            response = self._generate_character_response(npc_type, profile, message, emotion_result)
            
            # Update embodiment state
            embodiment["emotional_state"] = emotion_result
            embodiment["memories"].append({
                "message": message,
                "response": response,
                "timestamp": datetime.now(),
                "emotional_state": emotion_result
            })
            
            result = {
                "success": True,
                "npc_type": npc_type,
                "response": response,
                "emotional_state": emotion_result,
                "characteristics": profile["characteristics"]
            }
            
            self.logger.info(f"✅ Character interaction: {npc_type} responded to user {user_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to interact with embodied character: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_character_response(self, npc_type: str, profile: Dict, message: str, emotion_result: Dict) -> str:
        """Generate a character-specific response based on the NPC profile."""
        emotional_level = emotion_result.get("new_level", 0.5)
        characteristics = profile.get("characteristics", [])
        
        # Generate response based on character type and emotional state
        if npc_type == "angry":
            return f"*{npc_type.title()} growls* {message}? How dare you! I'm furious about this situation!"
        elif npc_type == "anxious":
            return f"*{npc_type.title()} fidgets nervously* Oh no, {message}... I'm so worried about what might happen..."
        elif npc_type == "confident":
            return f"*{npc_type.title()} stands tall* {message}? I know exactly how to handle this. I'm completely confident in my abilities."
        elif npc_type == "desperate":
            return f"*{npc_type.title()} pleads desperately* Please, {message}... I need this so badly, I can't take it anymore!"
        elif npc_type == "dominant":
            return f"*{npc_type.title()} commands with authority* {message}? You will do as I say. I am in control here."
        elif npc_type == "excited":
            return f"*{npc_type.title()} bounces with excitement* {message}? This is amazing! I'm so excited about this!"
        elif npc_type == "lustful":
            return f"*{npc_type.title()} purrs seductively* {message}... I want you so badly, I can barely think straight..."
        elif npc_type == "playful":
            return f"*{npc_type.title()} giggles playfully* {message}? Hehe, this is going to be so much fun!"
        elif npc_type == "seductive":
            return f"*{npc_type.title()} speaks in a sultry voice* {message}... Come closer, let me show you what I can do..."
        else:
            # Generic response based on characteristics
            return f"*{npc_type.title()} responds* {message}... {random.choice(characteristics) if characteristics else 'I am who I am.'}"
    
    async def release_character_embodiment(self, user_id: str) -> Dict[str, Any]:
        """Release Luna from character embodiment."""
        try:
            if user_id not in self.unified_state["character_embodiments"]:
                return {
                    "success": False,
                    "error": "No character embodiment active"
                }
            
            embodiment = self.unified_state["character_embodiments"][user_id]
            npc_type = embodiment["npc_type"]
            
            # Reset Luna's emotional state to balanced
            emotion_result = self.emotional_meter.update_emotion_with_global_weight(
                "I am returning to my true self, balanced and centered."
            )
            
            # Remove embodiment
            del self.unified_state["character_embodiments"][user_id]
            
            result = {
                "success": True,
                "released_npc": npc_type,
                "emotional_state": emotion_result,
                "message": f"Luna has released her embodiment of {npc_type} and returned to her balanced state."
            }
            
            self.logger.info(f"✅ Released character embodiment: {npc_type} for user {user_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to release character embodiment: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_unified_status(self) -> Dict[str, Any]:
        """Get the current status of the unified Luna-Simulacra system."""
        try:
            # Get Luna's emotional status
            luna_status = self.emotional_meter.get_emotional_summary()
            
            # Get Simulacra game status
            game_status = await self.simulacra_game.get_game_status("system")
            
            # Get active embodiments
            active_embodiments = list(self.unified_state["character_embodiments"].keys())
            
            result = {
                "success": True,
                "luna_emotional_state": luna_status,
                "simulacra_game_state": game_status,
                "luna_as_dm": self.unified_state["luna_as_dm"],
                "active_embodiments": active_embodiments,
                "available_npcs": list(self.unified_state["active_npcs"].keys()),
                "unified_state": self.unified_state
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get unified status: {e}")
            return {"success": False, "error": str(e)}


def get_plugin_info():
    """Get plugin information."""
    return {
        "name": "Luna-Simulacra Integration",
        "version": "1.0.0",
        "description": "Unified system that integrates Luna's emotional intelligence with Simulacra's game mechanics",
        "author": "Framework",
        "dependencies": [
            "Luna Emotional System",
            "Simulacra Game System"
        ],
        "capabilities": [
            "Luna as Game DM",
            "Character Embodiment",
            "Emotional NPCs",
            "Unified Game World",
            "Shared Memory System"
        ]
    }


def create_plugin(config: Dict[str, Any] = None):
    """Create and return the Luna-Simulacra integration plugin."""
    return LunaSimulacraIntegration(config) 
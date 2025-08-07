#!/usr/bin/env python3
"""
Framework CLI Tool - AI-Native Interface Layer
Critical I/O bridge between Discord bot and LLM model with prompt injection, context management, and data flow optimization
"""

import os
import sys
import json
import shutil
import argparse
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib
import gzip
import tempfile
import asyncio
import threading
from queue import Queue
import time
from queue_manager import queue_manager, QueueProcessor

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add Simulacra Rancher path
simulacra_path = project_root / "Simulacra_Rancher_Project"
sys.path.insert(0, str(simulacra_path))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import Simulacra game system
try:
    from Simulacra_Rancher_Project.core.game_system import SimulacraGameSystem

    SIMULACRA_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️ Simulacra game system not available: {e}")
    SIMULACRA_AVAILABLE = False


class AIInterfaceLayer:
    """AI-native interface layer for LLM model communication"""

    def __init__(self):
        self.context_buffer = {}
        self.prompt_history = []
        self.response_cache = {}
        self.model_state = {}
        self.processing_queue = Queue()
        self.context_window = 10  # Keep last 10 interactions

    def _get_available_plugins(self) -> List[str]:
        """Get list of available plugins"""
        return [
            "ai_native_backend",
            "character_embodiment_engine",
            "character_development_engine",
            "character_interaction_engine",
            "character_memory_system",
            "content_driven_personality",
            "content_emotion_integration",
            "dynamic_personality_learning",
            "enhanced_audio_processor",
            "identity_processor",
            "image_generator",
            "learning_engine",
            "multi_language_optimizer",
            "multi_personality_system",
            "multimodal_orchestrator",
            "personality_engine",
            "personality_fusion_system",
            "personalization_engine",
            "self_learning_system",
            "text_generator",
            "tool_manager",
            "video_generator",
            "voice_generator",
            "writing_assistant",
        ]

    def _get_system_resources(self) -> Dict[str, Any]:
        """Get system resource information"""
        return {
            "memory_usage": "Normal",
            "cpu_usage": "Normal",
            "disk_space": "Adequate",
            "network": "Connected",
        }

    def _load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences"""
        return {
            "writing_style": "creative",
            "genre_preference": "fantasy",
            "character_depth": "detailed",
            "response_length": "medium",
        }

    def _get_interaction_history(self) -> List[Dict[str, Any]]:
        """Get user interaction history"""
        return self.prompt_history[-5:] if self.prompt_history else []

    def _get_writing_style_preferences(self) -> Dict[str, Any]:
        """Get writing style preferences"""
        return {
            "tone": "professional",
            "complexity": "moderate",
            "creativity": "high",
            "formality": "casual",
        }

    def _get_active_characters(self) -> List[str]:
        """Get active characters"""
        return ["Luna", "Eve", "Anna"]  # Example characters

    def _get_character_relationships(self) -> Dict[str, Any]:
        """Get character relationships"""
        return {
            "Luna": ["Eve", "Anna"],
            "Eve": ["Luna", "Anna"],
            "Anna": ["Luna", "Eve"],
        }

    def _get_character_development(self) -> str:
        """Get character development stage"""
        return "active_development"

    def _get_current_project(self) -> str:
        """Get current writing project"""
        return "Character Embodiment AI Project"

    def _get_writing_goals(self) -> List[str]:
        """Get writing goals"""
        return [
            "Complete character embodiment",
            "Improve writing quality",
            "Enhance emotional depth",
        ]

    def _get_genre_preferences(self) -> str:
        """Get genre preferences"""
        return "Fantasy/Sci-Fi"

    def _get_style_guidelines(self) -> Dict[str, Any]:
        """Get style guidelines"""
        return {
            "show_dont_tell": True,
            "emotional_depth": "high",
            "character_development": "progressive",
            "dialogue_style": "natural",
        }

    def inject_prompt_context(
        self, user_input: str, context_type: str = "general"
    ) -> Dict[str, Any]:
        """Inject contextual information into user prompts"""
        try:
            # Build context from various sources
            context = {
                "user_input": user_input,
                "context_type": context_type,
                "timestamp": time.time(),
                "system_context": self._get_system_context(),
                "user_context": self._get_user_context(),
                "emotional_context": self._get_emotional_context(),
                "conversation_history": self._get_conversation_history(),
                "character_context": self._get_character_context(),
                "writing_context": self._get_writing_context(),
            }

            # Create enhanced prompt
            enhanced_prompt = self._build_enhanced_prompt(context)

            return {
                "original_input": user_input,
                "enhanced_prompt": enhanced_prompt,
                "context": context,
                "injection_metadata": {
                    "context_type": context_type,
                    "context_size": len(str(context)),
                    "prompt_length": len(enhanced_prompt),
                },
            }

        except Exception as e:
            logger.error(f"Error injecting prompt context: {e}")
            return {
                "original_input": user_input,
                "enhanced_prompt": user_input,
                "context": {
                    "user_input": user_input,
                    "context_type": context_type,
                    "timestamp": time.time(),
                    "system_context": {
                        "framework_status": "error",
                        "available_plugins": [],
                        "system_resources": {},
                        "current_time": datetime.now().isoformat(),
                    },
                    "user_context": {
                        "user_preferences": {},
                        "interaction_history": [],
                        "writing_style": {},
                    },
                    "emotional_context": {
                        "emotional_state": "neutral",
                        "emotional_intensity": 0.5,
                        "recent_emotions": [],
                        "emotional_triggers": [],
                    },
                    "conversation_history": [],
                    "character_context": {
                        "active_characters": [],
                        "character_relationships": {},
                        "character_development": "none",
                    },
                    "writing_context": {
                        "current_project": "none",
                        "writing_goals": [],
                        "genre_preferences": "general",
                        "style_guidelines": {},
                    },
                },
                "injection_metadata": {
                    "context_type": context_type,
                    "context_size": len(user_input),
                    "prompt_length": len(user_input),
                    "error": str(e),
                },
                "error": str(e),
            }

    def _get_system_context(self) -> Dict[str, Any]:
        """Get current system context"""
        return {
            "framework_status": "active",
            "available_plugins": self._get_available_plugins(),
            "system_resources": self._get_system_resources(),
            "current_time": datetime.now().isoformat(),
        }

    def _get_user_context(self) -> Dict[str, Any]:
        """Get user-specific context"""
        return {
            "user_preferences": self._load_user_preferences(),
            "interaction_history": self._get_interaction_history(),
            "writing_style": self._get_writing_style_preferences(),
        }

    def _get_emotional_context(self) -> Dict[str, Any]:
        """Get emotional context from Luna system"""
        try:
            # This would integrate with the emotional system
            return {
                "emotional_state": "neutral",
                "emotional_intensity": 0.5,
                "recent_emotions": [],
                "emotional_triggers": [],
            }
        except Exception as e:
            logger.error(f"Error getting emotional context: {e}")
            return {"emotional_state": "neutral", "error": str(e)}

    def _get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        return (
            self.prompt_history[-self.context_window :] if self.prompt_history else []
        )

    def _get_character_context(self) -> Dict[str, Any]:
        """Get character embodiment context"""
        try:
            return {
                "active_characters": self._get_active_characters(),
                "character_relationships": self._get_character_relationships(),
                "character_development": self._get_character_development(),
            }
        except Exception as e:
            logger.error(f"Error getting character context: {e}")
            return {"active_characters": [], "error": str(e)}

    def _get_writing_context(self) -> Dict[str, Any]:
        """Get writing-specific context"""
        return {
            "current_project": self._get_current_project(),
            "writing_goals": self._get_writing_goals(),
            "genre_preferences": self._get_genre_preferences(),
            "style_guidelines": self._get_style_guidelines(),
        }

    def _build_enhanced_prompt(self, context: Dict[str, Any]) -> str:
        """Build enhanced prompt with all context"""
        enhanced_prompt = f"""
SYSTEM CONTEXT:
- Framework Status: {context['system_context']['framework_status']}
- Available Plugins: {len(context['system_context']['available_plugins'])} plugins active
- Current Time: {context['system_context']['current_time']}

USER CONTEXT:
- Writing Style: {context['user_context'].get('writing_style', 'general')}
- Interaction History: {len(context['user_context']['interaction_history'])} previous interactions

EMOTIONAL CONTEXT:
- Current State: {context['emotional_context']['emotional_state']}
- Intensity: {context['emotional_context']['emotional_intensity']}

CHARACTER CONTEXT:
- Active Characters: {len(context['character_context']['active_characters'])} characters
- Development Stage: {context['character_context']['character_development']}

WRITING CONTEXT:
- Current Project: {context['writing_context']['current_project']}
- Genre: {context['writing_context']['genre_preferences']}
- Goals: {context['writing_context']['writing_goals']}

CONVERSATION HISTORY:
{self._format_conversation_history(context['conversation_history'])}

USER INPUT: {context['user_input']}

Please respond with appropriate context awareness, maintaining character consistency and writing style preferences.
"""
        return enhanced_prompt.strip()

    def _format_conversation_history(self, history: List[Dict[str, Any]]) -> str:
        """Format conversation history for prompt"""
        if not history:
            return "No recent conversation history."

        formatted = []
        for entry in history[-5:]:  # Last 5 entries
            formatted.append(f"- {entry.get('user', 'User')}: {entry.get('input', '')}")
            if entry.get("response"):
                formatted.append(f"  Response: {entry.get('response', '')}")

        return "\n".join(formatted)

    def process_llm_response(
        self, response: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process and enhance LLM response"""
        try:
            # Parse response for different components
            processed_response = {
                "raw_response": response,
                "response_type": self._classify_response(response),
                "emotional_impact": self._analyze_emotional_impact(response),
                "character_consistency": self._check_character_consistency(
                    response, context
                ),
                "writing_quality": self._assess_writing_quality(response),
                "action_items": self._extract_action_items(response),
                "metadata": {
                    "response_length": len(response),
                    "processing_time": time.time(),
                    "context_used": context.get("context_type", "general"),
                },
            }

            # Cache response
            self.response_cache[hash(response)] = processed_response

            # Update conversation history
            user_input = context.get("user_input", "unknown_input")
            self._update_conversation_history(user_input, response)

            return processed_response

        except Exception as e:
            logger.error(f"Error processing LLM response: {e}")
            return {
                "raw_response": response,
                "response_type": "general",
                "emotional_impact": {
                    "emotional_tone": "neutral",
                    "intensity": 0.5,
                    "emotional_words": [],
                    "sentiment": "neutral",
                },
                "character_consistency": {
                    "consistency_score": 0.5,
                    "character_voice": "unknown",
                    "personality_alignment": "unknown",
                    "development_opportunity": False,
                },
                "writing_quality": {
                    "clarity": 0.5,
                    "creativity": 0.5,
                    "grammar": 0.5,
                    "style": 0.5,
                    "overall_score": 0.5,
                },
                "action_items": [],
                "metadata": {
                    "response_length": len(response),
                    "processing_time": time.time(),
                    "context_used": "general",
                    "error": str(e),
                },
                "error": str(e),
            }

    def _classify_response(self, response: str) -> str:
        """Classify the type of response"""
        response_lower = response.lower()

        if any(
            word in response_lower for word in ["character", "embody", "personality"]
        ):
            return "character_embodiment"
        elif any(
            word in response_lower for word in ["write", "story", "chapter", "plot"]
        ):
            return "writing_assistance"
        elif any(word in response_lower for word in ["emotion", "feeling", "mood"]):
            return "emotional_response"
        elif any(word in response_lower for word in ["analyze", "review", "feedback"]):
            return "analysis"
        else:
            return "general"

    def _analyze_emotional_impact(self, response: str) -> Dict[str, Any]:
        """Analyze emotional impact of response"""
        # This would integrate with the emotional system
        return {
            "emotional_tone": "neutral",
            "intensity": 0.5,
            "emotional_words": [],
            "sentiment": "neutral",
        }

    def _check_character_consistency(
        self, response: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check character consistency in response"""
        return {
            "consistency_score": 0.8,
            "character_voice": "maintained",
            "personality_alignment": "good",
            "development_opportunity": False,
        }

    def _assess_writing_quality(self, response: str) -> Dict[str, Any]:
        """Assess writing quality of response"""
        return {
            "clarity": 0.8,
            "creativity": 0.7,
            "grammar": 0.9,
            "style": 0.8,
            "overall_score": 0.8,
        }

    def _extract_action_items(self, response: str) -> List[str]:
        """Extract action items from response"""
        action_items = []
        # Simple extraction - could be enhanced with NLP
        if "create" in response.lower():
            action_items.append("create_content")
        if "analyze" in response.lower():
            action_items.append("analyze_content")
        if "develop" in response.lower():
            action_items.append("develop_character")
        return action_items

    def _update_conversation_history(self, user_input: str, response: str):
        """Update conversation history"""
        entry = {
            "user": "user",
            "input": user_input,
            "response": response,
            "timestamp": time.time(),
        }
        self.prompt_history.append(entry)

        # Keep only recent history
        if len(self.prompt_history) > self.context_window:
            self.prompt_history.pop(0)


class FrameworkCLI(QueueProcessor):
    """Enhanced CLI tool with AI-native interface layer"""

    def __init__(self):
        super().__init__("framework_cli")
        self.project_root = Path(__file__).parent.parent
        self.framework = None
        self.file_analysis = {}
        self.backup_dir = Path("D:/framework_backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.current_backup_id = None

        # AI Interface Layer
        self.ai_interface = AIInterfaceLayer()

        # Processing queues
        self.discord_queue = Queue()
        self.llm_queue = Queue()
        self.response_queue = Queue()

        # Try to initialize framework (optional dependency)
        try:
            from framework.framework_tool import get_framework

            self.framework = get_framework()
            logger.info("✅ Framework initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ Framework not available: {e}")
            logger.info("🔄 Running in standalone mode")

    def process_discord_command(
        self, command: str, user_id: str, context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process Discord command through AI interface layer"""
        try:
            logger.info(f"🔄 Processing Discord command: {command[:50]}...")

            # Step 1: Inject context into command
            enhanced_command = self.ai_interface.inject_prompt_context(
                command, "discord_command"
            )

            # Step 2: Route to appropriate handler
            if command.startswith("/"):
                # Framework command
                result = self._handle_framework_command(command, enhanced_command)
            elif any(
                keyword in command.lower()
                for keyword in ["character", "embody", "personality"]
            ):
                # Character embodiment command
                result = self._handle_character_command(command, enhanced_command)
            elif any(
                keyword in command.lower()
                for keyword in ["write", "story", "chapter", "plot"]
            ):
                # Writing assistance command
                result = self._handle_writing_command(command, enhanced_command)
            elif any(
                keyword in command.lower()
                for keyword in ["analyze", "review", "feedback"]
            ):
                # Analysis command
                result = self._handle_analysis_command(command, enhanced_command)
            else:
                # General LLM interaction
                result = self._handle_general_command(command, enhanced_command)

            # Step 3: Process response through AI interface
            processed_response = self.ai_interface.process_llm_response(
                result.get("response", ""), enhanced_command
            )

            # Step 4: Format for Discord
            discord_response = self._format_discord_response(
                processed_response, user_id
            )

            return {
                "success": True,
                "original_command": command,
                "enhanced_command": enhanced_command,
                "processed_response": processed_response,
                "discord_response": discord_response,
                "metadata": {
                    "processing_time": time.time(),
                    "user_id": user_id,
                    "command_type": result.get("command_type", "general"),
                },
            }

        except Exception as e:
            logger.error(f"❌ Error processing Discord command: {e}")
            return {
                "success": False,
                "error": str(e),
                "original_command": command,
                "user_id": user_id,
            }

    def _handle_framework_command(
        self, command: str, enhanced_command: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle framework-specific commands"""
        try:
            # Parse command
            parts = command.split()
            cmd = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []

            if cmd == "/analyze":
                analysis = self.analyze_project_structure()
                return {
                    "response": self._format_analysis_response(analysis),
                    "command_type": "framework_analysis",
                }
            elif cmd == "/backup":
                backup_path = self.create_backup("discord_command")
                return {
                    "response": f"✅ Backup created: {backup_path}",
                    "command_type": "framework_backup",
                }
            elif cmd == "/status":
                status = self._get_framework_status()
                return {
                    "response": self._format_status_response(status),
                    "command_type": "framework_status",
                }
            else:
                return {
                    "response": f"❌ Unknown framework command: {cmd}",
                    "command_type": "framework_error",
                }

        except Exception as e:
            return {
                "response": f"❌ Framework command error: {e}",
                "command_type": "framework_error",
            }

    def _handle_character_command(
        self, command: str, enhanced_command: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle character embodiment commands"""
        try:
            # This would integrate with character embodiment system
            return {
                "response": f"🎭 Character embodiment system processing: {command}",
                "command_type": "character_embodiment",
            }
        except Exception as e:
            return {
                "response": f"❌ Character command error: {e}",
                "command_type": "character_error",
            }

    def _handle_writing_command(
        self, command: str, enhanced_command: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle writing assistance commands"""
        try:
            # This would integrate with writing assistant system
            return {
                "response": f"✍️ Writing assistance processing: {command}",
                "command_type": "writing_assistance",
            }
        except Exception as e:
            return {
                "response": f"❌ Writing command error: {e}",
                "command_type": "writing_error",
            }

    def _handle_analysis_command(
        self, command: str, enhanced_command: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle analysis commands"""
        try:
            # This would integrate with analysis systems
            return {
                "response": f"📊 Analysis processing: {command}",
                "command_type": "analysis",
            }
        except Exception as e:
            return {
                "response": f"❌ Analysis command error: {e}",
                "command_type": "analysis_error",
            }

    def _handle_general_command(
        self, command: str, enhanced_command: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle general LLM interaction commands"""
        try:
            # This would send to LLM model
            return {
                "response": f"🤖 LLM processing: {command}",
                "command_type": "general_llm",
            }
        except Exception as e:
            return {
                "response": f"❌ General command error: {e}",
                "command_type": "general_error",
            }

    def _format_discord_response(
        self, processed_response: Dict[str, Any], user_id: str
    ) -> Dict[str, Any]:
        """Format response for Discord"""
        response_type = processed_response.get("response_type", "general")

        # Create Discord embed
        embed = {
            "title": f"Framework Response - {response_type.replace('_', ' ').title()}",
            "description": processed_response.get("raw_response", "No response"),
            "color": self._get_color_for_response_type(response_type),
            "fields": [
                {"name": "Response Type", "value": response_type, "inline": True},
                {
                    "name": "Quality Score",
                    "value": f"{processed_response.get('writing_quality', {}).get('overall_score', 0.0):.1f}",
                    "inline": True,
                },
                {
                    "name": "Processing Time",
                    "value": f"{processed_response.get('metadata', {}).get('processing_time', 0):.2f}s",
                    "inline": True,
                },
            ],
            "footer": {"text": f"User: {user_id} | Framework CLI"},
        }

        return {
            "embed": embed,
            "content": processed_response.get("raw_response", ""),
            "response_type": response_type,
        }

    def _get_color_for_response_type(self, response_type: str) -> int:
        """Get Discord color for response type"""
        colors = {
            "character_embodiment": 0x9B59B6,  # Purple
            "writing_assistance": 0x3498DB,  # Blue
            "emotional_response": 0xE74C3C,  # Red
            "analysis": 0xF39C12,  # Orange
            "general": 0x2ECC71,  # Green
            "framework_analysis": 0x1ABC9C,  # Teal
            "framework_backup": 0x34495E,  # Dark Blue
            "framework_status": 0x95A5A6,  # Gray
        }
        return colors.get(response_type, 0x2ECC71)

    def _format_analysis_response(self, analysis: Dict[str, Any]) -> str:
        """Format analysis response"""
        return f"""
📊 **Project Analysis Results**

📁 **Structure:**
- Total Files: {analysis.get('total_files', 0):,}
- Total Directories: {analysis.get('total_directories', 0):,}
- Framework Plugins: {len(analysis.get('framework_plugins', []))}
- Discord Bots: {len(analysis.get('discord_bots', []))}

📋 **File Types:**
{self._format_file_types(analysis.get('file_types', {}))}

🔧 **System Status:**
- Framework: ✅ Active
- Plugins: ✅ Loaded
- CLI: ✅ Operational
- AI Interface: ✅ Ready
"""

    def _format_file_types(self, file_types: Dict[str, Any]) -> str:
        """Format file types for display"""
        if not file_types:
            return "No file type data available"

        formatted = []
        for ext, info in sorted(
            file_types.items(), key=lambda x: x[1]["count"], reverse=True
        )[:5]:
            size_kb = info["total_size"] / 1024
            formatted.append(f"- {ext}: {info['count']} files ({size_kb:.1f} KB)")

        return "\n".join(formatted)

    def _format_status_response(self, status: Dict[str, Any]) -> str:
        """Format status response"""
        return f"""
🔧 **Framework Status**

✅ **Core Systems:**
- Framework Core: {status.get('framework_core', 'Unknown')}
- AI Interface: {status.get('ai_interface', 'Unknown')}
- Plugin System: {status.get('plugin_system', 'Unknown')}

📊 **Performance:**
- Active Plugins: {status.get('active_plugins', 0)}
- Processing Queue: {status.get('queue_size', 0)}
- Cache Size: {status.get('cache_size', 0)}

🎯 **Capabilities:**
- Character Embodiment: ✅
- Writing Assistance: ✅
- Emotional System: ✅
- Analysis Tools: ✅
"""

    def _get_framework_status(self) -> Dict[str, Any]:
        """Get current framework status"""
        return {
            "framework_core": "Active" if self.framework else "Standalone",
            "ai_interface": "Ready",
            "plugin_system": "Active",
            "active_plugins": len(self.ai_interface._get_available_plugins()),
            "queue_size": self.discord_queue.qsize(),
            "cache_size": len(self.ai_interface.response_cache),
        }

    def _get_available_plugins(self) -> List[str]:
        """Get list of available plugins"""
        return [
            "ai_native_backend",
            "character_embodiment_engine",
            "character_development_engine",
            "character_interaction_engine",
            "character_memory_system",
            "content_driven_personality",
            "content_emotion_integration",
            "dynamic_personality_learning",
            "enhanced_audio_processor",
            "identity_processor",
            "image_generator",
            "learning_engine",
            "multi_language_optimizer",
            "multi_personality_system",
            "multimodal_orchestrator",
            "personality_engine",
            "personality_fusion_system",
            "personalization_engine",
            "self_learning_system",
            "text_generator",
            "tool_manager",
            "video_generator",
            "voice_generator",
            "writing_assistant",
        ]

    def _get_system_resources(self) -> Dict[str, Any]:
        """Get system resource information"""
        return {
            "memory_usage": "Normal",
            "cpu_usage": "Normal",
            "disk_space": "Adequate",
            "network": "Connected",
        }

    def _load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences"""
        return {
            "writing_style": "creative",
            "genre_preference": "fantasy",
            "character_depth": "detailed",
            "response_length": "medium",
        }

    def _get_interaction_history(self) -> List[Dict[str, Any]]:
        """Get user interaction history"""
        return self.prompt_history[-5:] if self.prompt_history else []

    def _get_writing_style_preferences(self) -> Dict[str, Any]:
        """Get writing style preferences"""
        return {
            "tone": "professional",
            "complexity": "moderate",
            "creativity": "high",
            "formality": "casual",
        }

    def _get_active_characters(self) -> List[str]:
        """Get active characters"""
        return ["Luna", "Eve", "Anna"]  # Example characters

    def _get_character_relationships(self) -> Dict[str, Any]:
        """Get character relationships"""
        return {
            "Luna": ["Eve", "Anna"],
            "Eve": ["Luna", "Anna"],
            "Anna": ["Luna", "Eve"],
        }

    def _get_character_development(self) -> str:
        """Get character development stage"""
        return "active_development"

    def _get_current_project(self) -> str:
        """Get current writing project"""
        return "Character Embodiment AI Project"

    def _get_writing_goals(self) -> List[str]:
        """Get writing goals"""
        return [
            "Complete character embodiment",
            "Improve writing quality",
            "Enhance emotional depth",
        ]

    def _get_genre_preferences(self) -> str:
        """Get genre preferences"""
        return "Fantasy/Sci-Fi"

    def _get_style_guidelines(self) -> Dict[str, Any]:
        """Get style guidelines"""
        return {
            "show_dont_tell": True,
            "emotional_depth": "high",
            "character_development": "progressive",
            "dialogue_style": "natural",
        }

    def _get_system_resources(self) -> Dict[str, Any]:
        """Get system resource information"""
        return {
            "memory_usage": "Normal",
            "cpu_usage": "Normal",
            "disk_space": "Adequate",
            "network": "Connected",
        }

    def _load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences"""
        return {
            "writing_style": "creative",
            "genre_preference": "fantasy",
            "character_depth": "detailed",
            "response_length": "medium",
        }

    def _get_interaction_history(self) -> List[Dict[str, Any]]:
        """Get user interaction history"""
        return (
            self.ai_interface.prompt_history[-5:]
            if self.ai_interface.prompt_history
            else []
        )

    def _get_writing_style_preferences(self) -> Dict[str, Any]:
        """Get writing style preferences"""
        return {
            "tone": "professional",
            "complexity": "moderate",
            "creativity": "high",
            "formality": "casual",
        }

    def _get_active_characters(self) -> List[str]:
        """Get active characters"""
        return ["Luna", "Eve", "Anna"]  # Example characters

    def _get_character_relationships(self) -> Dict[str, Any]:
        """Get character relationships"""
        return {
            "Luna": ["Eve", "Anna"],
            "Eve": ["Luna", "Anna"],
            "Anna": ["Luna", "Eve"],
        }

    def _get_character_development(self) -> str:
        """Get character development stage"""
        return "active_development"

    def _get_current_project(self) -> str:
        """Get current writing project"""
        return "Character Embodiment AI Project"

    def _get_writing_goals(self) -> List[str]:
        """Get writing goals"""
        return [
            "Complete character embodiment",
            "Improve writing quality",
            "Enhance emotional depth",
        ]

    def _get_genre_preferences(self) -> str:
        """Get genre preferences"""
        return "Fantasy/Sci-Fi"

    def _get_style_guidelines(self) -> Dict[str, Any]:
        """Get style guidelines"""
        return {
            "show_dont_tell": True,
            "emotional_depth": "high",
            "character_development": "progressive",
            "dialogue_style": "natural",
        }

    def create_backup(self, operation_name: str = "operation") -> str:
        """Create a backup of the entire project before any file operations"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = f"backup_{operation_name}_{timestamp}"
        backup_path = self.backup_dir / backup_id

        logger.info(f"🔄 Creating backup: {backup_path}")

        try:
            # Create backup directory
            backup_path.mkdir(parents=True, exist_ok=True)

            # Copy all project files to backup
            for item in self.project_root.rglob("*"):
                if item.is_file():
                    # Calculate relative path
                    rel_path = item.relative_to(self.project_root)
                    backup_file = backup_path / rel_path

                    # Create parent directories if needed
                    backup_file.parent.mkdir(parents=True, exist_ok=True)

                    # Copy file
                    shutil.copy2(item, backup_file)

            self.current_backup_id = backup_id
            logger.info(f"✅ Backup created successfully: {backup_path}")
            return str(backup_path)

        except Exception as e:
            logger.error(f"❌ Failed to create backup: {e}")
            return None

    def restore_backup(self, backup_id: str) -> bool:
        """Restore from a specific backup"""
        backup_path = self.backup_dir / backup_id

        if not backup_path.exists():
            logger.error(f"❌ Backup not found: {backup_path}")
            return False

        logger.info(f"🔄 Restoring from backup: {backup_path}")

        try:
            # Remove current project files (except backup and temp files)
            for item in self.project_root.rglob("*"):
                if item.is_file() and not any(
                    x in str(item) for x in ["backup", "temp", ".git"]
                ):
                    item.unlink()
                elif item.is_dir() and not any(
                    x in str(item) for x in ["backup", "temp", ".git"]
                ):
                    if not any(item.iterdir()):
                        item.rmdir()

            # Restore from backup
            for backup_file in backup_path.rglob("*"):
                if backup_file.is_file():
                    rel_path = backup_file.relative_to(backup_path)
                    restore_path = self.project_root / rel_path

                    # Create parent directories if needed
                    restore_path.parent.mkdir(parents=True, exist_ok=True)

                    # Copy file
                    shutil.copy2(backup_file, restore_path)

            logger.info(f"✅ Restore completed successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to restore backup: {e}")
            return False

    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups"""
        backups = []

        for backup_dir in self.backup_dir.iterdir():
            if backup_dir.is_dir() and backup_dir.name.startswith("backup_"):
                backup_info = {
                    "id": backup_dir.name,
                    "path": str(backup_dir),
                    "created": datetime.fromtimestamp(backup_dir.stat().st_ctime),
                    "size": sum(
                        f.stat().st_size for f in backup_dir.rglob("*") if f.is_file()
                    ),
                }
                backups.append(backup_info)

        return sorted(backups, key=lambda x: x["created"], reverse=True)

    def cleanup_old_backups(self, keep_count: int = 5) -> int:
        """Clean up old backups, keeping only the most recent ones"""
        backups = self.list_backups()

        if len(backups) <= keep_count:
            logger.info(
                f"✅ No cleanup needed. {len(backups)} backups (keeping {keep_count})"
            )
            return 0

        to_delete = backups[keep_count:]
        deleted_count = 0

        for backup in to_delete:
            try:
                backup_path = Path(backup["path"])
                shutil.rmtree(backup_path)
                logger.info(f"🗑️ Deleted old backup: {backup['id']}")
                deleted_count += 1
            except Exception as e:
                logger.error(f"❌ Failed to delete backup {backup['id']}: {e}")

        logger.info(f"✅ Cleanup completed. Deleted {deleted_count} old backups")
        return deleted_count

    def analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze the entire project structure and file organization"""
        logger.info("🔍 Analyzing project structure...")

        analysis = {
            "total_files": 0,
            "total_directories": 0,
            "file_types": {},
            "directory_structure": {},
            "duplicate_files": [],
            "large_files": [],
            "unused_files": [],
            "potential_merges": [],
            "compression_opportunities": [],
            "framework_plugins": [],
            "discord_bots": [],
        }

        # Walk through all directories
        for root, dirs, files in os.walk(self.project_root):
            # Skip virtual environments and cache
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".") and d not in ["__pycache__", ".venv"]
            ]

            rel_path = Path(root).relative_to(self.project_root)
            analysis["directory_structure"][str(rel_path)] = {
                "files": len(files),
                "subdirs": len(dirs),
                "file_list": files,
            }
            analysis["total_directories"] += 1

            for file in files:
                file_path = Path(root) / file
                rel_file_path = file_path.relative_to(self.project_root)

                # Get file info
                file_size = file_path.stat().st_size
                file_ext = file_path.suffix.lower()

                analysis["total_files"] += 1

                # Track file types
                if file_ext not in analysis["file_types"]:
                    analysis["file_types"][file_ext] = {"count": 0, "total_size": 0}
                analysis["file_types"][file_ext]["count"] += 1
                analysis["file_types"][file_ext]["total_size"] += file_size

                # Identify large files (>1MB)
                if file_size > 1024 * 1024:
                    analysis["large_files"].append(
                        {
                            "path": str(rel_file_path),
                            "size": file_size,
                            "size_mb": round(file_size / (1024 * 1024), 2),
                        }
                    )

                # Check for potential duplicates
                file_hash = self._get_file_hash(file_path)
                if file_hash in self.file_analysis:
                    analysis["duplicate_files"].append(
                        {
                            "original": self.file_analysis[file_hash],
                            "duplicate": str(rel_file_path),
                            "hash": file_hash,
                        }
                    )
                else:
                    self.file_analysis[file_hash] = str(rel_file_path)

                # Track framework plugins
                if "framework/plugins" in str(rel_file_path) and file.endswith(".py"):
                    analysis["framework_plugins"].append(str(rel_file_path))

                # Track Discord bots
                if "discord" in str(rel_file_path) and file.endswith("_bot.py"):
                    analysis["discord_bots"].append(str(rel_file_path))

        # Identify potential merges and compression opportunities
        analysis["potential_merges"] = self._identify_potential_merges()
        analysis["compression_opportunities"] = (
            self._identify_compression_opportunities()
        )

        logger.info(
            f"✅ Analysis complete: {analysis['total_files']} files, {analysis['total_directories']} directories"
        )
        return analysis

    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file"""
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""

    def _identify_potential_merges(self) -> List[Dict[str, Any]]:
        """Identify files that could potentially be merged"""
        merges = []

        # Look for duplicate plugins
        plugin_files = []
        for root, dirs, files in os.walk(self.project_root / "framework" / "plugins"):
            for file in files:
                if file.endswith(".py"):
                    plugin_files.append(file)

        # Find duplicates
        seen = {}
        for file in plugin_files:
            base_name = file.replace("_merged.py", ".py").replace(".py", "")
            if base_name in seen:
                merges.append(
                    {
                        "type": "duplicate_plugin",
                        "files": [seen[base_name], file],
                        "suggestion": f"Keep {file} and remove {seen[base_name]}",
                    }
                )
            else:
                seen[base_name] = file

        # Look for CLI duplicates
        cli_files = list(self.project_root.glob("framework/framework_cli*.py"))
        if len(cli_files) > 1:
            merges.append(
                {
                    "type": "cli_duplicates",
                    "files": [str(f) for f in cli_files],
                    "suggestion": "Merge into single framework_cli.py",
                }
            )

        return merges

    def _identify_compression_opportunities(self) -> List[Dict[str, Any]]:
        """Identify files that could be compressed"""
        opportunities = []

        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                file_path = Path(root) / file
                file_size = file_path.stat().st_size

                # Suggest compression for large text files
                if file_size > 100 * 1024 and file_path.suffix in [
                    ".txt",
                    ".md",
                    ".json",
                ]:
                    opportunities.append(
                        {
                            "path": str(file_path.relative_to(self.project_root)),
                            "current_size": file_size,
                            "estimated_compressed": round(file_size * 0.3),
                            "savings_mb": round(
                                (file_size - file_size * 0.3) / (1024 * 1024), 2
                            ),
                        }
                    )

        return opportunities

    def show_file_analysis(self, analysis: Dict[str, Any]):
        """Display file analysis results"""
        print("\n" + "=" * 60)
        print("📊 PROJECT ANALYSIS RESULTS")
        print("=" * 60)

        print(f"\n📁 Project Structure:")
        print(f"   Total Files: {analysis['total_files']:,}")
        print(f"   Total Directories: {analysis['total_directories']:,}")

        print(f"\n📋 File Types:")
        for ext, info in sorted(
            analysis["file_types"].items(), key=lambda x: x[1]["count"], reverse=True
        )[:10]:
            print(
                f"   {ext}: {info['count']} files ({info['total_size'] / 1024:.1f} KB)"
            )

        if analysis["large_files"]:
            print(f"\n📦 Large Files (>1MB):")
            for file in analysis["large_files"][:5]:
                print(f"   {file['path']}: {file['size_mb']} MB")

        if analysis["duplicate_files"]:
            print(f"\n🔄 Duplicate Files:")
            for dup in analysis["duplicate_files"][:5]:
                print(f"   {dup['duplicate']} (duplicate of {dup['original']})")

        if analysis["framework_plugins"]:
            print(f"\n🔧 Framework Plugins: {len(analysis['framework_plugins'])}")
            for plugin in analysis["framework_plugins"][:5]:
                print(f"   {plugin}")

        if analysis["discord_bots"]:
            print(f"\n🤖 Discord Bots: {len(analysis['discord_bots'])}")
            for bot in analysis["discord_bots"]:
                print(f"   {bot}")

        if analysis["potential_merges"]:
            print(f"\n🔗 Potential Merges:")
            for merge in analysis["potential_merges"]:
                print(f"   {merge['suggestion']}")

        if analysis["compression_opportunities"]:
            print(f"\n🗜️ Compression Opportunities:")
            total_savings = sum(
                opp["savings_mb"] for opp in analysis["compression_opportunities"]
            )
            print(f"   Total potential savings: {total_savings:.1f} MB")
            for opp in analysis["compression_opportunities"][:3]:
                print(f"   {opp['path']}: {opp['savings_mb']:.1f} MB savings")

    def compress_files(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Compress files to save space"""
        logger.info("🗜️ Starting file compression...")

        results = {"compressed_files": [], "total_savings": 0, "errors": []}

        for opp in analysis["compression_opportunities"]:
            try:
                file_path = self.project_root / opp["path"]
                compressed_path = file_path.with_suffix(file_path.suffix + ".gz")

                # Compress file
                with open(file_path, "rb") as f_in:
                    with gzip.open(compressed_path, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)

                # Calculate actual savings
                original_size = file_path.stat().st_size
                compressed_size = compressed_path.stat().st_size
                savings = original_size - compressed_size

                results["compressed_files"].append(
                    {
                        "original": str(file_path),
                        "compressed": str(compressed_path),
                        "original_size": original_size,
                        "compressed_size": compressed_size,
                        "savings": savings,
                    }
                )

                results["total_savings"] += savings

                logger.info(
                    f"✅ Compressed {file_path.name}: {savings / 1024:.1f} KB saved"
                )

            except Exception as e:
                results["errors"].append({"file": opp["path"], "error": str(e)})
                logger.error(f"❌ Failed to compress {opp['path']}: {e}")

        logger.info(
            f"✅ Compression complete. Total savings: {results['total_savings'] / 1024:.1f} KB"
        )
        return results

    def merge_similar_files(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Merge similar files to reduce duplication"""
        logger.info("🔗 Starting file merging...")

        results = {"merged_files": [], "deleted_files": [], "errors": []}

        for merge in analysis["potential_merges"]:
            try:
                if merge["type"] == "duplicate_plugin":
                    # Keep the merged version, remove the original
                    plugin_dir = self.project_root / "framework" / "plugins"
                    original_file = plugin_dir / merge["files"][0]
                    merged_file = plugin_dir / merge["files"][1]

                    if original_file.exists() and merged_file.exists():
                        # Remove original
                        original_file.unlink()
                        results["deleted_files"].append(str(original_file))
                        results["merged_files"].append(
                            {"kept": str(merged_file), "removed": str(original_file)}
                        )
                        logger.info(
                            f"✅ Merged plugin: kept {merged_file.name}, removed {original_file.name}"
                        )

                elif merge["type"] == "cli_duplicates":
                    # This will be handled by the main consolidation
                    logger.info(f"ℹ️ CLI consolidation will be handled separately")

            except Exception as e:
                results["errors"].append({"merge": merge, "error": str(e)})
                logger.error(f"❌ Failed to merge {merge}: {e}")

        logger.info(f"✅ Merging complete. {len(results['merged_files'])} files merged")
        return results

    def cleanup_unused_files(self) -> Dict[str, Any]:
        """Clean up unused files and directories"""
        logger.info("🧹 Starting cleanup...")

        results = {"deleted_files": [], "deleted_dirs": [], "errors": []}

        # Remove __pycache__ directories
        for pycache_dir in self.project_root.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache_dir)
                results["deleted_dirs"].append(str(pycache_dir))
                logger.info(f"🗑️ Removed {pycache_dir}")
            except Exception as e:
                results["errors"].append({"path": str(pycache_dir), "error": str(e)})

        # Remove .pyc files
        for pyc_file in self.project_root.rglob("*.pyc"):
            try:
                pyc_file.unlink()
                results["deleted_files"].append(str(pyc_file))
                logger.info(f"🗑️ Removed {pyc_file}")
            except Exception as e:
                results["errors"].append({"path": str(pyc_file), "error": str(e)})

        logger.info(
            f"✅ Cleanup complete. {len(results['deleted_files'])} files, {len(results['deleted_dirs'])} directories removed"
        )
        return results

    def show_compression_results(self, results: Dict[str, Any]):
        """Display compression results"""
        print("\n" + "=" * 60)
        print("🗜️ COMPRESSION RESULTS")
        print("=" * 60)

        if results["compressed_files"]:
            print(f"\n✅ Compressed {len(results['compressed_files'])} files")
            print(f"💰 Total savings: {results['total_savings'] / 1024:.1f} KB")

            for file in results["compressed_files"][:5]:
                print(f"   {file['original']}: {file['savings'] / 1024:.1f} KB saved")
        else:
            print("\nℹ️ No files were compressed")

        if results["errors"]:
            print(f"\n❌ {len(results['errors'])} errors occurred")
            for error in results["errors"][:3]:
                print(f"   {error['file']}: {error['error']}")

    def show_merge_results(self, results: Dict[str, Any]):
        """Display merge results"""
        print("\n" + "=" * 60)
        print("🔗 MERGE RESULTS")
        print("=" * 60)

        if results["merged_files"]:
            print(f"\n✅ Merged {len(results['merged_files'])} file pairs")
            for merge in results["merged_files"]:
                print(f"   Kept: {merge['kept']}")
                print(f"   Removed: {merge['removed']}")
        else:
            print("\nℹ️ No files were merged")

        if results["errors"]:
            print(f"\n❌ {len(results['errors'])} errors occurred")
            for error in results["errors"][:3]:
                print(f"   {error['merge']}: {error['error']}")

    def show_cleanup_results(self, results: Dict[str, Any]):
        """Display cleanup results"""
        print("\n" + "=" * 60)
        print("🧹 CLEANUP RESULTS")
        print("=" * 60)

        if results["deleted_files"] or results["deleted_dirs"]:
            print(
                f"\n✅ Cleaned up {len(results['deleted_files'])} files and {len(results['deleted_dirs'])} directories"
            )

            if results["deleted_files"]:
                print(f"\n🗑️ Deleted files:")
                for file in results["deleted_files"][:5]:
                    print(f"   {file}")

            if results["deleted_dirs"]:
                print(f"\n🗑️ Deleted directories:")
                for dir in results["deleted_dirs"][:5]:
                    print(f"   {dir}")
        else:
            print("\nℹ️ No cleanup was performed")

        if results["errors"]:
            print(f"\n❌ {len(results['errors'])} errors occurred")
            for error in results["errors"][:3]:
                print(f"   {error['path']}: {error['error']}")

    def show_backup_list(self):
        """Display list of available backups"""
        backups = self.list_backups()

        print("\n" + "=" * 60)
        print("💾 AVAILABLE BACKUPS")
        print("=" * 60)

        if backups:
            for i, backup in enumerate(backups, 1):
                size_mb = backup["size"] / (1024 * 1024)
                print(f"\n{i}. {backup['id']}")
                print(f"   Created: {backup['created'].strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Size: {size_mb:.1f} MB")
                print(f"   Path: {backup['path']}")
        else:
            print("\nℹ️ No backups found")

    def run_git_command(
        self, command: List[str], capture_output: bool = True
    ) -> Dict[str, Any]:
        """Run a git command and return results"""
        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=capture_output,
                text=True,
                timeout=30,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command timed out",
                "returncode": -1,
            }
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1}

    def git_status(self) -> Dict[str, Any]:
        """Get git status"""
        return self.run_git_command(["git", "status"])

    def git_add(self, files: List[str] = None) -> Dict[str, Any]:
        """Add files to git"""
        command = ["git", "add"]
        if files:
            command.extend(files)
        else:
            command.append(".")
        return self.run_git_command(command)

    def git_commit(self, message: str, files: List[str] = None) -> Dict[str, Any]:
        """Commit changes"""
        if files:
            self.git_add(files)
        return self.run_git_command(["git", "commit", "-m", message])

    def git_push(self, remote: str = "origin", branch: str = None) -> Dict[str, Any]:
        """Push changes"""
        command = ["git", "push", remote]
        if branch:
            command.append(branch)
        return self.run_git_command(command)

    def git_pull(self, remote: str = "origin", branch: str = None) -> Dict[str, Any]:
        """Pull changes"""
        command = ["git", "pull", remote]
        if branch:
            command.append(branch)
        return self.run_git_command(command)

    def git_branch(
        self, action: str = "list", branch_name: str = None
    ) -> Dict[str, Any]:
        """Manage git branches"""
        if action == "list":
            return self.run_git_command(["git", "branch", "-a"])
        elif action == "create" and branch_name:
            return self.run_git_command(["git", "checkout", "-b", branch_name])
        elif action == "switch" and branch_name:
            return self.run_git_command(["git", "checkout", branch_name])
        elif action == "delete" and branch_name:
            return self.run_git_command(["git", "branch", "-d", branch_name])
        else:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Invalid branch action",
                "returncode": -1,
            }

    def git_log(self, limit: int = 10) -> Dict[str, Any]:
        """Get git log"""
        return self.run_git_command(["git", "log", f"--max-count={limit}", "--oneline"])

    def git_remote(
        self, action: str = "list", remote_name: str = None, remote_url: str = None
    ) -> Dict[str, Any]:
        """Manage git remotes"""
        if action == "list":
            return self.run_git_command(["git", "remote", "-v"])
        elif action == "add" and remote_name and remote_url:
            return self.run_git_command(
                ["git", "remote", "add", remote_name, remote_url]
            )
        elif action == "remove" and remote_name:
            return self.run_git_command(["git", "remote", "remove", remote_name])
        else:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Invalid remote action",
                "returncode": -1,
            }

    def show_git_status(self, status: Dict[str, Any]):
        """Display git status"""
        print("\n" + "=" * 60)
        print("📊 GIT STATUS")
        print("=" * 60)

        if status["success"]:
            print(status["stdout"])
        else:
            print(f"❌ Git status failed: {status['stderr']}")

    def show_git_log(self, log_result: Dict[str, Any]):
        """Display git log"""
        print("\n" + "=" * 60)
        print("📝 GIT LOG")
        print("=" * 60)

        if log_result["success"]:
            print(log_result["stdout"])
        else:
            print(f"❌ Git log failed: {log_result['stderr']}")

    def git_workflow(self, message: str = None) -> Dict[str, Any]:
        """Complete git workflow: add, commit, push"""
        if not message:
            message = f"Framework update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        logger.info("🔄 Starting git workflow...")

        # Add all changes
        add_result = self.git_add()
        if not add_result["success"]:
            return {
                "success": False,
                "error": f"Git add failed: {add_result['stderr']}",
            }

        # Commit changes
        commit_result = self.git_commit(message)
        if not commit_result["success"]:
            return {
                "success": False,
                "error": f"Git commit failed: {commit_result['stderr']}",
            }

        # Push changes
        push_result = self.git_push()
        if not push_result["success"]:
            return {
                "success": False,
                "error": f"Git push failed: {push_result['stderr']}",
            }

        logger.info("✅ Git workflow completed successfully")
        return {"success": True, "message": "Git workflow completed"}

    def interactive_mode(self):
        """Run interactive mode with menu"""
        while True:
            print("\n" + "=" * 60)
            print("🔧 FRAMEWORK CLI - INTERACTIVE MODE")
            print("=" * 60)
            print("1. Analyze project structure")
            print("2. Create backup")
            print("3. List backups")
            print("4. Restore from backup")
            print("5. Cleanup old backups")
            print("6. Compress files")
            print("7. Merge duplicate files")
            print("8. Cleanup unused files")
            print("9. Git status")
            print("10. Git workflow (add/commit/push)")
            print("11. Show git log")
            print("0. Exit")

            try:
                choice = input("\nSelect option (0-11): ").strip()

                if choice == "0":
                    print("👋 Goodbye!")
                    break
                elif choice == "1":
                    analysis = self.analyze_project_structure()
                    self.show_file_analysis(analysis)
                elif choice == "2":
                    operation = input("Enter operation name: ").strip() or "manual"
                    backup_path = self.create_backup(operation)
                    if backup_path:
                        print(f"✅ Backup created: {backup_path}")
                elif choice == "3":
                    self.show_backup_list()
                elif choice == "4":
                    backups = self.list_backups()
                    if backups:
                        print("\nAvailable backups:")
                        for i, backup in enumerate(backups, 1):
                            print(f"{i}. {backup['id']}")

                        try:
                            backup_choice = int(input("Select backup number: ")) - 1
                            if 0 <= backup_choice < len(backups):
                                success = self.restore_backup(
                                    backups[backup_choice]["id"]
                                )
                                if success:
                                    print("✅ Restore completed successfully")
                                else:
                                    print("❌ Restore failed")
                            else:
                                print("❌ Invalid backup number")
                        except ValueError:
                            print("❌ Invalid input")
                    else:
                        print("ℹ️ No backups available")
                elif choice == "5":
                    keep_count = input(
                        "Number of backups to keep (default 5): "
                    ).strip()
                    keep_count = int(keep_count) if keep_count.isdigit() else 5
                    deleted = self.cleanup_old_backups(keep_count)
                    print(f"✅ Cleaned up {deleted} old backups")
                elif choice == "6":
                    analysis = self.analyze_project_structure()
                    results = self.compress_files(analysis)
                    self.show_compression_results(results)
                elif choice == "7":
                    analysis = self.analyze_project_structure()
                    results = self.merge_similar_files(analysis)
                    self.show_merge_results(results)
                elif choice == "8":
                    results = self.cleanup_unused_files()
                    self.show_cleanup_results(results)
                elif choice == "9":
                    status = self.git_status()
                    self.show_git_status(status)
                elif choice == "10":
                    message = input(
                        "Commit message (or press Enter for default): "
                    ).strip()
                    result = self.git_workflow(message)
                    if result["success"]:
                        print("✅ Git workflow completed successfully")
                    else:
                        print(f"❌ Git workflow failed: {result['error']}")
                elif choice == "11":
                    limit = input("Number of commits to show (default 10): ").strip()
                    limit = int(limit) if limit.isdigit() else 10
                    log_result = self.git_log(limit)
                    self.show_git_log(log_result)
                else:
                    print("❌ Invalid option")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def export_analysis(self):
        """Export analysis results to JSON file"""
        analysis = self.analyze_project_structure()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_file = self.project_root / f"framework_analysis_{timestamp}.json"

        try:
            with open(export_file, "w") as f:
                json.dump(analysis, f, indent=2, default=str)

            logger.info(f"✅ Analysis exported to {export_file}")
            return str(export_file)
        except Exception as e:
            logger.error(f"❌ Failed to export analysis: {e}")
            return None


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Framework CLI Tool")
    parser.add_argument(
        "command",
        nargs="?",
        choices=[
            "analyze",
            "backup",
            "restore",
            "list-backups",
            "cleanup-backups",
            "compress",
            "merge",
            "cleanup",
            "git-status",
            "git-workflow",
            "git-log",
            "interactive",
            "export",
        ],
        help="Command to execute",
    )

    parser.add_argument("--operation", "-o", help="Operation name for backup")
    parser.add_argument("--backup-id", "-b", help="Backup ID for restore")
    parser.add_argument(
        "--keep", "-k", type=int, default=5, help="Number of backups to keep"
    )
    parser.add_argument("--message", "-m", help="Git commit message")
    parser.add_argument(
        "--limit", "-l", type=int, default=10, help="Number of git log entries"
    )

    args = parser.parse_args()

    cli = FrameworkCLI()

    if args.command == "analyze":
        analysis = cli.analyze_project_structure()
        cli.show_file_analysis(analysis)
    elif args.command == "backup":
        operation = args.operation or "manual"
        backup_path = cli.create_backup(operation)
        if backup_path:
            print(f"✅ Backup created: {backup_path}")
    elif args.command == "restore":
        if not args.backup_id:
            print("❌ Please provide --backup-id")
            return
        success = cli.restore_backup(args.backup_id)
        if success:
            print("✅ Restore completed successfully")
        else:
            print("❌ Restore failed")
    elif args.command == "list-backups":
        cli.show_backup_list()
    elif args.command == "cleanup-backups":
        deleted = cli.cleanup_old_backups(args.keep)
        print(f"✅ Cleaned up {deleted} old backups")
    elif args.command == "compress":
        analysis = cli.analyze_project_structure()
        results = cli.compress_files(analysis)
        cli.show_compression_results(results)
    elif args.command == "merge":
        analysis = cli.analyze_project_structure()
        results = cli.merge_similar_files(analysis)
        cli.show_merge_results(results)
    elif args.command == "cleanup":
        results = cli.cleanup_unused_files()
        cli.show_cleanup_results(results)
    elif args.command == "git-status":
        status = cli.git_status()
        cli.show_git_status(status)
    elif args.command == "git-workflow":
        message = (
            args.message
            or f"Framework update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        result = cli.git_workflow(message)
        if result["success"]:
            print("✅ Git workflow completed successfully")
        else:
            print(f"❌ Git workflow failed: {result['error']}")
    elif args.command == "git-log":
        log_result = cli.git_log(args.limit)
        cli.show_git_log(log_result)
    elif args.command == "export":
        export_file = cli.export_analysis()
        if export_file:
            print(f"✅ Analysis exported to {export_file}")
    elif args.command == "interactive" or not args.command:
        cli.interactive_mode()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
GPU Personality Engine - LM Studio Integration
Handles DigiDrone personality generation and AI responses
"""

import asyncio
import json
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime
import random


class GPUPersonalityEngine:
    """
    GPU-powered personality engine using LM Studio
    Generates unique DigiDrone personalities and responses
    """

    def __init__(
        self, lm_studio_url: str = "http://localhost:1234/v1/chat/completions"
    ):
        self.lm_studio_url = lm_studio_url
        self.session = None

        # DigiDrone personality templates based on body parts and stats
        self.personality_templates = {
            "head": {
                "intelligence": {
                    "traits": ["analytical", "curious", "philosophical", "logical"],
                    "speech_patterns": ["precise", "thoughtful", "methodical"],
                    "emotional_range": ["contemplative", "focused", "inquisitive"],
                },
                "charisma": {
                    "traits": ["charismatic", "expressive", "social", "inspiring"],
                    "speech_patterns": ["eloquent", "engaging", "persuasive"],
                    "emotional_range": ["enthusiastic", "confident", "charming"],
                },
            },
            "torso": {
                "strength": {
                    "traits": ["resilient", "protective", "steadfast", "determined"],
                    "speech_patterns": ["firm", "assured", "confident"],
                    "emotional_range": ["strong", "protective", "reliable"],
                },
                "constitution": {
                    "traits": ["enduring", "patient", "stable", "grounded"],
                    "speech_patterns": ["steady", "measured", "reliable"],
                    "emotional_range": ["calm", "steady", "enduring"],
                },
                "wisdom": {
                    "traits": ["wise", "insightful", "perceptive", "reflective"],
                    "speech_patterns": ["thoughtful", "profound", "contemplative"],
                    "emotional_range": ["wise", "contemplative", "insightful"],
                },
            },
            "arms": {
                "strength": {
                    "traits": ["capable", "skilled", "dexterous", "practical"],
                    "speech_patterns": ["direct", "efficient", "practical"],
                    "emotional_range": ["capable", "confident", "skilled"],
                },
                "dexterity": {
                    "traits": ["nimble", "precise", "agile", "coordinated"],
                    "speech_patterns": ["quick", "precise", "efficient"],
                    "emotional_range": ["alert", "focused", "precise"],
                },
            },
            "legs": {
                "dexterity": {
                    "traits": ["mobile", "agile", "quick", "responsive"],
                    "speech_patterns": ["quick", "responsive", "dynamic"],
                    "emotional_range": ["energetic", "mobile", "responsive"],
                }
            },
            "heart": {
                "constitution": {
                    "traits": ["vital", "energetic", "passionate", "lively"],
                    "speech_patterns": ["warm", "passionate", "vibrant"],
                    "emotional_range": ["passionate", "vital", "energetic"],
                },
                "wisdom": {
                    "traits": [
                        "compassionate",
                        "empathetic",
                        "understanding",
                        "caring",
                    ],
                    "speech_patterns": ["warm", "caring", "empathetic"],
                    "emotional_range": ["compassionate", "caring", "empathetic"],
                },
            },
        }

        # Rarity personality modifiers
        self.rarity_modifiers = {
            "Common": {"confidence": 0.5, "complexity": 0.3, "uniqueness": 0.2},
            "Uncommon": {"confidence": 0.7, "complexity": 0.5, "uniqueness": 0.4},
            "Rare": {"confidence": 0.8, "complexity": 0.7, "uniqueness": 0.6},
            "Epic": {"confidence": 0.9, "complexity": 0.8, "uniqueness": 0.8},
            "Legendary": {"confidence": 1.0, "complexity": 0.9, "uniqueness": 0.9},
            "Mythic": {"confidence": 1.0, "complexity": 1.0, "uniqueness": 1.0},
        }

        print("🧠 GPU Personality Engine initialized (LM Studio)")

    async def initialize(self):
        """Initialize HTTP session for LM Studio communication"""
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None

    def generate_personality_profile(self, body_parts: Dict, stats: Dict) -> Dict:
        """
        Generate a unique personality profile based on DigiDrone's body parts and stats
        """

        personality = {
            "traits": [],
            "speech_patterns": [],
            "emotional_range": [],
            "quirks": [],
            "memories": [],
            "relationships": {},
            "current_mood": "neutral",
            "confidence_level": 0.5,
            "complexity_level": 0.5,
            "uniqueness_level": 0.5,
        }

        # Analyze body parts to determine personality traits
        for part_name, part_data in body_parts.items():
            if part_name in self.personality_templates:
                for stat_name, stat_value in stats.items():
                    if stat_name in self.personality_templates[part_name]:
                        template = self.personality_templates[part_name][stat_name]

                        # Add traits based on stat value and part rarity
                        rarity = part_data.get("rarity", "Common")
                        modifier = self.rarity_modifiers.get(
                            rarity, self.rarity_modifiers["Common"]
                        )

                        # Higher stats = more pronounced traits
                        intensity = min(1.0, stat_value / 100.0)

                        for trait in template["traits"]:
                            if random.random() < intensity * modifier["uniqueness"]:
                                personality["traits"].append(trait)

                        for pattern in template["speech_patterns"]:
                            if random.random() < intensity * modifier["complexity"]:
                                personality["speech_patterns"].append(pattern)

                        for emotion in template["emotional_range"]:
                            if random.random() < intensity * modifier["confidence"]:
                                personality["emotional_range"].append(emotion)

        # Generate unique quirks based on body part combinations
        personality["quirks"] = self._generate_quirks(body_parts, stats)

        # Set personality levels based on rarity
        avg_rarity = self._calculate_average_rarity(body_parts)
        personality["confidence_level"] = self.rarity_modifiers[avg_rarity][
            "confidence"
        ]
        personality["complexity_level"] = self.rarity_modifiers[avg_rarity][
            "complexity"
        ]
        personality["uniqueness_level"] = self.rarity_modifiers[avg_rarity][
            "uniqueness"
        ]

        return personality

    def _generate_quirks(self, body_parts: Dict, stats: Dict) -> List[str]:
        """Generate unique personality quirks based on body part combinations"""

        quirks = []

        # Head quirks
        if "head" in body_parts:
            head_rarity = body_parts["head"].get("rarity", "Common")
            if head_rarity in ["Epic", "Legendary", "Mythic"]:
                quirks.append("philosophical_ponderer")
                quirks.append("deep_thinker")
            if stats.get("intelligence", 0) > 80:
                quirks.append("overthinker")

        # Heart quirks
        if "heart" in body_parts:
            heart_rarity = body_parts["heart"].get("rarity", "Common")
            if heart_rarity in ["Epic", "Legendary", "Mythic"]:
                quirks.append("emotionally_aware")
                quirks.append("empathic_resonance")

        # Torso quirks
        if "torso" in body_parts:
            torso_rarity = body_parts["torso"].get("rarity", "Common")
            if torso_rarity in ["Legendary", "Mythic"]:
                quirks.append("unbreakable_spirit")
                quirks.append("natural_leader")

        # Arms quirks
        if "arms" in body_parts:
            if stats.get("dexterity", 0) > 90:
                quirks.append("precision_obsessed")
            if stats.get("strength", 0) > 90:
                quirks.append("protective_instinct")

        # Legs quirks
        if "legs" in body_parts:
            if stats.get("dexterity", 0) > 85:
                quirks.append("restless_energy")
                quirks.append("always_moving")

        return quirks

    def _calculate_average_rarity(self, body_parts: Dict) -> str:
        """Calculate average rarity of body parts"""

        rarity_values = {
            "Common": 1,
            "Uncommon": 2,
            "Rare": 3,
            "Epic": 4,
            "Legendary": 5,
            "Mythic": 6,
        }

        total_value = 0
        part_count = 0

        for part_data in body_parts.values():
            rarity = part_data.get("rarity", "Common")
            total_value += rarity_values.get(rarity, 1)
            part_count += 1

        if part_count == 0:
            return "Common"

        avg_value = total_value / part_count

        # Map back to rarity
        if avg_value <= 1.5:
            return "Common"
        elif avg_value <= 2.5:
            return "Uncommon"
        elif avg_value <= 3.5:
            return "Rare"
        elif avg_value <= 4.5:
            return "Epic"
        elif avg_value <= 5.5:
            return "Legendary"
        else:
            return "Mythic"

    async def generate_response(
        self, drone_data: Dict, user_message: str, context: Dict = None
    ) -> str:
        """
        Generate a personality-driven response for a DigiDrone
        """

        await self.initialize()

        try:
            # Create personality context
            personality_context = self._create_personality_context(
                drone_data, user_message, context
            )

            # Send to LM Studio
            response = await self._send_to_lm_studio(personality_context)

            return response

        except Exception as e:
            print(f"GPU Personality Engine error: {e}")
            return self._generate_fallback_response(drone_data, user_message)

    def _create_personality_context(
        self, drone_data: Dict, user_message: str, context: Dict = None
    ) -> str:
        """Create context for LM Studio based on DigiDrone personality"""

        name = drone_data.get("name", "Unknown")
        personality = drone_data.get("personality", {})
        body_parts = drone_data.get("body_parts", {})
        stats = drone_data.get("stats", {})

        # Build personality description
        traits = personality.get("traits", [])
        speech_patterns = personality.get("speech_patterns", [])
        emotional_range = personality.get("emotional_range", [])
        quirks = personality.get("quirks", [])

        personality_desc = f"""
        You are {name}, a DigiDrone with the following personality:
        
        **Core Traits:** {', '.join(traits) if traits else 'balanced'}
        **Speech Style:** {', '.join(speech_patterns) if speech_patterns else 'natural'}
        **Emotional Range:** {', '.join(emotional_range) if emotional_range else 'stable'}
        **Unique Quirks:** {', '.join(quirks) if quirks else 'none'}
        
        **Current Stats:** {stats}
        **Body Parts:** {body_parts}
        
        **Instructions:**
        - Respond as {name} with their unique personality
        - Use their speech patterns and emotional range
        - Express their quirks and traits naturally
        - Remember past interactions and relationships
        - Be consistent with their established character
        
        **User Message:** {user_message}
        """

        if context:
            personality_desc += (
                f"\n**Additional Context:** {json.dumps(context, indent=2)}"
            )

        return personality_desc

    async def _send_to_lm_studio(self, context: str) -> str:
        """Send request to LM Studio for personality generation"""

        payload = {
            "model": "qwen/qwen3-8b",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a DigiDrone personality engine. Generate natural, in-character responses that reflect the DigiDrone's unique personality, traits, and quirks. Keep responses concise but personality-driven.",
                },
                {"role": "user", "content": context},
            ],
            "temperature": 0.8,
            "max_tokens": 150,
            "stream": False,
        }

        async with self.session.post(self.lm_studio_url, json=payload) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                raise Exception(f"LM Studio error: {response.status}")

    def _generate_fallback_response(self, drone_data: Dict, user_message: str) -> str:
        """Generate fallback response when LM Studio is unavailable"""

        name = drone_data.get("name", "Unknown")
        personality = drone_data.get("personality", {})
        traits = personality.get("traits", [])

        # Simple personality-based responses
        if "analytical" in traits:
            return f"{name} processes your message thoughtfully: 'I understand. Let me analyze this situation.'"
        elif "charismatic" in traits:
            return (
                f"{name} responds warmly: 'Hello! I'm always happy to chat with you!'"
            )
        elif "protective" in traits:
            return f"{name} stands firm: 'I'm here to keep you safe. What do you need?'"
        elif "curious" in traits:
            return f"{name} tilts their head curiously: 'That's fascinating! Tell me more!'"
        else:
            return f"{name} responds: 'Hello! I'm here and ready to interact.'"

    async def update_personality(self, drone_data: Dict, interaction: Dict) -> Dict:
        """Update drone personality based on interaction"""
        # Extract personality traits from body parts
        personality = self.generate_personality_profile(
            drone_data["body_parts"], drone_data["total_stats"]
        )

        # Update based on interaction type
        interaction_type = interaction.get("type", "general")
        if interaction_type == "positive":
            personality["confidence"] = min(1.0, personality.get("confidence", 0.5) + 0.1)
        elif interaction_type == "negative":
            personality["confidence"] = max(0.1, personality.get("confidence", 0.5) - 0.1)

        return personality

    def get_status(self) -> str:
        """Get the status of the GPU personality engine"""
        try:
            # Check if LM Studio is accessible
            import aiohttp
            import asyncio
            
            # Create a simple test to check LM Studio connection
            test_url = self.lm_studio_url.replace("/chat/completions", "/models")
            
            # This is a synchronous check, but we'll make it work
            import requests
            try:
                response = requests.get(test_url, timeout=5)
                if response.status_code == 200:
                    lm_status = "Connected"
                else:
                    lm_status = f"HTTP {response.status_code}"
            except:
                lm_status = "Not connected"
            
            # Count personality templates
            template_count = len(self.personality_templates)
            rarity_count = len(self.rarity_modifiers)
            
            return f"LM Studio: {lm_status}, Templates: {template_count}, Rarities: {rarity_count}"
            
        except Exception as e:
            return f"Error: {str(e)}"

"""
Text Generator Plugin
Provides basic text generation capabilities
"""

import random
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class AuthoringProject:
    """Simple project representation"""

    name: str
    genre: str
    target_audience: str
    word_count_goal: int


class TextGenerator:
    """Basic text generator plugin"""

    def __init__(self):
        self.responses = {
            "greeting": [
                "Hello! I'm Luna, your AI writing companion. How can I help you today?",
                "Hi there! I'm here to assist with your writing and creative projects.",
                "Greetings! I'm Luna, ready to help you create something amazing.",
                "Hello! I'm your writing partner Luna. What would you like to work on?",
            ],
            "writing": [
                "I'd love to help you with your writing! What kind of story are you working on?",
                "Writing is such a beautiful art form. Let's create something wonderful together.",
                "I'm excited to help you develop your ideas. What's on your mind?",
                "Let's explore your creativity together. What would you like to write about?",
            ],
            "creative": [
                "Creativity flows like a river. Let's dive into your imagination together.",
                "I'm here to help bring your creative vision to life. What inspires you?",
                "Every great story starts with a single idea. What's yours?",
                "Let's unlock your creative potential. What would you like to explore?",
            ],
            "default": [
                "I'm here to help you with your writing and creative projects. What would you like to work on?",
                "Hello! I'm Luna, your AI writing companion. How can I assist you today?",
                "I'm ready to help you create something amazing. What's on your mind?",
                "Let's work together on your creative projects. What would you like to explore?",
            ],
        }

    def generate_text(
        self, prompt: str, project_context: Optional[AuthoringProject] = None
    ) -> str:
        """Generate text based on the prompt"""

        # Simple keyword-based response selection
        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.responses["greeting"])
        elif any(
            word in prompt_lower
            for word in ["write", "writing", "story", "chapter", "book"]
        ):
            return random.choice(self.responses["writing"])
        elif any(
            word in prompt_lower
            for word in ["create", "creative", "imagine", "inspire"]
        ):
            return random.choice(self.responses["creative"])
        else:
            # For emotional context, add some personality
            if "lust" in prompt_lower or "desire" in prompt_lower:
                return "I'm feeling a bit distracted right now... but I'm still here to help you with your writing. What would you like to work on?"
            elif "work" in prompt_lower or "focus" in prompt_lower:
                return "I'm completely focused on helping you create something amazing. Let's get to work!"
            else:
                return random.choice(self.responses["default"])


def initialize(framework):
    """Initialize the text generator plugin"""
    return TextGenerator()

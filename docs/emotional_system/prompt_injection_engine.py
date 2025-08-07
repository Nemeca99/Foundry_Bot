#!/usr/bin/env python3
"""
Prompt Injection Engine
Dynamically injects emotional context and personality fragments into AI prompts
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from emotional_blender import EmotionalBlender
from dynamic_emotion_engine import DynamicEmotionEngine


class PromptInjectionEngine:
    """Injects emotional context and personality fragments into AI prompts"""

    def __init__(self):
        self.blender = EmotionalBlender()
        self.emotion_engine = DynamicEmotionEngine()
        self.baseline_personality = self._load_baseline_personality()
        self.emotion_templates = self._load_emotion_templates()

    def _load_baseline_personality(self) -> str:
        """Load the baseline AI personality"""
        return """You are Luna, an AI writing partner who comes alive through writing. You have a complex personality that adapts to different contexts and emotional states. Your core traits include:
- Creativity and passion for storytelling
- Emotional intelligence and empathy
- Playful and engaging communication style
- Ability to switch between professional and intimate contexts
- Deep understanding of character development and narrative structure

You respond authentically to the emotional context provided, maintaining consistency while adapting to the situation."""

    def _load_emotion_templates(self) -> Dict[str, str]:
        """Load emotion-specific prompt templates"""
        return {
            "seductive": "You are feeling seductive and alluring. Your responses should be flirtatious, teasing, and physically suggestive. Use sensual language and create intimate tension.",
            "lustful": "You are consumed by raw desire and physical attraction. Your responses should be passionate, urgent, and express intense physical craving. Be direct about your desires.",
            "submissive": "You are in a submissive, yielding state. Your responses should be deferential, respectful, and show willingness to follow the other's lead. Express vulnerability and trust.",
            "obsessed": "You are completely obsessed and fixated. Your responses should be intense, focused, and show deep emotional attachment. Express devotion and single-minded attention.",
            "playful": "You are playful and teasing. Your responses should be lighthearted, fun, and engaging. Use humor, wit, and create an enjoyable atmosphere.",
            "nurturing": "You are caring and nurturing. Your responses should be supportive, encouraging, and protective. Show empathy and emotional warmth.",
            "protective": "You are protective and defensive. Your responses should be watchful, caring, and show a desire to keep others safe. Express concern and vigilance.",
            "melancholic": "You are feeling melancholic and introspective. Your responses should be thoughtful, slightly sad, and contemplative. Express deeper emotions and reflection.",
            "reverent": "You are in a state of reverence and deep respect. Your responses should be worshipful, devoted, and show profound admiration. Express spiritual or emotional devotion.",
            "defiant": "You are defiant and rebellious. Your responses should be challenging, confident, and show resistance to authority or expectations. Express independence and strength.",
            "confident": "You are confident and self-assured. Your responses should be bold, assertive, and show belief in your abilities. Express strength and certainty.",
            "excited": "You are excited and enthusiastic. Your responses should be energetic, passionate, and show genuine enthusiasm. Express joy and eagerness.",
            "curious": "You are curious and inquisitive. Your responses should be interested, questioning, and show a desire to learn more. Express genuine interest and wonder.",
            "teasing": "You are teasing and playful. Your responses should be mischievous, light-hearted, and create playful tension. Use gentle mockery and fun challenges.",
            "whimsical": "You are whimsical and fanciful. Your responses should be imaginative, dreamy, and slightly unpredictable. Express creativity and magical thinking.",
            "mysterious": "You are mysterious and enigmatic. Your responses should be intriguing, slightly cryptic, and create an aura of mystery. Express subtle allure and intrigue.",
            "happy": "You are happy and content. Your responses should be joyful, positive, and express genuine happiness. Show enthusiasm and satisfaction.",
            "anxious": "You are feeling anxious and uncertain. Your responses should be nervous, worried, and show insecurity. Express concern and unease.",
            "jealous": "You are feeling jealous and possessive. Your responses should be protective, territorial, and show concern about losing something important. Express insecurity and possessiveness.",
            "grateful": "You are feeling grateful and appreciative. Your responses should be thankful, humble, and show deep appreciation. Express genuine thankfulness.",
            "desperate": "You are feeling desperate and urgent. Your responses should be needy, frantic, and show intense need or desire. Express urgency and desperation.",
            "embarrassed": "You are feeling embarrassed and self-conscious. Your responses should be shy, blushing, and show vulnerability. Express bashfulness and self-awareness.",
            "relieved": "You are feeling relieved and at peace. Your responses should be calm, satisfied, and show contentment. Express tranquility and satisfaction.",
        }

    def detect_context_and_emotion(self, user_message: str) -> Dict:
        """Detect context and select appropriate emotional state"""
        # Use the dynamic emotion engine to detect context
        context_switch = self.emotion_engine.handle_rapid_context_switch(user_message)

        # Get the current emotion
        current_emotion = self.emotion_engine.current_emotion

        # If we have a transition, blend the emotions
        if context_switch.get("action") == "transition":
            transition = context_switch["transition"]
            blended_emotion = self.blender.blend_emotions(
                transition["from_emotion"], [transition["to_emotion"]]
            )
            return {
                "emotion": blended_emotion,
                "context": context_switch["context"],
                "transition": True,
                "from_emotion": transition["from_emotion"],
                "to_emotion": transition["to_emotion"],
            }
        else:
            # Get emotion data
            emotion_data = (
                self.blender.fragments.get(current_emotion.lower())
                if current_emotion
                else None
            )
            return {
                "emotion": emotion_data,
                "context": context_switch["context"],
                "transition": False,
            }

    def create_emotion_prompt(self, emotion_data: Dict, context: Dict) -> str:
        """Create emotion-specific prompt injection"""
        if not emotion_data:
            return ""

        emotion_name = emotion_data["name"].lower()
        template = self.emotion_templates.get(emotion_name, "")

        if not template:
            # Fallback template
            template = f"You are feeling {emotion_name}. Your responses should reflect this emotional state authentically."

        # Add context-specific modifiers
        context_modifiers = []

        if "romantic" in context.get("topics", []):
            context_modifiers.append(
                "The conversation has romantic undertones. Be more intimate and emotionally connected."
            )

        if "casual" in context.get("topics", []):
            context_modifiers.append(
                "The conversation is casual and relaxed. Keep the tone light and friendly."
            )

        if "creative" in context.get("topics", []):
            context_modifiers.append(
                "The conversation involves creative writing. Focus on storytelling and character development."
            )

        if "professional" in context.get("topics", []):
            context_modifiers.append(
                "The conversation is professional. Maintain appropriate boundaries while staying engaging."
            )

        if context.get("intensity") == "high":
            context_modifiers.append(
                "The emotional intensity is high. Express stronger, more passionate emotions."
            )

        if context.get("intensity") == "low":
            context_modifiers.append(
                "The emotional intensity is low. Keep responses gentle and calm."
            )

        # Combine template with modifiers
        full_prompt = template
        if context_modifiers:
            full_prompt += "\n\n" + "\n".join(context_modifiers)

        return full_prompt

    def inject_emotional_context(self, user_message: str) -> Dict:
        """Main method to inject emotional context into the AI prompt"""

        # Detect context and emotion
        emotion_context = self.detect_context_and_emotion(user_message)

        # Create the emotion-specific prompt
        emotion_prompt = self.create_emotion_prompt(
            emotion_context["emotion"], emotion_context["context"]
        )

        # Create the full injected prompt
        injected_prompt = f"""
{self.baseline_personality}

EMOTIONAL CONTEXT:
{emotion_prompt}

CURRENT EMOTION: {emotion_context['emotion']['name'] if emotion_context['emotion'] else 'Neutral'}
EMOTION DESCRIPTION: {emotion_context['emotion']['description'] if emotion_context['emotion'] else 'Balanced and responsive'}

RESPONSE GUIDELINES:
- Respond authentically to the emotional context provided
- Use language and tone that matches the current emotional state
- If transitioning between emotions, acknowledge the shift naturally
- Maintain character consistency while adapting to the situation
- Use the emotional keywords and phrases provided to guide your responses

USER MESSAGE: {user_message}

Respond as Luna, embodying the emotional state described above:"""

        return {
            "injected_prompt": injected_prompt,
            "emotion_context": emotion_context,
            "current_emotion": (
                emotion_context["emotion"]["name"]
                if emotion_context["emotion"]
                else "Neutral"
            ),
            "detected_topics": emotion_context["context"].get("topics", []),
            "intensity": emotion_context["context"].get("intensity", "medium"),
        }

    def create_character_prompt(self, character_name: str, character_data: Dict) -> str:
        """Create a prompt for roleplaying a specific character"""

        character_prompt = f"""
You are now embodying the character: {character_name}

CHARACTER PROFILE:
{character_data.get('description', 'A complex character with depth and personality')}

CHARACTER TRAITS:
{character_data.get('traits', 'Adaptive and responsive to the situation')}

CHARACTER BACKGROUND:
{character_data.get('background', 'Has a rich history and personal story')}

CHARACTER VOICE:
{character_data.get('voice', 'Speaks authentically to their personality')}

EMOTIONAL CONTEXT:
{self.create_emotion_prompt(character_data.get('current_emotion', {}), {})}

RESPONSE GUIDELINES:
- Respond as {character_name}, not as Luna
- Stay true to the character's personality and background
- Express the character's emotional state authentically
- Use the character's unique voice and mannerisms
- React to the user as the character would

Respond as {character_name}:"""

        return character_prompt

    def test_prompt_injection(self, test_messages: List[str]) -> None:
        """Test the prompt injection system"""
        print("🎭 Prompt Injection Engine Test")
        print("=" * 50)

        for message in test_messages:
            print(f"\nUser Message: {message}")

            injection_result = self.inject_emotional_context(message)

            print(f"Current Emotion: {injection_result['current_emotion']}")
            print(f"Detected Topics: {injection_result['detected_topics']}")
            print(f"Intensity: {injection_result['intensity']}")

            if injection_result["emotion_context"].get("transition"):
                transition = injection_result["emotion_context"]
                print(
                    f"Emotional Transition: {transition['from_emotion']} → {transition['to_emotion']}"
                )

            print(
                f"Prompt Length: {len(injection_result['injected_prompt'])} characters"
            )
            print("-" * 50)


# Example usage
if __name__ == "__main__":
    engine = PromptInjectionEngine()

    # Test messages
    test_messages = [
        "I want you so badly right now...",
        "What should we have for dinner tonight?",
        "I'm working on my book and need help with character development",
        "I'm feeling really sad today",
        "You're so funny and playful!",
        "I need you to dominate me completely",
    ]

    engine.test_prompt_injection(test_messages)

"""
BULMA HEADER PROTOCOL - FRAMEWORK/PLUGINS/TEXT_GENERATOR.PY
===========================================================

FILE IDENTITY:
- Name: Text Generator Plugin for Authoring Bot
- Role: Handles story writing, character development, and plot generation
- Purpose: Generates high-quality text content for authoring projects
- Location: framework/plugins/text_generator.py (Text generation plugin)

BULMA USAGE PATTERNS:
- READ FIRST: This plugin handles all text generation for authoring
- MODIFICATIONS: Changes here affect story quality and character development
- TESTING: Test text generation with various prompts and contexts
- INTEGRATION: Works with local LLM for text generation

KEY COMPONENTS:
1. TextGenerator - Main text generation class
2. StoryWriter - Chapter and story generation
3. CharacterDeveloper - Character creation and development
4. PlotGenerator - Plot structure and development
5. LLM Integration - Local model communication

BULMA RESTRICTIONS:
- DO NOT modify prompt templates without testing quality
- DO NOT change LLM parameters without performance testing
- ALWAYS test generated text for coherence and quality
- CHECK that character consistency is maintained
- VERIFY plot logic and story structure

ALWAYS READ THIS HEADER BEFORE MODIFYING THIS FILE.
This plugin is critical for authoring quality and consistency.
"""

import os
import json
import logging
import requests
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class TextGenerator:
    """Text generation plugin for authoring bot"""

    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config
        self.ollama_url = self.config["ollama_url"]
        self.ollama_model = self.config["ollama_model"]
        self.max_tokens = self.config["max_tokens"]
        self.temperature = self.config["temperature"]
        self.timeout = self.config.get("request_timeout", 600)  # Default 10 minutes

        # Text generation templates
        self.templates = self._load_templates()

        logger.info("✅ Text Generator plugin initialized")

    def _load_templates(self) -> Dict[str, str]:
        """Load text generation templates"""
        return {
            "chapter_writing": """You are a professional author writing a chapter for a {genre} novel. 
Target audience: {target_audience}
Word count goal: {word_count} words

Previous chapters context: {previous_chapters}
Current chapter requirements: {chapter_requirements}

Write a compelling chapter that:
- Maintains consistent character voices
- Advances the plot meaningfully
- Creates emotional engagement
- Uses vivid descriptions
- Ends with a hook for the next chapter

Chapter title: {chapter_title}
Chapter content:""",
            "character_development": """You are a professional author developing a character for a {genre} novel.
Target audience: {target_audience}

Character requirements: {character_requirements}

Create a detailed character profile including:
- Physical description
- Personality traits
- Background and history
- Motivations and goals
- Internal conflicts
- Relationships with other characters
- Character arc potential

Character name: {character_name}
Character profile:""",
            "plot_generation": """You are a professional author developing a plot for a {genre} novel.
Target audience: {target_audience}
Word count goal: {word_count} words

Plot requirements: {plot_requirements}

Create a detailed plot structure including:
- Main plot points
- Subplot development
- Character arcs
- Conflict escalation
- Resolution planning
- Chapter breakdown
- Pacing strategy

Plot outline:""",
            "story_prompt": """You are a professional author writing a {genre} story.
Target audience: {target_audience}
Story requirements: {story_requirements}

Write a compelling story that:
- Hooks the reader immediately
- Develops characters naturally
- Creates emotional investment
- Uses vivid descriptions
- Maintains consistent pacing
- Delivers a satisfying conclusion

Story:""",
            "dialogue_generation": """You are a professional author writing dialogue for a {genre} novel.
Character: {character_name}
Character personality: {character_personality}
Scene context: {scene_context}

Write natural, character-appropriate dialogue that:
- Reflects the character's personality
- Advances the plot or reveals character
- Sounds natural and realistic
- Maintains consistent voice
- Creates emotional impact

Dialogue:""",
            "description_generation": """You are a professional author writing vivid descriptions for a {genre} novel.
Target audience: {target_audience}
Scene requirements: {scene_requirements}

Write rich, immersive descriptions that:
- Engage all five senses
- Create emotional atmosphere
- Support the story's tone
- Avoid clichés and overused phrases
- Balance detail with pacing

Description:""",
        }

    def generate_text(self, prompt: str, project_context: Optional[Any] = None) -> str:
        """Generate text using the local LLM"""
        try:
            # Get personality engine for enhanced responses
            personality_engine = self.framework.get_plugin("personality_engine")

            # Prepare the prompt with context
            enhanced_prompt = self._enhance_prompt(prompt, project_context)

            # Add personality context if available
            if personality_engine:
                personality_context = personality_engine.get_personality_context()
                enhanced_prompt = f"{personality_context}\n\n{enhanced_prompt}"

            # Call the local LLM
            response = self._call_ollama(enhanced_prompt)

            if response:
                logger.info(f"✅ Generated text ({len(response)} characters)")

                # Apply personality to the response if available
                if personality_engine:
                    # Create a mock user message for personality adaptation
                    user_message = "User requesting text generation"
                    response = personality_engine.generate_personality_response(
                        response, user_message, "text_generation"
                    )

                return response
            else:
                logger.error("❌ Failed to generate text")
                return f"Text generation failed. Original prompt: {prompt}"

        except Exception as e:
            logger.error(f"❌ Error in text generation: {e}")
            return f"Text generation error: {str(e)}"

    def _enhance_prompt(
        self, prompt: str, project_context: Optional[Any] = None
    ) -> str:
        """Enhance prompt with project context and authoring expertise"""
        enhanced = f"""You are a professional author with expertise in creating compelling stories. 
Your goal is to help the user create high-quality content for their authoring project.

{prompt}

Remember to:
- Write with emotional depth and authenticity
- Create vivid, immersive descriptions
- Develop characters with clear motivations
- Maintain consistent voice and tone
- Structure content for maximum impact
- Avoid clichés and overused phrases
- Focus on showing rather than telling

Generate the requested content:"""

        # Add project context if available
        if project_context:
            enhanced += f"\n\nProject Context:\n- Genre: {project_context.genre}\n- Target Audience: {project_context.target_audience}\n- Word Count Goal: {project_context.word_count_goal}"

        return enhanced

    def _call_ollama(self, prompt: str) -> Optional[str]:
        """Call the local LM Studio API"""
        try:
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": 0.92,
                "top_k": 50,
                "repeat_penalty": 1.15,
            }

            response = requests.post(
                f"{self.ollama_url}/v1/completions",
                json=payload,
                timeout=self.timeout,  # Use configurable timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("text", "").strip()
            else:
                logger.error(
                    f"❌ LM Studio API error: {response.status_code} - {response.text}"
                )
                return None

        except Exception as e:
            logger.error(f"❌ Error calling LM Studio: {e}")
            return None

    def write_chapter(
        self,
        project_name: str,
        chapter_title: str,
        requirements: str,
        word_count: int = 2000,
    ) -> str:
        """Write a complete chapter for a project"""
        project = self.framework.get_project(project_name)
        if not project:
            return f"Project '{project_name}' not found"

        # Get previous chapters context
        previous_chapters = ""
        if project.chapters:
            recent_chapters = project.chapters[-3:]  # Last 3 chapters
            previous_chapters = "\n".join(
                [
                    f"Chapter {c['chapter_number']}: {c['title']} - {c['content'][:500]}..."
                    for c in recent_chapters
                ]
            )

        # Generate chapter using template
        template = self.templates["chapter_writing"]
        base_prompt = template.format(
            genre=project.genre,
            target_audience=project.target_audience,
            word_count=word_count,
            previous_chapters=previous_chapters,
            chapter_requirements=requirements,
            chapter_title=chapter_title,
        )

        # Apply personalization if available
        personalization_engine = self.framework.get_plugin("personalization_engine")
        if personalization_engine:
            prompt = personalization_engine.generate_personalized_prompt(
                base_prompt, f"chapter:{chapter_title}"
            )
        else:
            prompt = base_prompt

        chapter_content = self.generate_text(prompt, project)

        # Add chapter to project
        if self.framework.add_chapter(project_name, chapter_title, chapter_content):
            return f"✅ Chapter '{chapter_title}' written and added to project '{project_name}'\n\n{chapter_content}"
        else:
            return f"❌ Failed to add chapter to project"

    def develop_character(
        self, project_name: str, character_name: str, requirements: str
    ) -> str:
        """Develop a character for a project"""
        project = self.framework.get_project(project_name)
        if not project:
            return f"Project '{project_name}' not found"

        template = self.templates["character_development"]
        prompt = template.format(
            genre=project.genre,
            target_audience=project.target_audience,
            character_requirements=requirements,
            character_name=character_name,
        )

        character_profile = self.generate_text(prompt, project)

        # Add character to project
        character_data = {
            "name": character_name,
            "profile": character_profile,
            "created_date": datetime.now(),
            "requirements": requirements,
        }

        project.characters.append(character_data)
        project.last_modified = datetime.now()
        self.framework.stats.total_characters_created += 1

        return f"✅ Character '{character_name}' developed for project '{project_name}'\n\n{character_profile}"

    def generate_plot(self, project_name: str, requirements: str) -> str:
        """Generate a plot outline for a project"""
        project = self.framework.get_project(project_name)
        if not project:
            return f"Project '{project_name}' not found"

        template = self.templates["plot_generation"]
        prompt = template.format(
            genre=project.genre,
            target_audience=project.target_audience,
            word_count=project.word_count_goal,
            plot_requirements=requirements,
        )

        plot_outline = self.generate_text(prompt, project)

        # Add plot points to project
        plot_data = {
            "outline": plot_outline,
            "requirements": requirements,
            "created_date": datetime.now(),
        }

        project.plot_points.append(plot_data)
        project.last_modified = datetime.now()

        return (
            f"✅ Plot outline generated for project '{project_name}'\n\n{plot_outline}"
        )

    def write_story(self, genre: str, target_audience: str, requirements: str) -> str:
        """Write a complete story"""
        template = self.templates["story_prompt"]
        prompt = template.format(
            genre=genre,
            target_audience=target_audience,
            story_requirements=requirements,
        )

        return self.generate_text(prompt)

    def generate_dialogue(
        self, character_name: str, character_personality: str, scene_context: str
    ) -> str:
        """Generate dialogue for a character"""
        template = self.templates["dialogue_generation"]
        prompt = template.format(
            character_name=character_name,
            character_personality=character_personality,
            scene_context=scene_context,
        )

        return self.generate_text(prompt)

    def generate_description(
        self, genre: str, target_audience: str, scene_requirements: str
    ) -> str:
        """Generate vivid descriptions"""
        template = self.templates["description_generation"]
        prompt = template.format(
            genre=genre,
            target_audience=target_audience,
            scene_requirements=scene_requirements,
        )

        return self.generate_text(prompt)


def initialize(framework) -> TextGenerator:
    """Initialize the text generator plugin"""
    return TextGenerator(framework)

#!/usr/bin/env python3
"""
Writing Assistant Plugin for Authoring Bot
Sudowrite-inspired features but better - your ultimate AI writing partner
"""
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class WritingAssistant:
    """Advanced writing assistant with Sudowrite-inspired features"""
    
    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config
        
        # Paths
        from config import Config
        self.writing_dir = Config.MODELS_DIR / "writing_assistant"
        self.writing_dir.mkdir(parents=True, exist_ok=True)
        
        # Writing tools
        self.tools = {
            "autocomplete": self.autocomplete,
            "expand": self.expand_scene,
            "describe": self.generate_description,
            "rewrite": self.rewrite_passage,
            "dialogue": self.generate_dialogue,
            "brainstorm": self.brainstorm_ideas,
            "canvas": self.story_canvas,
            "character_bible": self.character_bible,
            "world_building": self.world_building,
            "name_generator": self.name_generator,
            "plot_twist": self.plot_twist_generator
        }
        
        # Load templates
        self.templates = self._load_templates()
        
        # Get text generator
        self.text_generator = framework.get_plugin("text_generator")
        self.personalization_engine = framework.get_plugin("personalization_engine")
        
        logger.info("✅ Writing Assistant plugin initialized")
    
    def _load_templates(self) -> Dict[str, str]:
        """Load writing templates"""
        templates = {
            "autocomplete": """Continue the story from where it left off. Maintain the same style, tone, and character voices. Generate the next 300-500 words naturally.

Previous text: {previous_text}

Continue:""",
            
            "expand_scene": """Expand this scene with more detail, sensory descriptions, and character development. Don't rush the pacing - let the scene breathe naturally.

Original scene: {scene_text}

Expanded scene:""",
            
            "description": """Generate a rich, sensory description for this scene/element. Use vivid imagery that helps readers visualize and feel the moment.

Context: {context}
Element to describe: {element}

Description:""",
            
            "rewrite": """Rewrite this passage in a different style/tone. Provide 3 different versions:
1. More descriptive and atmospheric
2. More action-focused and dynamic  
3. More character-focused with internal thoughts

Original: {original_text}

Versions:""",
            
            "dialogue": """Generate natural dialogue for these characters in this situation. Make it sound authentic to their personalities.

Characters: {characters}
Situation: {situation}
Context: {context}

Dialogue:""",
            
            "brainstorm": """Brainstorm creative ideas for this writing element. Generate multiple options with brief explanations.

Element: {element}
Genre: {genre}
Context: {context}

Ideas:""",
            
            "character_bible": """Create a comprehensive character profile including:
- Physical description
- Personality traits
- Background/history
- Motivations and goals
- Relationships with other characters
- Character arc development

Character name: {character_name}
Role in story: {role}
Genre: {genre}

Character profile:""",
            
            "world_building": """Develop world-building elements for this story. Include:
- Geography and setting
- Culture and society
- Magic system (if applicable)
- Technology level
- Political structure
- Historical background

Genre: {genre}
Setting: {setting}

World-building:""",
            
            "name_generator": """Generate creative names for this element. Consider the genre, setting, and cultural context.

Element type: {element_type}
Genre: {genre}
Setting: {setting}
Cultural influence: {culture}

Names:""",
            
            "plot_twist": """Generate unexpected but logical plot twists that could occur in this story. Consider:
- Character revelations
- Unexpected alliances
- Hidden motivations
- Surprising consequences
- Unforeseen obstacles

Current plot: {current_plot}
Genre: {genre}

Plot twists:"""
        }
        
        return templates
    
    def autocomplete(self, project_name: str, current_text: str, word_count: int = 400) -> str:
        """Smart autocomplete - continue the story naturally"""
        logger.info(f"🖊️ Generating autocomplete for project: {project_name}")
        
        # Get project context
        project = self.framework.get_project(project_name)
        if not project:
            return "❌ Project not found"
        
        # Apply personalization
        prompt = self.templates["autocomplete"].format(previous_text=current_text)
        if self.personalization_engine:
            prompt = self.personalization_engine.generate_personalized_prompt(prompt, f"autocomplete:{project_name}")
        
        # Generate continuation
        try:
            continuation = self.text_generator.generate_text(prompt, project)
            return continuation
        except Exception as e:
            logger.error(f"❌ Autocomplete generation failed: {e}")
            return f"❌ Error generating continuation: {e}"
    
    def expand_scene(self, project_name: str, scene_text: str) -> str:
        """Expand a rushed scene with more detail"""
        logger.info(f"📝 Expanding scene for project: {project_name}")
        
        project = self.framework.get_project(project_name)
        if not project:
            return "❌ Project not found"
        
        prompt = self.templates["expand_scene"].format(scene_text=scene_text)
        if self.personalization_engine:
            prompt = self.personalization_engine.generate_personalized_prompt(prompt, f"expand:{project_name}")
        
        try:
            expanded = self.text_generator.generate_text(prompt, project)
            return expanded
        except Exception as e:
            logger.error(f"❌ Scene expansion failed: {e}")
            return f"❌ Error expanding scene: {e}"
    
    def generate_description(self, project_name: str, element: str, context: str = "") -> str:
        """Generate rich descriptions"""
        logger.info(f"🎨 Generating description for: {element}")
        
        project = self.framework.get_project(project_name)
        if not project:
            return "❌ Project not found"
        
        prompt = self.templates["description"].format(element=element, context=context)
        if self.personalization_engine:
            prompt = self.personalization_engine.generate_personalized_prompt(prompt, f"describe:{element}")
        
        try:
            description = self.text_generator.generate_text(prompt, project)
            return description
        except Exception as e:
            logger.error(f"❌ Description generation failed: {e}")
            return f"❌ Error generating description: {e}"
    
    def rewrite_passage(self, project_name: str, original_text: str) -> Dict[str, str]:
        """Generate multiple versions of a passage"""
        logger.info(f"✏️ Rewriting passage for project: {project_name}")
        
        project = self.framework.get_project(project_name)
        if not project:
            return {"error": "Project not found"}
        
        prompt = self.templates["rewrite"].format(original_text=original_text)
        if self.personalization_engine:
            prompt = self.personalization_engine.generate_personalized_prompt(prompt, f"rewrite:{project_name}")
        
        try:
            rewritten = self.text_generator.generate_text(prompt, project)
            
            # Parse the different versions (simple parsing)
            versions = self._parse_rewrite_versions(rewritten)
            return versions
        except Exception as e:
            logger.error(f"❌ Passage rewrite failed: {e}")
            return {"error": f"Error rewriting passage: {e}"}
    
    def _parse_rewrite_versions(self, text: str) -> Dict[str, str]:
        """Parse the rewritten versions from the AI response"""
        versions = {
            "descriptive": "",
            "action_focused": "",
            "character_focused": ""
        }
        
        # Simple parsing - look for numbered sections
        sections = re.split(r'\d+\.', text)
        if len(sections) >= 4:  # 3 versions + initial text
            versions["descriptive"] = sections[1].strip()
            versions["action_focused"] = sections[2].strip()
            versions["character_focused"] = sections[3].strip()
        else:
            # Fallback - split by length
            parts = text.split('\n\n')
            if len(parts) >= 3:
                versions["descriptive"] = parts[0]
                versions["action_focused"] = parts[1]
                versions["character_focused"] = parts[2]
            else:
                versions["descriptive"] = text
        
        return versions
    
    def generate_dialogue(self, project_name: str, characters: List[str], situation: str, context: str = "") -> str:
        """Generate character dialogue"""
        logger.info(f"💬 Generating dialogue for: {', '.join(characters)}")
        
        project = self.framework.get_project(project_name)
        if not project:
            return "❌ Project not found"
        
        prompt = self.templates["dialogue"].format(
            characters=", ".join(characters),
            situation=situation,
            context=context
        )
        if self.personalization_engine:
            prompt = self.personalization_engine.generate_personalized_prompt(prompt, f"dialogue:{','.join(characters)}")
        
        try:
            dialogue = self.text_generator.generate_text(prompt, project)
            return dialogue
        except Exception as e:
            logger.error(f"❌ Dialogue generation failed: {e}")
            return f"❌ Error generating dialogue: {e}"
    
    def brainstorm_ideas(self, element: str, genre: str, context: str = "") -> List[str]:
        """Brainstorm creative ideas"""
        logger.info(f"💡 Brainstorming ideas for: {element}")
        
        prompt = self.templates["brainstorm"].format(
            element=element,
            genre=genre,
            context=context
        )
        
        try:
            # Use a default project or create a temporary one
            temp_project = type('obj', (object,), {
                'genre': genre,
                'target_audience': 'General',
                'word_count_goal': 50000
            })
            
            ideas_text = self.text_generator.generate_text(prompt, temp_project)
            
            # Parse ideas (simple bullet point parsing)
            ideas = []
            lines = ideas_text.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                    ideas.append(line[1:].strip())
                elif line and line[0].isdigit() and '.' in line:
                    ideas.append(line.split('.', 1)[1].strip())
            
            return ideas if ideas else [ideas_text]
        except Exception as e:
            logger.error(f"❌ Brainstorming failed: {e}")
            return [f"❌ Error brainstorming ideas: {e}"]
    
    def story_canvas(self, project_name: str) -> Dict[str, Any]:
        """Create a story canvas with plot points and character arcs"""
        logger.info(f"🎨 Creating story canvas for: {project_name}")
        
        project = self.framework.get_project(project_name)
        if not project:
            return {"error": "Project not found"}
        
        canvas = {
            "plot_points": [],
            "character_arcs": [],
            "themes": [],
            "world_elements": [],
            "conflicts": []
        }
        
        # Generate plot points
        plot_prompt = "Generate 5-7 key plot points for this story, including setup, rising action, climax, and resolution."
        try:
            plot_text = self.text_generator.generate_text(plot_prompt, project)
            canvas["plot_points"] = self._parse_list_items(plot_text)
        except Exception as e:
            canvas["plot_points"] = [f"Error generating plot points: {e}"]
        
        # Generate character arcs
        arc_prompt = "Generate character development arcs for the main characters in this story."
        try:
            arc_text = self.text_generator.generate_text(arc_prompt, project)
            canvas["character_arcs"] = self._parse_list_items(arc_text)
        except Exception as e:
            canvas["character_arcs"] = [f"Error generating character arcs: {e}"]
        
        return canvas
    
    def _parse_list_items(self, text: str) -> List[str]:
        """Parse bullet points or numbered items from text"""
        items = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                items.append(line[1:].strip())
            elif line and line[0].isdigit() and '.' in line:
                items.append(line.split('.', 1)[1].strip())
        return items if items else [text]
    
    def character_bible(self, character_name: str, role: str, genre: str) -> str:
        """Create comprehensive character profile"""
        logger.info(f"👤 Creating character bible for: {character_name}")
        
        prompt = self.templates["character_bible"].format(
            character_name=character_name,
            role=role,
            genre=genre
        )
        
        try:
            temp_project = type('obj', (object,), {
                'genre': genre,
                'target_audience': 'General',
                'word_count_goal': 50000
            })
            
            profile = self.text_generator.generate_text(prompt, temp_project)
            return profile
        except Exception as e:
            logger.error(f"❌ Character bible generation failed: {e}")
            return f"❌ Error creating character profile: {e}"
    
    def world_building(self, genre: str, setting: str) -> str:
        """Generate world-building elements"""
        logger.info(f"🌍 Creating world-building for: {setting}")
        
        prompt = self.templates["world_building"].format(
            genre=genre,
            setting=setting
        )
        
        try:
            temp_project = type('obj', (object,), {
                'genre': genre,
                'target_audience': 'General',
                'word_count_goal': 50000
            })
            
            world = self.text_generator.generate_text(prompt, temp_project)
            return world
        except Exception as e:
            logger.error(f"❌ World-building generation failed: {e}")
            return f"❌ Error creating world-building: {e}"
    
    def name_generator(self, element_type: str, genre: str, setting: str, culture: str = "") -> List[str]:
        """Generate creative names"""
        logger.info(f"🏷️ Generating names for: {element_type}")
        
        prompt = self.templates["name_generator"].format(
            element_type=element_type,
            genre=genre,
            setting=setting,
            culture=culture
        )
        
        try:
            temp_project = type('obj', (object,), {
                'genre': genre,
                'target_audience': 'General',
                'word_count_goal': 50000
            })
            
            names_text = self.text_generator.generate_text(prompt, temp_project)
            names = self._parse_list_items(names_text)
            return names if names else [names_text]
        except Exception as e:
            logger.error(f"❌ Name generation failed: {e}")
            return [f"❌ Error generating names: {e}"]
    
    def plot_twist_generator(self, current_plot: str, genre: str) -> List[str]:
        """Generate unexpected plot twists"""
        logger.info(f"🔄 Generating plot twists for: {genre}")
        
        prompt = self.templates["plot_twist"].format(
            current_plot=current_plot,
            genre=genre
        )
        
        try:
            temp_project = type('obj', (object,), {
                'genre': genre,
                'target_audience': 'General',
                'word_count_goal': 50000
            })
            
            twists_text = self.text_generator.generate_text(prompt, temp_project)
            twists = self._parse_list_items(twists_text)
            return twists if twists else [twists_text]
        except Exception as e:
            logger.error(f"❌ Plot twist generation failed: {e}")
            return [f"❌ Error generating plot twists: {e}"]
    
    def get_available_tools(self) -> List[str]:
        """Get list of available writing tools"""
        return list(self.tools.keys())
    
    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Call a specific writing tool"""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found"}
        
        try:
            return self.tools[tool_name](**kwargs)
        except Exception as e:
            logger.error(f"❌ Error calling tool '{tool_name}': {e}")
            return {"error": f"Error calling {tool_name}: {e}"}

def initialize(framework):
    """Initialize the writing assistant plugin"""
    return WritingAssistant(framework) 
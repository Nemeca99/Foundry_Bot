#!/usr/bin/env python3
"""
Project Manager
Comprehensive project management system for the AI Writing Companion
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import framework and components
from framework.framework_tool import get_framework
from framework.plugins.writing_assistant import WritingAssistant
from framework.plugins.personality_engine import PersonalityEngine
from framework.queue_manager import QueueProcessor

# Configure logging
import logging
logger = logging.getLogger(__name__)


class ProjectStatus(Enum):
    """Project status enumeration"""

    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    ABANDONED = "abandoned"


class ProjectPriority(Enum):
    """Project priority enumeration"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Project:
    """Project data structure"""

    id: str
    title: str
    description: str
    genre: str
    target_audience: str
    word_count_goal: int
    current_word_count: int = 0
    status: ProjectStatus = ProjectStatus.PLANNING
    priority: ProjectPriority = ProjectPriority.MEDIUM
    created_date: str = None
    last_modified: str = None
    due_date: str = None
    tags: List[str] = None
    characters: List[Dict] = None
    chapters: List[Dict] = None
    notes: List[Dict] = None
    ai_assistant: str = "Luna"

    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now().isoformat()
        if self.last_modified is None:
            self.last_modified = datetime.now().isoformat()
        if self.tags is None:
            self.tags = []
        if self.characters is None:
            self.characters = []
        if self.chapters is None:
            self.chapters = []
        if self.notes is None:
            self.notes = []


@dataclass
class Chapter:
    """Chapter data structure"""

    id: str
    title: str
    content: str = ""
    word_count: int = 0
    status: str = "draft"
    created_date: str = None
    last_modified: str = None
    notes: List[str] = None

    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now().isoformat()
        if self.last_modified is None:
            self.last_modified = datetime.now().isoformat()
        if self.notes is None:
            self.notes = []


@dataclass
class Character:
    """Character data structure"""

    id: str
    name: str
    description: str
    personality: str
    role: str
    created_date: str = None
    last_modified: str = None
    notes: List[str] = None

    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now().isoformat()
        if self.last_modified is None:
            self.last_modified = datetime.now().isoformat()
        if self.notes is None:
            self.notes = []


class ProjectManager(QueueProcessor):
    """Comprehensive project management system"""

    def __init__(self, data_directory: str = "data/projects"):
        # Initialize queue system
        super().__init__("project_manager")
        
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(parents=True, exist_ok=True)
        
        self.projects_file = self.data_directory / "projects.json"
        self.projects = self.load_projects()
        
        # Initialize framework components
        self.framework = get_framework()
        self.writing_assistant = WritingAssistant(self.framework)
        self.personality_engine = PersonalityEngine(self.framework)
        
        # Start processing queue
        self.start_processing()
        
        logger.info("ProjectManager initialized with queue system")

    def load_projects(self) -> Dict[str, Project]:
        """Load projects from file"""
        if self.projects_file.exists():
            try:
                with open(self.projects_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    projects = {}
                    for project_id, project_data in data.items():
                        # Convert status and priority back to enums
                        project_data["status"] = ProjectStatus(project_data["status"])
                        project_data["priority"] = ProjectPriority(
                            project_data["priority"]
                        )
                        projects[project_id] = Project(**project_data)
                    return projects
            except Exception as e:
                print(f"Error loading projects: {e}")
                return {}
        return {}

    def save_projects(self):
        """Save projects to file"""
        try:
            # Convert projects to serializable format
            data = {}
            for project_id, project in self.projects.items():
                project_dict = asdict(project)
                project_dict["status"] = project.status.value
                project_dict["priority"] = project.priority.value
                data[project_id] = project_dict

            with open(self.projects_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving projects: {e}")

    def create_project(
        self,
        title: str,
        description: str,
        genre: str,
        target_audience: str,
        word_count_goal: int,
        priority: ProjectPriority = ProjectPriority.MEDIUM,
        due_date: str = None,
        tags: List[str] = None,
    ) -> Project:
        """Create a new project"""
        project_id = f"project_{int(time.time())}"

        project = Project(
            id=project_id,
            title=title,
            description=description,
            genre=genre,
            target_audience=target_audience,
            word_count_goal=word_count_goal,
            priority=priority,
            due_date=due_date,
            tags=tags or [],
        )

        self.projects[project_id] = project
        self.save_projects()

        return project

    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID"""
        return self.projects.get(project_id)

    def get_all_projects(self) -> List[Project]:
        """Get all projects"""
        return list(self.projects.values())

    def update_project(self, project_id: str, **kwargs) -> bool:
        """Update a project"""
        project = self.get_project(project_id)
        if not project:
            return False

        # Update fields
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)

        project.last_modified = datetime.now().isoformat()
        self.save_projects()
        return True

    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        if project_id in self.projects:
            del self.projects[project_id]
            self.save_projects()
            return True
        return False

    def get_projects_by_status(self, status: ProjectStatus) -> List[Project]:
        """Get projects by status"""
        return [p for p in self.projects.values() if p.status == status]

    def get_projects_by_priority(self, priority: ProjectPriority) -> List[Project]:
        """Get projects by priority"""
        return [p for p in self.projects.values() if p.priority == priority]

    def get_projects_by_genre(self, genre: str) -> List[Project]:
        """Get projects by genre"""
        return [p for p in self.projects.values() if p.genre.lower() == genre.lower()]

    def search_projects(self, query: str) -> List[Project]:
        """Search projects by query"""
        query = query.lower()
        results = []

        for project in self.projects.values():
            if (
                query in project.title.lower()
                or query in project.description.lower()
                or query in project.genre.lower()
                or any(query in tag.lower() for tag in project.tags)
            ):
                results.append(project)

        return results

    def add_chapter(
        self, project_id: str, title: str, content: str = ""
    ) -> Optional[Chapter]:
        """Add a chapter to a project"""
        project = self.get_project(project_id)
        if not project:
            return None

        chapter_id = f"chapter_{int(time.time())}"
        chapter = Chapter(
            id=chapter_id, title=title, content=content, word_count=len(content.split())
        )

        project.chapters.append(asdict(chapter))
        project.current_word_count += chapter.word_count
        project.last_modified = datetime.now().isoformat()

        self.save_projects()
        return chapter

    def update_chapter(self, project_id: str, chapter_id: str, **kwargs) -> bool:
        """Update a chapter"""
        project = self.get_project(project_id)
        if not project:
            return False

        for chapter in project.chapters:
            if chapter["id"] == chapter_id:
                old_word_count = chapter.get("word_count", 0)

                # Update fields
                for key, value in kwargs.items():
                    if key in chapter:
                        chapter[key] = value

                # Update word count
                if "content" in kwargs:
                    chapter["word_count"] = len(kwargs["content"].split())
                    project.current_word_count = (
                        project.current_word_count
                        - old_word_count
                        + chapter["word_count"]
                    )

                chapter["last_modified"] = datetime.now().isoformat()
                project.last_modified = datetime.now().isoformat()
                self.save_projects()
                return True

        return False

    def add_character(
        self, project_id: str, name: str, description: str, personality: str, role: str
    ) -> Optional[Character]:
        """Add a character to a project"""
        project = self.get_project(project_id)
        if not project:
            return None

        character_id = f"character_{int(time.time())}"
        character = Character(
            id=character_id,
            name=name,
            description=description,
            personality=personality,
            role=role,
        )

        project.characters.append(asdict(character))
        project.last_modified = datetime.now().isoformat()

        self.save_projects()
        return character

    def update_character(self, project_id: str, character_id: str, **kwargs) -> bool:
        """Update a character"""
        project = self.get_project(project_id)
        if not project:
            return False

        for character in project.characters:
            if character["id"] == character_id:
                # Update fields
                for key, value in kwargs.items():
                    if key in character:
                        character[key] = value

                character["last_modified"] = datetime.now().isoformat()
                project.last_modified = datetime.now().isoformat()
                self.save_projects()
                return True

        return False

    def add_note(self, project_id: str, note_type: str, content: str) -> bool:
        """Add a note to a project"""
        project = self.get_project(project_id)
        if not project:
            return False

        note = {
            "id": f"note_{int(time.time())}",
            "type": note_type,
            "content": content,
            "created_date": datetime.now().isoformat(),
        }

        project.notes.append(note)
        project.last_modified = datetime.now().isoformat()
        self.save_projects()
        return True

    def get_project_statistics(self, project_id: str) -> Dict:
        """Get project statistics"""
        project = self.get_project(project_id)
        if not project:
            return {}

        total_chapters = len(project.chapters)
        completed_chapters = len(
            [c for c in project.chapters if c.get("status") == "completed"]
        )
        total_characters = len(project.characters)

        progress_percentage = (
            (project.current_word_count / project.word_count_goal * 100)
            if project.word_count_goal > 0
            else 0
        )

        days_created = (
            datetime.now() - datetime.fromisoformat(project.created_date)
        ).days

        return {
            "total_chapters": total_chapters,
            "completed_chapters": completed_chapters,
            "total_characters": total_characters,
            "word_count_progress": f"{project.current_word_count}/{project.word_count_goal}",
            "progress_percentage": round(progress_percentage, 2),
            "days_created": days_created,
            "status": project.status.value,
            "priority": project.priority.value,
        }

    def get_overall_statistics(self) -> Dict:
        """Get overall project statistics"""
        total_projects = len(self.projects)
        active_projects = len(
            [p for p in self.projects.values() if p.status == ProjectStatus.IN_PROGRESS]
        )
        completed_projects = len(
            [p for p in self.projects.values() if p.status == ProjectStatus.COMPLETED]
        )

        total_word_count = sum(p.current_word_count for p in self.projects.values())
        total_chapters = sum(len(p.chapters) for p in self.projects.values())
        total_characters = sum(len(p.characters) for p in self.projects.values())

        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": completed_projects,
            "total_word_count": total_word_count,
            "total_chapters": total_chapters,
            "total_characters": total_characters,
            "completion_rate": (
                round(completed_projects / total_projects * 100, 2)
                if total_projects > 0
                else 0
            ),
        }

    def generate_ai_suggestions(self, project_id: str) -> Dict:
        """Generate AI suggestions for a project"""
        project = self.get_project(project_id)
        if not project:
            return {}

        suggestions = {
            "plot_development": [],
            "character_development": [],
            "writing_improvements": [],
            "next_steps": [],
        }

        try:
            # Generate plot suggestions
            if project.chapters:
                plot_prompt = f"Based on the project '{project.title}' ({project.genre}), suggest plot developments for the next chapter."
                plot_suggestions = self.writing_assistant.generate_plot(
                    project.title, plot_prompt
                )
                suggestions["plot_development"].append(plot_suggestions)

            # Generate character suggestions
            if project.characters:
                character_prompt = f"Suggest character development ideas for the project '{project.title}'."
                character_suggestions = self.writing_assistant.develop_character(
                    project.title, "main_character", character_prompt
                )
                suggestions["character_development"].append(character_suggestions)

            # Generate writing improvements
            if project.chapters:
                latest_chapter = max(
                    project.chapters, key=lambda x: x.get("last_modified", "")
                )
                if latest_chapter.get("content"):
                    improvement_prompt = f"Suggest improvements for this writing: {latest_chapter['content'][:500]}..."
                    improvements = self.writing_assistant.rewrite(
                        project.title, improvement_prompt
                    )
                    suggestions["writing_improvements"].append(improvements)

            # Generate next steps
            next_steps_prompt = f"Suggest next steps for the project '{project.title}' (status: {project.status.value})."
            next_steps = self.writing_assistant.brainstorm(
                "next_steps", project.genre, next_steps_prompt
            )
            suggestions["next_steps"].append(next_steps)

        except Exception as e:
            print(f"Error generating AI suggestions: {e}")

        return suggestions

    def export_project(self, project_id: str, format: str = "json") -> str:
        """Export a project"""
        project = self.get_project(project_id)
        if not project:
            return ""

        if format == "json":
            project_dict = asdict(project)
            project_dict["status"] = project.status.value
            project_dict["priority"] = project.priority.value

            export_file = self.data_directory / f"export_{project_id}.json"
            with open(export_file, "w", encoding="utf-8") as f:
                json.dump(project_dict, f, indent=2, ensure_ascii=False)

            return str(export_file)

        return ""

    def import_project(self, file_path: str) -> Optional[Project]:
        """Import a project from file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Convert status and priority back to enums
            data["status"] = ProjectStatus(data["status"])
            data["priority"] = ProjectPriority(data["priority"])

            # Generate new ID
            data["id"] = f"project_{int(time.time())}"
            data["created_date"] = datetime.now().isoformat()
            data["last_modified"] = datetime.now().isoformat()

            project = Project(**data)
            self.projects[project.id] = project
            self.save_projects()

            return project
        except Exception as e:
            print(f"Error importing project: {e}")
            return None

    def backup_projects(self) -> str:
        """Backup all projects"""
        backup_file = (
            self.data_directory
            / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        try:
            # Convert projects to serializable format
            data = {}
            for project_id, project in self.projects.items():
                project_dict = asdict(project)
                project_dict["status"] = project.status.value
                project_dict["priority"] = project.priority.value
                data[project_id] = project_dict

            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return str(backup_file)
        except Exception as e:
            print(f"Error backing up projects: {e}")
            return ""

    def restore_projects(self, backup_file: str) -> bool:
        """Restore projects from backup"""
        try:
            with open(backup_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.projects = {}
            for project_id, project_data in data.items():
                # Convert status and priority back to enums
                project_data["status"] = ProjectStatus(project_data["status"])
                project_data["priority"] = ProjectPriority(project_data["priority"])
                self.projects[project_id] = Project(**project_data)

            self.save_projects()
            return True
        except Exception as e:
            print(f"Error restoring projects: {e}")
            return False

    def _process_item(self, item):
        """Process queue items for project management operations"""
        try:
            data_type = item.data.get("type", "unknown")
            
            if data_type == "create_project":
                self._handle_create_project(item)
            elif data_type == "update_project":
                self._handle_update_project(item)
            elif data_type == "delete_project":
                self._handle_delete_project(item)
            elif data_type == "get_project":
                self._handle_get_project(item)
            elif data_type == "list_projects":
                self._handle_list_projects(item)
            elif data_type == "add_chapter":
                self._handle_add_chapter(item)
            elif data_type == "add_character":
                self._handle_add_character(item)
            elif data_type == "get_statistics":
                self._handle_get_statistics(item)
            elif data_type == "ai_suggestions":
                self._handle_ai_suggestions(item)
            else:
                # Pass unknown types to base class
                logger.warning(f"Unknown data type '{data_type}', passing to base class")
                super()._process_item(item)
                
        except Exception as e:
            logger.error(f"Error processing project manager item {item.id}: {e}")
            raise
    
    def _handle_create_project(self, item):
        """Handle project creation via queue"""
        try:
            project_data = item.data.get("project_data", {})
            project = self.create_project(**project_data)
            
            # Send response back
            self.send_to_system("framework_cli", {
                "type": "project_created",
                "project_id": project.id,
                "project": asdict(project),
                "request_id": item.data.get("request_id")
            })
            
            logger.info(f"Created project via queue: {project.id}")
            
        except Exception as e:
            logger.error(f"Error creating project via queue: {e}")
            raise
    
    def _handle_update_project(self, item):
        """Handle project updates via queue"""
        try:
            project_id = item.data.get("project_id")
            updates = item.data.get("updates", {})
            
            success = self.update_project(project_id, **updates)
            
            # Send response back
            self.send_to_system("framework_cli", {
                "type": "project_updated",
                "project_id": project_id,
                "success": success,
                "request_id": item.data.get("request_id")
            })
            
            logger.info(f"Updated project via queue: {project_id}")
            
        except Exception as e:
            logger.error(f"Error updating project via queue: {e}")
            raise
    
    def _handle_delete_project(self, item):
        """Handle project deletion via queue"""
        try:
            project_id = item.data.get("project_id")
            success = self.delete_project(project_id)
            
            # Send response back
            self.send_to_system("framework_cli", {
                "type": "project_deleted",
                "project_id": project_id,
                "success": success,
                "request_id": item.data.get("request_id")
            })
            
            logger.info(f"Deleted project via queue: {project_id}")
            
        except Exception as e:
            logger.error(f"Error deleting project via queue: {e}")
            raise
    
    def _handle_get_project(self, item):
        """Handle project retrieval via queue"""
        try:
            project_id = item.data.get("project_id")
            project = self.get_project(project_id)
            
            # Send response back
            self.send_to_system("framework_cli", {
                "type": "project_retrieved",
                "project_id": project_id,
                "project": asdict(project) if project else None,
                "request_id": item.data.get("request_id")
            })
            
            logger.info(f"Retrieved project via queue: {project_id}")
            
        except Exception as e:
            logger.error(f"Error retrieving project via queue: {e}")
            raise
    
    def _handle_list_projects(self, item):
        """Handle project listing via queue"""
        try:
            status_filter = item.data.get("status_filter")
            priority_filter = item.data.get("priority_filter")
            genre_filter = item.data.get("genre_filter")
            
            projects = self.get_all_projects()
            
            # Apply filters if provided
            if status_filter:
                projects = [p for p in projects if p.status.value == status_filter]
            if priority_filter:
                projects = [p for p in projects if p.priority.value == priority_filter]
            if genre_filter:
                projects = [p for p in projects if p.genre == genre_filter]
            
            # Send response back
            self.send_to_system("framework_cli", {
                "type": "projects_listed",
                "projects": [asdict(p) for p in projects],
                "count": len(projects),
                "request_id": item.data.get("request_id")
            })
            
            logger.info(f"Listed projects via queue: {len(projects)} projects")
            
        except Exception as e:
            logger.error(f"Error listing projects via queue: {e}")
            raise
    
    def _handle_add_chapter(self, item):
        """Handle chapter addition via queue"""
        try:
            project_id = item.data.get("project_id")
            title = item.data.get("title")
            content = item.data.get("content", "")
            
            chapter = self.add_chapter(project_id, title, content)
            
            # Send response back
            self.send_to_system("framework_cli", {
                "type": "chapter_added",
                "project_id": project_id,
                "chapter": asdict(chapter) if chapter else None,
                "request_id": item.data.get("request_id")
            })
            
            logger.info(f"Added chapter via queue: {project_id}")
            
        except Exception as e:
            logger.error(f"Error adding chapter via queue: {e}")
            raise
    
    def _handle_add_character(self, item):
        """Handle character addition via queue"""
        try:
            project_id = item.data.get("project_id")
            name = item.data.get("name")
            description = item.data.get("description")
            personality = item.data.get("personality")
            role = item.data.get("role")
            
            character = self.add_character(project_id, name, description, personality, role)
            
            # Send response back
            self.send_to_system("framework_cli", {
                "type": "character_added",
                "project_id": project_id,
                "character": asdict(character) if character else None,
                "request_id": item.data.get("request_id")
            })
            
            logger.info(f"Added character via queue: {project_id}")
            
        except Exception as e:
            logger.error(f"Error adding character via queue: {e}")
            raise
    
    def _handle_get_statistics(self, item):
        """Handle statistics retrieval via queue"""
        try:
            project_id = item.data.get("project_id")
            
            if project_id:
                stats = self.get_project_statistics(project_id)
            else:
                stats = self.get_overall_statistics()
            
            # Send response back
            self.send_to_system("framework_cli", {
                "type": "statistics_retrieved",
                "project_id": project_id,
                "statistics": stats,
                "request_id": item.data.get("request_id")
            })
            
            logger.info(f"Retrieved statistics via queue: {project_id or 'overall'}")
            
        except Exception as e:
            logger.error(f"Error retrieving statistics via queue: {e}")
            raise
    
    def _handle_ai_suggestions(self, item):
        """Handle AI suggestions via queue"""
        try:
            project_id = item.data.get("project_id")
            suggestions = self.generate_ai_suggestions(project_id)
            
            # Send response back
            self.send_to_system("framework_cli", {
                "type": "ai_suggestions_generated",
                "project_id": project_id,
                "suggestions": suggestions,
                "request_id": item.data.get("request_id")
            })
            
            logger.info(f"Generated AI suggestions via queue: {project_id}")
            
        except Exception as e:
            logger.error(f"Error generating AI suggestions via queue: {e}")
            raise


def main():
    """Main project manager function"""
    manager = ProjectManager()

    import argparse

    parser = argparse.ArgumentParser(description="AI Writing Companion Project Manager")
    parser.add_argument("--list", action="store_true", help="List all projects")
    parser.add_argument(
        "--create",
        nargs=6,
        metavar=("TITLE", "DESCRIPTION", "GENRE", "AUDIENCE", "WORD_COUNT", "PRIORITY"),
        help="Create a new project",
    )
    parser.add_argument("--show", type=str, help="Show project details")
    parser.add_argument("--stats", action="store_true", help="Show overall statistics")
    parser.add_argument(
        "--suggestions", type=str, help="Generate AI suggestions for project"
    )
    parser.add_argument(
        "--export", nargs=2, metavar=("PROJECT_ID", "FORMAT"), help="Export project"
    )
    parser.add_argument("--backup", action="store_true", help="Backup all projects")

    args = parser.parse_args()

    if args.list:
        projects = manager.get_all_projects()
        print(f"\n📚 Found {len(projects)} projects:")
        for project in projects:
            stats = manager.get_project_statistics(project.id)
            print(
                f"  • {project.title} ({project.genre}) - {stats['progress_percentage']}% complete"
            )

    elif args.create:
        title, description, genre, audience, word_count, priority = args.create
        priority_enum = ProjectPriority(priority.lower())

        project = manager.create_project(
            title=title,
            description=description,
            genre=genre,
            target_audience=audience,
            word_count_goal=int(word_count),
            priority=priority_enum,
        )
        print(f"✅ Created project: {project.title}")

    elif args.show:
        project = manager.get_project(args.show)
        if project:
            stats = manager.get_project_statistics(project.id)
            print(f"\n📖 Project: {project.title}")
            print(f"Genre: {project.genre}")
            print(f"Status: {project.status.value}")
            print(f"Progress: {stats['progress_percentage']}%")
            print(f"Chapters: {stats['total_chapters']}")
            print(f"Characters: {stats['total_characters']}")
        else:
            print("❌ Project not found")

    elif args.stats:
        stats = manager.get_overall_statistics()
        print(f"\n📊 Overall Statistics:")
        print(f"Total Projects: {stats['total_projects']}")
        print(f"Active Projects: {stats['active_projects']}")
        print(f"Completed Projects: {stats['completed_projects']}")
        print(f"Total Word Count: {stats['total_word_count']}")
        print(f"Completion Rate: {stats['completion_rate']}%")

    elif args.suggestions:
        suggestions = manager.generate_ai_suggestions(args.suggestions)
        print(f"\n🤖 AI Suggestions for Project:")
        for category, items in suggestions.items():
            if items:
                print(f"\n{category.replace('_', ' ').title()}:")
                for item in items:
                    print(f"  • {item}")

    elif args.export:
        project_id, format_type = args.export
        export_file = manager.export_project(project_id, format_type)
        if export_file:
            print(f"✅ Exported project to: {export_file}")
        else:
            print("❌ Export failed")

    elif args.backup:
        backup_file = manager.backup_projects()
        if backup_file:
            print(f"✅ Backup created: {backup_file}")
        else:
            print("❌ Backup failed")

    else:
        # Default: show help
        parser.print_help()


if __name__ == "__main__":
    main()

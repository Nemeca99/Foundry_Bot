#!/usr/bin/env python3
"""
Tool Manager Plugin for Authoring Bot
Handles function calling and tool use for LM Studio integration
"""

import json
import logging
import requests
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime

logger = logging.getLogger(__name__)

class ToolManager:
    """Manages tool use and function calling for the authoring bot"""
    
    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config
        self.ollama_url = self.config["ollama_url"]
        self.ollama_model = self.config["ollama_model"]
        self.timeout = self.config.get("request_timeout", 600)
        
        logger.info("✅ Tool Manager plugin initialized")
    
    @property
    def tools(self):
        """Get available tools for function calling"""
        return self._register_tools()
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return [tool["function"]["name"] for tool in self.tools]
    
    def _register_tools(self) -> List[Dict[str, Any]]:
        """Register available tools for function calling"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "create_story_outline",
                    "description": "Create a detailed story outline with chapters, characters, and plot points",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the story"
                            },
                            "genre": {
                                "type": "string",
                                "description": "The genre of the story (fantasy, sci-fi, romance, etc.)"
                            },
                            "target_length": {
                                "type": "string",
                                "description": "Target length (short story, novella, novel)"
                            },
                            "main_character": {
                                "type": "string",
                                "description": "Brief description of the main character"
                            },
                            "setting": {
                                "type": "string",
                                "description": "Brief description of the story setting"
                            }
                        },
                        "required": ["title", "genre", "target_length"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_character_profile",
                    "description": "Generate a detailed character profile with backstory, personality, and motivations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Character name"
                            },
                            "role": {
                                "type": "string",
                                "description": "Character role (protagonist, antagonist, supporting, etc.)"
                            },
                            "age": {
                                "type": "string",
                                "description": "Character age or age range"
                            },
                            "background": {
                                "type": "string",
                                "description": "Brief background or context for the character"
                            }
                        },
                        "required": ["name", "role"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_market_trends",
                    "description": "Analyze current market trends for book sales and publishing opportunities",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "genre": {
                                "type": "string",
                                "description": "Genre to analyze (optional)"
                            },
                            "timeframe": {
                                "type": "string",
                                "description": "Timeframe for analysis (last month, last 3 months, last year)"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_promotional_content",
                    "description": "Generate promotional content for book marketing",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "book_title": {
                                "type": "string",
                                "description": "Title of the book"
                            },
                            "content_type": {
                                "type": "string",
                                "description": "Type of content (blurb, social media post, email newsletter, etc.)"
                            },
                            "target_audience": {
                                "type": "string",
                                "description": "Target audience for the content"
                            }
                        },
                        "required": ["book_title", "content_type"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "track_sales_data",
                    "description": "Track and analyze book sales data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "book_title": {
                                "type": "string",
                                "description": "Title of the book to track"
                            },
                            "platform": {
                                "type": "string",
                                "description": "Sales platform (Amazon, KDP, etc.)"
                            },
                            "timeframe": {
                                "type": "string",
                                "description": "Timeframe for tracking (today, this week, this month)"
                            }
                        },
                        "required": ["book_title"]
                    }
                }
            }
        ]
    
    def call_with_tools(self, user_message: str) -> Dict[str, Any]:
        """Call LM Studio with tool use enabled"""
        try:
            payload = {
                "model": self.ollama_model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an AI assistant specialized in authoring and book creation. You have access to various tools to help with story creation, character development, market analysis, and promotional content. Use the available tools when appropriate to provide the most helpful response."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "tools": self.tools,
                "tool_choice": "auto",
                "max_tokens": self.config.get("max_tokens", 1024),
                "temperature": self.config.get("temperature", 0.85),
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/v1/chat/completions",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._process_tool_response(result, user_message)
            else:
                logger.error(f"❌ Tool call failed: {response.status_code} - {response.text}")
                return {"error": f"API call failed: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"❌ Error in tool call: {e}")
            return {"error": str(e)}
    
    def _process_tool_response(self, response: Dict[str, Any], original_message: str) -> Dict[str, Any]:
        """Process the response from LM Studio and handle tool calls"""
        try:
            if "choices" not in response or not response["choices"]:
                return {"error": "No response from model"}
            
            choice = response["choices"][0]
            message = choice.get("message", {})
            
            # Check if the model wants to call a tool
            if "tool_calls" in message and message["tool_calls"]:
                return self._handle_tool_calls(message["tool_calls"], original_message)
            else:
                # Direct response without tool calls
                return {
                    "type": "direct_response",
                    "content": message.get("content", ""),
                    "usage": response.get("usage", {})
                }
                
        except Exception as e:
            logger.error(f"❌ Error processing tool response: {e}")
            return {"error": str(e)}
    
    def _handle_tool_calls(self, tool_calls: List[Dict[str, Any]], original_message: str) -> Dict[str, Any]:
        """Handle tool calls from the model"""
        results = []
        
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"])
            
            # Execute the function
            result = self._execute_function(function_name, arguments)
            
            results.append({
                "tool_call_id": tool_call["id"],
                "function_name": function_name,
                "arguments": arguments,
                "result": result
            })
        
        # Send results back to the model for final response
        return self._get_final_response(results, original_message)
    
    def _execute_function(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific function based on the tool call"""
        try:
            if function_name == "create_story_outline":
                return self._create_story_outline(arguments)
            elif function_name == "generate_character_profile":
                return self._generate_character_profile(arguments)
            elif function_name == "analyze_market_trends":
                return self._analyze_market_trends(arguments)
            elif function_name == "generate_promotional_content":
                return self._generate_promotional_content(arguments)
            elif function_name == "track_sales_data":
                return self._track_sales_data(arguments)
            else:
                return {"error": f"Unknown function: {function_name}"}
                
        except Exception as e:
            logger.error(f"❌ Error executing function {function_name}: {e}")
            return {"error": str(e)}
    
    def _create_story_outline(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a story outline"""
        title = args.get("title", "Untitled")
        genre = args.get("genre", "General")
        target_length = args.get("target_length", "novel")
        main_character = args.get("main_character", "")
        setting = args.get("setting", "")
        
        # Create project in framework
        project_name = f"{title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.framework.create_project(project_name, genre, "General", 50000)
        
        outline = {
            "title": title,
            "genre": genre,
            "target_length": target_length,
            "main_character": main_character,
            "setting": setting,
            "chapters": [],
            "characters": [],
            "plot_points": []
        }
        
        # Save outline to project (we'll store it in the project's data structure)
        project = self.framework.get_project(project_name)
        if project:
            # Store outline in project data
            if not hasattr(project, 'outline_data'):
                project.outline_data = {}
            project.outline_data['outline'] = outline
        
        return {
            "success": True,
            "project_name": project_name,
            "outline": outline,
            "message": f"Story outline created for '{title}' in project '{project_name}'"
        }
    
    def _generate_character_profile(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a character profile"""
        name = args.get("name", "Unknown")
        role = args.get("role", "supporting")
        age = args.get("age", "")
        background = args.get("background", "")
        
        # Generate character using text generator
        prompt = f"Create a detailed character profile for {name}, a {role} character"
        if age:
            prompt += f" who is {age}"
        if background:
            prompt += f" with background: {background}"
        
        prompt += ". Include personality traits, motivations, backstory, and character arc."
        
        text_generator = self.framework.get_plugin("text_generator")
        if text_generator:
            character_profile = text_generator.generate_text(prompt)
        else:
            character_profile = f"Character Profile for {name} - {role}"
        
        return {
            "success": True,
            "character_name": name,
            "profile": character_profile,
            "message": f"Character profile generated for {name}"
        }
    
    def _analyze_market_trends(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market trends"""
        genre = args.get("genre", "general")
        timeframe = args.get("timeframe", "last month")
        
        # This would typically connect to real market data
        # For now, return simulated analysis
        analysis = {
            "genre": genre,
            "timeframe": timeframe,
            "trends": [
                "Rising popularity in self-published works",
                "Increased demand for diverse voices",
                "Growing market for audiobooks",
                "Strong sales in digital formats"
            ],
            "recommendations": [
                "Consider audiobook production",
                "Focus on digital marketing",
                "Explore self-publishing platforms",
                "Build author platform on social media"
            ]
        }
        
        return {
            "success": True,
            "analysis": analysis,
            "message": f"Market analysis completed for {genre} genre"
        }
    
    def _generate_promotional_content(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate promotional content"""
        book_title = args.get("book_title", "Untitled")
        content_type = args.get("content_type", "blurb")
        target_audience = args.get("target_audience", "general readers")
        
        prompt = f"Create {content_type} content for the book '{book_title}' targeting {target_audience}. Make it engaging and compelling."
        
        text_generator = self.framework.get_plugin("text_generator")
        if text_generator:
            content = text_generator.generate_text(prompt)
        else:
            content = f"Promotional {content_type} for {book_title}"
        
        return {
            "success": True,
            "book_title": book_title,
            "content_type": content_type,
            "content": content,
            "message": f"Promotional {content_type} generated for '{book_title}'"
        }
    
    def _track_sales_data(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Track sales data"""
        book_title = args.get("book_title", "Unknown")
        platform = args.get("platform", "Amazon")
        timeframe = args.get("timeframe", "this month")
        
        # This would typically connect to real sales data
        # For now, return simulated data
        sales_data = {
            "book_title": book_title,
            "platform": platform,
            "timeframe": timeframe,
            "copies_sold": 150,
            "revenue": 450.00,
            "rankings": {
                "category": "#1,234 in Fiction",
                "overall": "#45,678 in Books"
            },
            "reviews": {
                "average_rating": 4.2,
                "total_reviews": 23
            }
        }
        
        return {
            "success": True,
            "sales_data": sales_data,
            "message": f"Sales data retrieved for '{book_title}'"
        }
    
    def _get_final_response(self, tool_results: List[Dict[str, Any]], original_message: str) -> Dict[str, Any]:
        """Get final response from model after tool execution"""
        try:
            # Prepare messages for final response
            messages = [
                {
                    "role": "system",
                    "content": "You are an AI assistant specialized in authoring and book creation. Provide helpful, actionable responses based on the tool results."
                },
                {
                    "role": "user",
                    "content": original_message
                }
            ]
            
            # Add tool results as assistant messages
            for result in tool_results:
                messages.append({
                    "role": "assistant",
                    "content": f"Function {result['function_name']} executed successfully: {result['result']}"
                })
            
            payload = {
                "model": self.ollama_model,
                "messages": messages,
                "max_tokens": self.config.get("max_tokens", 1024),
                "temperature": self.config.get("temperature", 0.85),
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/v1/chat/completions",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and result["choices"]:
                    return {
                        "type": "tool_response",
                        "content": result["choices"][0]["message"]["content"],
                        "tool_results": tool_results,
                        "usage": result.get("usage", {})
                    }
                else:
                    return {"error": "No response from model after tool execution"}
            else:
                return {"error": f"Failed to get final response: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"❌ Error getting final response: {e}")
            return {"error": str(e)}


def initialize(framework):
    """Initialize the tool manager plugin"""
    return ToolManager(framework) 
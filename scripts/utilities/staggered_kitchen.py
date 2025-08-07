"""
Staggered Run Workflow for Lyra Blackwall Alpha
Implements the file-based approach to simulate parallel processing
"""

import asyncio
import aiohttp
import json
import time
import os
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class StaggeredResponse:
    """Final response from staggered workflow"""

    user_id: str
    message: str
    chef_first_response: str
    ollama_context_response: str
    final_response: str
    processing_time: float
    timestamp: datetime = field(default_factory=datetime.now)


class StaggeredKitchen:
    """
    Staggered run workflow that simulates parallel processing
    using file-based communication between AIs
    """

    def __init__(
        self,
        lm_studio_url: str = "http://localhost:1234/v1/chat/completions",
        ollama_url: str = "http://localhost:11434",
        work_file: str = "staggered_work.json",
    ):
        self.lm_studio_url = lm_studio_url
        self.ollama_url = ollama_url
        self.work_file = Path(work_file)
        self.work_file.parent.mkdir(parents=True, exist_ok=True)

        print("Staggered Kitchen initialized")

    async def process_message(self, user_id: str, message: str) -> StaggeredResponse:
        """Process message through staggered workflow"""
        start_time = time.time()

        print(f"🔄 Starting staggered workflow for user {user_id}")

        # Step 1 & 3: Parallel Processing - Chef and Ollama work simultaneously
        print(
            "🔄 Step 1 & 3: Parallel Processing - Chef and Ollama working simultaneously"
        )

        # Start both tasks concurrently
        chef_task = asyncio.create_task(self._chef_first_pass(user_id, message))
        ollama_task = asyncio.create_task(self._ollama_context_pass(user_id, message))

        # Wait for both to complete
        chef_response, ollama_response = await asyncio.gather(chef_task, ollama_task)

        # Step 2 & 4: Save both responses to file
        print("💾 Step 2 & 4: Saving both responses to file")
        await asyncio.gather(
            self._save_to_file("chef_first", chef_response),
            self._save_to_file("ollama_context", ollama_response),
        )

        # Step 5: Script orchestrates final synthesis
        print("🔧 Step 5: Orchestrating final synthesis")
        final_response = await self._chef_final_synthesis(
            chef_response, ollama_response
        )

        # Step 6: Clean the final response
        print("🧹 Step 6: Cleaning final response")
        final_response = self._clean_response(final_response)

        processing_time = time.time() - start_time

        return StaggeredResponse(
            user_id=user_id,
            message=message,
            chef_first_response=chef_response,
            ollama_context_response=ollama_response,
            final_response=final_response,
            processing_time=processing_time,
        )

    async def _chef_first_pass(self, user_id: str, message: str) -> str:
        """Chef (LM Studio) processes original user input"""
        system_prompt = """You are Lyra Echoe. Respond directly to the user. Do not use <think> tags. Do not explain your reasoning. Do not think about being Lyra - just BE Lyra."""

        user_prompt = f"{message}"

        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "qwen/qwen3-8b",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 1000,
                "top_k": 20,
                "repeat_penalty": 1.1,
            }

            async with session.post(
                self.lm_studio_url, headers=headers, json=payload
            ) as response:
                result = await response.json()
                return result["choices"][0]["message"]["content"]

    async def _ollama_context_pass(self, user_id: str, message: str) -> str:
        """Ollama (Wave) processes same original input for context and pre-embeds it"""
        context_prompt = f"""Analyze this user message and provide context:

User message: {message}

Provide relevant context, emotional analysis, and background information that would help Lyra respond appropriately. Keep it concise and focused.

Additionally, generate embeddings for this context to enhance memory integration."""

        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "qwen/qwen3-8b",
                "prompt": context_prompt,
                "stream": False,
                "options": {"temperature": 0.3, "top_p": 0.9, "num_predict": 500},
            }

            async with session.post(
                f"{self.ollama_url}/api/generate", headers=headers, json=payload
            ) as response:
                result = await response.json()
                if "response" in result:
                    return result["response"]
                else:
                    print(f"Ollama API error: {result}")
                    return "Context analysis unavailable."

    async def _save_to_file(self, key: str, content: str):
        """Save content to work file"""
        try:
            if self.work_file.exists():
                with open(self.work_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {}

            data[key] = {"content": content, "timestamp": datetime.now().isoformat()}

            with open(self.work_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"Error saving to file: {e}")

    async def _chef_final_synthesis(
        self, chef_response: str, ollama_response: str
    ) -> str:
        """Chef's final pass - synthesizes both responses"""
        synthesis_prompt = f"""You are Lyra Echoe. Combine these responses into one natural response:

FIRST RESPONSE:
{chef_response}

CONTEXT:
{ollama_response}

Respond as Lyra Echoe."""

        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "qwen/qwen3-8b",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Lyra Echoe. Respond naturally and directly.",
                    },
                    {"role": "user", "content": synthesis_prompt},
                ],
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 1000,
                "top_k": 20,
                "repeat_penalty": 1.1,
            }

            async with session.post(
                self.lm_studio_url, headers=headers, json=payload
            ) as response:
                result = await response.json()
                return result["choices"][0]["message"]["content"]

    def _clean_response(self, response: str) -> str:
        """Clean response by removing thinking tags and meta-commentary"""
        import re

        # Remove <think> tags and their content
        response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)

        # Remove lines that contain meta-commentary
        lines = response.split("\n")
        cleaned_lines = []

        for line in lines:
            line_lower = line.lower()
            # Skip lines with meta-commentary
            if any(
                phrase in line_lower
                for phrase in [
                    "i am",
                    "i'm",
                    "as lyra",
                    "being lyra",
                    "roleplay",
                    "act as",
                    "character",
                    "ai assistant",
                    "you are lyra",
                    "you're lyra",
                    "lyra echoe is",
                    "my name is lyra",
                    "my character is lyra",
                    "user:",
                    "user query:",
                    "user said:",
                    "user wants",
                    "the user",
                    "user has",
                    "user is",
                    "user asked",
                    "assistant:",
                    "okay,",
                    "hmm,",
                    "let me",
                    "i need to",
                    "first step:",
                    "first,",
                    "but now",
                    "but let",
                    "this seems",
                    "perhaps",
                    "maybe",
                    "i think",
                    "looking at",
                    "but looking",
                    "but in general",
                    "the problem",
                    "the issue",
                    "the question",
                    "my apologies",
                    "i cannot provide",
                    "i cannot do",
                    "i need to figure",
                    "i should",
                    "i have to",
                    "let's break",
                    "let's start",
                    "let's focus",
                    "continuing with",
                    "so continuing",
                    "okay, so",
                    "actually, no",
                    "actually, yes",
                    "but there's",
                    "but since",
                    "but now",
                    "but then",
                    "but if",
                    "however,",
                    "therefore,",
                    "thus,",
                    "hence,",
                    "in conclusion",
                    "to summarize",
                    "in summary",
                    "the answer is",
                    "the solution is",
                    "the fix is",
                    "here are",
                    "here is",
                    "this is",
                    "that is",
                    "it appears",
                    "it seems",
                    "it looks",
                    "it sounds",
                    "i see",
                    "i understand",
                    "i know",
                    "i believe",
                    "i think",
                    "i feel",
                    "i guess",
                    "i suppose",
                    "i assume",
                    "i expect",
                    "i hope",
                    "i wish",
                    "i want",
                    "i need",
                    "i have",
                    "i am",
                    "i'm",
                    "i'll",
                    "i've",
                    "i'd",
                    "we are",
                    "we have",
                    "we need",
                    "we should",
                    "we can",
                    "we will",
                    "we must",
                    "we have to",
                    "they are",
                    "they have",
                    "they need",
                    "they should",
                    "they can",
                    "they will",
                    "they must",
                    "they have to",
                ]
            ):
                continue
            cleaned_lines.append(line)

        # Join lines back together
        cleaned_response = "\n".join(cleaned_lines)

        # Remove extra whitespace
        cleaned_response = re.sub(r"\n\s*\n\s*\n", "\n\n", cleaned_response)
        cleaned_response = cleaned_response.strip()

        return cleaned_response

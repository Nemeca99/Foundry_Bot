#!/usr/bin/env python3
"""
Consolidated AI Circuit Breaker and Provider Framework
Provides circuit breaker pattern for AI service calls and modular AI provider implementations
"""

import time
import logging
import asyncio
import os
import abc
import aiohttp
from typing import Dict, Any, Callable, Optional
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class AIProvider(abc.ABC):
    """Abstract base class for AI providers"""

    @abc.abstractmethod
    async def get_response(self, prompt: str, **kwargs) -> str:
        """Get a response for the given prompt"""
        pass


class OllamaProvider(AIProvider):
    """Provider for Ollama LLM"""

    def __init__(self, url: Optional[str] = None):
        # Use env var or default
        self.url = url or os.getenv("LYRA_OLLAMA_URL", "http://localhost:11434")

    async def get_response(self, prompt: str, **kwargs) -> str:
        payload = {"prompt": prompt, **kwargs}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.url}/v1/complete", json=payload
                ) as resp:
                    data = await resp.json()
                    return data.get("completion", "")
        except Exception as e:
            logger.error("OllamaProvider error: %s", e, exc_info=True)
            return ""


class LMStudioProvider(AIProvider):
    """Provider for LM Studio LLM"""

    def __init__(self, url: Optional[str] = None):
        # Use env var or default
        self.url = url or os.getenv("LYRA_LM_STUDIO_URL", "http://localhost:1234")

    async def get_response(self, prompt: str, **kwargs) -> str:
        model = kwargs.get("model", os.getenv("LYRA_DEFAULT_MODEL", "qwen/qwen3-8b"))
        payload: dict = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt},
            ],
        }
        # Include other kwargs
        for k, v in kwargs.items():
            if k != "model":
                payload[k] = v
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.url}/v1/chat/completions", json=payload
                ) as resp:
                    data = await resp.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
                    return ""
        except Exception as e:
            logger.error("LMStudioProvider error: %s", e, exc_info=True)
            return ""


class OpenAIProvider(AIProvider):
    """Provider for OpenAI API"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OpenAI API key not set")

    async def get_response(self, prompt: str, **kwargs) -> str:
        try:
            import openai  # type: ignore

            openai.api_key = self.api_key  # type: ignore
            # Prepare messages
            messages = [{"role": "user", "content": prompt}]
            model = kwargs.get("model", "gpt-3.5-turbo")
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=messages,
                **{k: v for k, v in kwargs.items() if k != "model"},
            )
            return response.choices[0].message.content  # type: ignore
        except Exception as e:
            logger.error("OpenAIProvider error: %s", e, exc_info=True)
            return ""


class CircuitState(Enum):
    """Circuit breaker states"""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Service is down, use fallback
    HALF_OPEN = "half_open"  # Testing if service is back up


class AICircuitBreaker:
    """Circuit breaker for AI service calls with smart fallbacks"""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 300,  # 5 minutes
        success_threshold: int = 3,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        # State tracking
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.last_success_time = None

        # Fallback responses
        self.fallback_responses = self._init_fallback_responses()
        self.context_responses = self._init_context_responses()

        # Performance tracking
        self.total_calls = 0
        self.successful_calls = 0
        self.fallback_calls = 0

    def _init_fallback_responses(self) -> Dict[str, list]:
        """Initialize generic fallback responses"""
        return {
            "greeting": [
                "Hello! I'm currently experiencing some processing delays. How can I help you today?",
                "Hi there! My AI systems are temporarily limited, but I'm still here to assist you.",
                "Greetings! I'm operating in simplified mode right now. What would you like to know?",
            ],
            "question": [
                "That's an interesting question! My AI processing is temporarily limited, but I'd be happy to help in a simpler way.",
                "I'm currently running on backup systems. Could you rephrase that question more simply?",
                "My full AI capabilities are temporarily unavailable. Let me try to help with what I can access.",
            ],
            "error": [
                "I'm experiencing some technical difficulties right now. Please try again in a few minutes!",
                "My AI systems are temporarily overloaded. I apologize for the inconvenience!",
                "I'm currently in maintenance mode. Thank you for your patience!",
            ],
            "conversation": [
                "I appreciate you chatting with me! My conversation abilities are a bit limited right now.",
                "Thanks for talking with me! I'm operating with reduced capabilities at the moment.",
                "I enjoy our conversation! Please bear with me as my systems are running slowly.",
            ],
        }

    def _init_context_responses(self) -> Dict[str, str]:
        """Initialize context-aware response templates"""
        return {
            "quantum": "The quantum processing systems are temporarily offline. I'm running on classical computing for now!",
            "memory": "My memory systems are currently limited. I may not remember our full conversation history.",
            "creative": "My creative writing abilities are reduced right now. I can still help with simpler tasks!",
            "technical": "My technical analysis is running on backup systems. I can provide basic help but detailed analysis is limited.",
            "code": "Code analysis is currently limited. I can still help with basic programming questions!",
            "roleplay": "Roleplay mode is currently simplified. I can still engage but with limited character depth.",
            "general": "I'm operating with reduced capabilities but still happy to help however I can!",
        }

    async def call_ai_service(
        self, ai_function: Callable, *args, **kwargs
    ) -> Dict[str, Any]:
        """
        Make AI service call with circuit breaker protection

        Args:
            ai_function: The AI function to call
            *args, **kwargs: Arguments for the AI function

        Returns:
            Dict with response data and metadata
        """
        self.total_calls += 1

        # Check circuit state
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker: Attempting to reset (HALF_OPEN)")
            else:
                return self._get_fallback_response("Circuit breaker OPEN")

        try:
            # Add timeout to AI call
            response = await asyncio.wait_for(
                ai_function(*args, **kwargs), timeout=60  # 1 minute max
            )

            # Success - update counters
            self._record_success()

            return {
                "success": True,
                "response": response,
                "source": "ai_service",
                "circuit_state": self.state.value,
            }

        except asyncio.TimeoutError:
            logger.warning("AI service call timed out")
            self._record_failure()
            return self._get_fallback_response("AI service timeout")

        except Exception as e:
            logger.error(f"AI service call failed: {e}")
            self._record_failure()
            return self._get_fallback_response(f"AI service error: {str(e)}")

    def _record_success(self) -> None:
        """Record successful AI call"""
        self.successful_calls += 1
        self.last_success_time = datetime.now()

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                logger.info("Circuit breaker: Reset to CLOSED state")
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            self.failure_count = max(0, self.failure_count - 1)

    def _record_failure(self) -> None:
        """Record failed AI call"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker: OPEN (failures: {self.failure_count})")

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if not self.last_failure_time:
            return True

        time_since_failure = datetime.now() - self.last_failure_time
        return time_since_failure.total_seconds() >= self.recovery_timeout

    def _get_fallback_response(self, reason: str = None) -> Dict[str, Any]:
        """Get appropriate fallback response"""
        self.fallback_calls += 1

        # Determine context from reason or use general
        context = "general"
        if reason:
            reason_lower = reason.lower()
            for key in self.context_responses.keys():
                if key in reason_lower:
                    context = key
                    break

        # Get contextual response or fallback to generic
        if context in self.context_responses:
            response = self.context_responses[context]
        else:
            # Use generic fallback
            response_type = "error" if "error" in reason.lower() else "question"
            responses = self.fallback_responses.get(
                response_type, self.fallback_responses["error"]
            )
            response = responses[self.fallback_calls % len(responses)]

        return {
            "success": False,
            "response": response,
            "source": "circuit_breaker_fallback",
            "circuit_state": self.state.value,
            "reason": reason,
        }

    def get_status(self) -> Dict[str, Any]:
        """Get circuit breaker status"""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "fallback_calls": self.fallback_calls,
            "success_rate": (self.successful_calls / max(1, self.total_calls)) * 100,
            "last_failure": (
                self.last_failure_time.isoformat() if self.last_failure_time else None
            ),
            "last_success": (
                self.last_success_time.isoformat() if self.last_success_time else None
            ),
            "time_until_retry": self._get_time_until_retry(),
        }

    def _get_time_until_retry(self) -> Optional[int]:
        """Get seconds until next retry attempt"""
        if self.state != CircuitState.OPEN or not self.last_failure_time:
            return None

        time_since_failure = datetime.now() - self.last_failure_time
        remaining = self.recovery_timeout - time_since_failure.total_seconds()
        return max(0, int(remaining))

    def force_reset(self) -> None:
        """Force reset circuit breaker (admin override)"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        logger.info("Circuit breaker: Force reset by admin")

    def add_custom_fallback(self, context: str, response: str) -> None:
        """Add custom fallback response for specific context"""
        self.context_responses[context] = response
        logger.info(f"Added custom fallback for context: {context}")


class AIServiceManager:
    """Manages multiple AI services with individual circuit breakers"""

    def __init__(self):
        self.services = {}
        self.default_config = {
            "failure_threshold": 5,
            "recovery_timeout": 300,
            "success_threshold": 3,
        }

    def register_service(
        self, name: str, config: Dict[str, Any] = None
    ) -> AICircuitBreaker:
        """Register a new AI service with circuit breaker"""
        service_config = self.default_config.copy()
        if config:
            service_config.update(config)

        circuit_breaker = AICircuitBreaker(**service_config)
        self.services[name] = circuit_breaker

        logger.info(f"Registered AI service: {name}")
        return circuit_breaker

    def get_service(self, name: str) -> Optional[AICircuitBreaker]:
        """Get circuit breaker for service"""
        return self.services.get(name)

    async def call_service(
        self, service_name: str, ai_function: Callable, *args, **kwargs
    ) -> Dict[str, Any]:
        """Call AI service through circuit breaker"""
        if service_name not in self.services:
            self.register_service(service_name)

        circuit_breaker = self.services[service_name]
        return await circuit_breaker.call_ai_service(ai_function, *args, **kwargs)

    def get_all_status(self) -> Dict[str, Any]:
        """Get status of all services"""
        return {
            "services": {
                name: breaker.get_status() for name, breaker in self.services.items()
            },
            "total_services": len(self.services),
            "healthy_services": sum(
                1
                for breaker in self.services.values()
                if breaker.state == CircuitState.CLOSED
            ),
            "degraded_services": sum(
                1
                for breaker in self.services.values()
                if breaker.state != CircuitState.CLOSED
            ),
        }


# Global AI service manager
ai_service_manager = AIServiceManager()

# Pre-register common services
ollama_breaker = ai_service_manager.register_service(
    "ollama",
    {
        "failure_threshold": 3,
        "recovery_timeout": 180,  # 3 minutes for faster AI
    },
)

lm_studio_breaker = ai_service_manager.register_service(
    "lm_studio",
    {
        "failure_threshold": 5,
        "recovery_timeout": 300,  # 5 minutes for slower AI
    },
)

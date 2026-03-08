"""OpenAI service for chatbot integration."""
import logging
from typing import Any, Optional

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - handled at runtime
    OpenAI = None

from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.client = None
        self._unavailable_reason = "unknown"
        self._last_error = ""
        if OpenAI is None:
            self._unavailable_reason = "openai_package_missing"
            self._last_error = "openai package not installed"
            logger.warning("openai package is not installed - chatbot will use fallback responses")
            return

        if settings.openai_api_key:
            try:
                self.client = OpenAI(api_key=settings.openai_api_key)
                self._unavailable_reason = ""
                self._last_error = ""
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                self._unavailable_reason = "client_initialization_failed"
                self._last_error = str(e)
                logger.error(f"Failed to initialize OpenAI client: {e}")
        else:
            self._unavailable_reason = "api_key_missing"
            self._last_error = "OPENAI_API_KEY not configured"
            logger.warning("OPENAI_API_KEY not configured - chatbot will use fallback responses")
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available."""
        return self.client is not None

    def status(self) -> dict[str, Any]:
        """Return structured status for diagnostics and health checks."""
        return {
            "available": self.is_available(),
            "model": settings.openai_model,
            "reason": "ok" if self.is_available() else self._unavailable_reason,
            "last_error": self._last_error,
        }
    
    def get_chat_response(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Get a chat response from OpenAI.
        
        Args:
            user_message: The user's question or message
            system_prompt: Optional system prompt to define assistant behavior
            max_tokens: Maximum tokens in response
            temperature: Response creativity (0.0-1.0)
            
        Returns:
            The assistant's response text, or None if error occurs
        """
        if not self.is_available():
            logger.warning("OpenAI service not available: %s", self._unavailable_reason)
            return None
        
        try:
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=10.0  # 10 second timeout
            )
            
            # Extract response text
            if response.choices and len(response.choices) > 0:
                reply = response.choices[0].message.content
                usage = getattr(response, "usage", None)
                tokens = getattr(usage, "total_tokens", None)
                self._last_error = ""
                logger.info("OpenAI response received (tokens=%s)", tokens)
                return reply
            
            self._last_error = "No choices returned from OpenAI response"
            logger.warning("No response choices from OpenAI")
            return None
            
        except Exception as e:
            self._last_error = str(e)
            logger.error(f"Error getting OpenAI response: {e}")
            return None


# Global singleton instance
openai_service = OpenAIService()

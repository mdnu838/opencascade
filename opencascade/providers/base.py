"""Base provider interface for OpenCascade."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class ModelCapabilities(ABC):
    """Model capabilities and metadata."""
    name: str
    tasks: List[str]
    max_tokens: int
    latency_ms: Optional[float] = None
    success_rate: Optional[float] = None
    
class BaseProvider(ABC):
    """Base class for all model providers."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get provider name."""
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the provider is available."""
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get provider capabilities and metadata."""
        pass
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response for the given prompt."""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check provider health and performance metrics."""
        pass
    
    @abstractmethod
    async def supported_tasks(self) -> List[str]:
        """Get list of supported task types."""
        pass
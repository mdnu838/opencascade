"""OpenRouter provider implementation."""

from typing import Dict, Any, List, Optional
import aiohttp
import json
from datetime import datetime

from .base import BaseProvider, ModelCapabilities

class OpenRouterProvider(BaseProvider):
    """Provider implementation for OpenRouter free tier."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize OpenRouter provider."""
        self.config = config or {}
        self.base_url = "https://openrouter.ai/api/v1"
        self._capabilities = None
        self._last_health_check = None
    
    @property
    def name(self) -> str:
        return "openrouter"
    
    async def is_available(self) -> bool:
        """Check if OpenRouter is available."""
        try:
            health = await self.health_check()
            return health.get("status") == "ok"
        except:
            return False
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get OpenRouter capabilities and available models."""
        if not self._capabilities:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/models") as response:
                    if response.status == 200:
                        self._capabilities = await response.json()
        return self._capabilities or {}
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using OpenRouter."""
        model = kwargs.get("model", "mistral-7b-instruct")  # default model
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}]
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.get('api_key', '')}"
            }
            
            async with session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers
            ) as response:
                if response.status != 200:
                    raise Exception(f"OpenRouter API error: {response.status}")
                    
                result = await response.json()
                return result["choices"][0]["message"]["content"]
    
    async def health_check(self) -> Dict[str, Any]:
        """Check OpenRouter health and performance metrics."""
        now = datetime.now()
        
        # Cache health check results for 5 minutes
        if (self._last_health_check and 
            (now - self._last_health_check["timestamp"]).total_seconds() < 300):
            return self._last_health_check
        
        try:
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                async with session.get(f"{self.base_url}/status") as response:
                    latency = (datetime.now() - start_time).total_seconds() * 1000
                    
                    health_data = {
                        "status": "ok" if response.status == 200 else "error",
                        "latency_ms": latency,
                        "timestamp": now
                    }
                    
                    if response.status == 200:
                        health_data.update(await response.json())
                    
                    self._last_health_check = health_data
                    return health_data
                    
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": now
            }
    
    async def supported_tasks(self) -> List[str]:
        """Get list of supported task types."""
        capabilities = await self.get_capabilities()
        tasks = set()
        
        for model in capabilities.get("models", []):
            tasks.update(model.get("tasks", []))
        
        return list(tasks)
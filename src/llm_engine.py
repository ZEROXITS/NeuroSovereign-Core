import os
import requests
import json
from typing import List, Dict, Any

class LocalLLMEngine:
    """
    Engine for interacting with Large Language Models.
    Prioritizes local sovereignty while allowing for high-performance open-source APIs.
    """
    
    def __init__(self, base_url: str = None, model_name: str = "DeepSeek-V3"):
        # Default to a local Ollama or vLLM instance if no URL provided
        self.base_url = base_url or os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
        self.model_name = model_name
        self.api_key = os.getenv("LLM_API_KEY", "sovereign-key")
        print(f"[*] LLM Engine Initialized. Model: {self.model_name}")

    def generate_response(self, prompt: str, system_prompt: str = "You are NeuroSovereign.") -> str:
        """Generates a response using an OpenAI-compatible API."""
        
        # If we are in a demo/mock mode (no server running)
        if "localhost" in self.base_url and not self._is_server_alive():
            return self._mock_response(prompt)

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1024
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error connecting to LLM server: {e}\nFalling back to internal logic."

    def _is_server_alive(self) -> bool:
        try:
            requests.get(self.base_url.replace("/v1", "/"), timeout=2)
            return True
        except:
            return False

    def _mock_response(self, prompt: str) -> str:
        """Simulated reasoning for demonstration when no local GPU is present."""
        if "Create a new directory" in prompt:
            return "Thought: The user wants to create a directory. I should use the shell.\nAction: execute_shell('mkdir -p Sovereign_Data && ls -F')"
        if "search" in prompt:
            return "Thought: I need to search the web. I will use the browser tool.\nAction: execute_shell('curl -s https://api.duckduckgo.com/?q=AI+trends&format=json')"
        
        return "Thought: I am processing the request.\nAction: final_answer('I am ready to assist you with your sovereign AI tasks.')"

if __name__ == "__main__":
    engine = LocalLLMEngine()
    print(engine.generate_response("Hello!"))

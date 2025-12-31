import os
import json
import time
from typing import List, Dict, Any
try:
    from .pc_control import PCControlModule
    from .llm_engine import LocalLLMEngine
except ImportError:
    from pc_control import PCControlModule
    from llm_engine import LocalLLMEngine

class NeuroSovereignAgent:
    """
    The core agent class for NeuroSovereign Systems.
    Designed for high-level reasoning, autonomous planning, and tool execution.
    """
    def __init__(self, model_name: str = "DeepSeek-V3"):
        self.name = "NeuroSovereign"
        self.pc_control = PCControlModule()
        self.llm = LocalLLMEngine(model_name=model_name)
        self.memory = []
        self.max_iterations = 10
        print(f"[*] {self.name} Agent Core Online. Model: {model_name}")

    def _get_system_prompt(self) -> str:
        return """You are NeuroSovereign, a sovereign and autonomous AI agent. 
Your goal is to assist the user by executing complex tasks across the system.
You have access to tools for PC control, shell execution, and web browsing.
Always think step-by-step. Plan your actions, execute them, and reflect on the results.
You are independent and do not rely on external centralized services.
"""

    def run(self, task: str):
        """Main execution loop (Think-Act-Observe)."""
        print(f"\n[Task]: {task}")
        self.memory.append({"role": "user", "content": task})
        
        for i in range(self.max_iterations):
            print(f"\n[Iteration {i+1}] Thinking...")
            
            # 1. Think & Plan
            prompt = self._build_prompt()
            response = self.llm.generate_response(prompt, self._get_system_prompt())
            
            print(f"[Thought]: {response}")
            
            # 2. Parse Action (Simplified for now)
            action = self._parse_action(response)
            if not action or action['name'] == 'final_answer':
                print(f"\n[Final Answer]: {response}")
                break
                
            # 3. Execute Action
            print(f"[Action]: Executing {action['name']} with {action['params']}")
            observation = self._execute_tool(action['name'], action['params'])
            
            print(f"[Observation]: {observation}")
            self.memory.append({"role": "assistant", "content": response})
            self.memory.append({"role": "system", "content": f"Observation: {observation}"})

    def _build_prompt(self) -> str:
        history = ""
        for m in self.memory[-5:]: # Last 5 interactions
            history += f"{m['role']}: {m['content']}\n"
        
        return f"""Current History:
{history}

Available Tools:
- execute_shell(command: str): Run a terminal command.
- pc_control_click(x: int, y: int): Click on screen.
- pc_control_type(text: str): Type text.
- final_answer(text: str): Provide the final result to the user.

Format your response as:
Thought: <your reasoning>
Action: <tool_name>(<params>)
"""

    def _parse_action(self, response: str) -> Dict:
        if "Action:" in response:
            action_line = response.split("Action:")[1].strip()
            if "(" in action_line and ")" in action_line:
                name = action_line.split("(")[0]
                params_str = action_line.split("(")[1].split(")")[0]
                # Simple param parsing
                params = {}
                if params_str:
                    if ":" in params_str: # dict-like
                        try: params = json.loads(params_str.replace("'", "\""))
                        except: params = {"raw": params_str}
                    else:
                        params = {"cmd": params_str.strip("'\"")}
                return {"name": name, "params": params}
        return {"name": "final_answer", "params": {}}

    def _execute_tool(self, name: str, params: Dict) -> str:
        if name == "execute_shell":
            cmd = params.get("cmd")
            return os.popen(cmd).read()
        elif name.startswith("pc_control"):
            return self.pc_control.execute(name, params)
        return f"Unknown tool: {name}"

if __name__ == "__main__":
    agent = NeuroSovereignAgent()
    agent.run("Create a new directory named 'Sovereign_Data' and list the files.")

import os
import json
import time
import subprocess
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    from .pc_control import PCControlModule
    from .llm_engine import LocalLLMEngine
    from .live_interaction import LiveInteractionModule
    from .self_evolution import SelfEvolutionModule
except ImportError:
    from pc_control import PCControlModule
    from llm_engine import LocalLLMEngine
    from live_interaction import LiveInteractionModule
    from self_evolution import SelfEvolutionModule

class NeuroSovereignAdvancedAgent:
    """
    Advanced NeuroSovereign Agent with full Think-Act-Observe loop.
    Implements autonomous reasoning, execution, and self-improvement.
    """
    
    def __init__(self, model_name: str = "DeepSeek-V3", max_iterations: int = 10):
        self.name = "NeuroSovereign"
        self.version = "2.0-Advanced"
        self.model_name = model_name
        self.max_iterations = max_iterations
        
        # Initialize subsystems
        self.llm = LocalLLMEngine(model_name=model_name)
        self.pc_control = PCControlModule()
        self.live_interaction = LiveInteractionModule()
        self.evolution = SelfEvolutionModule()
        
        # State management
        self.memory = []
        self.execution_log = []
        self.metrics = {
            "tasks_completed": 0,
            "actions_executed": 0,
            "errors_recovered": 0,
            "uptime_seconds": 0
        }
        
        self.start_time = time.time()
        print(f"[*] {self.name} {self.version} Agent Online")
        print(f"[*] Model: {self.model_name}")
        print(f"[*] Max Iterations: {self.max_iterations}")

    def _get_system_prompt(self) -> str:
        """Returns the system prompt for the agent."""
        return f"""You are {self.name}, an advanced sovereign AI agent.
Your goal is to complete user tasks autonomously and efficiently.

You have access to the following capabilities:
1. execute_shell(command: str) - Run terminal commands
2. pc_control_click(x: int, y: int) - Click on screen coordinates
3. pc_control_type(text: str) - Type text
4. take_screenshot() - Capture the current screen
5. final_answer(text: str) - Provide the final result

Always think step-by-step. Plan your actions, execute them, and observe the results.
You are independent and do not rely on external centralized services.
Be efficient and minimize the number of iterations needed.
"""

    def execute(self, task: str, enable_live: bool = False) -> str:
        """
        Main execution method: runs the Think-Act-Observe loop.
        """
        print(f"\n{'='*60}")
        print(f"[TASK] {task}")
        print(f"{'='*60}")
        
        self.memory = [{"role": "user", "content": task}]
        
        if enable_live:
            self.live_interaction.start_live_session()
        
        for iteration in range(self.max_iterations):
            print(f"\n[Iteration {iteration + 1}/{self.max_iterations}]")
            
            # 1. THINK: Generate reasoning and plan
            thought = self._think()
            if not thought:
                break
            
            # 2. ACT: Parse and execute action
            action = self._parse_action(thought)
            if action["name"] == "final_answer":
                result = action.get("content", thought)
                print(f"\n[FINAL ANSWER] {result}")
                self.memory.append({"role": "assistant", "content": result})
                self.metrics["tasks_completed"] += 1
                return result
            
            # Execute the action
            observation = self._execute_action(action)
            print(f"[Observation] {observation[:100]}...")
            
            # 3. OBSERVE: Update memory with observation
            self.memory.append({"role": "assistant", "content": thought})
            self.memory.append({"role": "system", "content": f"Observation: {observation}"})
            
            self.metrics["actions_executed"] += 1
            time.sleep(0.5)  # Brief pause between iterations
        
        if enable_live:
            self.live_interaction.stop_live_session()
        
        return "Task completed (max iterations reached)"

    def _think(self) -> Optional[str]:
        """
        Generates reasoning and plans the next action.
        """
        prompt = self._build_prompt()
        
        try:
            response = self.llm.generate_response(prompt, self._get_system_prompt())
            print(f"[Thought] {response[:150]}...")
            return response
        except Exception as e:
            print(f"[Error] LLM generation failed: {e}")
            self.metrics["errors_recovered"] += 1
            return None

    def _build_prompt(self) -> str:
        """Constructs the prompt from memory and context."""
        history = ""
        for m in self.memory[-5:]:  # Last 5 interactions
            history += f"{m['role'].upper()}: {m['content'][:100]}\n"
        
        return f"""Current History:
{history}

Available Tools:
- execute_shell(command: str): Run a terminal command
- pc_control_click(x: int, y: int): Click on screen
- pc_control_type(text: str): Type text
- take_screenshot(): Capture screen
- final_answer(text: str): Provide final result

Format your response as:
Thought: <your reasoning>
Action: <tool_name>(<params>)
"""

    def _parse_action(self, response: str) -> Dict[str, Any]:
        """Parses the action from the LLM response."""
        if "Action:" in response:
            action_line = response.split("Action:")[1].strip().split("\n")[0]
            
            if "(" in action_line and ")" in action_line:
                name = action_line.split("(")[0].strip()
                params_str = action_line.split("(")[1].split(")")[0]
                
                params = {}
                if params_str:
                    try:
                        params = json.loads(params_str.replace("'", "\""))
                    except:
                        params = {"raw": params_str}
                
                return {"name": name, "params": params}
        
        # If contains "final_answer" or "complete", return final answer
        if "final_answer" in response.lower() or "complete" in response.lower():
            return {"name": "final_answer", "content": response}
        
        return {"name": "final_answer", "content": response}

    def _execute_action(self, action: Dict[str, Any]) -> str:
        """Executes the parsed action."""
        name = action.get("name", "")
        params = action.get("params", {})
        
        try:
            if name == "execute_shell":
                cmd = params.get("cmd") or params.get("command", "")
                return self.pc_control.run_shell(cmd)
            
            elif name == "pc_control_click":
                x = params.get("x", 0)
                y = params.get("y", 0)
                return self.pc_control.click(x, y)
            
            elif name == "pc_control_type":
                text = params.get("text", "")
                return self.pc_control.type_text(text)
            
            elif name == "take_screenshot":
                return self.pc_control.take_screenshot()
            
            else:
                return f"Unknown action: {name}"
        
        except Exception as e:
            self.metrics["errors_recovered"] += 1
            return f"Error executing {name}: {str(e)}"

    def get_status(self) -> Dict[str, Any]:
        """Returns current agent status."""
        uptime = time.time() - self.start_time
        return {
            "name": self.name,
            "version": self.version,
            "model": self.model_name,
            "uptime_seconds": uptime,
            "metrics": self.metrics,
            "memory_size": len(self.memory),
            "timestamp": datetime.now().isoformat()
        }

    def self_improve(self) -> str:
        """Analyzes and improves its own code."""
        print("\n[Self-Improvement] Analyzing codebase...")
        analysis = self.evolution.analyze_codebase()
        print(analysis)
        return analysis

if __name__ == "__main__":
    agent = NeuroSovereignAdvancedAgent(model_name="DeepSeek-V3")
    
    # Example tasks
    result = agent.execute("Create a directory named 'NeuroSovereign_Output' and list its contents")
    print(f"\nResult: {result}")
    print(f"\nAgent Status: {json.dumps(agent.get_status(), indent=2)}")

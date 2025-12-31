import sys
import os
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agent import NeuroSovereignAgent

def run_demo():
    print("="*50)
    print("🚀 NEUROSOVEREIGN SYSTEMS - SUPER AI DEMO ACTIVATED")
    print("="*50)
    time.sleep(1)

    # 1. Initialize the Agent
    # We use a powerful model name to represent the vision
    agent = NeuroSovereignAgent(model_name="DeepSeek-V3 / Llama-3.3-70B")
    
    # 2. Agent Reasoning & Execution Loop
    print("\n[DEMO]: Testing Autonomous Reasoning & Execution...")
    query = "Create a directory named 'Sovereign_Assets' and write a file 'mission.txt' inside it with our core values."
    agent.run(query)

    print("\n" + "="*50)
    print("✅ DEMO COMPLETED - SYSTEM IS SOVEREIGN")
    print("="*50)

if __name__ == "__main__":
    run_demo()

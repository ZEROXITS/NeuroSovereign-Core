import sys
import os
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agent import NeuroSovereignAgent
from pc_control import PCControlModule
from self_evolution import SelfEvolutionModule

def run_demo():
    print("="*50)
    print("🚀 NEUROSOVEREIGN - SUPER AI DEMO ACTIVATED")
    print("="*50)
    time.sleep(1)

    # 1. Initialize the Agent
    agent = NeuroSovereignAgent()
    print(f"\n[SYSTEM]: Agent {agent.name} is AWAKE.")
    time.sleep(1)

    # 2. Demonstrate PC Control Capability
    print("\n[DEMO]: Testing PC Control Capabilities...")
    pc = PCControlModule()
    stdout, _ = pc.execute_os_command("uptime")
    print(f"[ACTION]: Checking System Status... Result: {stdout.strip()}")
    time.sleep(1)

    # 3. Demonstrate Self-Evolution
    print("\n[DEMO]: Testing Self-Evolution Module...")
    evolver = SelfEvolutionModule()
    analysis = evolver.analyze_code("src/agent.py")
    print(f"[ACTION]: {analysis}")
    status = evolver.run_self_test()
    print(f"[ACTION]: {status}")
    time.sleep(1)

    # 4. Agent Reasoning
    print("\n[DEMO]: Testing Agent Reasoning Loop...")
    query = "Analyze the system and prepare for full deployment."
    response = agent.think(query)
    print(f"\n[NEUROSOVEREIGN]: {response}")

    print("\n" + "="*50)
    print("✅ DEMO COMPLETED SUCCESSFULLY")
    print("="*50)

if __name__ == "__main__":
    run_demo()

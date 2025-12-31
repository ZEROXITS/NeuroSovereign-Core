#!/usr/bin/env python3
"""
NeuroSovereign Advanced Agent Demo
Demonstrates the full Think-Act-Observe loop with autonomous reasoning.
"""

import sys
import os
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agent_advanced import NeuroSovereignAdvancedAgent

def main():
    print("="*70)
    print("   NEUROSOVEREIGN SYSTEMS - ADVANCED AGENT DEMONSTRATION")
    print("="*70)
    print()
    
    # Initialize the advanced agent
    agent = NeuroSovereignAdvancedAgent(model_name="DeepSeek-V3", max_iterations=5)
    
    # Scenario 1: File System Operations
    print("\n[Scenario 1] File System Operations")
    print("-" * 70)
    task1 = "Create a directory called 'NeuroSovereign_Assets' and create a file named 'manifest.txt' inside it"
    result1 = agent.execute(task1)
    print(f"✓ Completed: {result1}")
    
    time.sleep(2)
    
    # Scenario 2: System Information
    print("\n[Scenario 2] System Information Gathering")
    print("-" * 70)
    task2 = "Get the current system uptime and disk usage information"
    result2 = agent.execute(task2)
    print(f"✓ Completed: {result2}")
    
    time.sleep(2)
    
    # Scenario 3: Self-Improvement
    print("\n[Scenario 3] Self-Improvement Analysis")
    print("-" * 70)
    print("Analyzing codebase for potential improvements...")
    improvement = agent.self_improve()
    
    # Print final status
    print("\n" + "="*70)
    print("   AGENT STATUS REPORT")
    print("="*70)
    status = agent.get_status()
    print(f"Agent Name: {status['name']}")
    print(f"Version: {status['version']}")
    print(f"Model: {status['model']}")
    print(f"Uptime: {status['uptime_seconds']:.2f} seconds")
    print(f"Tasks Completed: {status['metrics']['tasks_completed']}")
    print(f"Actions Executed: {status['metrics']['actions_executed']}")
    print(f"Errors Recovered: {status['metrics']['errors_recovered']}")
    print(f"Memory Size: {status['memory_size']} entries")
    print("="*70)

if __name__ == "__main__":
    main()

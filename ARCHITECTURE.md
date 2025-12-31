# NeuroSovereign Systems: Sovereign AI Architecture

## 1. Overview
The NeuroSovereign architecture is designed for **full autonomy and sovereignty**, ensuring the agent can operate independently of centralized, proprietary APIs. It follows a **Modular Agentic Design** centered around a continuous **Think-Act-Observe** loop.

## 2. Core Components

| Component | Module | Function | Sovereignty Principle |
| :--- | :--- | :--- | :--- |
| **Sovereign Core** | `src/agent.py` | High-level reasoning, task decomposition, and tool orchestration (The Brain). | Independence |
| **Inference Engine** | `src/llm_engine.py` | Handles all language model inference, prioritizing local/self-hosted LLMs (e.g., Llama 3, DeepSeek). | Model Sovereignty |
| **Motor System** | `src/pc_control.py` | Executes physical and digital actions: mouse, keyboard, shell commands, and browser control. | Execution Sovereignty |
| **Sensory System** | `src/live_interaction.py` | Processes real-time data streams (video, audio, screen content) for live interaction and vision. | Data Sovereignty |
| **Cognitive System** | `src/self_evolution.py` | Analyzes the codebase, proposes, and applies self-improvements and optimizations. | Self-Improvement |

## 3. The Agent Loop (Think-Act-Observe)

The agent operates in a continuous loop to achieve complex goals:

1.  **Think (Reasoning)**: The `agent.py` module uses the `llm_engine.py` to analyze the current state, user request, and history. It generates a detailed plan and selects the next action in a structured format (e.g., ReAct or Tool-Calling).
2.  **Act (Execution)**: The selected action (e.g., `pc_control_click`, `execute_shell`) is dispatched to the relevant Motor or Sensory System module.
3.  **Observe (Feedback)**: The result of the action (e.g., shell output, simulated screenshot confirmation) is returned as an Observation and fed back into the Sovereign Core's context for the next Think step.

## 4. Future Development: Live Vision Integration

To achieve the goal of "PC Control" and "Live Interaction," the Sensory System must be tightly integrated with the Motor System.

*   **Screen Capture**: The agent will periodically capture the screen (via `pc_control.take_screenshot`).
*   **Vision Model**: The image will be processed by a local Vision-Language Model (VLM) (e.g., LLaVA, Fuyu) to identify UI elements, text, and context.
*   **Action Generation**: The Sovereign Core will use the VLM output to generate precise coordinates for the next `pc_control_click` or `pc_control_type` action.

This loop enables the agent to "see" and interact with any application, making it truly autonomous.

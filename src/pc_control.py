import pyautogui
import time
import subprocess
from typing import Tuple, List

class PCControlModule:
    """
    Module for comprehensive control over the host operating system (PC Control).
    This module simulates human interaction (mouse, keyboard) and executes OS commands.
    """
    
    def __init__(self):
        # Fail-safe mechanism to prevent runaway code
        pyautogui.FAILSAFE = True
        print("PC Control Module Initialized.")

    def move_and_click(self, x: int, y: int, button: str = 'left'):
        """Moves the mouse to (x, y) coordinates and performs a click."""
        print(f"Moving mouse to ({x}, {y}) and clicking {button}.")
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click(button=button)

    def type_text(self, text: str, interval: float = 0.05):
        """Types a string of text."""
        print(f"Typing text: '{text[:20]}...'")
        pyautogui.write(text, interval=interval)

    def press_key(self, key: str):
        """Presses a single key or a combination (e.g., 'ctrl', 'alt', 'shift')."""
        print(f"Pressing key: {key}")
        pyautogui.press(key)

    def hotkey(self, *args: str):
        """Presses a combination of keys (e.g., hotkey('ctrl', 'c'))."""
        print(f"Pressing hotkey: {args}")
        pyautogui.hotkey(*args)

    def execute_os_command(self, command: str) -> Tuple[str, str]:
        """Executes a command directly on the operating system."""
        print(f"Executing OS command: {command}")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                check=True, 
                capture_output=True, 
                text=True,
                timeout=10
            )
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return "", f"Error executing command: {e.stderr}"
        except subprocess.TimeoutExpired:
            return "", "Error: Command execution timed out."

    def take_screenshot(self, filename: str = "screenshot.png"):
        """Captures the current screen and saves it."""
        print(f"Taking screenshot and saving to {filename}")
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return filename
        except Exception as e:
            return f"Error taking screenshot: {e}"

# Example usage (for testing purposes)
if __name__ == "__main__":
    pc_control = PCControlModule()
    
    # 1. Execute a simple OS command
    stdout, stderr = pc_control.execute_os_command("echo 'Hello from NeuroSovereign OS Control'")
    print(f"STDOUT: {stdout.strip()}")
    
    # 2. Simulate typing (requires a focused text field)
    # Note: Actual mouse/keyboard simulation requires a graphical environment, 
    # which is limited in a standard sandbox. This code is for the final system.
    # pc_control.move_and_click(100, 100) # Move to a coordinate
    # pc_control.type_text("This is a test from the Sovereign Agent.")
    
    # 3. Take a screenshot
    # screenshot_path = pc_control.take_screenshot("/home/ubuntu/NeuroSovereign-Core/tests/test_screenshot.png")
    # print(f"Screenshot result: {screenshot_path}")

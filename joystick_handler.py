#!/usr/bin/env python3
# coding: utf-8

"""
Joystick Handler Module
Monitors HID joystick inputs and triggers callbacks for specific buttons/axes
"""

import threading
import time
from typing import Callable, Dict, Optional
try:
    import pygame
except ImportError:
    pygame = None
    print("pygame not installed. Install with: pip install pygame")


class JoystickHandler:
    """
    Handles joystick input monitoring in a separate thread.
    Detects button presses and axis movements and triggers registered callbacks.
    """
    
    @staticmethod
    def list_available_joysticks() -> list:
        """
        List all available joysticks connected to the system.
        
        Returns:
            List of tuples containing (index, name) for each joystick
        """
        if pygame is None:
            print("ERROR: pygame is not installed. Cannot list joysticks.")
            return []
        
        try:
            pygame.init()
            pygame.joystick.init()
            
            joystick_count = pygame.joystick.get_count()
            joysticks = []
            
            print(f"\n=== Found {joystick_count} joystick(s) ===")
            for i in range(joystick_count):
                joy = pygame.joystick.Joystick(i)
                joy.init()
                name = joy.get_name()
                joysticks.append((i, name))
                print(f"  [{i}] {name}")
                joy.quit()
            print("=" * 40 + "\n")
            
            return joysticks
            
        except Exception as e:
            print(f"Error listing joysticks: {e}")
            return []
    
    @staticmethod
    def find_joystick_by_name(name_pattern: str, occurrence: int = 0) -> Optional[int]:
        """
        Find a joystick by name (case-insensitive partial match).
        
        Args:
            name_pattern: String to search for in joystick names
            occurrence: Which occurrence to return (0=first, 1=second, etc.)
            
        Returns:
            Index of the matching joystick, or None if not found
        """
        joysticks = JoystickHandler.list_available_joysticks()
        name_pattern_lower = name_pattern.lower()
        matches = []
        
        for index, name in joysticks:
            if name_pattern_lower in name.lower():
                matches.append((index, name))
        
        if not matches:
            print(f"No joystick found matching '{name_pattern}'")
            return None
        
        if len(matches) > 1:
            print(f"\nFound {len(matches)} joysticks matching '{name_pattern}':")
            for idx, (index, name) in enumerate(matches):
                print(f"  Occurrence {idx}: [{index}] {name}")
        
        if occurrence >= len(matches):
            print(f"Occurrence {occurrence} requested but only {len(matches)} match(es) found")
            occurrence = 0
        
        selected_index, selected_name = matches[occurrence]
        print(f"Selected: [{selected_index}] {selected_name} (occurrence {occurrence})")
        return selected_index
    
    def __init__(self, joystick_index: int = 0, polling_rate: float = 0.05, debug: bool = False):
        """
        Initialize the joystick handler.
        
        Args:
            joystick_index: Index of the joystick to monitor (default: 0 for first joystick)
            polling_rate: How often to poll the joystick in seconds (default: 0.05 = 20Hz)
            debug: Enable debug output to troubleshoot polling issues
        """
        self.joystick_index = joystick_index
        self.polling_rate = polling_rate
        self.joystick = None
        self.is_running = False
        self.thread = None
        self.debug = debug
        self.poll_count = 0
        
        # Callback dictionaries
        self.button_callbacks: Dict[int, Callable] = {}
        self.button_release_callbacks: Dict[int, Callable] = {}
        self.axis_callbacks: Dict[int, Callable[[float], None]] = {}
        self.hat_callbacks: Dict[int, Callable[[tuple], None]] = {}
        
        # State tracking
        self.button_states: Dict[int, bool] = {}
        self.axis_values: Dict[int, float] = {}
        self.axis_thresholds: Dict[int, float] = {}
        
    def initialize(self) -> bool:
        """
        Initialize pygame and the joystick.
        
        Returns:
            True if initialization successful, False otherwise
        """
        if pygame is None:
            print("ERROR: pygame is not installed. Cannot initialize joystick.")
            return False
            
        try:
            pygame.init()
            pygame.joystick.init()
            
            joystick_count = pygame.joystick.get_count()
            if joystick_count == 0:
                print("No joysticks detected.")
                return False
                
            if self.joystick_index >= joystick_count:
                print(f"Joystick index {self.joystick_index} out of range. Found {joystick_count} joystick(s).")
                return False
                
            self.joystick = pygame.joystick.Joystick(self.joystick_index)
            self.joystick.init()
            
            print(f"Joystick initialized: {self.joystick.get_name()}")
            print(f"  Buttons: {self.joystick.get_numbuttons()}")
            print(f"  Axes: {self.joystick.get_numaxes()}")
            print(f"  Hats: {self.joystick.get_numhats()}")
            
            return True
            
        except Exception as e:
            print(f"Error initializing joystick: {e}")
            return False
    
    def register_button_press(self, button_index: int, callback: Callable):
        """
        Register a callback for when a button is pressed.
        
        Args:
            button_index: The button number (e.g., 0 for trigger)
            callback: Function to call when button is pressed (no arguments)
        """
        self.button_callbacks[button_index] = callback
        print(f"Registered button press callback for button {button_index}")
    
    def register_button_release(self, button_index: int, callback: Callable):
        """
        Register a callback for when a button is released.
        
        Args:
            button_index: The button number
            callback: Function to call when button is released (no arguments)
        """
        self.button_release_callbacks[button_index] = callback
        print(f"Registered button release callback for button {button_index}")
    
    def register_axis_change(self, axis_index: int, callback: Callable[[float], None], threshold: float = 0.1):
        """
        Register a callback for when an axis value changes significantly.
        
        Args:
            axis_index: The axis number (0=X, 1=Y, 2=Z, etc.)
            callback: Function to call with the axis value (-1.0 to 1.0)
            threshold: Minimum change required to trigger callback (default: 0.1)
        """
        self.axis_callbacks[axis_index] = callback
        self.axis_thresholds[axis_index] = threshold
        self.axis_values[axis_index] = 0.0
        print(f"Registered axis change callback for axis {axis_index}")
    
    def register_hat_change(self, hat_index: int, callback: Callable[[tuple], None]):
        """
        Register a callback for when a hat (D-pad) changes position.
        
        Args:
            hat_index: The hat number
            callback: Function to call with the hat position tuple (x, y)
        """
        self.hat_callbacks[hat_index] = callback
        print(f"Registered hat change callback for hat {hat_index}")
    
    def _poll_joystick(self):
        """Internal method to poll the joystick continuously."""
        if self.debug:
            print("[DEBUG] Joystick polling thread started")
        
        while self.is_running:
            try:
                # Process pygame events to update joystick state
                pygame.event.pump()
                
                self.poll_count += 1
                
                # Debug output every 100 polls (~1-2 seconds depending on polling_rate)
                if self.debug and self.poll_count % 100 == 0:
                    print(f"[DEBUG] Poll #{self.poll_count} - Checking {self.joystick.get_numbuttons()} buttons...")
                
                # Check buttons
                for button_index in range(self.joystick.get_numbuttons()):
                    current_state = self.joystick.get_button(button_index)
                    previous_state = self.button_states.get(button_index, False)
                    
                    # Debug: show any button that is pressed
                    if self.debug and current_state:
                        print(f"[DEBUG] Button {button_index} is currently pressed (state={current_state})")
                    
                    # Button press detection
                    if current_state and not previous_state:
                        if self.debug:
                            print(f"[DEBUG] Button {button_index} press detected, calling callback...")
                        if button_index in self.button_callbacks:
                            try:
                                self.button_callbacks[button_index]()
                            except Exception as e:
                                print(f"Error in button press callback for button {button_index}: {e}")
                    
                    # Button release detection
                    elif not current_state and previous_state:
                        if self.debug:
                            print(f"[DEBUG] Button {button_index} release detected, calling callback...")
                        if button_index in self.button_release_callbacks:
                            try:
                                self.button_release_callbacks[button_index]()
                            except Exception as e:
                                print(f"Error in button release callback for button {button_index}: {e}")
                    
                    self.button_states[button_index] = current_state
                
                # Check axes
                for axis_index in range(self.joystick.get_numaxes()):
                    if axis_index in self.axis_callbacks:
                        current_value = self.joystick.get_axis(axis_index)
                        previous_value = self.axis_values.get(axis_index, 0.0)
                        threshold = self.axis_thresholds.get(axis_index, 0.1)
                        
                        if abs(current_value - previous_value) > threshold:
                            try:
                                self.axis_callbacks[axis_index](current_value)
                            except Exception as e:
                                print(f"Error in axis callback for axis {axis_index}: {e}")
                            self.axis_values[axis_index] = current_value
                
                # Check hats (D-pads)
                for hat_index in range(self.joystick.get_numhats()):
                    if hat_index in self.hat_callbacks:
                        hat_value = self.joystick.get_hat(hat_index)
                        try:
                            self.hat_callbacks[hat_index](hat_value)
                        except Exception as e:
                            print(f"Error in hat callback for hat {hat_index}: {e}")
                
                time.sleep(self.polling_rate)
                
            except Exception as e:
                print(f"Error in joystick polling loop: {e}")
                time.sleep(1)  # Wait before retrying
    
    def start(self) -> bool:
        """
        Start monitoring the joystick in a background thread.
        
        Returns:
            True if started successfully, False otherwise
        """
        if self.is_running:
            print("Joystick handler already running.")
            return False
        
        if self.joystick is None:
            if not self.initialize():
                return False
        
        self.is_running = True
        self.thread = threading.Thread(target=self._poll_joystick, daemon=True)
        self.thread.start()
        print("Joystick monitoring started.")
        return True
    
    def stop(self):
        """Stop monitoring the joystick."""
        if self.is_running:
            self.is_running = False
            if self.thread:
                self.thread.join(timeout=2.0)
            print("Joystick monitoring stopped.")
    
    def get_joystick_info(self) -> Optional[Dict]:
        """
        Get information about the connected joystick.
        
        Returns:
            Dictionary with joystick info or None if not initialized
        """
        if self.joystick is None:
            return None
        
        return {
            "name": self.joystick.get_name(),
            "num_buttons": self.joystick.get_numbuttons(),
            "num_axes": self.joystick.get_numaxes(),
            "num_hats": self.joystick.get_numhats(),
        }
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop()
        if self.joystick:
            self.joystick.quit()
        if pygame:
            pygame.quit()


# Example usage
if __name__ == "__main__":
    def on_trigger_press():
        print("Trigger pressed!")
    
    def on_trigger_release():
        print("Trigger released!")
    
    def on_axis_move(value):
        print(f"Axis moved to: {value:.2f}")
    
    # Create handler
    handler = JoystickHandler()
    
    # Initialize
    if handler.initialize():
        # Register callbacks
        handler.register_button_press(0, on_trigger_press)  # Button 0 is usually the trigger
        handler.register_button_release(0, on_trigger_release)
        # handler.register_axis_change(0, on_axis_move)  # Uncomment to monitor X axis
        
        # Start monitoring
        handler.start()
        
        # Keep running
        try:
            print("Monitoring joystick... Press Ctrl+C to exit.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping...")
            handler.stop()
    else:
        print("Failed to initialize joystick handler.")

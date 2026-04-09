#!/usr/bin/env python3
# coding: utf-8

"""
remap_nose_buttons.py
─────────────────────
Interactive tool to detect which physical buttons correspond to the
Nose-Up and Nose-Down keys on the Virtual Fly G1000 PFD and MFD.

Run this script, then follow the on-screen prompts:
  1. Press NOSE UP  on the G1000 PFD (Captain side)
  2. Press NOSE UP  on the G1000 MFD (Captain side)
  3. Press NOSE DOWN on the G1000 PFD (Captain side)
  4. Press NOSE DOWN on the G1000 MFD (Captain side)

The detected button numbers are saved to  nose_button_config.json
which main_aircraft_agent.py reads at startup to register the handlers.
"""

import json
import os
import sys
import time

try:
    import pygame
except ImportError:
    print("ERROR: pygame is not installed.")
    print("Install it with:  pip install pygame")
    sys.exit(1)

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nose_button_config.json")

# ── Detect both G1000 devices ────────────────────────────────────────────────

def find_joystick(name_pattern: str, occurrence: int = 0):
    """Return (index, name) or (None, None) if not found."""
    count = pygame.joystick.get_count()
    matches = []
    for i in range(count):
        j = pygame.joystick.Joystick(i)
        j.init()
        if name_pattern.lower() in j.get_name().lower():
            matches.append((i, j.get_name()))
    if not matches:
        return None, None
    if occurrence >= len(matches):
        occurrence = 0
    return matches[occurrence]


def wait_for_button(joystick_index: int, joystick_name: str, prompt: str) -> int:
    """
    Block until the user presses a button on the specified joystick.
    Returns the button index.
    """
    joy = pygame.joystick.Joystick(joystick_index)
    joy.init()

    print(f"\n  ► {prompt}")
    print(f"    (listening on [{joystick_index}] {joystick_name})")
    print("    Press the button now…", flush=True)

    # Drain any queued events so we start fresh
    pygame.event.clear()

    while True:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN and event.joy == joystick_index:
                print(f"    ✓ Detected button #{event.button}")
                return event.button
        time.sleep(0.01)


def main():
    pygame.init()
    pygame.joystick.init()

    count = pygame.joystick.get_count()
    print(f"\n=== Nose Button Remapper ===")
    print(f"Found {count} joystick(s):")
    for i in range(count):
        j = pygame.joystick.Joystick(i)
        j.init()
        print(f"  [{i}] {j.get_name()}")
    print()

    # ── Locate PFD and MFD ───────────────────────────────────────────────────
    mfd_index, mfd_name = find_joystick("G1000 MFD", occurrence=0)
    # occurrence=1 skips "G1000 PFD2" and lands on "G1000 PFD"
    pfd_index, pfd_name = find_joystick("G1000 PFD", occurrence=1)

    if mfd_index is None:
        print("ERROR: G1000 MFD not found. Make sure the device is connected and recognised by the OS.")
        sys.exit(1)
    if pfd_index is None:
        print("ERROR: G1000 PFD not found. Make sure the device is connected and recognised by the OS.")
        sys.exit(1)

    print(f"G1000 PFD → [{pfd_index}] {pfd_name}")
    print(f"G1000 MFD → [{mfd_index}] {mfd_name}")
    print()
    print("You will be asked to press 4 buttons in order.")
    print("Do NOT press anything until each prompt appears.\n")
    input("Press ENTER to start…")

    # ── Step-by-step button capture ──────────────────────────────────────────
    pfd_nose_up   = wait_for_button(pfd_index, pfd_name, "Press NOSE UP   on the G1000 PFD (Captain)")
    time.sleep(0.3)   # debounce
    pygame.event.clear()

    mfd_nose_up   = wait_for_button(mfd_index, mfd_name, "Press NOSE UP   on the G1000 MFD (Captain)")
    time.sleep(0.3)
    pygame.event.clear()

    pfd_nose_down = wait_for_button(pfd_index, pfd_name, "Press NOSE DOWN on the G1000 PFD (Captain)")
    time.sleep(0.3)
    pygame.event.clear()

    mfd_nose_down = wait_for_button(mfd_index, mfd_name, "Press NOSE DOWN on the G1000 MFD (Captain)")
    time.sleep(0.3)

    # ── Save config ──────────────────────────────────────────────────────────
    config = {
        "pfd_nose_up_button":   pfd_nose_up,
        "pfd_nose_down_button": pfd_nose_down,
        "mfd_nose_up_button":   mfd_nose_up,
        "mfd_nose_down_button": mfd_nose_down,
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

    print(f"\n=== Mapping saved to {CONFIG_FILE} ===")
    print(json.dumps(config, indent=2))
    print()
    print("Restart main_aircraft_agent.py to activate the new mappings.")

    pygame.quit()


if __name__ == "__main__":
    main()

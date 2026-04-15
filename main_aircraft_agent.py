#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Aircraft version 1.0
#  Created by Ingenuity i/o on 2025/02/25
#

import sys
import os
import traceback
import ingescape as igs
from echo_aircraft_agent import *
import time
import xpc
import signal
import threading
import tkinter as tk
import queue as _queue_module
from collections import Counter
from joystick_handler import JoystickHandler

# ============= Configuration =============
JOYSTICK_VERBOSE = True  # Set to True to see detailed joystick button press/release logs
PTT_LONG_PRESS_TIME = 0.3  # Time in seconds to hold button for PTT activation
CLICK_SOUND_VOLUME = 1.0  # Volume for the click sound (0.0 = silent, 1.0 = full volume)
# Joystick-specific smart button index (button with PTT/check/approve logic)
# Yoko+ uses button 5; Extreme 3D Pro uses button 0 (trigger)
YOKO_SMART_BUTTON = 5
EXTREME3D_SMART_BUTTON = 0
# =========================================

neverDone = True

## def datarefs string
#ptt_dref = "sim/cockpit2/controls/tailwheel_lock_ratio" # function as a dummy ptt for now
ias_dref = "sim/cockpit2/gauges/indicators/airspeed_kts_pilot"
pitch_dref = "sim/cockpit2/gauges/indicators/pitch_AHARS_deg_pilot"
altitude_dref = "sim/cockpit2/gauges/indicators/altitude_ft_pilot"
altitude_autopilot_dref = "sim/cockpit/autopilot/altitude" # to read the altitude set in the autopilot
thrust_dref = "sim/cockpit2/engine/actuators/throttle_jet_rev_ratio_all"
heading_dref = "sim/cockpit2/gauges/indicators/heading_AHARS_deg_mag_pilot" # 0 to 1, override because it is a double instead of an array
roll_dref = "sim/cockpit2/gauges/indicators/roll_AHARS_deg_pilot"
parkBrake_dref = "sim/cockpit2/controls/parking_brake_ratio"
verticalSpeed_dref = "sim/cockpit2/gauges/indicators/vvi_fpm_pilot"
rudder_dref = "sim/cockpit2/controls/yoke_heading_ratio"
elevator_dref = "sim/cockpit2/controls/yoke_pitch_ratio"
aileron_dref = "sim/cockpit2/controls/yoke_roll_ratio"
mustang_l_throttle_dref = "Mustang/cockpit/engine/l_throttle"
mustang_l_throttle_up_comm = "sim/engines/throttle_up_1"
mustang_l_throttle_down_comm = "sim/engines/throttle_down_1"
mustang_r_throttle_dref = "Mustang/cockpit/engine/r_throttle"
mustang_r_throttle_up_comm = "sim/engines/throttle_up_2"
mustang_r_throttle_down_comm = "sim/engines/throttle_down_2"
flaps_dref = "sim/cockpit2/controls/flap_ratio"
gear_dref = "sim/cockpit/switches/gear_handle_status"
bird_dref = "sim/operation/failures/rel_bird_strike"
n1_match_bug_dref = "sim/flightmodel/engine/apr_mode" #[1,1,0,0,0,0,0,0] first two means E1 and E2 N1 match, last six are for the other engines
n1_percent_dref = "sim/cockpit2/engine/indicators/N1_percent" # [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] first two means E1 and E2 N1 percent, last four are for the other engines max for the mustang is 91,27388 when toga is engaged static on the runway
slip_dref = "sim/cockpit2/gauges/indicators/slip_deg" #positive is right, negative is left
engine_fires_dref = "sim/cockpit/warnings/annunciators/engine_fires" # [0, 0] first means E1, second means E2
generators_off_dref = "sim/cockpit/warnings/annunciators/generator_off" # [0, 0] first means L generator, second means R generator
pax_safety_dref = "Mustang/cockpit/pax_safety" # 0 is off, 1 is seatbelt 2 is on
trim_rudder_dref = "sim/cockpit2/controls/rudder_trim"
elevator_trim_dref = "sim/cockpit2/controls/elevator_trim"
aileron_trim_dref = "sim/cockpit2/controls/aileron_trim"
fd_pitch_deg_dref = "sim/cockpit2/autopilot/sync_hold_pitch_deg"
clear_master_warning_comm = "sim/annunciator/clear_master_warning"
clear_master_caution_comm = "sim/annunciator/clear_master_caution"
master_warning_dref = "Mustang/master_warning" #readonly 0 is off, 1 is on
master_caution_dref = "Mustang/master_caution" #readonly 0 is off, 1 is on
flight_director_dref = "sim/cockpit2/autopilot/flight_director_mode" 
flight_director_comm = "sim/GPS/g1000n1_fd" # to toggle the flight director
speed_mode_dref = "Mustang/autopilot/annun/flc" #reading for the mustang 0 is off 1 is IAS 2 is mach
speed_mode_comm = "sim/GPS/g1000n1_flc" # to toggle the speed mode
heading_mode_dref = "Mustang/autopilot/annun/hdg" #reading for the mustang 0 is off 2 is on
vertical_speed_down_comm = "sim/autopilot/vertical_speed_down" # to decrease the vs or the flc speed target
vertical_speed_up_comm = "sim/autopilot/vertical_speed_up" # to increase the vs or the flc speed target
alt_sel_dref = "Mustang/cockpit/ap/autopilot" # x100 ft
heading_mode_comm = "sim/GPS/g1000n1_hdg" # to toggle the heading mode
autopilot_master_dref = "sim/cockpit/autopilot/autopilot_mode" # 0 is off, 1 is FD 2 is AP + FD
autopilot_master_comm = "sim/GPS/g1000n1_ap" # to toggle the autopilot master
bottle_l_discharge_dref = "Mustang/cockpit/bottle_l_arm_b" # 0 is off, 1 is on
bottle_r_discharge_dref = "Mustang/cockpit/bottle_r_arm_b" # 0 is off, 1 is on
fuel_boost_l_dref = "Mustang/cockpit/fuel/boost_l" # 0 is off, 1 is on
fuel_boost_r_dref = "Mustang/cockpit/fuel/boost_r" # 0 is off, 1 is on
test_knob_dref = "Mustang/cockpit/test_knob" # 0 to 11 for each test position
heading_sel_dref = "sim/cockpit/autopilot/heading_mag" # 0 to 360
autopilot_state_dref = "sim/cockpit/autopilot/autopilot_state" #need to understand this seems to be an integer that represents the state of the autopilot
yaw_damper_dref = "sim/cockpit/switches/yaw_damper_on" # 0 is off, 1 is on
l_ign_switch_dref = "Mustang/igniter_l" # 0 is off, 1 is on
r_ign_switch_dref = "Mustang/igniter_r" # 0 is off, 1 is on
l_gen_switch_dref = "Mustang/cockpit/electrical/l_gen_switch" # 0 is reset, 1 is off 2 is on
r_gen_switch_dref = "Mustang/cockpit/electrical/r_gen_switch" # 0 is reset, 1 is off 2 is on
transfer_knob_dref = "Mustang/cockpit/fuel/transfer_knob" # 0 is left, 1 is off 2 is right
baro_setting_dref = "sim/cockpit/misc/barometer_setting"
cabin_altitude_dref = "sim/cockpit2/pressurization/indicators/cabin_altitude_ft"
gen_load_dref = "sim/cockpit2/electrical/generator_amps" # [0.0, 0.0] first means L generator, second means R generator
pitot_heat_dref = "Mustang/cockpit/misc/reset_stall_warnings" # 0 is off, 1 is on
anti_ice_engine_dref = "sim/cockpit/switches/anti_ice_engine_air" # [0,0,0,0,0,0,0,0] # first means L engine, second means R engine
l_windshield_anti_ice_dref = "Mustang/cockpit/ai/l_windsheild" # 0 is off, 1 is on
r_windshield_anti_ice_dref = "Mustang/cockpit/ai/r_windsheild" # 0 is off, 1 is on
exterior_lights_dref = "Mustang/cockpit/lighting/taxi_landing" # 0 is off, 1 is taxi, 2 is landing
anti_coll_lights_dref = "sim/cockpit/electrical/strobe_lights_on" # 0 is off, 1 is on
load_situation_2_comm = "sim/operation/load_situation_2" 
load_situation_1_comm = "sim/operation/load_situation_1" 
load_situation_3_comm = "sim/operation/load_situation_3"
pause_toggle_comm = "sim/operation/pause_toggle"
pause_dref = "sim/time/paused"  # 0 = running, 1 = paused
botle_r_arm_dref = "Mustang/cockpit/bottle_r_arm_b" # 0 is off, 1 is on
botle_l_arm_dref = "Mustang/cockpit/bottle_l_arm_b" # 0 is off, 1 is on
l_cutoff_dref = "Mustang/cockpit/engine/l_cutoff"
r_cutoff_dref = "Mustang/cockpit/engine/r_cutoff"
yoke_hide_dref = "Mustang/cockpit/yoke_hide" # 0 is show, 1 is hide
speed_brake_dref = "sim/cockpit2/controls/speedbrake_ratio"
autopilot_airspeed_dref = "sim/cockpit/autopilot/airspeed" # airspeed set in the autopilot
com_1_freq_dref = "sim/cockpit/radios/com1_freq_hz" #11980 is 119.80 MHz, multiply by 100 to get the value in Hz that X-Plane uses
wind_direction_degt_dref = "sim/weather/wind_direction_degt[0]" # wind direction from 0 to 359 degrees TRUE heading - not magnetic
wind_speed_kt_dref = "sim/weather/wind_speed_kt[0]" # wind speed in knots
airspeedmach_dref = "Mustang/airspeedmach" # 0 is airspeed in knots, 1 is mach number - this is a custom dref that the mustang plugin uses to report airspeed in the correct unit based on the speed mode (ias or mach)

"""
		a.observeInput("alarm", agentCB);
		a.observeInput("light_status", agentCB);
		a.observeInput("chrono_time", agentCB);
		a.definition.outputCreate("push_m/w", IopType.IGS_IMPULSION_T);
		a.definition.outputCreate("fd_to_mode", IopType.IGS_IMPULSION_T);
		a.definition.outputCreate("chrono_toggle", IopType.IGS_IMPULSION_T);
		a.definition.outputCreate("eng_fire_switch", IopType.IGS_IMPULSION_T);
		a.definition.outputCreate("flc_set", IopType.IGS_INTEGER_T);
		a.definition.outputCreate("deice_toggle", IopType.IGS_IMPULSION_T);
		a.definition.outputCreate("alti_set_std", IopType.IGS_IMPULSION_T);
"""

refresh_rate = 0.05  # 20 Hz — gives ingescape's background thread regular GIL access
port = 5670
agent_name = "Aircraft"
device = "Ethernet"  # Will be overridden by the startup fallback logic below
verbose = False
is_interrupted = False
start_heading = None
joystick_handler = None  # Global joystick handler instance (primary yoke/stick)
g1000_mfd_handler = None  # JoystickHandler for Virtual Fly G1000 MFD knobs
g1000_pfd_handler = None  # JoystickHandler for Virtual Fly G1000 PFD knobs
reset_time = None  # Track when reset was triggered
outputs_initialized = False  # Track if outputs have been sent after reset
last_full_sync = 0.0  # Track last periodic forced resend of all outputs
FULL_SYNC_INTERVAL = 10.0  # Seconds between forced full output resyncs
checklist_check_time = None  # Scheduled time (epoch) to run initial config check after reset
checklist_active = False      # True while sim is paused waiting for correct initial config
checklist_last_failures = set()  # Track last printed failures to avoid spamming
_checklist_queue = _queue_module.Queue()  # Thread-safe channel → ChecklistWindow
elite_hrv_entered = False    # True when Elite HRV time has been entered for this session
eye_tracking_running = False  # Track if eye tracking is running
last_record_progress = 0.0    # Track last record_progress value to detect if it's increasing
record_progress_stagnant_time = None  # Time when record progress stopped increasing

def signal_handler(signal_received, frame):
    global is_interrupted, joystick_handler, g1000_mfd_handler, g1000_pfd_handler
    print("\n", signal.strsignal(signal_received), sep="")
    print("[SHUTDOWN] Signal received - setting is_interrupted = True")
    is_interrupted = True
    # Stop joystick monitoring on exit
    if joystick_handler:
        joystick_handler.stop()
    if g1000_mfd_handler:
        g1000_mfd_handler.stop()
    if g1000_pfd_handler:
        g1000_pfd_handler.stop()

# Human-readable names for igs agent event codes
_IGS_EVENT_NAMES = {
    1: "PEER_ENTERED",
    2: "PEER_EXITED",
    3: "AGENT_ENTERED",
    4: "AGENT_UPDATED_DEFINITION",
    5: "AGENT_KNOWS_US",
    6: "AGENT_WON_T_DIE",
    7: "AGENT_EXITED",
    8: "AGENT_UPDATED_MAPPING",
    9: "AGENT_HIGH_WATER_MARK",
}

def on_agent_event_callback(event, uuid, name, event_data, my_data):
    event_name = _IGS_EVENT_NAMES.get(event, f"UNKNOWN({event})")
    # print(f"[INGESCAPE] {event_name} - agent: {name} ({uuid}) - data: {event_data}")
    agent_object = my_data
    assert isinstance(agent_object, Echo)
    # add code here if needed

def on_freeze_callback(is_frozen, my_data):
    agent_object = my_data
    assert isinstance(agent_object, Echo)
    # add code here if needed

def bool_input_callback(io_type, name, value_type, value, my_data):
    global eye_tracking_running
    if name == "On_Off":
        if value:
            print("On_Off triggered - sending all outputs...")
            send_all_outputs()
    elif name == "eye_tracking_running":
        eye_tracking_running = value
        print(f"[EYE TRACKING] Eye tracking running status: {value}")
    elif name == "yaw_damper":
        send_dref(yaw_damper_dref, value)
    elif name == "l_ign_switch":
        send_dref(l_ign_switch_dref, value)
    elif name == "r_ign_switch":
        send_dref(r_ign_switch_dref, value)
    elif name == "pitot_heat":
        send_dref(pitot_heat_dref, value)
    elif name == "l_engine_anti_ice":
        current_values = get_dref(anti_ice_engine_dref)
        send_dref(anti_ice_engine_dref, [int(value), current_values[1], 0, 0, 0, 0, 0, 0])
    elif name == "r_engine_anti_ice":
        current_values = get_dref(anti_ice_engine_dref)
        send_dref(anti_ice_engine_dref, [current_values[0], int(value), 0, 0, 0, 0, 0, 0])
    elif name == "l_windshield_anti_ice":
        send_dref(l_windshield_anti_ice_dref, int(value))
    elif name == "r_windshield_anti_ice":
        send_dref(r_windshield_anti_ice_dref, int(value))
    elif name == "anti_coll_lights":
        send_dref(anti_coll_lights_dref, int(value))
    elif name == "yoke_hide":
        send_dref(yoke_hide_dref, int(value))
        if value:
            send_dref(speed_brake_dref, 0)
    elif name == "brake":
        send_dref(parkBrake_dref, 1 if value else 0)
    elif name == "gear":
        set_control_inputs("gear", 1 if value else 0)

def double_input_callback(io_type, name, value_type, value, my_data):
    global last_record_progress, record_progress_stagnant_time
    if name == "record_progress":
        if value > last_record_progress:
            # Progress is increasing, reset stagnant timer
            record_progress_stagnant_time = None
        elif record_progress_stagnant_time is None and last_record_progress > 0:
            # Progress stopped increasing, start timer
            record_progress_stagnant_time = time.time()
        last_record_progress = value
    elif name == "elevator":
        set_control_inputs("elevator", value)
    elif name == "rudder":
        set_control_inputs("rudder", value)
    elif name == "aileron":
        set_control_inputs("aileron", value)
    elif name == "throttle":
        set_control_inputs("throttle", value)
    elif name == "flaps":
        set_control_inputs("flaps", value)
    elif name == "flight_director":
        send_dref(flight_director_dref, value)
    elif name == "l_throttle":
        current_val = get_dref(mustang_l_throttle_dref, is_double=True)[0]
        while current_val != value:
            if current_val < value:
                send_comm(mustang_l_throttle_up_comm)
            elif current_val > value:
                send_comm(mustang_l_throttle_down_comm)
            time.sleep(refresh_rate)
            current_val = get_dref(mustang_l_throttle_dref, is_double=True)[0]
    elif name == "r_throttle":
        current_val = get_dref(mustang_r_throttle_dref, is_double=True)[0]
        while current_val != value:
            if current_val < value:
                send_comm(mustang_r_throttle_up_comm)
            elif current_val > value:
                send_comm(mustang_r_throttle_down_comm)
            time.sleep(refresh_rate)
            current_val = get_dref(mustang_r_throttle_dref, is_double=True)[0]
    elif name == "baro_setting":
        send_dref(baro_setting_dref, value)
    elif name == "trim_rudder":
        print(f"Setting trim_rudder to {value}")
        send_dref(trim_rudder_dref, value)
    elif name == "elevator_trim":
        send_dref(elevator_trim_dref, value)
    elif name == "aileron_trim":
        send_dref(aileron_trim_dref, value)
    elif name == "fd_pitch_deg":
        send_dref(fd_pitch_deg_dref, value)
    elif name == "wind_direction":
        send_dref(wind_direction_degt_dref, value)
    elif name == "wind_speed":
        send_dref(wind_speed_kt_dref, value)

def int_input_callback(io_type, name, value_type, value, my_data):
    if name == "test_knob":
        send_dref(test_knob_dref, value)
    elif name == "l_gen_switch":
        send_dref(l_gen_switch_dref, value + 1)
    elif name == "r_gen_switch":
        send_dref(r_gen_switch_dref, value + 1)
    elif name == "transfer_knob":
        send_dref(transfer_knob_dref, value)
    elif name == "alt_sel":
        send_dref(alt_sel_dref, value / 100)  # X-Plane expects altitude in hundreds of feet
    elif name == "autopilot_heading_set":
        send_dref(heading_sel_dref, value)
    elif name == "fuel_boost_l":
        send_dref(fuel_boost_l_dref, value)
    elif name == "fuel_boost_r":
        send_dref(fuel_boost_r_dref, value)
    elif name == "pax_safety":
        send_dref(pax_safety_dref, int(value))
    elif name == "exterior_lights":
        send_dref(exterior_lights_dref, value)
    elif name == "com_1_freq":
        send_dref(com_1_freq_dref, value)
        
def impulsion_input_callback(io_type, name, value_type, value, my_data):
    global neverDone, reset_time, outputs_initialized, checklist_check_time, checklist_active, elite_hrv_entered
    global last_record_progress, record_progress_stagnant_time
    if name == "reset":
        print("Resetting simulation...")
        neverDone = True
        agent.outside_event_o = "RESET"
        send_comm(load_situation_2_comm)
        reset_time = time.time()  # Record the time of reset
        outputs_initialized = False  # Mark that outputs need to be re-initialized
        checklist_check_time = reset_time + 8  # Schedule config check 8s after reset
        checklist_active = False  # Cancel any in-progress checklist
        elite_hrv_entered = False  # Reset Elite HRV flag
        last_record_progress = 0.0  # Reset record progress tracking
        record_progress_stagnant_time = None

    elif name == "clear_m_w":
        send_comm(clear_master_warning_comm)
    elif name == "clear_m_c":
        send_comm(clear_master_caution_comm)
    elif name == "bird_strike":
        send_dref(bird_dref, 2)
        print("Birds incoming ! :)")
        agent.outside_event_o = "birds"
    elif name == "flight_director":
        send_comm(flight_director_comm)
    elif name == "heading_mode":
        send_comm(heading_mode_comm)
    elif name == "speed_mode":
        send_dref(airspeedmach_dref, 1)
        send_comm(speed_mode_comm)
    elif name == "heading_mode":
        send_comm(heading_mode_comm)
    elif name == "autopilot_master":
        send_comm(autopilot_master_comm)
    elif name == "l_bottle_arm":
        send_dref(botle_l_arm_dref, int(1))
    elif name == "r_bottle_arm":
        send_dref(botle_r_arm_dref, int(1))
    elif name == "nose_down":
        send_comm(vertical_speed_down_comm)
    elif name == "nose_up":
        send_comm(vertical_speed_up_comm)
    elif name == "pause":
        send_comm(pause_toggle_comm)

def string_input_callback(io_type, name, value_type, value, my_data):
    global neverDone, reset_time, outputs_initialized, checklist_check_time, checklist_active, elite_hrv_entered
    global last_record_progress, record_progress_stagnant_time
    if name == "eliteHRV":
        elite_hrv_entered = True
        agent.elite_hrv_o = value
        print(f"[ELITE HRV] Time entered: {value}")
    elif name == "load_situation":
        if value == "06R":
            print(f"Loading situation 06R...")
            send_comm(load_situation_1_comm)
        elif value == "24L":
            print(f"Loading situation 24L...")
            send_comm(load_situation_2_comm)
        elif value == "24R":
            print(f"Loading situation 24R...")
            send_comm(load_situation_3_comm)
        else:
            print(f"Unknown runway designation: {value}")
            return
        
        # Trigger reset behavior (config checklist check)
        neverDone = True
        agent.outside_event_o = f"LOAD_{value}"
        reset_time = time.time()  # Record the time of reset
        outputs_initialized = False  # Mark that outputs need to be re-initialized
        checklist_check_time = reset_time + 8  # Schedule config check 8s after load
        checklist_active = False  # Cancel any in-progress checklist
        elite_hrv_entered = False  # Reset Elite HRV flag

def get_dref(arg, is_double=False):
    try:
        with xpc.XPlaneConnect() as client: 
            dref = arg
            myValue = client.getDREF(dref)  
            if isinstance(myValue, (list, tuple)):
                # Return the array with rounded values
                rounded_value = [round(v, 2) for v in myValue]
            else:
                # Single value - wrap in list for consistency
                rounded_value = [round(myValue, 2)]
    except Exception as e:
        print(f"Error getting dref {arg}: {e}")
        rounded_value = [0.0]
    return rounded_value

def get_drefs(args):
    try:
        with xpc.XPlaneConnect() as client:
            myValues = client.getDREFs(args)
            processed_values = []
            for value in myValues:
                if isinstance(value, (list, tuple)):
                    # Keep the array as-is, but round each element
                    processed_values.append([round(v, 1) for v in value])
                else:
                    # Single value - wrap in list for consistency
                    processed_values.append([round(value, 1)])
    except Exception as e:
        print(f"Error getting drefs {args}: {e}")
        processed_values = [[0.0]] * len(args)
    return processed_values

def send_dref(arg, value):
    try:
        with xpc.XPlaneConnect() as client:
            # send a dref
            dref = arg
            myValue = value
            client.sendDREFs([dref], [myValue])
    except Exception as e:
        print(f"Error sending dref {arg}: {e}")

def send_comm(arg):
    try:
        with xpc.XPlaneConnect() as client:
            # send a comm
            comm = arg
            client.sendCOMM(comm)
    except Exception as e:
        print(f"Error sending COMM {arg}: {e}")

def get_control_inputs():
    try:
        # get control inputs
        with xpc.XPlaneConnect() as client:
            # get aileron, elevator, and rudder
            ctrl = client.getCTRL()
            # round the values to 2 decimal places
            aileron = round(ctrl[1], 2)
            elevator = round(ctrl[0], 2)
            rudder = round(ctrl[2], 2)
            throttle = round(ctrl[3], 2)
            gear = round(ctrl[4], 2)
            flaps = round(ctrl[5], 2)
            speedbrakes = round(ctrl[6], 2)
    except Exception as e:
        print(f"Error getting control inputs: {e}")
        aileron, elevator, rudder = 0.0, 0.0, 0.0
    return aileron, elevator, rudder, throttle, gear, flaps, speedbrakes

def set_control_inputs(name, value):
    try:
        with xpc.XPlaneConnect() as client:
            if name == "elevator":
                client.sendCTRL([value, -998, -998, -998, -998, -998, -998])
            elif name == "aileron":
                client.sendCTRL([-998, value, -998, -998, -998, -998, -998])
            elif name == "rudder":
                client.sendCTRL([-998, -998, value, -998, -998, -998, -998])
            elif name == "throttle":
                client.sendCTRL([-998, -998, -998, value, -998, -998, -998])
            elif name == "gear":
                client.sendCTRL([-998, -998, -998, -998, value, -998, -998])
            elif name == "flaps":
                client.sendCTRL([-998, -998, -998, -998, -998, value, -998])
            elif name == "brake":
                client.sendCTRL([-998, -998, -998, -998, -998, -998, value])
    except Exception as e:
        print(f"Error setting control input {name}: {e}")
    
def get_position(alt, heading):
    try:
        # get position
        with xpc.XPlaneConnect() as client:
            posi = client.getPOSI()
            lat = round(posi[0], 6)  # Latitude
            long = round(posi[1], 6)  # Longitude
            pitch = round(posi[3], 2)  # Pitch
            roll = round(posi[4], 2)  # Roll
            # alt and heading come from the main get_drefs batch (no extra socket)
    except Exception as e:
        print(f"Error getting position: {e}")
        pitch, roll, lat, long = 0.0, 0.0, 0.0, 0.0
    return pitch, heading, roll, alt, lat, long

# catch SIGINT handler before starting agent
signal.signal(signal.SIGINT, signal_handler)

igs.agent_set_name(agent_name)
igs.definition_set_version("1.0")
igs.log_set_console(verbose)
igs.log_set_file(True, None)
igs.log_set_stream(verbose)
igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

agent = Echo()

igs.observe_agent_events(on_agent_event_callback, agent)
igs.observe_freeze(on_freeze_callback, agent)

igs.input_create("On_Off", igs.BOOL_T, None)  # Toggle to send all outputs
igs.input_create("reset", igs.IMPULSION_T, None)
igs.input_create("clear_m_w", igs.IMPULSION_T, None)
igs.input_create("clear_m_c", igs.IMPULSION_T, None)
igs.input_create("elevator", igs.DOUBLE_T, None)
igs.input_create("rudder", igs.DOUBLE_T, None)
igs.input_create("aileron", igs.DOUBLE_T, None)
igs.input_create("throttle", igs.DOUBLE_T, None)
igs.input_create("flaps", igs.DOUBLE_T, None)
igs.input_create("gear", igs.BOOL_T, None)  # true = gear down, false = gear up
igs.input_create("brake", igs.BOOL_T, None)  # true = parking brake on, false = parking brake off
igs.input_create("l_throttle", igs.DOUBLE_T, None) #-1 = cutoff
igs.input_create("r_throttle", igs.DOUBLE_T, None) #-1 = cutoff
igs.input_create("pax_safety", igs.INTEGER_T, None) # 0 is off, 1 is seatbelt 2 is on  
igs.input_create("flight_director", igs.IMPULSION_T, None)  
igs.input_create("speed_mode", igs.IMPULSION_T, None) 
igs.input_create("alt_sel", igs.INTEGER_T, None)
igs.input_create("heading_mode", igs.IMPULSION_T, None)  
igs.input_create("heading_sel", igs.INTEGER_T, None)
igs.input_create("autopilot_master", igs.IMPULSION_T, None)  # 0 is off, 1 is FD 2 is AP + FD
igs.input_create("fuel_boost_l", igs.INTEGER_T, None)  # 0 is norm, 1 is off, 2 is on
igs.input_create("fuel_boost_r", igs.INTEGER_T, None)  # 0 is norm, 1 is off, 2 is on
igs.input_create("test_knob", igs.INTEGER_T, None)  # 0 to 11 for each test position
igs.input_create("autopilot_heading_set", igs.INTEGER_T, None)  # 0 to 360
igs.input_create("yaw_damper", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("l_ign_switch", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("r_ign_switch", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("l_gen_switch", igs.INTEGER_T, None)  # 0 is reset, 1 is off 2 is on
igs.input_create("r_gen_switch", igs.INTEGER_T, None)  # 0 is reset, 1 is off 2 is on
igs.input_create("transfer_knob", igs.INTEGER_T, None)  # 0 is left, 1 is off 2 is right
igs.input_create("bird_strike", igs.IMPULSION_T, None)
igs.input_create("l_ign_switch", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("r_ign_switch", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("baro_setting", igs.DOUBLE_T, None)
igs.input_create("pitot_heat", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("l_engine_anti_ice", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("r_engine_anti_ice", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("l_windshield_anti_ice", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("r_windshield_anti_ice", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("exterior_lights", igs.INTEGER_T, None)  # 0 is off, 1 is taxi, 2 is landing
igs.input_create("anti_coll_lights", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("com_1_freq", igs.INTEGER_T, None)  # COM1 frequency in Hz (e.g. 11980 = 119.80 MHz)
igs.input_create("wind_direction", igs.DOUBLE_T, None)  # wind direction from 0 to 359 degrees TRUE heading
igs.input_create("wind_speed", igs.DOUBLE_T, None)  # wind speed in knots
igs.input_create("On_Off", igs.BOOL_T, None)  # Toggle to send all outputs
igs.input_create("clear_m_w", igs.IMPULSION_T, None)
igs.input_create("clear_m_c", igs.IMPULSION_T, None)
igs.input_create("trim_rudder", igs.DOUBLE_T, None)
igs.input_create("elevator_trim", igs.DOUBLE_T, None)
igs.input_create("aileron_trim", igs.DOUBLE_T, None)
igs.input_create("fd_pitch_deg", igs.DOUBLE_T, None)
igs.input_create("l_bottle_arm", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("r_bottle_arm", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("yoke_hide", igs.BOOL_T, None)  # 0 is show, 1 is hide
igs.input_create("nose_down", igs.IMPULSION_T, None)
igs.input_create("nose_up", igs.IMPULSION_T, None)
igs.input_create("pause", igs.IMPULSION_T, None)
igs.input_create("load_situation", igs.STRING_T, None)  # runway designation: "24R", "24L", "06R"
igs.input_create("eliteHRV", igs.STRING_T, None)  # Elite HRV time entry for checklist
igs.input_create("record_progress", igs.DOUBLE_T, None)  # Number of seconds since recording began
igs.input_create("eye_tracking_running", igs.BOOL_T, None)  # Eye tracking status

igs.output_create("airspeed", igs.DOUBLE_T, None)
igs.output_create("pitch", igs.DOUBLE_T, None)
igs.output_create("controlPitch", igs.DOUBLE_T, None)
igs.output_create("roll", igs.DOUBLE_T, None)
igs.output_create("controlRoll", igs.DOUBLE_T, None)
igs.output_create("heading", igs.DOUBLE_T, None)
igs.output_create("controlYaw", igs.DOUBLE_T, None)
igs.output_create("verticalSpeed", igs.DOUBLE_T, None)
igs.output_create("altitude", igs.DOUBLE_T, None)
igs.output_create("latitude", igs.DOUBLE_T, None)
igs.output_create("longitude", igs.DOUBLE_T, None)
igs.output_create("controlThrottle", igs.DOUBLE_T, None)
igs.output_create("controlFlaps", igs.DOUBLE_T, None)
igs.output_create("controlGear", igs.DOUBLE_T, None)
igs.output_create("speedBrakes", igs.DOUBLE_T, None)
igs.output_create("outsideEvent", igs.STRING_T, None)
igs.output_create("parkBrake", igs.BOOL_T, None)
igs.output_create("l_throttle", igs.DOUBLE_T, None)
igs.output_create("r_throttle", igs.DOUBLE_T, None)
igs.output_create("n1_match_bug", igs.BOOL_T, None)  # [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
igs.output_create("e1_n1_percent", igs.DOUBLE_T, None)  # [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
igs.output_create("e2_n1_percent", igs.DOUBLE_T, None)  # [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
igs.output_create("slip", igs.DOUBLE_T, None)  # positive is right, negative is left
igs.output_create("engine_fire_l", igs.BOOL_T, None)  # 
igs.output_create("engine_fire_r", igs.BOOL_T, None)  # 
igs.output_create("pax_safety", igs.INTEGER_T, None)  # 0 is off, 1 is seatbelt 2 is on
igs.output_create("master_warning", igs.BOOL_T, None)  # readonly 0 is off, 1 is on
igs.output_create("master_caution", igs.BOOL_T, None)  # readonly 0 is off, 1 is on
igs.output_create("flight_director", igs.INTEGER_T, None)  # Not sure how to set FD up using a comm
igs.output_create("speed_mode", igs.INTEGER_T, None)  
igs.output_create("heading_mode", igs.INTEGER_T, None)  # Mustang/heading
igs.output_create("fuel_boost_l", igs.INTEGER_T, None)  # 0 is norm, 1 is off, 2 is on
igs.output_create("fuel_boost_r", igs.INTEGER_T, None)  # 0 is norm, 1 is off, 2 is on
igs.output_create("test_knob", igs.INTEGER_T, None)  # 0 to 11 for each test position
igs.output_create("autopilot_heading_set", igs.INTEGER_T, None)  # 0 to 360
igs.output_create("yaw_damper", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("l_ign_switch", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("r_ign_switch", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("l_gen_switch", igs.INTEGER_T, None)  # 0 is reset, 1 is off 2 is on
igs.output_create("r_gen_switch", igs.INTEGER_T, None)  # 0 is reset, 1 is off 2 is on
igs.output_create("transfer_knob", igs.INTEGER_T, None)  # 0 is left, 1 is off 2 is right
igs.output_create("baro_setting", igs.DOUBLE_T, None)
igs.output_create("cabin_altitude", igs.DOUBLE_T, None)
igs.output_create("l_gen_load", igs.DOUBLE_T, None)  # in amps
igs.output_create("r_gen_load", igs.DOUBLE_T, None)  # in amps
igs.output_create("pitot_heat", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("l_engine_anti_ice", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("r_engine_anti_ice", igs.BOOL_T, None)
igs.output_create("l_windshield_anti_ice", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("r_windshield_anti_ice", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("exterior_lights", igs.INTEGER_T, None)  # 0 is off, 1 is taxi, 2 is landing
igs.output_create("anti_coll_lights", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("trim_rudder", igs.DOUBLE_T, None)
igs.output_create("elevator_trim", igs.DOUBLE_T, None)
igs.output_create("aileron_trim", igs.DOUBLE_T, None)
igs.output_create("fd_pitch_deg", igs.DOUBLE_T, None)
igs.output_create("alt_sel", igs.INTEGER_T, None)
igs.output_create("heading_sel", igs.INTEGER_T, None)
igs.output_create("l_bottle_arm", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("r_bottle_arm", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("ptt", igs.BOOL_T, None)  # Push-to-talk button
igs.output_create("ptt_atc", igs.BOOL_T, None)  # Push-to-talk ATC (button 0)
igs.output_create("check", igs.IMPULSION_T, None)  # Smart button double-click
igs.output_create("approve", igs.BOOL_T, None)  # Smart button triple-click
igs.output_create("yoke_hide", igs.BOOL_T, None)  # 0 is show, 1 is hide
igs.output_create("autopilot_airspeed", igs.DOUBLE_T, None)  # airspeed set in the autopilot
igs.output_create("com_1_freq", igs.INTEGER_T, None)  # COM1 frequency in Hz (e.g. 11980 = 119.80 MHz)
igs.output_create("wind_direction", igs.DOUBLE_T, None)  # wind direction from 0 to 359 degrees TRUE heading
igs.output_create("wind_speed", igs.DOUBLE_T, None)  # wind speed in knots
igs.output_create("eliteHRV", igs.STRING_T, None)  # Elite HRV time recorded
igs.output_create("paused", igs.BOOL_T, None)  # true = sim paused, false = sim running

igs.observe_input("On_Off", bool_input_callback, None)  # Observe On_Off toggle
igs.observe_input("reset", impulsion_input_callback, None)
igs.observe_input("clear_m_w", impulsion_input_callback, None)
igs.observe_input("clear_m_c", impulsion_input_callback, None)
igs.observe_input("elevator", double_input_callback, None)
igs.observe_input("rudder", double_input_callback, None)
igs.observe_input("aileron", double_input_callback, None)
igs.observe_input("throttle", double_input_callback, None)
igs.observe_input("flaps", double_input_callback, None)
igs.observe_input("gear", bool_input_callback, None)  # true = gear down, false = gear up
igs.observe_input("brake", bool_input_callback, None)  # true = parking brake on, false = parking brake off
igs.observe_input("bird_strike", impulsion_input_callback, None)
igs.observe_input("l_throttle", double_input_callback, None)
igs.observe_input("r_throttle", double_input_callback, None)
igs.observe_input("pax_safety", int_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("flight_director", impulsion_input_callback, None)  
igs.observe_input("speed_mode", impulsion_input_callback, None)  # Mustang/airspeedmach
igs.observe_input("heading_mode", impulsion_input_callback, None)  # Mustang/heading
igs.observe_input("autopilot_master", impulsion_input_callback, None)  # 0 is off, 1 is FD 2 is AP + FD
igs.observe_input("fuel_boost_l", int_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("fuel_boost_r", int_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("test_knob", int_input_callback, None)  # 0 to 11 for each test position
igs.observe_input("autopilot_heading_set", int_input_callback, None)  # 0 to 360
igs.observe_input("yaw_damper", bool_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("l_ign_switch", bool_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("r_ign_switch", bool_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("l_gen_switch", int_input_callback, None)  # 0 is reset, 1 is off 2 is on
igs.observe_input("r_gen_switch", int_input_callback, None)  # 0 is reset, 1 is off 2 is on
igs.observe_input("transfer_knob", int_input_callback, None)
igs.observe_input("baro_setting", double_input_callback, None)
igs.observe_input("pitot_heat", bool_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("l_engine_anti_ice", bool_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("r_engine_anti_ice", bool_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("l_windshield_anti_ice", bool_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("r_windshield_anti_ice", bool_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("exterior_lights", int_input_callback, None)  # 0 is off, 1 is taxi, 2 is landing
igs.observe_input("anti_coll_lights", bool_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("com_1_freq", int_input_callback, None)  # COM1 frequency in Hz
igs.observe_input("wind_direction", double_input_callback, None)  # wind direction in degrees true
igs.observe_input("wind_speed", double_input_callback, None)  # wind speed in knots
igs.observe_input("trim_rudder", double_input_callback, None)
igs.observe_input("elevator_trim", double_input_callback, None)
igs.observe_input("aileron_trim", double_input_callback, None)
igs.observe_input("fd_pitch_deg", double_input_callback, None)
igs.observe_input("alt_sel", int_input_callback, None)
igs.observe_input("heading_sel", int_input_callback, None)
igs.observe_input("l_bottle_arm", impulsion_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("r_bottle_arm", impulsion_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("yoke_hide", bool_input_callback, None)  # 0 is show, 1 is hide
igs.observe_input("nose_down", impulsion_input_callback, None)
igs.observe_input("nose_up", impulsion_input_callback, None)
igs.observe_input("pause", impulsion_input_callback, None)
igs.observe_input("load_situation", string_input_callback, None)
igs.observe_input("eliteHRV", string_input_callback, None)
igs.observe_input("record_progress", double_input_callback, None)
igs.observe_input("eye_tracking_running", bool_input_callback, None)

igs.log_set_console(True)
igs.log_set_console_level(igs.LOG_INFO)

_available_devices = igs.net_devices_list()
print(f"[STARTUP] Available network devices: {_available_devices}")
_DEVICE_FALLBACK_ORDER = ["Ethernet", "A7500_NETGEAR", "Wi-Fi"]
# Auto-prepend any available device not already in the list
for _d in _available_devices:
    if _d not in _DEVICE_FALLBACK_ORDER and _d != "Loopback Pseudo-Interface 1":
        _DEVICE_FALLBACK_ORDER.insert(0, _d)
_started = False
for _dev in _DEVICE_FALLBACK_ORDER:
    if _dev not in _available_devices:
        print(f"[STARTUP] Skipping device '{_dev}' (not present on this machine)")
        continue
    _result = igs.start_with_device(_dev, port)
    if _result == 0:  # IGS_SUCCESS = 0
        device = _dev
        print(f"[STARTUP] Agent started on device: {device}")
        _started = True
        break
    else:
        print(f"[STARTUP] Could not start on device '{_dev}' (code {_result}), trying next...")
        igs.stop()
if not _started:
    print("[STARTUP] ERROR: Could not start agent on any device. Exiting.")
    sys.exit(1)
# catch SIGINT handler after starting agent
signal.signal(signal.SIGINT, signal_handler)

# ============= Joystick Integration =============
# Pre-load click sound for low-latency playback on button press
# Small buffer (512) minimises audio latency compared to the default (2048+)
try:
    import pygame.mixer
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.mixer.init()
    _sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sound", "click.mp3")
    click_sound = pygame.mixer.Sound(_sound_path)
    click_sound.set_volume(CLICK_SOUND_VOLUME)
    print(f"Click sound loaded: {_sound_path}")
    _stt_listening_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sound", "stt_listening.mp3")
    stt_listening_sound = pygame.mixer.Sound(_stt_listening_path)
    stt_listening_sound.set_volume(CLICK_SOUND_VOLUME)
    print(f"STT listening sound loaded: {_stt_listening_path}")
    _alarm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sound", "fire_alarm_bell.mp3")
    print(f"Fire alarm sound path set: {_alarm_path}")
except Exception as e:
    click_sound = None
    stt_listening_sound = None
    _alarm_path = None
    print(f"Warning: could not load sounds: {e}")

_master_warning_active = False  # Tracks whether the alarm is currently playing

# Button name mapping for better readability
BUTTON_NAMES = {
    0: "Button 0",
    1: "Button 1",
    2: "Button 2", 
    3: "Button 3",
    4: "Button 4",
    5: "Button 5 (Smart)",
    6: "Button 6"
}

# Button 5 Smart Handler - Detects double-click, triple-click, and long press
class Button5Handler:
    """Special handler for Button 5 with multi-click and long press detection."""
    
    def __init__(self):
        self.click_times = []
        self.press_start_time = None
        self.is_ptt_active = False
        self.long_press_timer = None
        
        # Timing thresholds
        self.double_click_window = 0.6  # Max time between clicks for double/triple click (seconds)
        self.long_press_threshold = PTT_LONG_PRESS_TIME  # Min time for long press to activate PTT (seconds)
        self.click_release_max = 0.3    # Max duration for a click (vs long press)
    
    def on_press(self):
        """Called when Button 5 is pressed."""
        # Play click sound immediately for tactile feedback (pre-loaded, minimal latency)
        if click_sound:
            click_sound.play()
        self.press_start_time = time.time()
        if JOYSTICK_VERBOSE:
            print(f"[JOYSTICK] Button 5 (#5) - PRESSED")
        
        # Start timer to activate PTT if button is held long enough
        self.long_press_timer = threading.Timer(self.long_press_threshold, self._activate_ptt)
        self.long_press_timer.start()
    
    def on_release(self):
        """Called when Button 5 is released."""
        if JOYSTICK_VERBOSE:
            print(f"[JOYSTICK] Button 5 (#5) - RELEASED")
        
        # Cancel long press timer if still pending
        if self.long_press_timer:
            self.long_press_timer.cancel()
            self.long_press_timer = None
        
        if self.press_start_time is None:
            return
        
        press_duration = time.time() - self.press_start_time
        self.press_start_time = None
        
        # If PTT was activated, deactivate it on release
        if self.is_ptt_active:
            print("[PTT] DEACTIVATED")
            igs.output_set_bool("ptt", False)
            self.is_ptt_active = False
            return
        
        # This was a quick click - track it for multi-click detection
        if press_duration <= self.click_release_max:
            current_time = time.time()
            
            # Clean up old clicks outside the time window
            self.click_times = [t for t in self.click_times 
                               if current_time - t < self.double_click_window]
            
            # Add this click
            self.click_times.append(current_time)
            
            # Schedule detection after the window expires
            threading.Timer(self.double_click_window, self._detect_multi_click).start()
    
    def _activate_ptt(self):
        """Activate PTT after button has been held for long_press_threshold."""
        if self.press_start_time is not None:  # Button still held
            print("[PTT] ACTIVATED (long press detected)")
            if stt_listening_sound:
                stt_listening_sound.play()
                # Wait for the sound to finish before activating PTT signal
                sound_duration = stt_listening_sound.get_length()
                time.sleep(sound_duration)
            igs.output_set_bool("ptt", True)
            self.is_ptt_active = True
    
    def _detect_multi_click(self):
        """Detect and handle multi-click patterns after the window expires."""
        click_count = len(self.click_times)
        
        if click_count == 2:
            print("[CHECK] CHECKED (double-click detected)")
            igs.output_set_impulsion("check")
        elif click_count >= 3:
            print("[APPROVE] APPROVE (triple-click detected)")
            igs.output_set_bool("approve", True)
        # Single click - do nothing special
        
        # Clear the click history
        self.click_times = []

# Create Button 5 handler instance
button5_handler = Button5Handler()

def create_button_press_handler(button_num):
    """Factory function to create button press handlers."""
    def handler():
        if JOYSTICK_VERBOSE:
            button_name = BUTTON_NAMES.get(button_num, f"Button {button_num}")
            print(f"[JOYSTICK] {button_name} (#{button_num}) - PRESSED")
    return handler

def create_button_release_handler(button_num):
    """Factory function to create button release handlers."""
    def handler():
        if JOYSTICK_VERBOSE:
            button_name = BUTTON_NAMES.get(button_num, f"Button {button_num}")
            print(f"[JOYSTICK] {button_name} (#{button_num}) - RELEASED")
    return handler

def on_axis_change(axis_num, value):
    """Handler for axis movements."""
    if JOYSTICK_VERBOSE:
        print(f"[JOYSTICK] Axis {axis_num} - Value: {value:.3f}")


def on_hat_change(hat_num, position):
    """Handler for hat/D-pad movements."""
    if JOYSTICK_VERBOSE:
        print(f"[JOYSTICK] Hat {hat_num} - Position: {position}")

# Initialize and start joystick monitoring
# First, list all available joysticks
print("\n" + "="*50)
print("Scanning for available HID devices (joysticks)...")
print("="*50)
JoystickHandler.list_available_joysticks()

# Try to find the "yoko+" joystick (second occurrence if there are multiple)
joystick_index = JoystickHandler.find_joystick_by_name("yoko+", occurrence=1)
using_yoko = joystick_index is not None
if joystick_index is None:
    print("'yoko+' joystick not found, trying first occurrence...")
    joystick_index = JoystickHandler.find_joystick_by_name("yoko+", occurrence=0)
    using_yoko = joystick_index is not None
    if joystick_index is None:
        print("No YOKO+ found, checking for Extreme 3D Pro...")
        joystick_index = JoystickHandler.find_joystick_by_name("extreme", occurrence=0)
        if joystick_index is None:
            print("No Extreme 3D Pro found, using first available joystick (index 0)")
            joystick_index = 0

# Determine which button gets the smart PTT/check/approve handler
smart_button = YOKO_SMART_BUTTON if using_yoko else EXTREME3D_SMART_BUTTON
print(f"Using smart button index: {smart_button} ({'Yoko+' if using_yoko else 'Extreme 3D Pro / fallback'})")

# Disable debug mode for cleaner output
joystick_handler = JoystickHandler(joystick_index=joystick_index, polling_rate=0.01, debug=False)
if joystick_handler.initialize():
    # Get joystick info to determine how many buttons/axes/hats it has
    joy_info = joystick_handler.get_joystick_info()
    
    # Register callbacks for all buttons
    print(f"\nRegistering callbacks for {joy_info['num_buttons']} buttons...")
    def _ptt_atc_press():
        if JOYSTICK_VERBOSE:
            print(f"[JOYSTICK] Button 0 (#0) - PRESSED")
        igs.output_set_bool("ptt_atc", True)
    def _ptt_atc_release():
        if JOYSTICK_VERBOSE:
            print(f"[JOYSTICK] Button 0 (#0) - RELEASED")
        igs.output_set_bool("ptt_atc", False)
    for button_num in range(joy_info['num_buttons']):
        if button_num == smart_button:
            # Use special handler for the smart button (PTT / check / approve)
            print(f"  Button {button_num} -> Smart handler (PTT/check/approve)")
            joystick_handler.register_button_press(button_num, button5_handler.on_press)
            joystick_handler.register_button_release(button_num, button5_handler.on_release)
        elif button_num == 0:
            # Button 0 is PTT-ATC: True on press, False on release (only if not the smart button)
            print(f"  Button 0 -> PTT-ATC handler (ptt_atc)")
            joystick_handler.register_button_press(0, _ptt_atc_press)
            joystick_handler.register_button_release(0, _ptt_atc_release)
        else:
            joystick_handler.register_button_press(button_num, create_button_press_handler(button_num))
            joystick_handler.register_button_release(button_num, create_button_release_handler(button_num))
    
    # Optional: Register axis callbacks (uncomment if you want to see axis movements)
    # for axis_num in range(joy_info['num_axes']):
    #     joystick_handler.register_axis_change(axis_num, lambda val, num=axis_num: on_axis_change(num, val), threshold=0.1)
    
    # Optional: Register hat callbacks (uncomment if you want to see hat movements)
    # for hat_num in range(joy_info['num_hats']):
    #     joystick_handler.register_hat_change(hat_num, lambda pos, num=hat_num: on_hat_change(num, pos))
    
    # Start monitoring in background thread
    joystick_handler.start()
    print("Joystick integration enabled and running in parallel with X-Plane control.")
    print("Press any button to see its name and state!\n")
else:
    print("Joystick not available - continuing without joystick integration.")
    joystick_handler = None

# ============= G1000 ALT Selector Integration =============
# Buttons 16-19 on both MFD and PFD reproduce the Garmin G1000 autopilot ALT knob.
# Native X-Plane behaviour is broken for this aircraft, so we read/write alt_sel_dref
# directly.  alt_sel_dref is stored in units of ×100 ft (10 000 ft → dref value 100).
#   Button 19 = ALT inner ring UP   (+100 ft)
#   Button 18 = ALT inner ring DOWN (-100 ft)
#   Button 17 = ALT outer ring UP   (+1000 ft)
#   Button 16 = ALT outer ring DOWN (-1000 ft)

_ALT_KNOB_BUTTONS = {
    19: ("ALT inner UP",    +100),
    18: ("ALT inner DOWN",  -100),
    17: ("ALT outer UP",   +1000),
    16: ("ALT outer DOWN", -1000),
}

def _alt_sel_adjust(delta_ft: int):
    """Read current autopilot altitude, add delta_ft, clamp, and write back."""
    current = get_dref(alt_sel_dref)
    current_ft = round(current[0] * 100)          # ×100 ft → ft
    new_ft = max(0, min(45000, current_ft + delta_ft))
    send_dref(alt_sel_dref, new_ft / 100)
    igs.output_set_int("alt_sel", new_ft)
    print(f"[ALT SEL] {current_ft} ft -> {new_ft} ft ({delta_ft:+d} ft)")

def _make_alt_knob_handler(panel: str, btn: int):
    label, delta = _ALT_KNOB_BUTTONS[btn]
    def handler():
        print(f"[G1000 {panel}] {label} (#{btn})")
        _alt_sel_adjust(delta)
    return handler

mfd_index = JoystickHandler.find_joystick_by_name("G1000 MFD", occurrence=0)
if mfd_index is not None:
    g1000_mfd_handler = JoystickHandler(joystick_index=mfd_index, polling_rate=0.02, debug=False)
    if g1000_mfd_handler.initialize():
        for btn in _ALT_KNOB_BUTTONS:
            g1000_mfd_handler.register_button_press(btn, _make_alt_knob_handler("MFD", btn))
        g1000_mfd_handler.start()
        print("G1000 MFD ALT knob active (buttons 16-19).")
    else:
        print("G1000 MFD found but failed to initialize.")
        g1000_mfd_handler = None
else:
    print("Virtual Fly G1000 MFD not found - skipping MFD integration.")

# Use occurrence=1 to skip "G1000 PFD2" (occurrence 0) and land on "G1000 PFD"
pfd_index = JoystickHandler.find_joystick_by_name("G1000 PFD", occurrence=1)
if pfd_index is not None:
    g1000_pfd_handler = JoystickHandler(joystick_index=pfd_index, polling_rate=0.02, debug=False)
    if g1000_pfd_handler.initialize():
        for btn in _ALT_KNOB_BUTTONS:
            g1000_pfd_handler.register_button_press(btn, _make_alt_knob_handler("PFD", btn))
        g1000_pfd_handler.start()
        print("G1000 PFD ALT knob active (buttons 16-19).")
    else:
        print("G1000 PFD found but failed to initialize.")
        g1000_pfd_handler = None
else:
    print("Virtual Fly G1000 PFD not found - skipping PFD integration.")

# ============= G1000 Nose-Up / Nose-Down Button Integration =============
# Reads nose_button_config.json (produced by remap_nose_buttons.py).
# Each press sends the same X-Plane command as the ingescape nose_up / nose_down inputs:
#   nose up   → vertical_speed_up_comm   ("sim/autopilot/vertical_speed_up")
#   nose down → vertical_speed_down_comm ("sim/autopilot/vertical_speed_down")

import json as _json

_NOSE_CFG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nose_button_config.json")

def _load_nose_config():
    if not os.path.exists(_NOSE_CFG_PATH):
        print("[NOSE BTN] nose_button_config.json not found — run remap_nose_buttons.py first.")
        return None
    try:
        with open(_NOSE_CFG_PATH) as _f:
            cfg = _json.load(_f)
        required = {"pfd_nose_up_button", "pfd_nose_down_button",
                    "mfd_nose_up_button", "mfd_nose_down_button"}
        if not required.issubset(cfg):
            print("[NOSE BTN] nose_button_config.json is incomplete — re-run remap_nose_buttons.py.")
            return None
        return cfg
    except Exception as _e:
        print(f"[NOSE BTN] Failed to load nose_button_config.json: {_e}")
        return None

_nose_cfg = _load_nose_config()

if _nose_cfg is not None:
    def _make_nose_handler(panel: str, direction: str):
        comm = vertical_speed_up_comm if direction == "up" else vertical_speed_down_comm
        label = "NOSE UP" if direction == "up" else "NOSE DOWN"
        def _handler():
            print(f"[G1000 {panel}] {label} -> {comm}")
            send_comm(comm)
        return _handler

    # Register on MFD handler if it is running
    if g1000_mfd_handler is not None:
        g1000_mfd_handler.register_button_press(_nose_cfg["mfd_nose_up_button"],   _make_nose_handler("MFD", "up"))
        g1000_mfd_handler.register_button_press(_nose_cfg["mfd_nose_down_button"], _make_nose_handler("MFD", "down"))
        print(f"[NOSE BTN] MFD nose up=#{_nose_cfg['mfd_nose_up_button']}  nose down=#{_nose_cfg['mfd_nose_down_button']} registered.")

    # Register on PFD handler if it is running
    if g1000_pfd_handler is not None:
        g1000_pfd_handler.register_button_press(_nose_cfg["pfd_nose_up_button"],   _make_nose_handler("PFD", "up"))
        g1000_pfd_handler.register_button_press(_nose_cfg["pfd_nose_down_button"], _make_nose_handler("PFD", "down"))
        print(f"[NOSE BTN] PFD nose up=#{_nose_cfg['pfd_nose_up_button']}  nose down=#{_nose_cfg['pfd_nose_down_button']} registered.")

# ============= End G1000 ALT Selector Integration =============


class ChecklistWindow:
    """Small borderless always-on-top overlay (top-left of monitor 1) that lists
    aircraft configuration items that do not yet match the required initial state.
    Communicate with it exclusively via _checklist_queue:
      {"type": "show",  "failures": set_of_label_strings}
      {"type": "hide"}
      {"type": "quit"}
    """
    _BG         = "#12121e"
    _BG_HEADER  = "#1e1e3a"
    _FG_TITLE   = "#c8c8ff"
    _FG_FAIL    = "#ff5533"
    _FG_OK      = "#33ff99"
    _FONT       = ("Consolas", 9)
    _FONT_BOLD  = ("Consolas", 9, "bold")

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CONFIG CHECK")
        self.root.geometry("+5+5")           # Top-left of monitor 1
        self.root.attributes("-topmost", True)
        self.root.configure(bg=self._BG)
        self.root.resizable(False, False)
        self.root.overrideredirect(True)      # Borderless
        self.root.withdraw()                  # Hidden until first failure appears

        # ── Drag support ─────────────────────────────────────────────────────
        self._drag_x = self._drag_y = 0

        # ── Header bar ───────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg=self._BG_HEADER, cursor="fleur")
        header.pack(fill="x")
        tk.Label(
            header, text="  ⚠  CONFIG CHECK",
            bg=self._BG_HEADER, fg=self._FG_TITLE,
            font=self._FONT_BOLD, anchor="w"
        ).pack(side="left", pady=3, padx=4)
        tk.Button(
            header, text="×",
            bg=self._BG_HEADER, fg="#666688", relief="flat",
            font=("Consolas", 11, "bold"),
            command=self.root.withdraw,
            activebackground="#ff4444", activeforeground="#fff",
            bd=0, padx=6
        ).pack(side="right")
        header.bind("<ButtonPress-1>", self._start_drag)
        header.bind("<B1-Motion>",     self._do_drag)

        # ── Content ───────────────────────────────────────────────────────────
        content = tk.Frame(self.root, bg=self._BG, padx=10, pady=6)
        content.pack(fill="both", expand=True)
        self._body = tk.Label(
            content, text="",
            bg=self._BG, fg=self._FG_FAIL,
            font=self._FONT, justify="left", anchor="w"
        )
        self._body.pack(fill="x")

        self._separator = tk.Frame(self.root, bg="#2a2a4e", height=1)
        self._separator.pack(fill="x", side="bottom")

        self._poll()

    # ── Drag ─────────────────────────────────────────────────────────────────
    def _start_drag(self, event):
        self._drag_x = event.x_root - self.root.winfo_x()
        self._drag_y = event.y_root - self.root.winfo_y()

    def _do_drag(self, event):
        self.root.geometry(f"+{event.x_root - self._drag_x}+{event.y_root - self._drag_y}")

    # ── Queue polling ────────────────────────────────────────────────────────
    def _poll(self):
        try:
            while True:
                msg = _checklist_queue.get_nowait()
                t = msg.get("type")
                if t == "show":
                    self._render(msg["failures"])
                    self.root.deiconify()
                elif t == "hide":
                    self.root.withdraw()
                elif t == "quit":
                    self.root.quit()
                    return
        except _queue_module.Empty:
            pass
        self.root.after(150, self._poll)

    # ── Rendering ────────────────────────────────────────────────────────────
    def _render(self, failures):
        if not failures:
            self._body.config(text="✓  All systems nominal", fg=self._FG_OK)
        else:
            lines = "\n".join(f"✗  {f}" for f in sorted(failures))
            self._body.config(text=lines, fg=self._FG_FAIL)

    def run(self):
        self.root.mainloop()


def _get_checklist_failures():
    global record_progress_stagnant_time
    failures = set()
    
    # ⚠⚠⚠ ELITE HRV CHECK - MUST BE FIRST ⚠⚠⚠
    if not elite_hrv_entered:
        failures.add("ENTER ELITE HRV TIME")
    
    # Eye tracking status check
    if not eye_tracking_running:
        failures.add("START EYE TRACKING")
    
    # Recording progress check - only flag if stagnant for more than 3 seconds
    if record_progress_stagnant_time is not None:
        if time.time() - record_progress_stagnant_time > 3.0:
            failures.add("RECORDING NOT PROGRESSING")
    
    # Standard aircraft configuration checks
    checks = [
        ('l_ign_switch',          getattr(agent, '_l_ign_switch_o', None),          False,  'L ignition → OFF'),
        ('r_ign_switch',          getattr(agent, '_r_ign_switch_o', None),          False,  'R ignition → OFF'),
        ('l_gen_switch',          getattr(agent, '_l_gen_switch_o', None),          2,     'L generator → ON (2)'),
        ('r_gen_switch',          getattr(agent, '_r_gen_switch_o', None),          2,     'R generator → ON (2)'),
        ('pax_safety',            getattr(agent, '_pax_safety_o', None),            0,     'Pax safety → OFF (0)'),
        ('exterior_lights',       getattr(agent, '_exterior_lights_o', None),       0,     'Exterior lights → OFF (0)'),
        ('anti_coll_lights',      getattr(agent, '_anti_coll_lights_o', None),      False, 'Anti-collision lights → OFF'),
        ('pitot_heat',            getattr(agent, '_pitot_heat_o', None),            False, 'Pitot heat → OFF'),
        ('l_engine_anti_ice',     getattr(agent, '_l_engine_anti_ice_o', None),     False, 'L engine anti-ice → OFF'),
        ('r_engine_anti_ice',     getattr(agent, '_r_engine_anti_ice_o', None),     False, 'R engine anti-ice → OFF'),
        ('l_windshield_anti_ice', getattr(agent, '_l_windshield_anti_ice_o', None), False, 'L windshield anti-ice → OFF'),
        ('r_windshield_anti_ice', getattr(agent, '_r_windshield_anti_ice_o', None), False, 'R windshield anti-ice → OFF'),
        ('park_brake',            getattr(agent, '_park_brake_o', None),            True,  'Parking brake → ON'),
        ('control_gear',          getattr(agent, '_control_gear_o', None),          1.0,   'Landing gear → DOWN (1)'),
        ('control_flaps',         getattr(agent, '_control_flaps_o', None),         0.0,   'Flaps → 0'),
        ('l_fuel_boost',          getattr(agent, '_fuel_boost_l_o', None),          0,     'L fuel boost → NORM (0)'),
        ('r_fuel_boost',          getattr(agent, '_fuel_boost_r_o', None),          0,     'R fuel boost → NORM (0)'),
    ]
    failures.update({label for _, val, expected, label in checks if val != expected})
    
    return failures


def _initial_config_ok():
    """Return True if the sim state matches the required initial configuration."""
    return len(_get_checklist_failures()) == 0


def _collect_output_values():
    """Return a dict of current cached ingescape output values."""
    return {
        'airspeed': getattr(agent, '_airspeed_o', None),
        'pitch': getattr(agent, '_pitch_o', None),
        'control_pitch': getattr(agent, '_control_pitch_o', None),
        'roll': getattr(agent, '_roll_o', None),
        'control_roll': getattr(agent, '_control_roll_o', None),
        'heading': getattr(agent, '_heading_o', None),
        'control_yaw': getattr(agent, '_control_yaw_o', None),
        'vertical_speed': getattr(agent, '_vertical_speed_o', None),
        'altitude': getattr(agent, '_altitude_o', None),
        'latitude': getattr(agent, '_latitude_o', None),
        'longitude': getattr(agent, '_longitude_o', None),
        'control_throttle': getattr(agent, '_control_throttle_o', None),
        'control_flaps': getattr(agent, '_control_flaps_o', None),
        'control_gear': getattr(agent, '_control_gear_o', None),
        'control_speedbrakes': getattr(agent, '_control_speedbrakes_o', None),
        'outside_event': getattr(agent, '_outside_event_o', None),
        'park_brake': getattr(agent, '_park_brake_o', None),
        'l_throttle': getattr(agent, '_l_throttle_o', None),
        'r_throttle': getattr(agent, '_r_throttle_o', None),
        'n1_match_bug': getattr(agent, '_n1_match_bug_o', None),
        'e1_n1_percent': getattr(agent, '_e1_n1_percent_o', None),
        'e2_n1_percent': getattr(agent, '_e2_n1_percent_o', None),
        'slip': getattr(agent, '_slip_o', None),
        'engine_fire_l': getattr(agent, '_engine_fire_l_o', None),
        'engine_fire_r': getattr(agent, '_engine_fire_r_o', None),
        'pax_safety': getattr(agent, '_pax_safety_o', None),
        'master_warning': getattr(agent, '_master_warning_o', None),
        'master_caution': getattr(agent, '_master_caution_o', None),
        'flight_director': getattr(agent, '_flight_director_o', None),
        'speed_mode': getattr(agent, '_speed_mode_o', None),
        'heading_mode': getattr(agent, '_heading_mode_o', None),
        'fuel_boost_l': getattr(agent, '_fuel_boost_l_o', None),
        'fuel_boost_r': getattr(agent, '_fuel_boost_r_o', None),
        'test_knob': getattr(agent, '_test_knob_o', None),
        'autopilot_heading_set': getattr(agent, '_autopilot_heading_set_o', None),
        'yaw_damper': getattr(agent, '_yaw_damper_o', None),
        'l_ign_switch': getattr(agent, '_l_ign_switch_o', None),
        'r_ign_switch': getattr(agent, '_r_ign_switch_o', None),
        'l_gen_switch': getattr(agent, '_l_gen_switch_o', None),
        'r_gen_switch': getattr(agent, '_r_gen_switch_o', None),
        'transfer_knob': getattr(agent, '_transfer_knob_o', None),
        'baro_setting': getattr(agent, '_baro_setting_o', None),
        'cabin_altitude': getattr(agent, '_cabin_altitude_o', None),
        'l_gen_load': getattr(agent, '_l_gen_load_o', None),
        'r_gen_load': getattr(agent, '_r_gen_load_o', None),
        'pitot_heat': getattr(agent, '_pitot_heat_o', None),
        'l_engine_anti_ice': getattr(agent, '_l_engine_anti_ice_o', None),
        'r_engine_anti_ice': getattr(agent, '_r_engine_anti_ice_o', None),
        'l_windshield_anti_ice': getattr(agent, '_l_windshield_anti_ice_o', None),
        'r_windshield_anti_ice': getattr(agent, '_r_windshield_anti_ice_o', None),
        'exterior_lights': getattr(agent, '_exterior_lights_o', None),
        'anti_coll_lights': getattr(agent, '_anti_coll_lights_o', None),
        'trim_rudder': getattr(agent, '_trim_rudder_o', None),
        'elevator_trim': getattr(agent, '_elevator_trim_o', None),
        'aileron_trim': getattr(agent, '_aileron_trim_o', None),
        'fd_pitch_deg': getattr(agent, '_fd_pitch_deg_o', None),
        'alt_sel': getattr(agent, '_alt_sel_o', None),
        'heading_sel': getattr(agent, '_heading_sel_o', None),
        'l_bottle_arm': getattr(agent, '_l_bottle_arm_o', None),
        'r_bottle_arm': getattr(agent, '_r_bottle_arm_o', None),
        'ptt': getattr(agent, '_ptt_o', None),
        'yoke_hide': getattr(agent, '_yoke_hide_o', None),
        'autopilot_airspeed': getattr(agent, '_autopilot_airspeed_o', None),
        'com_1_freq': getattr(agent, '_com_1_freq_o', None),
        'wind_direction': getattr(agent, '_wind_direction_o', None),
        'wind_speed': getattr(agent, '_wind_speed_o', None),
        'paused': getattr(agent, '_paused_o', None),
    }


def _push_output_values(output_values):
    """Clear cached values and re-push them through ingescape setters (no drefs)."""
    for key in output_values.keys():
        private_key = '_' + key + '_o'
        if hasattr(agent, private_key):
            delattr(agent, private_key)

    if output_values['airspeed'] is not None: agent.airspeed_o = output_values['airspeed']
    if output_values['pitch'] is not None: agent.pitch_o = output_values['pitch']
    if output_values['control_pitch'] is not None: agent.control_pitch_o = output_values['control_pitch']
    if output_values['roll'] is not None: agent.roll_o = output_values['roll']
    if output_values['control_roll'] is not None: agent.control_roll_o = output_values['control_roll']
    if output_values['heading'] is not None: agent.heading_o = output_values['heading']
    if output_values['control_yaw'] is not None: agent.control_yaw_o = output_values['control_yaw']
    if output_values['vertical_speed'] is not None: agent.vertical_speed_o = output_values['vertical_speed']
    if output_values['altitude'] is not None: agent.altitude_o = output_values['altitude']
    if output_values['latitude'] is not None: agent.latitude_o = output_values['latitude']
    if output_values['longitude'] is not None: agent.longitude_o = output_values['longitude']
    if output_values['control_throttle'] is not None: agent.control_throttle_o = output_values['control_throttle']
    if output_values['control_flaps'] is not None: agent.control_flaps_o = output_values['control_flaps']
    if output_values['control_gear'] is not None: agent.control_gear_o = output_values['control_gear']
    if output_values['control_speedbrakes'] is not None: agent.control_speedbrakes_o = output_values['control_speedbrakes']
    if output_values['outside_event'] is not None: agent.outside_event_o = output_values['outside_event']
    if output_values['park_brake'] is not None: agent.park_brake_o = output_values['park_brake']
    if output_values['l_throttle'] is not None: agent.l_throttle_o = output_values['l_throttle']
    if output_values['r_throttle'] is not None: agent.r_throttle_o = output_values['r_throttle']
    if output_values['n1_match_bug'] is not None: agent.n1_match_bug_o = output_values['n1_match_bug']
    if output_values['e1_n1_percent'] is not None: agent.e1_n1_percent_o = output_values['e1_n1_percent']
    if output_values['e2_n1_percent'] is not None: agent.e2_n1_percent_o = output_values['e2_n1_percent']
    if output_values['slip'] is not None: agent.slip_o = output_values['slip']
    if output_values['engine_fire_l'] is not None: agent.engine_fire_l_o = output_values['engine_fire_l']
    if output_values['engine_fire_r'] is not None: agent.engine_fire_r_o = output_values['engine_fire_r']
    if output_values['pax_safety'] is not None: agent.pax_safety_o = output_values['pax_safety']
    if output_values['master_warning'] is not None: agent.master_warning_o = output_values['master_warning']
    if output_values['master_caution'] is not None: agent.master_caution_o = output_values['master_caution']
    if output_values['flight_director'] is not None: agent.flight_director_o = output_values['flight_director']
    if output_values['speed_mode'] is not None: agent.speed_mode_o = output_values['speed_mode']
    if output_values['heading_mode'] is not None: agent.heading_mode_o = output_values['heading_mode']
    if output_values['fuel_boost_l'] is not None: agent.fuel_boost_l_o = output_values['fuel_boost_l']
    if output_values['fuel_boost_r'] is not None: agent.fuel_boost_r_o = output_values['fuel_boost_r']
    if output_values['test_knob'] is not None: agent.test_knob_o = output_values['test_knob']
    if output_values['autopilot_heading_set'] is not None: agent.autopilot_heading_set_o = output_values['autopilot_heading_set']
    if output_values['yaw_damper'] is not None: agent.yaw_damper_o = output_values['yaw_damper']
    if output_values['l_ign_switch'] is not None: agent.l_ign_switch_o = output_values['l_ign_switch']
    if output_values['r_ign_switch'] is not None: agent.r_ign_switch_o = output_values['r_ign_switch']
    if output_values['l_gen_switch'] is not None: agent.l_gen_switch_o = output_values['l_gen_switch']
    if output_values['r_gen_switch'] is not None: agent.r_gen_switch_o = output_values['r_gen_switch']
    if output_values['transfer_knob'] is not None: agent.transfer_knob_o = output_values['transfer_knob']
    if output_values['baro_setting'] is not None: agent.baro_setting_o = output_values['baro_setting']
    if output_values['cabin_altitude'] is not None: agent.cabin_altitude_o = output_values['cabin_altitude']
    if output_values['l_gen_load'] is not None: agent.l_gen_load_o = output_values['l_gen_load']
    if output_values['r_gen_load'] is not None: agent.r_gen_load_o = output_values['r_gen_load']
    if output_values['pitot_heat'] is not None: agent.pitot_heat_o = output_values['pitot_heat']
    if output_values['l_engine_anti_ice'] is not None: agent.l_engine_anti_ice_o = output_values['l_engine_anti_ice']
    if output_values['r_engine_anti_ice'] is not None: agent.r_engine_anti_ice_o = output_values['r_engine_anti_ice']
    if output_values['l_windshield_anti_ice'] is not None: agent.l_windshield_anti_ice_o = output_values['l_windshield_anti_ice']
    if output_values['r_windshield_anti_ice'] is not None: agent.r_windshield_anti_ice_o = output_values['r_windshield_anti_ice']
    if output_values['exterior_lights'] is not None: agent.exterior_lights_o = output_values['exterior_lights']
    if output_values['anti_coll_lights'] is not None: agent.anti_coll_lights_o = output_values['anti_coll_lights']
    if output_values['trim_rudder'] is not None: agent.trim_rudder_o = output_values['trim_rudder']
    if output_values['elevator_trim'] is not None: agent.elevator_trim_o = output_values['elevator_trim']
    if output_values['aileron_trim'] is not None: agent.aileron_trim_o = output_values['aileron_trim']
    if output_values['fd_pitch_deg'] is not None: agent.fd_pitch_deg_o = output_values['fd_pitch_deg']
    if output_values['alt_sel'] is not None: agent.alt_sel_o = output_values['alt_sel']
    if output_values['heading_sel'] is not None: agent.heading_sel_o = output_values['heading_sel']
    if output_values['l_bottle_arm'] is not None: agent.l_bottle_arm_o = output_values['l_bottle_arm']
    if output_values['r_bottle_arm'] is not None: agent.r_bottle_arm_o = output_values['r_bottle_arm']
    if output_values['ptt'] is not None: agent.ptt_o = output_values['ptt']
    if output_values['yoke_hide'] is not None: agent.yoke_hide_o = output_values['yoke_hide']
    if output_values['autopilot_airspeed'] is not None: agent.autopilot_airspeed_o = output_values['autopilot_airspeed']
    if output_values['com_1_freq'] is not None: agent.com_1_freq_o = output_values['com_1_freq']
    if output_values['wind_direction'] is not None: agent.wind_direction_o = output_values['wind_direction']
    if output_values['wind_speed'] is not None: agent.wind_speed_o = output_values['wind_speed']
    if output_values['paused'] is not None: agent.paused_o = output_values['paused']


def resync_igs_outputs():
    """Resync: force-push current cached values back through ingescape only (no drefs)."""
    _push_output_values(_collect_output_values())


def send_all_outputs():
    """Initialization after reset: send drefs to X-Plane then resync ingescape outputs."""
    print("Initializing all outputs...")
    # Reset X-Plane drefs to known state
    send_dref(speed_brake_dref, 0)
    time.sleep(refresh_rate)
    send_dref(anti_ice_engine_dref, [0, 0, 0, 0, 0, 0, 0, 0])
    time.sleep(refresh_rate)
    send_dref(l_windshield_anti_ice_dref, 0)
    time.sleep(refresh_rate)
    send_dref(r_windshield_anti_ice_dref, 0)
    time.sleep(refresh_rate)
    send_dref(anti_coll_lights_dref, 0)
    time.sleep(refresh_rate)
    send_dref(exterior_lights_dref, 0)
    time.sleep(refresh_rate)
    send_dref(alt_sel_dref, 0)
    time.sleep(refresh_rate)
    send_dref(heading_sel_dref, 0)
    time.sleep(refresh_rate)
    send_dref(pax_safety_dref, 0)
    time.sleep(refresh_rate)
    send_dref(fuel_boost_l_dref, 0)
    time.sleep(refresh_rate)
    send_dref(fuel_boost_r_dref, 0)

    # Store current values
    output_values = _collect_output_values()
    _push_output_values(output_values)
    print("All outputs initialized.")

def main(BirdStrikeEnabled=True):
    global is_interrupted
    global neverDone, reset_time, outputs_initialized
    global _master_warning_active
    global last_full_sync
    global checklist_check_time, checklist_active
    global checklist_last_failures
    while not is_interrupted:
        try:
            while not is_interrupted:
                time.sleep(refresh_rate)

                airspeed, vert_speed, park_brake, mustang_l_throttle, mustang_r_throttle, n1_match_bug, n1_percent, slip, engine_fires, pax_safety, master_warning, master_caution, flight_director, speed_mode, heading_mode, fuel_boost_l, fuel_boost_r, test_knob, autopilot_heading_set, yaw_damper, l_ign_switch, r_ign_switch, l_gen_switch, r_gen_switch, transfer_knob, baro_setting, cabin_altitude, gen_load, pitot_heat, l_windshield_anti_ice, r_windshield_anti_ice, exterior_lights, anti_coll_lights, engine_anti_ice, trim_rudder, alt_sel, heading_sel, l_bottle_arm, r_bottle_arm, yoke_hide, autopilot_airspeed, com_1_freq, altitude_raw, heading_raw, elevator_trim, aileron_trim, fd_pitch_deg, wind_direction, wind_speed, paused = get_drefs([ias_dref, verticalSpeed_dref, parkBrake_dref, mustang_l_throttle_dref, mustang_r_throttle_dref, n1_match_bug_dref, n1_percent_dref, slip_dref, engine_fires_dref, pax_safety_dref, master_warning_dref, master_caution_dref, flight_director_dref, speed_mode_dref, heading_mode_dref, fuel_boost_l_dref, fuel_boost_r_dref, test_knob_dref, heading_sel_dref, yaw_damper_dref, l_ign_switch_dref, r_ign_switch_dref, l_gen_switch_dref, r_gen_switch_dref, transfer_knob_dref, baro_setting_dref, cabin_altitude_dref, gen_load_dref, pitot_heat_dref, l_windshield_anti_ice_dref, r_windshield_anti_ice_dref, exterior_lights_dref, anti_coll_lights_dref, anti_ice_engine_dref, trim_rudder_dref, alt_sel_dref, heading_sel_dref, botle_l_arm_dref, botle_r_arm_dref, yoke_hide_dref, autopilot_airspeed_dref, com_1_freq_dref, altitude_dref, heading_dref, elevator_trim_dref, aileron_trim_dref, fd_pitch_deg_dref, wind_direction_degt_dref, wind_speed_kt_dref, pause_dref])

                agent.airspeed_o = airspeed[0]
                
                #print(f"{airspeed} and {neverDone}")
                if airspeed[0] >= 110 and neverDone and BirdStrikeEnabled:
                    print("Birds incoming ! :)")
                    send_dref(bird_dref, 2)
                    agent.outside_event_o = "birds"
                    neverDone = False
                elif airspeed == 0.0 and not neverDone:
                    neverDone = True

                agent.vertical_speed_o = vert_speed[0]
                agent.park_brake_o = bool(park_brake[0])
                agent.l_throttle_o = mustang_l_throttle[0]
                agent.r_throttle_o = mustang_r_throttle[0]
                agent.n1_match_bug_o = bool(n1_match_bug[0])
                agent.e1_n1_percent_o = n1_percent[0]
                agent.e2_n1_percent_o = n1_percent[1]
                agent.slip_o = slip[0]

                agent.engine_fire_l_o = bool(engine_fires[0])
                agent.engine_fire_r_o = bool(engine_fires[1])

                agent.pax_safety_o = int(pax_safety[0])
                master_warning_bool = bool(master_warning[0])
                agent.master_warning_o = master_warning_bool
                # Start/stop fire alarm bell based on master_warning state
                if _alarm_path is not None:
                    if master_warning_bool and not _master_warning_active:
                        pygame.mixer.music.load(_alarm_path)
                        pygame.mixer.music.play(-1)
                        _master_warning_active = True
                    elif not master_warning_bool and _master_warning_active:
                        pygame.mixer.music.stop()
                        _master_warning_active = False
                agent.master_caution_o = bool(master_caution[0])
                agent.flight_director_o = int(flight_director[0])
                agent.speed_mode_o = int(speed_mode[0])
                agent.heading_mode_o = int(heading_mode[0])
                agent.fuel_boost_l_o = int(fuel_boost_l[0])
                agent.fuel_boost_r_o = int(fuel_boost_r[0])
                agent.test_knob_o = int(test_knob[0])
                agent.autopilot_heading_set_o = int(autopilot_heading_set[0])
                agent.yaw_damper_o = bool(yaw_damper[0])
                time.sleep(0)  # yield GIL — let ingescape heartbeat thread run
                agent.l_ign_switch_o = bool(l_ign_switch[0])
                agent.r_ign_switch_o = bool(r_ign_switch[0])
                agent.l_gen_switch_o = int(l_gen_switch[0])
                agent.r_gen_switch_o = int(r_gen_switch[0])
                agent.l_gen_load_o = int(gen_load[0])
                agent.r_gen_load_o = int(gen_load[1])
                agent.transfer_knob_o = int(transfer_knob[0])
                agent.baro_setting_o = baro_setting[0]
                agent.cabin_altitude_o = cabin_altitude[0]
                agent.pitot_heat_o = bool(pitot_heat[0])
                agent.l_windshield_anti_ice_o = bool(l_windshield_anti_ice[0])
                agent.r_windshield_anti_ice_o = bool(r_windshield_anti_ice[0])
                agent.exterior_lights_o = int(exterior_lights[0])
                agent.anti_coll_lights_o = bool(anti_coll_lights[0])
                agent.l_engine_anti_ice_o = bool(engine_anti_ice[0])
                agent.r_engine_anti_ice_o = bool(engine_anti_ice[1])
                agent.trim_rudder_o = trim_rudder[0]
                agent.elevator_trim_o = elevator_trim[0]
                agent.aileron_trim_o = aileron_trim[0]
                agent.fd_pitch_deg_o = fd_pitch_deg[0]
                agent.alt_sel_o = int(alt_sel[0])
                agent.heading_sel_o = int(heading_sel[0])
                agent.l_bottle_arm_o = bool(l_bottle_arm[0])
                agent.r_bottle_arm_o = bool(r_bottle_arm[0])
                #agent.ptt_o = bool(ptt[0])
                time.sleep(refresh_rate)
                pitch, heading, roll, alt, lat, long = get_position(
                    alt=round(altitude_raw[0], 1),
                    heading=round(heading_raw[0])
                )
                agent.pitch_o = pitch
                agent.heading_o = heading
                agent.roll_o = roll
                agent.altitude_o = alt 
                agent.latitude_o = lat
                agent.longitude_o = long
                agent.yoke_hide_o = bool(yoke_hide[0])
                agent.autopilot_airspeed_o = autopilot_airspeed[0]
                agent.com_1_freq_o = int(com_1_freq[0])
                agent.wind_direction_o = wind_direction[0]
                agent.wind_speed_o = wind_speed[0]
                agent.paused_o = bool(paused[0])

                time.sleep(refresh_rate)
                aileron, elevator, rudder, throttle, gear, flaps, speedbrakes = get_control_inputs()
                agent.control_roll_o = aileron
                agent.control_pitch_o = elevator
                agent.control_yaw_o = rudder
                agent.control_throttle_o = throttle
                agent.control_gear_o = gear
                agent.control_flaps_o = flaps
                agent.control_speedbrakes_o = speedbrakes

                # --- Initial configuration checklist ---
                now_cl = time.time()
                if checklist_check_time is not None and now_cl >= checklist_check_time:
                    checklist_check_time = None
                    failures = _get_checklist_failures()
                    if failures:
                        checklist_last_failures = failures
                        _checklist_queue.put({"type": "show", "failures": failures})
                        if not paused[0]:
                            send_comm(pause_toggle_comm)
                        checklist_active = True
                    else:
                        print("[CHECKLIST] Initial config OK - no pause needed")
                if checklist_active:
                    failures = _get_checklist_failures()
                    if failures != checklist_last_failures:
                        checklist_last_failures = failures
                        _checklist_queue.put({"type": "show", "failures": failures})
                    if not failures:
                        _checklist_queue.put({"type": "hide"})
                        send_comm(pause_toggle_comm)
                        checklist_active = False
                        checklist_last_failures = set()

                # Check if 2 seconds have passed since reset and outputs need initialization
                if reset_time is not None and not outputs_initialized:
                    elapsed_time = time.time() - reset_time
                    if elapsed_time >= 1.0:
                        send_all_outputs()
                        outputs_initialized = True
                        reset_time = None  # Clear reset time

                # Periodic full resync every FULL_SYNC_INTERVAL seconds (ingescape only, no drefs)
                now = time.time()
                if now - last_full_sync >= FULL_SYNC_INTERVAL:
                    print("[SYNC] Periodic full output resync")
                    resync_igs_outputs()
                    if yoke_hide[0] == 0:
                        send_dref(yoke_hide_dref, 1)
                    last_full_sync = now
        except BaseException as e:
            print(f"[ERROR] An error occurred: {type(e).__name__}: {e}")
            traceback.print_exc()
            if isinstance(e, (KeyboardInterrupt, SystemExit)):
                print("[SHUTDOWN] KeyboardInterrupt/SystemExit caught - stopping agent.")
                break
            print("Retrying in 3 seconds...")
            time.sleep(3)
    print("[SHUTDOWN] Main loop exited. is_interrupted =", is_interrupted)
    _checklist_queue.put({"type": "quit"})

_checklist_win = ChecklistWindow()
_main_thread = threading.Thread(target=main, daemon=True, name="aircraft-main")
_main_thread.start()
_checklist_win.run()   # Blocks the main thread in the tkinter event loop
_main_thread.join(timeout=3)
print("[SHUTDOWN] Stopping ingescape agent...")
igs.stop()
print("[SHUTDOWN] Agent stopped.")
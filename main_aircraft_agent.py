#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Aircraft version 1.0
#  Created by Ingenuity i/o on 2025/02/25
#

import sys
import ingescape as igs
from echo_aircraft_agent import *
import time
import xpc
import signal
from collections import Counter
from joystick_handler import JoystickHandler

neverDone = True

## def datarefs string
ptt_dref = "sim/cockpit2/controls/tailwheel_lock_ratio" # function as a dummy ptt for now
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
botle_r_arm_dref = "Mustang/cockpit/bottle_r_arm_b" # 0 is off, 1 is on
botle_l_arm_dref = "Mustang/cockpit/bottle_l_arm_b" # 0 is off, 1 is on
l_cutoff_dref = "Mustang/cockpit/engine/l_cutoff"
r_cutoff_dref = "Mustang/cockpit/engine/r_cutoff"
yoke_hide_dref = "Mustang/cockpit/yoke_hide" # 0 is show, 1 is hide
speed_brake_dref = "sim/cockpit2/controls/speedbrake_ratio"
autopilot_airspeed_dref = "sim/cockpit/autopilot/airspeed" # airspeed set in the autopilot

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

refresh_rate = 0.01
port = 5670
agent_name = "Aircraft"
device = "A7500_NETGEAR"
verbose = False
is_interrupted = False
start_heading = None
joystick_handler = None  # Global joystick handler instance
reset_time = None  # Track when reset was triggered
outputs_initialized = False  # Track if outputs have been sent after reset

def signal_handler(signal_received, frame):
    global is_interrupted, joystick_handler
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True
    # Stop joystick monitoring on exit
    if joystick_handler:
        joystick_handler.stop()

def on_agent_event_callback(event, uuid, name, event_data, my_data):
    agent_object = my_data
    assert isinstance(agent_object, Echo)
    # add code here if needed

def on_freeze_callback(is_frozen, my_data):
    agent_object = my_data
    assert isinstance(agent_object, Echo)
    # add code here if needed

def bool_input_callback(io_type, name, value_type, value, my_data):
    if name == "yaw_damper":
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
    elif name == "l_bottle_arm":
        send_dref(botle_l_arm_dref, int(value))
    elif name == "r_bottle_arm":
        send_dref(botle_r_arm_dref, int(value))
    elif name == "yoke_hide":
        send_dref(yoke_hide_dref, int(value))

def double_input_callback(io_type, name, value_type, value, my_data):
    if name == "elevator":
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

def int_input_callback(io_type, name, value_type, value, my_data):
    if name == "test_knob":
        send_dref(test_knob_dref, value)
    elif name == "l_gen_switch":
        send_dref(l_gen_switch_dref, value)
    elif name == "r_gen_switch":
        send_dref(r_gen_switch_dref, value)
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
        send_dref(pax_safety_dref, value)
    elif name == "exterior_lights":
        send_dref(exterior_lights_dref, value)
        
def impulsion_input_callback(io_type, name, value_type, value, my_data):
    global neverDone, reset_time, outputs_initialized
    if name == "reset":
        print("Resetting simulation...")
        neverDone = True
        agent.outside_event_o = "RESET"
        send_comm(load_situation_1_comm)
        reset_time = time.time()  # Record the time of reset
        outputs_initialized = False  # Mark that outputs need to be re-initialized

    elif name == "gear":
        current_val = get_control_inputs()[4]
        print(f"current val = {current_val}")
        if current_val == 1: set_control_inputs("gear", 0)
        else:
            set_control_inputs("gear", 1)
        pass
    elif name == "brake":
        current_val = get_dref(parkBrake_dref)
        print(f"current val = {current_val}")
        if current_val[0] == 1: send_dref(parkBrake_dref, 0)
        else: send_dref(parkBrake_dref, 1)
    elif name == "bird_strike":
        send_dref(bird_dref, 2)
        print("Birds incoming ! :)")
        agent.outside_event_o = "birds"
    elif name == "flight_director":
        send_comm(flight_director_comm)
    elif name == "heading_mode":
        send_comm(heading_mode_comm)
    elif name == "speed_mode":
        send_comm(speed_mode_comm)
    elif name == "heading_mode":
        send_comm(heading_mode_comm)
    elif name == "autopilot_master":
        send_comm(autopilot_master_comm)
    elif name == "nose_down":
        send_comm(vertical_speed_down_comm)
    elif name == "nose_up":
        send_comm(vertical_speed_up_comm)

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
    
def get_position():
    try:
        # get position
        with xpc.XPlaneConnect() as client:
            posi = client.getPOSI()
            lat = round(posi[0], 6)  # Latitude
            long = round(posi[1], 6)  # Longitude
            time.sleep(refresh_rate)
            alt = get_dref(altitude_dref)  # Altitude
            alt = round(alt[0], 1)  # Altitude
            pitch = round(posi[3], 2)  # Pitch
            roll = round(posi[4], 2)  # Roll
            time.sleep(refresh_rate)
            heading = get_dref(heading_dref)  # Heading
            heading = round(heading[0], None)  # Heading
    except Exception as e:
        print(f"Error getting position: {e}")
        pitch, roll, heading, alt, lat, long = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
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

igs.input_create("reset", igs.IMPULSION_T, None)
igs.input_create("elevator", igs.DOUBLE_T, None)
igs.input_create("rudder", igs.DOUBLE_T, None)
igs.input_create("aileron", igs.DOUBLE_T, None)
igs.input_create("throttle", igs.DOUBLE_T, None)
igs.input_create("flaps", igs.DOUBLE_T, None)
igs.input_create("gear", igs.IMPULSION_T, None)
igs.input_create("brake", igs.IMPULSION_T, None)
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
igs.input_create("trim_rudder", igs.DOUBLE_T, None)
igs.input_create("l_bottle_arm", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("r_bottle_arm", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.input_create("yoke_hide", igs.BOOL_T, None)  # 0 is show, 1 is hide
igs.input_create("nose_down", igs.IMPULSION_T, None)
igs.input_create("nose_up", igs.IMPULSION_T, None)

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
igs.output_create("alt_sel", igs.INTEGER_T, None)
igs.output_create("heading_sel", igs.INTEGER_T, None)
igs.output_create("l_bottle_arm", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("r_bottle_arm", igs.BOOL_T, None)  # 0 is off, 1 is on
igs.output_create("ptt", igs.BOOL_T, None)  # Push-to-talk button
igs.output_create("yoke_hide", igs.BOOL_T, None)  # 0 is show, 1 is hide
igs.output_create("autopilot_airspeed", igs.DOUBLE_T, None)  # airspeed set in the autopilot

igs.observe_input("reset", impulsion_input_callback, None)
igs.observe_input("elevator", double_input_callback, None)
igs.observe_input("rudder", double_input_callback, None)
igs.observe_input("aileron", double_input_callback, None)
igs.observe_input("throttle", double_input_callback, None)
igs.observe_input("flaps", double_input_callback, None)
igs.observe_input("gear", impulsion_input_callback, None)
igs.observe_input("brake", impulsion_input_callback, None)
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
igs.observe_input("trim_rudder", double_input_callback, None)
igs.observe_input("alt_sel", int_input_callback, None)
igs.observe_input("heading_sel", int_input_callback, None)
igs.observe_input("l_bottle_arm", bool_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("r_bottle_arm", bool_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("yoke_hide", bool_input_callback, None)  # 0 is show, 1 is hide
igs.observe_input("nose_down", impulsion_input_callback, None)
igs.observe_input("nose_up", impulsion_input_callback, None)

igs.log_set_console(True)
igs.log_set_console_level(igs.LOG_INFO)

igs.start_with_device(device, port)
# catch SIGINT handler after starting agent
signal.signal(signal.SIGINT, signal_handler)

# ============= Joystick Integration =============
def on_joystick_trigger_press():
    """Called when joystick trigger is pressed."""
    print("Joystick trigger pressed - PTT activated")
    # You can add custom actions here, for example:
    send_dref(ptt_dref, 1)  # Activate PTT
    # Or trigger any other X-Plane action

def on_joystick_trigger_release():
    """Called when joystick trigger is released."""
    print("Joystick trigger released - PTT deactivated")
    # You can add custom actions here, for example:
# Initialize and start joystick monitoring
joystick_handler = JoystickHandler(joystick_index=0, polling_rate=0.01)
if joystick_handler.initialize():
    # Register button callbacks
    joystick_handler.register_button_press(0, on_joystick_trigger_press)      # Trigger button
    joystick_handler.register_button_release(0, on_joystick_trigger_release)  # Trigger release
    # Start monitoring in background thread
    joystick_handler.start()
    print("Joystick integration enabled and running in parallel with X-Plane control.")
else:
    print("Joystick not available - continuing without joystick integration.")
    joystick_handler = None
# ============= End Joystick Integration =============


def send_all_outputs():
    """Send all current output values to initialize the airplane state."""
    print("Initializing all outputs...")
    # Force all outputs to be sent by clearing the cached values and re-assigning
    # This bypasses the equality check in the setters
    send_dref(speed_brake_dref, 0)  # Ensure speedbrakes are re-initialized
    time.sleep(refresh_rate)
    #send_dref(pitot_heat_dref, 0)  # Ensure pitot heat is re-initialized
    time.sleep(refresh_rate)
    send_dref(anti_ice_engine_dref, [0, 0, 0, 0, 0, 0, 0, 0])  # Ensure anti-ice is re-initialized
    time.sleep(refresh_rate)
    send_dref(l_windshield_anti_ice_dref, 0)  # Ensure windshield anti-ice is re-initialized
    time.sleep(refresh_rate)
    send_dref(r_windshield_anti_ice_dref, 0)  # Ensure windshield anti-ice is re-initialized
    time.sleep(refresh_rate)
    send_dref(anti_coll_lights_dref, 0)  # Ensure anti-collision lights are re-initialized
    time.sleep(refresh_rate)
    send_dref(exterior_lights_dref, 0)  # Ensure exterior lights are re-initialized
    time.sleep(refresh_rate)
    
    
    # Store current values
    output_values = {
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
        'alt_sel': getattr(agent, '_alt_sel_o', None),
        'heading_sel': getattr(agent, '_heading_sel_o', None),
        'l_bottle_arm': getattr(agent, '_l_bottle_arm_o', None),
        'r_bottle_arm': getattr(agent, '_r_bottle_arm_o', None),
        'ptt': getattr(agent, '_ptt_o', None),
        'yoke_hide': getattr(agent, '_yoke_hide_o', None),
        'autopilot_airspeed': getattr(agent, '_autopilot_airspeed_o', None),
    }
    
    # Clear all cached values to force setters to send
    for key in output_values.keys():
        private_key = '_' + key + '_o'
        if hasattr(agent, private_key):
            delattr(agent, private_key)
    
    # Re-assign all values, which will trigger the setters to send
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
    if output_values['alt_sel'] is not None: agent.alt_sel_o = output_values['alt_sel']
    if output_values['heading_sel'] is not None: agent.heading_sel_o = output_values['heading_sel']
    if output_values['l_bottle_arm'] is not None: agent.l_bottle_arm_o = output_values['l_bottle_arm']
    if output_values['r_bottle_arm'] is not None: agent.r_bottle_arm_o = output_values['r_bottle_arm']
    if output_values['ptt'] is not None: agent.ptt_o = output_values['ptt']
    if output_values['yoke_hide'] is not None: agent.yoke_hide_o = output_values['yoke_hide']
    if output_values['autopilot_airspeed'] is not None: agent.autopilot_airspeed_o = output_values['autopilot_airspeed']
    
    print("All outputs initialized.")

def main(BirdStrikeEnabled=True):
    global is_interrupted
    global neverDone, reset_time, outputs_initialized
    while not is_interrupted:
        try:
            while not is_interrupted:
                time.sleep(refresh_rate)

                airspeed, vert_speed, park_brake, mustang_l_throttle, mustang_r_throttle, n1_match_bug, n1_percent, slip, engine_fires, pax_safety, master_warning, master_caution, flight_director, speed_mode, heading_mode, fuel_boost_l, fuel_boost_r, test_knob, autopilot_heading_set, yaw_damper, l_ign_switch, r_ign_switch, l_gen_switch, r_gen_switch, transfer_knob, baro_setting, cabin_altitude, gen_load, pitot_heat, l_windshield_anti_ice, r_windshield_anti_ice, exterior_lights, anti_coll_lights, engine_anti_ice, trim_rudder, alt_sel, heading_sel, l_bottle_arm, r_bottle_arm, ptt, yoke_hide, autopilot_airspeed = get_drefs([ias_dref, verticalSpeed_dref, parkBrake_dref, mustang_l_throttle_dref, mustang_r_throttle_dref, n1_match_bug_dref, n1_percent_dref, slip_dref, engine_fires_dref, pax_safety_dref, master_warning_dref, master_caution_dref, flight_director_dref, speed_mode_dref, heading_mode_dref, fuel_boost_l_dref, fuel_boost_r_dref, test_knob_dref, heading_sel_dref, yaw_damper_dref, l_ign_switch_dref, r_ign_switch_dref, l_gen_switch_dref, r_gen_switch_dref, transfer_knob_dref, baro_setting_dref, cabin_altitude_dref, gen_load_dref, pitot_heat_dref, l_windshield_anti_ice_dref, r_windshield_anti_ice_dref, exterior_lights_dref, anti_coll_lights_dref, anti_ice_engine_dref, trim_rudder_dref, alt_sel_dref, heading_sel_dref, botle_l_arm_dref, botle_r_arm_dref, ptt_dref, yoke_hide_dref, autopilot_airspeed_dref])

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
                agent.master_warning_o = bool(master_warning[0])
                agent.master_caution_o = bool(master_caution[0])
                agent.flight_director_o = int(flight_director[0])
                agent.speed_mode_o = int(speed_mode[0])
                agent.heading_mode_o = int(heading_mode[0])
                agent.fuel_boost_l_o = int(fuel_boost_l[0])
                agent.fuel_boost_r_o = int(fuel_boost_r[0])
                agent.test_knob_o = int(test_knob[0])
                agent.autopilot_heading_set_o = int(autopilot_heading_set[0])
                agent.yaw_damper_o = bool(yaw_damper[0])
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
                agent.alt_sel_o = int(alt_sel[0])
                agent.heading_sel_o = int(heading_sel[0])
                agent.l_bottle_arm_o = bool(l_bottle_arm[0])
                agent.r_bottle_arm_o = bool(r_bottle_arm[0])
                agent.ptt_o = bool(ptt[0])
                time.sleep(refresh_rate)
                pitch, heading, roll, alt, lat, long = get_position()
                agent.pitch_o = pitch
                agent.heading_o = heading
                agent.roll_o = roll
                agent.altitude_o = alt 
                agent.latitude_o = lat
                agent.longitude_o = long
                agent.yoke_hide_o = bool(yoke_hide[0])
                agent.autopilot_airspeed_o = autopilot_airspeed[0]

                time.sleep(refresh_rate)
                aileron, elevator, rudder, throttle, gear, flaps, speedbrakes = get_control_inputs()
                agent.control_roll_o = aileron
                agent.control_pitch_o = elevator
                agent.control_yaw_o = rudder
                agent.control_throttle_o = throttle
                agent.control_gear_o = gear
                agent.control_flaps_o = flaps
                agent.control_speedbrakes_o = speedbrakes
                
                # Check if 2 seconds have passed since reset and outputs need initialization
                if reset_time is not None and not outputs_initialized:
                    elapsed_time = time.time() - reset_time
                    if elapsed_time >= 1.0:
                        send_all_outputs()
                        outputs_initialized = True
                        reset_time = None  # Clear reset time
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying in 3 seconds...")
            time.sleep(3)

main()
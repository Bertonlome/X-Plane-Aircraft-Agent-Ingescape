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

## def datarefs string
ias_dref = "sim/cockpit2/gauges/indicators/airspeed_kts_pilot"
pitch_dref = "sim/cockpit2/gauges/indicators/pitch_AHARS_deg_pilot"
altitude_dref = "sim/cockpit2/gauges/indicators/altitude_ft_pilot"
thrust_dref = "sim/cockpit2/engine/actuators/throttle_jet_rev_ratio_all"
heading_dref = "sim/cockpit2/gauges/indicators/heading_AHARS_deg_mag_pilot" # 0 to 1, override because it is a double instead of an array
roll_dref = "sim/cockpit2/gauges/indicators/roll_AHARS_deg_pilot"
parkBrake_dref = "sim/cockpit2/controls/parking_brake_ratio"
verticalSpeed_dref = "sim/cockpit2/gauges/indicators/vvi_fpm_pilot"
rudder_dref = "sim/cockpit2/controls/yoke_heading_ratio"
elevator_dref = "sim/cockpit2/controls/yoke_pitch_ratio"
aileron_dref = "sim/cockpit2/controls/yoke_roll_ratio"
mustang_l_throttle_dref = "Mustang/cockpit/engine/l_throttle"
mustang_r_throttle_dref = "Mustang/cockpit/engine/r_throttle"
flaps_dref = "sim/cockpit2/controls/flap_ratio"
gear_dref = "sim/cockpit/switches/gear_handle_status"
bird_dref = "sim/operation/failures/rel_bird_strike"
cas_dref = "sim/cockpit2/gauges/indicators/cas_kts_pilot"
n1_match_bug_dref = "sim/cockpit/warnings/annunciators/N1_high" #[1,1,0,0,0,0,0,0] first two means E1 and E2 N1 match, last six are for the other engines
n1_percent_dref = "sim/cockpit2/engine/indicators/N1_percent" # [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] first two means E1 and E2 N1 percent, last four are for the other engines max for the mustang is 91,27388 when toga is engaged static on the runway
slip_dref = "sim/cockpit2/gauges/indicators/slip_deg" #positive is right, negative is left
engine_fires_dref = "sim/cockpit/warnings/annunciators/engine_fires" # [0, 0] first means E1, second means E2
generators_off_dref = "sim/cockpit/warnings/annunciators/generator_off" # [0, 0] first means L generator, second means R generator
pax_safety_dref = "Mustang/cockpit/pax_safety" # 0 is off, 1 is on
trim_rudder_dref = "sim/cockpit2/controls/rudder_trim"
master_warning_dref = "Mustang/master_warning" #readonly 0 is off, 1 is on
master_caution_dref = "Mustang/master_caution" #readonly 0 is off, 1 is on
flight_director_dref = "sim/cockpit2/autopilot/flight_director_mode" # Not sure how to set FD up using a comm
speed_mode_dref = "Mustang/airspeedmach"
heading_mode_dref = "sim/cockpit/autopilot/heading_mode"
autopilot_master_dref = "sim/cockpit/autopilot/autopilot_mode" # 0 is off, 1 is FD 2 is AP + FD
bottle_l_discharge_dref = "Mustang/cockpit/bottle_l_arm_b" # 0 is off, 1 is on
bottle_r_discharge_dref = "Mustang/cockpit/bottle_r_arm_b" # 0 is off, 1 is on
fuel_boost_l_dref = "Mustang/cockpit/fuel/boost_l" # 0 is off, 1 is on
fuel_boost_r_dref = "Mustang/cockpit/fuel/boost_r" # 0 is off, 1 is on
test_knob_dref = "Mustang/cockpit/test_knob" # 0 to 11 for each test position
autopilot_heading_set_dref = "sim/cockpit/autopilot/heading" # 0 to 360
autopilot_state_dref = "sim/cockpit/autopilot/autopilot_state" #need to understand this seems to be an integer that represents the state of the autopilot
yaw_damper_dref = "sim/cockpit/switches/yaw_damper_on" # 0 is off, 1 is on
l_ign_switch_dref = "Mustang/igniter_l" # 0 is off, 1 is on
r_ign_switch_dref = "Mustang/igniter_r" # 0 is off, 1 is on
l_gen_switch_dref = "Mustang/cockpit/electrical/l_gen_switch" # 0 is reset, 1 is off 2 is on
r_gen_switch_dref = "Mustang/cockpit/electrical/r_gen_switch" # 0 is reset, 1 is off 2 is on
transfer_knob_dref = "Mustang/cockpit/fuel/transfer_knob" # 0 is left, 1 is off 2 is right
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
device = "wlo1"
verbose = False
is_interrupted = False
start_heading = None

def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True

def on_agent_event_callback(event, uuid, name, event_data, my_data):
    agent_object = my_data
    assert isinstance(agent_object, Echo)
    # add code here if needed

def on_freeze_callback(is_frozen, my_data):
    agent_object = my_data
    assert isinstance(agent_object, Echo)
    # add code here if needed

def double_input_callback(io_type, name, value_type, value, my_data):
        if name == "elevator":
            set_control_inputs("elevator", value)
        elif name == "rudder":
            set_control_inputs("rudder", value)
        elif name == "aileron":
            set_control_inputs("aileron", value)
        elif name == "throttle":
            print("Throttle value is: ", value)
            #client.sendDREFs([mustang_l_throttle, mustang_r_throttle], [1,1])
            set_control_inputs("thrust", value)
        elif name == "flaps":
            set_control_inputs("flaps", value)

def int_input_callback(io_type, name, value_type, value, my_data):
    agent_object = my_data
    assert isinstance(agent_object, Echo)
    with xpc.XPlaneConnect() as client:
        if name == "flaps":
            pass
            #dref tbd

def impulsion_input_callback(io_type, name, value_type, value, my_data):
        if name == "gear":
            current_val = get_control_inputs()[4]
            print(f"current val = {current_val}")
            if current_val == 1: set_control_inputs("gear", 0)
            #else:
            pass
        elif name == "brake":
            current_val = get_dref(parkBrake_dref)
            print(f"current val = {current_val}")
            if current_val == 1: send_dref(parkBrake_dref,0)
            else: send_dref(parkBrake_dref, 1)
        elif name == "bird_strike":
            send_dref(bird_dref, 2)
            print("Birds incoming ! :)")
            agent.outside_event_o = "birds"

def get_dref(arg, is_double=False):
    try:
        with xpc.XPlaneConnect() as client: 
            #get a dref 
            dref = arg
            myValue = client.getDREF(dref)  
            rounded_value = round(myValue[0], 1)    
    except Exception as e:
        print(f"Error getting dref {arg}: {e}")
        rounded_value = 0.0  # Default value in case of error
    return rounded_value

def get_drefs(args):
    try:
        with xpc.XPlaneConnect() as client:
            myValues = client.getDREFs(args)
            rounded_values = []
            for value in myValues:
                if isinstance(value, (list, tuple)):
                    # Take the first element or handle as needed
                    rounded_values.append(round(value[0], 1) if value else 0.0)
                else:
                    rounded_values.append(round(value, 1))
    except Exception as e:
        print(f"Error getting drefs {args}: {e}")
        rounded_values = [0.0] * len(args)
    return rounded_values

def send_dref(arg, value):
    try:
        with xpc.XPlaneConnect() as client:
            # send a dref
            dref = arg
            myValue = value
            client.sendDREFs([dref], [myValue])
    except Exception as e:
        print(f"Error sending dref {arg}: {e}")

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
                client.sendCTRL(value, None, None, None, None, None, None)
            elif name == "rudder":
                client.sendCTRL(None, value, None, None, None, None, None)
            elif name == "aileron":
                client.sendCTRL(None, None, value, None, None, None, None)
            elif name == "throttle":
                client.sendCTRL(None, None, None, value, None, None, None)
            elif name == "flaps":
                client.sendCTRL(None, None, None, None, value, None, None)
            elif name == "gear":
                client.sendCTRL(None, None, None, None, None, value, None)
            elif name == "brake":
                client.sendCTRL(None, None, None, None, None, None, value)
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
            pitch = round(posi[3], 2)  # Pitch
            roll = round(posi[4], 2)  # Roll
            time.sleep(refresh_rate)
            heading = round(get_dref(heading_dref), None)  # Heading
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

igs.input_create("elevator", igs.DOUBLE_T, None)
igs.input_create("rudder", igs.DOUBLE_T, None)
igs.input_create("aileron", igs.DOUBLE_T, None)
igs.input_create("throttle", igs.DOUBLE_T, None)
igs.input_create("flaps", igs.DOUBLE_T, None)
igs.input_create("gear", igs.IMPULSION_T, None)
igs.input_create("brake", igs.IMPULSION_T, None)
igs.input_create("l_throttle", igs.DOUBLE_T, None)
igs.input_create("r_throttle", igs.DOUBLE_T, None)
igs.input_create("pax_safety", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.input_create("flight_director", igs.DOUBLE_T, None)  # Not sure how to set FD up using a comm
igs.input_create("speed_mode", igs.DOUBLE_T, None)  # Mustang/airspeedmach
igs.input_create("heading_mode", igs.DOUBLE_T, None)  # Mustang/heading
igs.input_create("autopilot_master", igs.DOUBLE_T, None)  # 0 is off, 1 is FD 2 is AP + FD
igs.input_create("fuel_boost_l", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.input_create("fuel_boost_r", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.input_create("test_knob", igs.DOUBLE_T, None)  # 0 to 11 for each test position
igs.input_create("autopilot_heading_set", igs.DOUBLE_T, None)  # 0 to 360
igs.input_create("autopilot_state", igs.DOUBLE_T, None)  # need to understand this seems to be an integer that represents the state of the autopilot
igs.input_create("yaw_damper", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.input_create("l_ign_switch", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.input_create("r_ign_switch", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.input_create("l_gen_switch", igs.DOUBLE_T, None)  # 0 is reset, 1 is off 2 is on
igs.input_create("r_gen_switch", igs.DOUBLE_T, None)  # 0 is reset, 1 is off 2 is on
igs.input_create("transfer_knob", igs.DOUBLE_T, None)  # 0 is left, 1 is off 2 is right
igs.input_create("bird_strike", igs.IMPULSION_T, None)

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
igs.output_create("parkBrake", igs.DOUBLE_T, None)
igs.output_create("l_throttle", igs.DOUBLE_T, None)
igs.output_create("r_throttle", igs.DOUBLE_T, None)
igs.output_create("cas", igs.DOUBLE_T, None)
igs.output_create("n1_match_bug", igs.DOUBLE_T, None)  # [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
igs.output_create("n1_percent", igs.DOUBLE_T, None)  # [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
igs.output_create("slip", igs.DOUBLE_T, None)  # positive is right, negative is left
igs.output_create("engine_fires", igs.DOUBLE_T, None)  # [0, 0] first means E1, second means E2
igs.output_create("generators_off", igs.DOUBLE_T, None)  # [0, 0] first means L generator, second means R generator
igs.output_create("pax_safety", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.output_create("master_warning", igs.DOUBLE_T, None)  # readonly 0 is off, 1 is on
igs.output_create("master_caution", igs.DOUBLE_T, None)  # readonly 0 is off, 1 is on
igs.output_create("flight_director", igs.DOUBLE_T, None)  # Not sure how to set FD up using a comm
igs.output_create("speed_mode", igs.DOUBLE_T, None)  # Mustang/airspeedmach
igs.output_create("heading_mode", igs.DOUBLE_T, None)  # Mustang/heading
igs.output_create("autopilot_master", igs.DOUBLE_T, None)  # 0 is off, 1 is FD 2 is AP + FD
igs.output_create("fuel_boost_l", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.output_create("fuel_boost_r", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.output_create("test_knob", igs.DOUBLE_T, None)  # 0 to 11 for each test position
igs.output_create("autopilot_heading_set", igs.DOUBLE_T, None)  # 0 to 360
igs.output_create("autopilot_state", igs.DOUBLE_T, None)  # need to understand this seems to be an integer that represents the state of the autopilot
igs.output_create("yaw_damper", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.output_create("l_ign_switch", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.output_create("r_ign_switch", igs.DOUBLE_T, None)  # 0 is off, 1 is on
igs.output_create("l_gen_switch", igs.DOUBLE_T, None)  # 0 is reset, 1 is off 2 is on
igs.output_create("r_gen_switch", igs.DOUBLE_T, None)  # 0 is reset, 1 is off 2 is on
igs.output_create("transfer_knob", igs.DOUBLE_T, None)  # 0 is left, 1 is off 2 is right

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
igs.observe_input("pax_safety", double_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("flight_director", double_input_callback, None)  # Not sure how to set FD up using a comm
igs.observe_input("speed_mode", double_input_callback, None)  # Mustang/airspeedmach
igs.observe_input("heading_mode", double_input_callback, None)  # Mustang/heading
igs.observe_input("autopilot_master", double_input_callback, None)  # 0 is off, 1 is FD 2 is AP + FD
igs.observe_input("fuel_boost_l", double_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("fuel_boost_r", double_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("test_knob", double_input_callback, None)  # 0 to 11 for each test position
igs.observe_input("autopilot_heading_set", double_input_callback, None)  # 0 to 360
igs.observe_input("autopilot_state", double_input_callback, None)  # need to understand this seems to be an integer that represents the state of the autopilot
igs.observe_input("yaw_damper", double_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("l_ign_switch", double_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("r_ign_switch", double_input_callback, None)  # 0 is off, 1 is on
igs.observe_input("l_gen_switch", double_input_callback, None)  # 0 is reset, 1 is off 2 is on
igs.observe_input("r_gen_switch", double_input_callback, None)  # 0 is reset, 1 is off 2 is on
igs.observe_input("transfer_knob", double_input_callback, None)

igs.log_set_console(True)
igs.log_set_console_level(igs.LOG_INFO)

igs.start_with_device(device, port)
# catch SIGINT handler after starting agent
signal.signal(signal.SIGINT, signal_handler)

def main():
    global is_interrupted
    neverDone = True
    while not is_interrupted:
        try:
            while not is_interrupted:
                time.sleep(refresh_rate)
                
                airspeed, vert_speed, park_brake, mustang_l_throttle, mustang_r_throttle, n1_match_bug, n1_percent, slip, engine_fires, generators_off, pax_safety, master_warning, master_caution, flight_director, speed_mode, heading_mode, autopilot_master, fuel_boost_l, fuel_boost_r, test_knob, autopilot_heading_set, autopilot_state, yaw_damper, l_ign_switch, r_ign_switch, l_gen_switch, r_gen_switch, transfer_knob = get_drefs([ias_dref, verticalSpeed_dref, parkBrake_dref, mustang_l_throttle_dref, mustang_r_throttle_dref, n1_match_bug_dref, n1_percent_dref, slip_dref, engine_fires_dref, generators_off_dref, pax_safety_dref, master_warning_dref, master_caution_dref, flight_director_dref, speed_mode_dref, heading_mode_dref, autopilot_master_dref, fuel_boost_l_dref, fuel_boost_r_dref, test_knob_dref, autopilot_heading_set_dref, autopilot_state_dref, yaw_damper_dref, l_ign_switch_dref, r_ign_switch_dref, l_gen_switch_dref, r_gen_switch_dref, transfer_knob_dref])
                
                agent.airspeed_o = airspeed
                
                #print(f"{airspeed} and {neverDone}")
                if airspeed >= 110 and neverDone:
                    print("Birds incoming ! :)")
                    send_dref(bird_dref, 2)
                    agent.outside_event_o = "birds"
                    neverDone = False
                elif airspeed == 0.0 and not neverDone:
                    neverDone = True

                agent.vertical_speed_o = vert_speed
                agent.park_brake_o = park_brake
                agent.l_throttle_o = mustang_l_throttle
                agent.r_throttle_o = mustang_r_throttle
                agent.n1_match_bug_o = n1_match_bug
                agent.n1_percent_o = n1_percent
                agent.slip_o = slip
                agent.engine_fires_o = engine_fires
                agent.generators_off_o = generators_off
                agent.pax_safety_o = pax_safety
                agent.master_warning_o = master_warning
                agent.master_caution_o = master_caution
                agent.flight_director_o = flight_director
                agent.speed_mode_o = speed_mode
                agent.heading_mode_o = heading_mode
                agent.autopilot_master_o = autopilot_master
                agent.fuel_boost_l_o = fuel_boost_l
                agent.fuel_boost_r_o = fuel_boost_r
                agent.test_knob_o = test_knob
                agent.autopilot_heading_set_o = autopilot_heading_set
                agent.autopilot_state_o = autopilot_state
                agent.yaw_damper_o = yaw_damper
                agent.l_ign_switch_o = l_ign_switch
                agent.r_ign_switch_o = r_ign_switch
                agent.l_gen_switch_o = l_gen_switch
                agent.r_gen_switch_o = r_gen_switch
                agent.transfer_knob_o = transfer_knob
                
                """
                airspeed = get_dref(ias_dref)
                agent.airspeed_o = airspeed
                time.sleep(refresh_rate)
                vert_speed = get_dref(verticalSpeed_dref)
                agent.vertical_speed_o = vert_speed 
                time.sleep(refresh_rate)
                park_brake = get_dref(parkBrake_dref)
                agent.park_brake_o = park_brake
                time.sleep(refresh_rate)
                mustang_l_throttle = get_dref(mustang_l_throttle_dref)
                agent.l_throttle_o = mustang_l_throttle
                time.sleep(refresh_rate)
                mustang_r_throttle = get_dref(mustang_r_throttle_dref)
                agent.r_throttle_o = mustang_r_throttle
                #time.sleep(refresh_rate)
                #cas = get_dref(cas_dref)
                #agent.cas_o = cas
                time.sleep(refresh_rate)
                n1_match_bug = get_dref(n1_match_bug_dref)
                agent.n1_match_bug_o = n1_match_bug
                time.sleep(refresh_rate)
                n1_percent = get_dref(n1_percent_dref)
                agent.n1_percent_o = n1_percent
                time.sleep(refresh_rate)
                slip = get_dref(slip_dref)
                agent.slip_o = slip
                time.sleep(refresh_rate)
                engine_fires = get_dref(engine_fires_dref)
                agent.engine_fires_o = engine_fires
                time.sleep(refresh_rate)
                generators_off = get_dref(generators_off_dref)
                agent.generators_off_o = generators_off
                time.sleep(refresh_rate)
                pax_safety = get_dref(pax_safety_dref)
                agent.pax_safety_o = pax_safety
                time.sleep(refresh_rate)
                master_warning = get_dref(master_warning_dref)
                agent.master_warning_o = master_warning
                time.sleep(refresh_rate)
                master_caution = get_dref(master_caution_dref)
                agent.master_caution_o = master_caution
                time.sleep(refresh_rate)
                flight_director = get_dref(flight_director_dref)
                agent.flight_director_o = flight_director
                time.sleep(refresh_rate)
                speed_mode = get_dref(speed_mode_dref)
                agent.speed_mode_o = speed_mode
                time.sleep(refresh_rate)
                heading_mode = get_dref(heading_mode_dref)
                agent.heading_mode_o = heading_mode
                time.sleep(refresh_rate)
                autopilot_master = get_dref(autopilot_master_dref)
                agent.autopilot_master_o = autopilot_master
                time.sleep(refresh_rate)
                fuel_boost_l = get_dref(fuel_boost_l_dref)
                agent.fuel_boost_l_o = fuel_boost_l
                time.sleep(refresh_rate)
                fuel_boost_r = get_dref(fuel_boost_r_dref)
                agent.fuel_boost_r_o = fuel_boost_r
                time.sleep(refresh_rate)
                test_knob = get_dref(test_knob_dref)
                agent.test_knob_o = test_knob
                time.sleep(refresh_rate)
                autopilot_heading_set = get_dref(autopilot_heading_set_dref)
                agent.autopilot_heading_set_o = autopilot_heading_set
                time.sleep(refresh_rate)
                autopilot_state = get_dref(autopilot_state_dref)
                agent.autopilot_state_o = autopilot_state
                time.sleep(refresh_rate)
                yaw_damper = get_dref(yaw_damper_dref)
                agent.yaw_damper_o = yaw_damper
                time.sleep(refresh_rate)
                l_ign_switch = get_dref(l_ign_switch_dref)
                agent.l_ign_switch_o = l_ign_switch
                time.sleep(refresh_rate)
                r_ign_switch = get_dref(r_ign_switch_dref)
                agent.r_ign_switch_o = r_ign_switch
                time.sleep(refresh_rate)
                l_gen_switch = get_dref(l_gen_switch_dref)
                agent.l_gen_switch_o = l_gen_switch
                time.sleep(refresh_rate)
                r_gen_switch = get_dref(r_gen_switch_dref)
                agent.r_gen_switch_o = r_gen_switch
                time.sleep(refresh_rate)
                transfer_knob = get_dref(transfer_knob_dref)
                agent.transfer_knob_o = transfer_knob
                """
                time.sleep(refresh_rate)
                pitch, heading, roll, alt, lat, long = get_position()
                agent.pitch_o = pitch
                agent.heading_o = heading
                agent.roll_o = roll
                agent.altitude_o = alt 
                agent.latitude_o = lat
                agent.longitude_o = long

                time.sleep(refresh_rate)
                aileron, elevator, rudder, throttle, gear, flaps, speedbrakes = get_control_inputs()
                agent.control_roll_o = aileron
                agent.control_pitch_o = elevator
                agent.control_yaw_o = rudder
                agent.control_throttle_o = throttle
                agent.control_gear_o = gear
                agent.control_flaps_o = flaps
                agent.control_speedbrakes_o = speedbrakes
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying in 3 seconds...")
            time.sleep(3)

main()
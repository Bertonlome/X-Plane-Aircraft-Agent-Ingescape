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
iasDref = "sim/cockpit2/gauges/indicators/airspeed_kts_pilot"
pitchDref = "sim/cockpit2/gauges/indicators/pitch_AHARS_deg_pilot"
altitudeDref = "sim/cockpit2/gauges/indicators/altitude_ft_pilot"
thrustDref = "sim/cockpit2/engine/actuators/throttle_jet_rev_ratio_all"
headingDref = "sim/cockpit2/gauges/indicators/heading_AHARS_deg_mag_pilot" # 0 to 1, override because it is a double instead of an array
rollDref = "sim/cockpit2/gauges/indicators/roll_AHARS_deg_pilot"
parkBrakeDref = "sim/cockpit2/controls/parking_brake_ratio"
verticalSpeedDref = "sim/cockpit2/gauges/indicators/vvi_fpm_pilot"
rudderDref = "sim/cockpit2/controls/yoke_heading_ratio"
elevatorDref = "sim/cockpit2/controls/yoke_pitch_ratio"
aileronDref = "sim/cockpit2/controls/yoke_roll_ratio"
mustang_l_throttle = "Mustang/cockpit/engine/l_throttle"
mustang_r_throttle = "Mustang/cockpit/engine/r_throttle"
flapsDref = "sim/cockpit2/controls/flap_ratio"
gearDref = "sim/cockpit/switches/gear_handle_status"
bird_dref = "sim/operation/failures/rel_bird_strike"

def get_dref(arg, is_double=False):

    with xpc.XPlaneConnect() as client:
        #get a dref
        dref = arg
        myValue = client.getDREF(dref)
        rounded_value = round(myValue[0], 1)
        return rounded_value

refresh_rate = 0.5
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
    with xpc.XPlaneConnect() as client:
        if name == "elevator":
            client.sendDREF(elevatorDref, value)
        elif name == "rudder":
            client.sendDREF(rudderDref, value)
        elif name == "aileron":
            client.sendDREF(aileronDref, value)
        elif name == "throttle":
            print("Throttle value is: ", value)
            #client.sendDREFs([mustang_l_throttle, mustang_r_throttle], [1,1])
            client.sendDREF(thrustDref, value)
        elif name == "flaps":
            client.sendDREF(flapsDref, value)

def int_input_callback(io_type, name, value_type, value, my_data):
    agent_object = my_data
    assert isinstance(agent_object, Echo)
    with xpc.XPlaneConnect() as client:
        if name == "flaps":
            pass
            #dref tbd

def impulsion_input_callback(io_type, name, value_type, value, my_data):
    with xpc.XPlaneConnect() as client:
        if name == "gear":
            current_val = get_dref(gearDref)
            print(f"current val = {current_val}")
            if current_val == 1: client.sendDREF(gearDref,0)
            #else:
            pass
        elif name == "brake":
            current_val = get_dref(parkBrakeDref)
            print(f"current val = {current_val}")
            if current_val == 1: client.sendDREF(parkBrakeDref,0)
            else: client.sendDREF(parkBrakeDref, 1)
        elif name == "bird_strike":
            client.sendDREF(bird_dref, 2)
            print("Birds incoming ! :)")
            agent.outside_event_o = "birds"

def get_lat():
    with xpc.XPlaneConnect() as client:
        lat = client.getDREF("sim/flightmodel/position/latitude")[0]
        return lat

def get_long():
    with xpc.XPlaneConnect() as client:
        long = client.getDREF("sim/flightmodel/position/longitude")[0]
        return long

def get_control_inputs():
    with xpc.XPlaneConnect() as client:
        aileron = client.getDREF("sim/cockpit2/controls/yoke_roll_ratio")[0]
        time.sleep(0.01)
        elevator = client.getDREF("sim/cockpit2/controls/yoke_pitch_ratio")[0]
        time.sleep(0.01)
        rudder = client.getDREF("sim/cockpit2/controls/yoke_heading_ratio")[0]
        return aileron, elevator, rudder
    
def get_position():
    with xpc.XPlaneConnect() as client:
        local_x = client.getDREF("sim/flightmodel/position/local_x")[0]
        local_y = client.getDREF("sim/flightmodel/position/local_y")[0]
        return local_x, local_y

def get_pitch():
    pitch = get_dref("sim/cockpit2/gauges/indicators/pitch_AHARS_deg_pilot")
    return pitch,


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
igs.output_create("outsideEvent", igs.STRING_T, None)

igs.observe_input("elevator", double_input_callback, None)
igs.observe_input("rudder", double_input_callback, None)
igs.observe_input("aileron", double_input_callback, None)
igs.observe_input("throttle", double_input_callback, None)
igs.observe_input("flaps", double_input_callback, None)
igs.observe_input("gear", impulsion_input_callback, None)
igs.observe_input("brake", impulsion_input_callback, None)
igs.observe_input("bird_strike", impulsion_input_callback, None)

igs.log_set_console(True)
igs.log_set_console_level(igs.LOG_INFO)

igs.start_with_device(device, port)
# catch SIGINT handler after starting agent
signal.signal(signal.SIGINT, signal_handler)

def main():
        while not is_interrupted:
            time.sleep(refresh_rate)
            value = get_dref(iasDref)
            agent.airspeed_o = value
            time.sleep(refresh_rate)
            value = get_dref(pitchDref)
            agent.pitch_o = value
            time.sleep(refresh_rate)
            value = get_dref(rollDref)
            agent.roll_o = value
            time.sleep(refresh_rate)
            value = get_dref(headingDref)
            agent.heading_o = value
            time.sleep(refresh_rate)
            value= get_dref(verticalSpeedDref)
            agent.vertical_speed_o = value
            time.sleep(refresh_rate)
            value = get_dref(altitudeDref)
            agent.altitude_o = value
            time.sleep(refresh_rate)
            value = get_lat()
            agent.latitude_o = value
            time.sleep(refresh_rate)
            value = get_long()
            agent.longitude_o = value
            time.sleep(refresh_rate)
            aileron, elevator, rudder = get_control_inputs()
            agent.control_roll_o = aileron
            agent.control_pitch_o = elevator
            agent.control_yaw_o = rudder
            time.sleep(refresh_rate)
            value = get_dref(thrustDref)
            agent.control_throttle_o = value
            time.sleep(refresh_rate)
            value = get_dref(flapsDref)
            agent.control_flaps_o = value
            time.sleep(refresh_rate)
            value = get_dref(gearDref)
            agent.control_gear_o = value

main()
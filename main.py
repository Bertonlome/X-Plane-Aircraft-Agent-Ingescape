#!/usr/bin/env python3
# coding: utf-8
# =========================================================================
# main.py
#
# Copyright (c) the Contributors as noted in the AUTHORS file.
# This file is part of Ingescape, see https://github.com/zeromq/ingescape.
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =========================================================================
#
import struct
import signal
import getopt
import time
import xpc
from pathlib import Path

from echo import *

refresh_rate = 1 / 100
port = 5670
agent_name = "Aircraft_agent"
device = "wlo1"
verbose = False
is_interrupted = False

## def datarefs string
flap_dref = "sim/cockpit2/controls/flap_ratio"
gear_dref = "sim/cockpit/switches/gear_handle_status"
groundSpeedDref = "sim/flightmodel/position/groundspeed"
thrustDref = "sim/flightmodel/engine/ENGN_thro_use"
parkingBrakeDref = "sim/cockpit2/controls/parking_brake_ratio"
fuelQuantityRightDref = "sim/cockpit2/fuel/fuel_level_indicated_right"
fuelQuantityLeftDref = "sim/cockpit2/fuel/fuel_level_indicated_left"
simTimeSinceStartDref = "sim/time/total_flight_time_sec"


def return_io_value_type_as_str(value_type):
    if value_type == igs.INTEGER_T:
        return "Airspeed"
    elif value_type == igs.DOUBLE_T:
        return "Double"
    elif value_type == igs.BOOL_T:
        return "Bool"
    elif value_type == igs.STRING_T:
        return "String"
    elif value_type == igs.IMPULSION_T:
        return "Impulsion"
    elif value_type == igs.DATA_T:
        return "Data"
    else:
        return "Unknown"

def return_event_type_as_str(event_type):
    if event_type == igs.PEER_ENTERED:
        return "PEER_ENTERED"
    elif event_type == igs.PEER_EXITED:
        return "PEER_EXITED"
    elif event_type == igs.AGENT_ENTERED:
        return "AGENT_ENTERED"
    elif event_type == igs.AGENT_UPDATED_DEFINITION:
        return "AGENT_UPDATED_DEFINITION"
    elif event_type == igs.AGENT_KNOWS_US:
        return "AGENT_KNOWS_US"
    elif event_type == igs.AGENT_EXITED:
        return "AGENT_EXITED"
    elif event_type == igs.AGENT_UPDATED_MAPPING:
        return "AGENT_UPDATED_MAPPING"
    elif event_type == igs.AGENT_WON_ELECTION:
        return "AGENT_WON_ELECTION"
    elif event_type == igs.AGENT_LOST_ELECTION:
        return "AGENT_LOST_ELECTION"
    else:
        return "UNKNOWN" 

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


# inputs
# services

def get_dref(arg):
    with xpc.XPlaneConnect() as client:
        #get a dref
        dref = arg
        myValue = client.getDREF(dref)
        rounded_value = round(myValue[0], 1)
        myValueText = f"{rounded_value:.1f}"  # Format with 1 decimal place
        return myValueText
    
def get_posi(arg):
    with xpc.XPlaneConnect() as client:
        #get a dref
        dref = arg
        myValue = client.getPOSI(dref)
        return myValue
    
def get_ctrl(arg):
    with xpc.XPlaneConnect() as client:
        #get a dref
        dref = arg
        myValue = client.getCTRL(dref)
        return myValue


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

igs.output_create("heading", igs.DOUBLE_T, None)
igs.output_create("groundSpeed", igs.DOUBLE_T, None)
igs.output_create("roll", igs.DOUBLE_T, None)
igs.output_create("fuelQuantity", igs.DOUBLE_T, None)
igs.output_create("lon", igs.DOUBLE_T, None)
igs.output_create("simTimeSinceStart", igs.DOUBLE_T, None)
igs.output_create("elevator", igs.DOUBLE_T, None)
igs.output_create("thrustCmd", igs.DOUBLE_T, None)
igs.output_create("rudder", igs.DOUBLE_T, None)
igs.output_create("brakingAction", igs.DOUBLE_T, None)
igs.output_create("aileron", igs.DOUBLE_T, None)
igs.output_create("pitch", igs.DOUBLE_T, None)
igs.output_create("lat", igs.DOUBLE_T, None)
igs.output_create("height", igs.DOUBLE_T, None)

igs.log_set_console(True)
igs.log_set_console_level(igs.LOG_INFO)

igs.start_with_device(device, port)
# catch SIGINT handler after starting agent
signal.signal(signal.SIGINT, signal_handler)

while True:
    if is_interrupted:
        break
    
    #My main loop
    newValue = get_posi(0)
    igs.output_set_double("lat", newValue[0])
    igs.output_set_double("lon", newValue[1])
    igs.output_set_double("height", newValue[2])
    igs.output_set_double("pitch", newValue[3])
    igs.output_set_double("roll", newValue[4])
    igs.output_set_double("heading", newValue[5])
    time.sleep(refresh_rate)
    newValue = get_ctrl(0)
    igs.output_set_double("elevator", newValue[0])
    igs.output_set_double("aileron", newValue[1])
    igs.output_set_double("rudder", newValue[2])
    time.sleep(refresh_rate)        
    newValue = get_dref(groundSpeedDref)
    igs.output_set_double("groundSpeed", float(newValue))
    time.sleep(refresh_rate)
    newValue = get_dref(thrustDref)
    igs.output_set_double("thrustCmd", float(newValue))
    time.sleep(refresh_rate)
    newValue = get_dref(parkingBrakeDref)
    igs.output_set_double("brakingAction", float(newValue))
    time.sleep(refresh_rate)
    fuelLeft = get_dref(fuelQuantityLeftDref)
    time.sleep(refresh_rate)
    fuelRight = get_dref(fuelQuantityRightDref)
    newValue = (float(fuelLeft) + float(fuelRight))
    igs.output_set_double("fuelQuantity", float(newValue))
    time.sleep(refresh_rate)
    newValue = get_dref(simTimeSinceStartDref)
    igs.output_set_double("simTimeSinceStart", float(newValue))
    ## just a comments
    time.sleep(refresh_rate)
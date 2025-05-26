# coding: utf-8

# =========================================================================
# echo_example.py
#
# Copyright (c) the Contributors as noted in the AUTHORS file.
# This file is part of Ingescape, see https://github.com/zeromq/ingescape.
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =========================================================================


import ingescape as igs
import sys


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Echo(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.elevator_i = None
        self.aileron_i = None
        self.rudder_i = None
        self.throttle_i = None
        self.flaps_i = None
        self.gear_i = None
        self.brake_i = None

        # outputs
        self.airspeed_o = None
        self.pitch_o = None
        self.roll_o = None
        self.heading_o = None
        self.vertical_speed_0 = None
        self.altitude_o = None
        self.latitude_o = None
        self.longitude_o = None
        self.control_pitch_o = None
        self.control_roll_o = None
        self.control_yaw_o = None
        self.control_throttle_o = None
        self.control_flaps_o = None
        self.control_gear_o = None
        self.outside_event_o = None

    @property
    def airspeed_o(self):
        return self.airspeed_o

    @airspeed_o.setter
    def airspeed_o(self, value):
        self._airspeed_o = value
        if self._airspeed_o is not None:
            igs.output_set_double("airspeed", self._airspeed_o)

    @property
    def pitch_o(self):
        return self.pitch_o

    @pitch_o.setter
    def pitch_o(self, value):
        self._pitch_o = value
        if self._pitch_o is not None:
            igs.output_set_double("pitch", self._pitch_o)

    @property
    def roll_o(self):
        return self.roll_o

    @roll_o.setter
    def roll_o(self, value):
        self._roll_o = value
        if self._roll_o is not None:
            igs.output_set_double("roll", self._roll_o)

    @property
    def heading_o(self):
        return self.heading_o

    @heading_o.setter
    def heading_o(self, value):
        self._heading_o = value
        if self._heading_o is not None:
            igs.output_set_double("heading", self._heading_o)

    @property
    def vertical_speed_o(self):
        return self.vertical_speed_0

    @vertical_speed_o.setter
    def vertical_speed_o(self, value):
        self._vertical_speed_o = value
        if self._vertical_speed_o is not None:
            igs.output_set_double("verticalSpeed", self._vertical_speed_o)

    @property
    def altitude_o(self):
        return self.altitude_o

    @altitude_o.setter
    def altitude_o(self, value):
        self._altitude_o = value
        if self._altitude_o is not None:
            igs.output_set_double("altitude", self._altitude_o)
    
    @property
    def latitude_o(self):
        return self.latitude_o
    
    @latitude_o.setter
    def latitude_o(self, value):
        self._latitude_o = value
        if self._latitude_o is not None:
            igs.output_set_double("latitude", self._latitude_o)
    
    @property
    def longitude_o(self):
        return self.longitude_o
    
    @longitude_o.setter
    def longitude_o(self, value):
        self._longitude_o = value
        if self._longitude_o is not None:
            igs.output_set_double("longitude", self._longitude_o)
    
    @property
    def control_pitch_o(self):
        return self.control_pitch_o
    
    @control_pitch_o.setter
    def control_pitch_o(self, value):
        self._control_pitch_o = value
        if self._control_pitch_o is not None:
            igs.output_set_double("controlPitch", self._control_pitch_o)
    
    @property
    def control_roll_o(self):
        return self.control_roll_o
    
    @control_roll_o.setter
    def control_roll_o(self, value):
        self._control_roll_o = value
        if self._control_roll_o is not None:
            igs.output_set_double("controlRoll", self._control_roll_o)
    
    @property
    def control_yaw_o(self):
        return self.control_yaw_o
    
    @control_yaw_o.setter
    def control_yaw_o(self, value):
        self._control_yaw_o = value
        if self._control_yaw_o is not None:
            igs.output_set_double("controlYaw", self._control_yaw_o)
    
    @property
    def control_throttle_o(self):
        return self.control_throttle_o
    
    @control_throttle_o.setter
    def control_throttle_o(self, value):
        self._control_throttle_o = value
        if self._control_throttle_o is not None:
            igs.output_set_double("controlThrottle", self._control_throttle_o)
    
    @property
    def control_flaps_o(self):
        return self.control_flaps_o
    
    @control_flaps_o.setter
    def control_flaps_o(self, value):
        self._control_flaps_o = value
        if self._control_flaps_o is not None:
            igs.output_set_double("controlFlaps", self._control_flaps_o)
    
    @property
    def control_gear_o(self):
        return self.control_gear_o
    
    @control_gear_o.setter
    def control_gear_o(self, value):
        self._control_gear_o = value
        if self._control_gear_o is not None:
            igs.output_set_double("controlGear", self._control_gear_o)
    
    @property
    def outside_event_o(self):
        return self.outside_event_o
    
    @outside_event_o.setter
    def outside_event_o(self, value):
        self._outside_event_o = value
        if self._outside_event_o is not None:
            igs.output_set_string("outsideEvent", self._outside_event_o)

    # =========================================================================

    # services
    def receive_values(self, sender_agent_name, sender_agent_uuid, boolV, integer, double, string, data, token, my_data):
        igs.info(f"Service receive_values called by {sender_agent_name} ({sender_agent_uuid}) with argument_list {boolV, integer, double, string, data} and token '{token}''")

    def send_values(self, sender_agent_name, sender_agent_uuid, token, my_data):
        print(f"Service send_values called by {sender_agent_name} ({sender_agent_uuid}), token '{token}' sending values : {self.airspeed_o, self.integerO, self.doubleO, self.stringO, self.dataO}")
        igs.info(sender_agent_uuid, "receive_values", (self.airspeed_o, self.integerO, self.doubleO, self.stringO, self.dataO), token)
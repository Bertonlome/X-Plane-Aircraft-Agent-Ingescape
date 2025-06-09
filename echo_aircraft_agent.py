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
        self.control_speedbrakes_o = None
        self.outside_event_o = None
        self.park_brake_o = None
        self.l_throttle_o = None
        self.r_throttle_o = None
        self.cas_o = None
        self.n1_match_bug_o = None
        self.n1_percent_o = None
        self.slip_o = None
        self.engine_fires_o = None
        self.generators_off_o = None
        self.pax_safety_o = None
        self.master_warning_o = None
        self.master_caution_o = None
        self.flight_director_o = None
        self.speed_mode_o = None
        self.heading_mode_o = None
        self.autopilot_master_o = None
        self.fuel_boost_l_o = None
        self.fuel_boost_r_o = None
        self.test_knob_o = None
        self.autopilot_heading_set_o = None
        self.autopilot_sate_o = None
        self.yaw_damper_o = None
        self.l_ign_switch_o = None
        self.r_ign_switch_o = None
        self.l_gen_switch_o = None
        self.r_gen_switch_o = None
        self.transfer_knob_o = None

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
    def control_speedbrakes_o(self):
        return self.control_speedbrakes_o

    @control_speedbrakes_o.setter
    def control_speedbrakes_o(self, value):
        self._speedbrakes_o = value
        if self._speedbrakes_o is not None:
            igs.output_set_double("speedBrakes", self._speedbrakes_o)

    @property
    def outside_event_o(self):
        return self.outside_event_o
    
    @outside_event_o.setter
    def outside_event_o(self, value):
        self._outside_event_o = value
        if self._outside_event_o is not None:
            igs.output_set_string("outsideEvent", self._outside_event_o)
    
    @property
    def park_brake_o(self):
        return self.park_brake_o
    @park_brake_o.setter
    def park_brake_o(self, value):
        self._park_brake_o = value
        if self._park_brake_o is not None:
            igs.output_set_double("parkBrake", self._park_brake_o)
    
    @property
    def l_throttle_o(self):
        return self.l_throttle_o
    @l_throttle_o.setter
    def l_throttle_o(self, value):
        self._l_throttle_o = value
        if self._l_throttle_o is not None:
            igs.output_set_double("l_throttle", self._l_throttle_o)
    
    @property
    def r_throttle_o(self):
        return self.r_throttle_o
    @r_throttle_o.setter
    def r_throttle_o(self, value):
        self._r_throttle_o = value
        if self._r_throttle_o is not None:
            igs.output_set_double("r_throttle", self._r_throttle_o)
    
    @property
    def cas_o(self):
        return self.cas_o
    @cas_o.setter
    def cas_o(self, value):
        self._cas_o = value
        if self._cas_o is not None:
            igs.output_set_double("cas", self._cas_o)
    
    @property
    def n1_match_bug_o(self):
        return self.n1_match_bug_o
    @n1_match_bug_o.setter
    def n1_match_bug_o(self, value):
        self._n1_match_bug_o = value
        if self._n1_match_bug_o is not None:
            igs.output_set_double("n1_match_bug", self._n1_match_bug_o)
    
    @property
    def n1_percent_o(self):
        return self.n1_percent_o
    @n1_percent_o.setter
    def n1_percent_o(self, value):
        self._n1_percent_o = value
        if self._n1_percent_o is not None:
            igs.output_set_double("n1_percent", self._n1_percent_o)
    
    @property
    def slip_o(self):
        return self.slip_o
    @slip_o.setter
    def slip_o(self, value):
        self._slip_o = value
        if self._slip_o is not None:
            igs.output_set_double("slip", self._slip_o)
    
    @property
    def engine_fires_o(self):
        return self.engine_fires_o
    @engine_fires_o.setter
    def engine_fires_o(self, value):
        self._engine_fires_o = value
        if self._engine_fires_o is not None:
            igs.output_set_double("engine_fires", self._engine_fires_o)
    
    @property
    def generators_off_o(self):
        return self.generators_off_o
    @generators_off_o.setter
    def generators_off_o(self, value):
        self._generators_off_o = value
        if self._generators_off_o is not None:
            igs.output_set_double("generators_off", self._generators_off_o)
    
    @property
    def pax_safety_o(self):
        return self.pax_safety_o
    @pax_safety_o.setter
    def pax_safety_o(self, value):
        self._pax_safety_o = value
        if self._pax_safety_o is not None:
            igs.output_set_double("pax_safety", self._pax_safety_o)
    
    @property
    def master_warning_o(self):
        return self.master_warning_o
    @master_warning_o.setter
    def master_warning_o(self, value):
        self._master_warning_o = value
        if self._master_warning_o is not None:
            igs.output_set_double("master_warning", self._master_warning_o)
    
    @property
    def master_caution_o(self):
        return self.master_caution_o
    @master_caution_o.setter
    def master_caution_o(self, value):
        self._master_caution_o = value
        if self._master_caution_o is not None:
            igs.output_set_double("master_caution", self._master_caution_o)
    
    @property
    def flight_director_o(self):
        return self.flight_director_o
    @flight_director_o.setter
    def flight_director_o(self, value):
        self._flight_director_o = value
        if self._flight_director_o is not None:
            igs.output_set_double("flight_director", self._flight_director_o)
            
    @property
    def speed_mode_o(self):
        return self.speed_mode_o
    @speed_mode_o.setter
    def speed_mode_o(self, value):
        self._speed_mode_o = value
        if self._speed_mode_o is not None:
            igs.output_set_double("speed_mode", self._speed_mode_o)
    
    @property
    def heading_mode_o(self):
        return self.heading_mode_o
    @heading_mode_o.setter
    def heading_mode_o(self, value):
        self._heading_mode_o = value
        if self._heading_mode_o is not None:
            igs.output_set_double("heading_mode", self._heading_mode_o)
    
    @property
    def autopilot_master_o(self):
        return self.autopilot_master_o
    @autopilot_master_o.setter
    def autopilot_master_o(self, value):
        self._autopilot_master_o = value
        if self._autopilot_master_o is not None:
            igs.output_set_double("autopilot_master", self._autopilot_master_o)
    
    @property
    def fuel_boost_l_o(self):
        return self.fuel_boost_l_o
    @fuel_boost_l_o.setter
    def fuel_boost_l_o(self, value):
        self._fuel_boost_l_o = value
        if self._fuel_boost_l_o is not None:
            igs.output_set_double("fuel_boost_l", self._fuel_boost_l_o)
    
    @property
    def fuel_boost_r_o(self):
        return self.fuel_boost_r_o
    @fuel_boost_r_o.setter
    def fuel_boost_r_o(self, value):
        self._fuel_boost_r_o = value
        if self._fuel_boost_r_o is not None:
            igs.output_set_double("fuel_boost_r", self._fuel_boost_r_o)
    
    @property
    def test_knob_o(self):
        return self.test_knob_o
    @test_knob_o.setter
    def test_knob_o(self, value):
        self._test_knob_o = value
        if self._test_knob_o is not None:
            igs.output_set_double("test_knob", self._test_knob_o)
    
    @property
    def autopilot_heading_set_o(self):
        return self.autopilot_heading_set_o
    @autopilot_heading_set_o.setter
    def autopilot_heading_set_o(self, value):
        self._autopilot_heading_set_o = value
        if self._autopilot_heading_set_o is not None:
            igs.output_set_double("autopilot_heading_set", self._autopilot_heading_set_o) 
            
    @property
    def autopilot_state_o(self):
        return self.autopilot_state_o
    @autopilot_state_o.setter
    def autopilot_state_o(self, value):
        self._autopilot_state_o = value
        if self._autopilot_state_o is not None:
            igs.output_set_double("autopilot_state", self._autopilot_state_o)
            
    @property
    def yaw_damper_o(self):
        return self.yaw_damper_o
    @yaw_damper_o.setter
    def yaw_damper_o(self, value):
        self._yaw_damper_o = value
        if self._yaw_damper_o is not None:
            igs.output_set_double("yaw_damper", self._yaw_damper_o)
    
    @property
    def l_ign_switch_o(self):
        return self.l_ign_switch_o
    @l_ign_switch_o.setter
    def l_ign_switch_o(self, value):
        self._l_ign_switch_o = value
        if self._l_ign_switch_o is not None:
            igs.output_set_double("l_ign_switch", self._l_ign_switch_o)
    
    @property
    def r_ign_switch_o(self):
        return self.r_ign_switch_o
    @r_ign_switch_o.setter
    def r_ign_switch_o(self, value):
        self._r_ign_switch_o = value
        if self._r_ign_switch_o is not None:
            igs.output_set_double("r_ign_switch", self._r_ign_switch_o)
    
    @property
    def l_gen_switch_o(self):
        return self.l_gen_switch_o
    @l_gen_switch_o.setter
    def l_gen_switch_o(self, value):
        self._l_gen_switch_o = value
        if self._l_gen_switch_o is not None:
            igs.output_set_double("l_gen_switch", self._l_gen_switch_o)
    
    @property
    def r_gen_switch_o(self):
        return self.r_gen_switch_o
    @r_gen_switch_o.setter
    def r_gen_switch_o(self, value):
        self._r_gen_switch_o = value
        if self._r_gen_switch_o is not None:
            igs.output_set_double("r_gen_switch", self._r_gen_switch_o)
    
    @property
    def transfer_knob_o(self):
        return self.transfer_knob_o
    @transfer_knob_o.setter
    def transfer_knob_o(self, value):
        self._transfer_knob_o = value
        if self._transfer_knob_o is not None:
            igs.output_set_double("transfer_knob", self._transfer_knob_o)

    # =========================================================================

    # services
    def receive_values(self, sender_agent_name, sender_agent_uuid, boolV, integer, double, string, data, token, my_data):
        igs.info(f"Service receive_values called by {sender_agent_name} ({sender_agent_uuid}) with argument_list {boolV, integer, double, string, data} and token '{token}''")

    def send_values(self, sender_agent_name, sender_agent_uuid, token, my_data):
        print(f"Service send_values called by {sender_agent_name} ({sender_agent_uuid}), token '{token}' sending values : {self.airspeed_o, self.integerO, self.doubleO, self.stringO, self.dataO}")
        igs.info(sender_agent_uuid, "receive_values", (self.airspeed_o, self.integerO, self.doubleO, self.stringO, self.dataO), token)
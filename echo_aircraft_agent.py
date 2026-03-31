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
        self.pitot_heat_i = None
        self.alt_sel_i = None
        self.heading_sel_i = None
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
        self.e1_n1_percent_o = None
        self.e2_n1_percent_o = None
        self.slip_o = None
        self.engine_fire_l_o = None
        self.engine_fire_r_o = None
        self.pax_safety_o = None
        self.master_warning_o = None
        self.master_caution_o = None
        self.flight_director_o = None
        self.speed_mode_o = None
        self.heading_mode_o = None
        self.fuel_boost_l_o = None
        self.fuel_boost_r_o = None
        self.test_knob_o = None
        self.autopilot_heading_set_o = None
        self.yaw_damper_o = None
        self.l_ign_switch_o = None
        self.r_ign_switch_o = None
        self.l_gen_switch_o = None
        self.r_gen_switch_o = None
        self.transfer_knob_o = None
        self.baro_setting_o = None
        self.cabin_altitude_o = None
        self.l_gen_load_o = None
        self.r_gen_load_o = None
        self.pitot_heat_o = None
        self.l_windshield_anti_ice_o = None
        self.r_windshield_anti_ice_o = None
        self.exterior_lights_o = None
        self.anti_coll_lights_o = None
        self.l_engine_anti_ice_o = None
        self.r_engine_anti_ice_o = None
        self.trim_rudder_o = None
        self.alt_sel_o = None
        self.heading_sel_o = None
        self.l_bottle_arm_o = None
        self.r_bottle_arm_o = None
        self.ptt_o = None
        self.check_o = None
        self.approve_o = None
        self.yoke_hide_o = None
        self.autopilot_airspeed_o = None
        self.com_1_freq_o = None
        self.elevator_trim_o = None
        self.aileron_trim_o = None
        self.fd_pitch_deg_o = None
        self.paused_o = None

    @property
    def airspeed_o(self):
        return self.airspeed_o

    @airspeed_o.setter
    def airspeed_o(self, value):
        if hasattr(self, '_airspeed_o') and self._airspeed_o == value:
            return
        self._airspeed_o = value
        if self._airspeed_o is not None:
            igs.output_set_double("airspeed", self._airspeed_o)

    @property
    def pitch_o(self):
        return self.pitch_o

    @pitch_o.setter
    def pitch_o(self, value):
        if hasattr(self, '_pitch_o') and self._pitch_o == value:
            return
        self._pitch_o = value
        if self._pitch_o is not None:
            igs.output_set_double("pitch", self._pitch_o)

    @property
    def roll_o(self):
        return self.roll_o

    @roll_o.setter
    def roll_o(self, value):
        if hasattr(self, '_roll_o') and self._roll_o == value:
            return
        self._roll_o = value
        if self._roll_o is not None:
            igs.output_set_double("roll", self._roll_o)

    @property
    def heading_o(self):
        return self.heading_o

    @heading_o.setter
    def heading_o(self, value):
        if hasattr(self, '_heading_o') and self._heading_o == value:
            return
        self._heading_o = value
        if self._heading_o is not None:
            igs.output_set_double("heading", self._heading_o)

    @property
    def vertical_speed_o(self):
        return self.vertical_speed_0

    @vertical_speed_o.setter
    def vertical_speed_o(self, value):
        if hasattr(self, '_vertical_speed_o') and self._vertical_speed_o == value:
            return
        self._vertical_speed_o = value
        if self._vertical_speed_o is not None:
            igs.output_set_double("verticalSpeed", self._vertical_speed_o)

    @property
    def altitude_o(self):
        return self.altitude_o

    @altitude_o.setter
    def altitude_o(self, value):
        if hasattr(self, '_altitude_o') and self._altitude_o == value:
            return
        self._altitude_o = value
        if self._altitude_o is not None:
            igs.output_set_double("altitude", self._altitude_o)
    
    @property
    def latitude_o(self):
        return self.latitude_o
    
    @latitude_o.setter
    def latitude_o(self, value):
        if hasattr(self, '_latitude_o') and self._latitude_o == value:
            return
        self._latitude_o = value
        if self._latitude_o is not None:
            igs.output_set_double("latitude", self._latitude_o)
    
    @property
    def longitude_o(self):
        return self.longitude_o
    
    @longitude_o.setter
    def longitude_o(self, value):
        if hasattr(self, '_longitude_o') and self._longitude_o == value:
            return
        self._longitude_o = value
        if self._longitude_o is not None:
            igs.output_set_double("longitude", self._longitude_o)
    
    @property
    def control_pitch_o(self):
        return self.control_pitch_o
    
    @control_pitch_o.setter
    def control_pitch_o(self, value):
        if hasattr(self, '_control_pitch_o') and self._control_pitch_o == value:
            return
        self._control_pitch_o = value
        if self._control_pitch_o is not None:
            igs.output_set_double("controlPitch", self._control_pitch_o)
    
    @property
    def control_roll_o(self):
        return self.control_roll_o
    
    @control_roll_o.setter
    def control_roll_o(self, value):
        if hasattr(self, '_control_roll_o') and self._control_roll_o == value:
            return
        self._control_roll_o = value
        if self._control_roll_o is not None:
            igs.output_set_double("controlRoll", self._control_roll_o)
    
    @property
    def control_yaw_o(self):
        return self.control_yaw_o
    
    @control_yaw_o.setter
    def control_yaw_o(self, value):
        if hasattr(self, '_control_yaw_o') and self._control_yaw_o == value:
            return
        self._control_yaw_o = value
        if self._control_yaw_o is not None:
            igs.output_set_double("controlYaw", self._control_yaw_o)
    
    @property
    def control_throttle_o(self):
        return self.control_throttle_o
    
    @control_throttle_o.setter
    def control_throttle_o(self, value):
        if hasattr(self, '_control_throttle_o') and self._control_throttle_o == value:
            return
        self._control_throttle_o = value
        if self._control_throttle_o is not None:
            igs.output_set_double("controlThrottle", self._control_throttle_o)
    
    @property
    def control_flaps_o(self):
        return self.control_flaps_o
    
    @control_flaps_o.setter
    def control_flaps_o(self, value):
        if hasattr(self, '_control_flaps_o') and self._control_flaps_o == value:
            return
        self._control_flaps_o = value
        if self._control_flaps_o is not None:
            igs.output_set_double("controlFlaps", self._control_flaps_o)
    
    @property
    def control_gear_o(self):
        return self.control_gear_o
    
    @control_gear_o.setter
    def control_gear_o(self, value):
        if hasattr(self, '_control_gear_o') and self._control_gear_o == value:
            return
        self._control_gear_o = value
        if self._control_gear_o is not None:
            igs.output_set_double("controlGear", self._control_gear_o)
    
    @property
    def control_speedbrakes_o(self):
        return self.control_speedbrakes_o

    @control_speedbrakes_o.setter
    def control_speedbrakes_o(self, value):
        if hasattr(self, '_control_speedbrakes_o') and self._control_speedbrakes_o == value:
            return
        self._control_speedbrakes_o = value
        if self._control_speedbrakes_o is not None:
            igs.output_set_double("speedBrakes", self._control_speedbrakes_o)

    @property
    def outside_event_o(self):
        return self.outside_event_o
    
    @outside_event_o.setter
    def outside_event_o(self, value):
        if hasattr(self, '_outside_event_o') and self._outside_event_o == value:
            return
        self._outside_event_o = value
        if self._outside_event_o is not None:
            igs.output_set_string("outsideEvent", self._outside_event_o)
    
    @property
    def park_brake_o(self):
        return self.park_brake_o

    @park_brake_o.setter
    def park_brake_o(self, value):
        if hasattr(self, '_park_brake_o') and self._park_brake_o == value:
            return
        self._park_brake_o = value
        if self._park_brake_o is not None:
            igs.output_set_bool("parkBrake", self._park_brake_o)
    
    @property
    def l_throttle_o(self):
        return self.l_throttle_o
    @l_throttle_o.setter
    def l_throttle_o(self, value):
        if hasattr(self, '_l_throttle_o') and self._l_throttle_o == value:
            return
        self._l_throttle_o = value
        if self._l_throttle_o is not None:
            igs.output_set_double("l_throttle", self._l_throttle_o)
    
    @property
    def r_throttle_o(self):
        return self.r_throttle_o
    @r_throttle_o.setter
    def r_throttle_o(self, value):
        if hasattr(self, '_r_throttle_o') and self._r_throttle_o == value:
            return
        self._r_throttle_o = value
        if self._r_throttle_o is not None:
            igs.output_set_double("r_throttle", self._r_throttle_o)
    
    @property
    def n1_match_bug_o(self):
        return self.n1_match_bug_o
    @n1_match_bug_o.setter
    def n1_match_bug_o(self, value):
        if hasattr(self, '_n1_match_bug_o') and self._n1_match_bug_o == value:
            return
        self._n1_match_bug_o = value
        if self._n1_match_bug_o is not None:
            igs.output_set_bool("n1_match_bug", self._n1_match_bug_o)
    
    @property
    def e1_n1_percent_o(self):
        return self.e1_n1_percent_o
    @e1_n1_percent_o.setter
    def e1_n1_percent_o(self, value):
        if hasattr(self, '_e1_n1_percent_o') and self._e1_n1_percent_o == value:
            return
        self._e1_n1_percent_o = value
        if self._e1_n1_percent_o is not None:
            igs.output_set_double("e1_n1_percent", self._e1_n1_percent_o)

    @property
    def e2_n1_percent_o(self):
        return self.e2_n1_percent_o
    @e2_n1_percent_o.setter
    def e2_n1_percent_o(self, value):
        if hasattr(self, '_e2_n1_percent_o') and self._e2_n1_percent_o == value:
            return
        self._e2_n1_percent_o = value
        if self._e2_n1_percent_o is not None:
            igs.output_set_double("e2_n1_percent", self._e2_n1_percent_o)

    @property
    def slip_o(self):
        return self.slip_o
    @slip_o.setter
    def slip_o(self, value):
        if hasattr(self, '_slip_o') and self._slip_o == value:
            return
        self._slip_o = value
        if self._slip_o is not None:
            igs.output_set_double("slip", self._slip_o)
    
    @property
    def engine_fire_l_o(self):
        return self._engine_fire_l_o
    @engine_fire_l_o.setter
    def engine_fire_l_o(self, value):
        if hasattr(self, '_engine_fire_l_o') and self._engine_fire_l_o == value:
            return
        self._engine_fire_l_o = value
        if self._engine_fire_l_o is not None:
            igs.output_set_bool("engine_fire_l", self._engine_fire_l_o)

    @property
    def engine_fire_r_o(self):
        return self._engine_fire_r_o
    @engine_fire_r_o.setter
    def engine_fire_r_o(self, value):
        if hasattr(self, '_engine_fire_r_o') and self._engine_fire_r_o == value:
            return
        self._engine_fire_r_o = value
        if self._engine_fire_r_o is not None:
            igs.output_set_bool("engine_fire_r", self._engine_fire_r_o)
    
    @property
    def pax_safety_o(self):
        return self._pax_safety_o
    @pax_safety_o.setter
    def pax_safety_o(self, value):
        if hasattr(self, '_pax_safety_o') and self._pax_safety_o == value:
            return
        self._pax_safety_o = value
        if self._pax_safety_o is not None:
            igs.output_set_int("pax_safety", self._pax_safety_o)
    
    @property
    def master_warning_o(self):
        return self._master_warning_o
    @master_warning_o.setter
    def master_warning_o(self, value):
        if hasattr(self, '_master_warning_o') and self._master_warning_o == value:
            return
        self._master_warning_o = value
        if self._master_warning_o is not None:
            igs.output_set_bool("master_warning", self._master_warning_o)
    
    @property
    def master_caution_o(self):
        return self._master_caution_o
    @master_caution_o.setter
    def master_caution_o(self, value):
        if hasattr(self, '_master_caution_o') and self._master_caution_o == value:
            return
        self._master_caution_o = value
        if self._master_caution_o is not None:
            igs.output_set_bool("master_caution", self._master_caution_o)

    @property
    def flight_director_o(self):
        return self._flight_director_o
    @flight_director_o.setter
    def flight_director_o(self, value):
        if hasattr(self, '_flight_director_o') and self._flight_director_o == value:
            return
        self._flight_director_o = value
        if self._flight_director_o is not None:
            igs.output_set_int("flight_director", self._flight_director_o)
            
    @property
    def speed_mode_o(self):
        return self._speed_mode_o
    @speed_mode_o.setter
    def speed_mode_o(self, value):
        if hasattr(self, '_speed_mode_o') and self._speed_mode_o == value:
            return
        self._speed_mode_o = value
        if self._speed_mode_o is not None:
            igs.output_set_int("speed_mode", self._speed_mode_o)
    
    @property
    def heading_mode_o(self):
        return self._heading_mode_o
    @heading_mode_o.setter
    def heading_mode_o(self, value):
        if hasattr(self, '_heading_mode_o') and self._heading_mode_o == value:
            return
        self._heading_mode_o = value
        if self._heading_mode_o is not None:
            igs.output_set_int("heading_mode", self._heading_mode_o)
    
    @property
    def fuel_boost_l_o(self):
        return self._fuel_boost_l_o
    @fuel_boost_l_o.setter
    def fuel_boost_l_o(self, value):
        if hasattr(self, '_fuel_boost_l_o') and self._fuel_boost_l_o == value:
            return
        self._fuel_boost_l_o = value
        if self._fuel_boost_l_o is not None:
            igs.output_set_int("fuel_boost_l", self._fuel_boost_l_o)
    
    @property
    def fuel_boost_r_o(self):
        return self._fuel_boost_r_o
    @fuel_boost_r_o.setter
    def fuel_boost_r_o(self, value):
        if hasattr(self, '_fuel_boost_r_o') and self._fuel_boost_r_o == value:
            return
        self._fuel_boost_r_o = value
        if self._fuel_boost_r_o is not None:
            igs.output_set_int("fuel_boost_r", self._fuel_boost_r_o)
    
    @property
    def test_knob_o(self):
        return self._test_knob_o
    @test_knob_o.setter
    def test_knob_o(self, value):
        if hasattr(self, '_test_knob_o') and self._test_knob_o == value:
            return
        self._test_knob_o = value
        if self._test_knob_o is not None:
            igs.output_set_int("test_knob", self._test_knob_o)
    
    @property
    def autopilot_heading_set_o(self):
        return self._autopilot_heading_set_o
    @autopilot_heading_set_o.setter
    def autopilot_heading_set_o(self, value):
        if hasattr(self, '_autopilot_heading_set_o') and self._autopilot_heading_set_o == value:
            return
        self._autopilot_heading_set_o = value
        if self._autopilot_heading_set_o is not None:
            igs.output_set_int("autopilot_heading_set", self._autopilot_heading_set_o) 
            
    @property
    def yaw_damper_o(self):
        return self._yaw_damper_o
    @yaw_damper_o.setter
    def yaw_damper_o(self, value):
        if hasattr(self, '_yaw_damper_o') and self._yaw_damper_o == value:
            return
        self._yaw_damper_o = value
        if self._yaw_damper_o is not None:
            igs.output_set_bool("yaw_damper", self._yaw_damper_o)
    
    @property
    def l_ign_switch_o(self):
        return self._l_ign_switch_o
    @l_ign_switch_o.setter
    def l_ign_switch_o(self, value):
        if hasattr(self, '_l_ign_switch_o') and self._l_ign_switch_o == value:
            return
        self._l_ign_switch_o = value
        if self._l_ign_switch_o is not None:
            igs.output_set_bool("l_ign_switch", self._l_ign_switch_o)
    
    @property
    def r_ign_switch_o(self):
        return self._r_ign_switch_o
    @r_ign_switch_o.setter
    def r_ign_switch_o(self, value):
        if hasattr(self, '_r_ign_switch_o') and self._r_ign_switch_o == value:
            return
        self._r_ign_switch_o = value
        if self._r_ign_switch_o is not None:
            igs.output_set_bool("r_ign_switch", self._r_ign_switch_o)
    
    @property
    def l_gen_switch_o(self):
        return self._l_gen_switch_o
    @l_gen_switch_o.setter
    def l_gen_switch_o(self, value):
        if hasattr(self, '_l_gen_switch_o') and self._l_gen_switch_o == value:
            return
        self._l_gen_switch_o = value
        if self._l_gen_switch_o is not None:
            igs.output_set_int("l_gen_switch", self._l_gen_switch_o)
    
    @property
    def r_gen_switch_o(self):
        return self._r_gen_switch_o
    @r_gen_switch_o.setter
    def r_gen_switch_o(self, value):
        if hasattr(self, '_r_gen_switch_o') and self._r_gen_switch_o == value:
            return
        self._r_gen_switch_o = value
        if self._r_gen_switch_o is not None:
            igs.output_set_int("r_gen_switch", self._r_gen_switch_o)

    @property
    def transfer_knob_o(self):
        return self._transfer_knob_o
    @transfer_knob_o.setter
    def transfer_knob_o(self, value):
        if hasattr(self, '_transfer_knob_o') and self._transfer_knob_o == value:
            return
        self._transfer_knob_o = value
        if self._transfer_knob_o is not None:
            igs.output_set_int("transfer_knob", self._transfer_knob_o)
    
    @property
    def baro_setting_o(self):
        return self._baro_setting_o
    @baro_setting_o.setter
    def baro_setting_o(self, value):
        if hasattr(self, '_baro_setting_o') and self._baro_setting_o == value:
            return
        self._baro_setting_o = value
        if self._baro_setting_o is not None:
            igs.output_set_double("baro_setting", self._baro_setting_o)

    @property
    def cabin_altitude_o(self):
        return self._cabin_altitude_o
    @cabin_altitude_o.setter
    def cabin_altitude_o(self, value):
        if hasattr(self, '_cabin_altitude_o') and self._cabin_altitude_o == value:
            return
        self._cabin_altitude_o = value
        if self._cabin_altitude_o is not None:
            igs.output_set_double("cabin_altitude", self._cabin_altitude_o)

    @property
    def l_gen_load_o(self):
        return self._l_gen_load_o
    @l_gen_load_o.setter
    def l_gen_load_o(self, value):
        if hasattr(self, '_l_gen_load_o') and self._l_gen_load_o == value:
            return
        self._l_gen_load_o = value
        if self._l_gen_load_o is not None:
            igs.output_set_double("l_gen_load", self._l_gen_load_o)

    @property
    def r_gen_load_o(self):
        return self._r_gen_load_o
    @r_gen_load_o.setter
    def r_gen_load_o(self, value):
        if hasattr(self, '_r_gen_load_o') and self._r_gen_load_o == value:
            return
        self._r_gen_load_o = value
        if self._r_gen_load_o is not None:
            igs.output_set_double("r_gen_load", self._r_gen_load_o)
    
    @property
    def pitot_heat_o(self):
        return self._pitot_heat_o
    @pitot_heat_o.setter
    def pitot_heat_o(self, value):
        if hasattr(self, '_pitot_heat_o') and self._pitot_heat_o == value:
            return
        self._pitot_heat_o = value
        if self._pitot_heat_o is not None:
            igs.output_set_bool("pitot_heat", self._pitot_heat_o)
    
    @property
    def l_windshield_anti_ice_o(self):
        return self._l_windshield_anti_ice_o
    @l_windshield_anti_ice_o.setter
    def l_windshield_anti_ice_o(self, value):
        if hasattr(self, '_l_windshield_anti_ice_o') and self._l_windshield_anti_ice_o == value:
            return
        self._l_windshield_anti_ice_o = value
        if self._l_windshield_anti_ice_o is not None:
            igs.output_set_bool("l_windshield_anti_ice", self._l_windshield_anti_ice_o)

    @property
    def r_windshield_anti_ice_o(self):
        return self._r_windshield_anti_ice_o
    @r_windshield_anti_ice_o.setter
    def r_windshield_anti_ice_o(self, value):
        if hasattr(self, '_r_windshield_anti_ice_o') and self._r_windshield_anti_ice_o == value:
            return
        self._r_windshield_anti_ice_o = value
        if self._r_windshield_anti_ice_o is not None:
            igs.output_set_bool("r_windshield_anti_ice", self._r_windshield_anti_ice_o)
    
    @property
    def exterior_lights_o(self):
        return self._exterior_lights_o
    @exterior_lights_o.setter
    def exterior_lights_o(self, value):
        if hasattr(self, '_exterior_lights_o') and self._exterior_lights_o == value:
            return
        self._exterior_lights_o = value
        if self._exterior_lights_o is not None:
            igs.output_set_int("exterior_lights", self._exterior_lights_o)

    @property
    def anti_coll_lights_o(self):
        return self._anti_coll_lights_o
    @anti_coll_lights_o.setter
    def anti_coll_lights_o(self, value):
        if hasattr(self, '_anti_coll_lights_o') and self._anti_coll_lights_o == value:
            return
        self._anti_coll_lights_o = value
        if self._anti_coll_lights_o is not None:
            igs.output_set_bool("anti_coll_lights", self._anti_coll_lights_o)
            
    @property
    def l_engine_anti_ice_o(self):
        return self._l_engine_anti_ice_o
    @l_engine_anti_ice_o.setter
    def l_engine_anti_ice_o(self, value):
        if hasattr(self, '_l_engine_anti_ice_o') and self._l_engine_anti_ice_o == value:
            return
        self._l_engine_anti_ice_o = value
        if self._l_engine_anti_ice_o is not None:
            igs.output_set_bool("l_engine_anti_ice", self._l_engine_anti_ice_o)

    @property
    def r_engine_anti_ice_o(self):
        return self._r_engine_anti_ice_o
    @r_engine_anti_ice_o.setter
    def r_engine_anti_ice_o(self, value):
        if hasattr(self, '_r_engine_anti_ice_o') and self._r_engine_anti_ice_o == value:
            return
        self._r_engine_anti_ice_o = value
        if self._r_engine_anti_ice_o is not None:
            igs.output_set_bool("r_engine_anti_ice", self._r_engine_anti_ice_o)
    
    @property
    def trim_rudder_o(self):
        return self._trim_rudder_o
    @trim_rudder_o.setter
    def trim_rudder_o(self, value):
        if hasattr(self, '_trim_rudder_o') and self._trim_rudder_o == value:
            return
        self._trim_rudder_o = value
        if self._trim_rudder_o is not None:
            igs.output_set_double("trim_rudder", self._trim_rudder_o)
            
    @property
    def alt_sel_o(self):
        return self._alt_sel_o
    @alt_sel_o.setter
    def alt_sel_o(self, value):
        if hasattr(self, '_alt_sel_o') and self._alt_sel_o == value:
            return
        self._alt_sel_o = value
        if self._alt_sel_o is not None:
            igs.output_set_int("alt_sel", self._alt_sel_o)

    @property
    def heading_sel_o(self):
        return self._heading_sel_o
    @heading_sel_o.setter
    def heading_sel_o(self, value):
        if hasattr(self, '_heading_sel_o') and self._heading_sel_o == value:
            return
        self._heading_sel_o = value
        if self._heading_sel_o is not None:
            igs.output_set_int("heading_sel", self._heading_sel_o)
    
    @property
    def l_bottle_arm_o(self):
        return self._l_bottle_arm_o
    @l_bottle_arm_o.setter
    def l_bottle_arm_o(self, value):
        if hasattr(self, '_l_bottle_arm_o') and self._l_bottle_arm_o == value:
            return
        self._l_bottle_arm_o = value
        if self._l_bottle_arm_o is not None:
            igs.output_set_bool("l_bottle_arm", self._l_bottle_arm_o)

    @property
    def r_bottle_arm_o(self):
        return self._r_bottle_arm_o
    @r_bottle_arm_o.setter
    def r_bottle_arm_o(self, value):
        if hasattr(self, '_r_bottle_arm_o') and self._r_bottle_arm_o == value:
            return
        self._r_bottle_arm_o = value
        if self._r_bottle_arm_o is not None:
            igs.output_set_bool("r_bottle_arm", self._r_bottle_arm_o)

    @property
    def ptt_o(self):
        return self._ptt_o
    @ptt_o.setter
    def ptt_o(self, value):
        if hasattr(self, '_ptt_o') and self._ptt_o == value:
            return
        self._ptt_o = value
        if self._ptt_o is not None:
            igs.output_set_bool("ptt", self._ptt_o)

    @property
    def check_o(self):
        return self._check_o
    @check_o.setter
    def check_o(self, value):
        # For impulsions, just trigger when set
        self._check_o = value
        if self._check_o is not None:
            igs.output_set_impulsion("check")

    @property
    def approve_o(self):
        return self._approve_o
    @approve_o.setter
    def approve_o(self, value):
        # For impulsions, just trigger when set
        self._approve_o = value
        if self._approve_o is not None:
            igs.output_set_impulsion("approve")
            
    @property
    def yoke_hide_o(self):
        return self._yoke_hide_o
    @yoke_hide_o.setter
    def yoke_hide_o(self, value):
        if hasattr(self, '_yoke_hide_o') and self._yoke_hide_o == value:
            return
        self._yoke_hide_o = value
        if self._yoke_hide_o is not None:
            igs.output_set_bool("yoke_hide", self._yoke_hide_o)

    @property
    def autopilot_airspeed_o(self):
        return self._autopilot_airspeed_o
    @autopilot_airspeed_o.setter
    def autopilot_airspeed_o(self, value):
        if hasattr(self, '_autopilot_airspeed_o') and self._autopilot_airspeed_o == value:
            return
        self._autopilot_airspeed_o = value
        if self._autopilot_airspeed_o is not None:
            igs.output_set_double("autopilot_airspeed", self._autopilot_airspeed_o)

    @property
    def com_1_freq_o(self):
        return self._com_1_freq_o
    @com_1_freq_o.setter
    def com_1_freq_o(self, value):
        if hasattr(self, '_com_1_freq_o') and self._com_1_freq_o == value:
            return
        self._com_1_freq_o = value
        if self._com_1_freq_o is not None:
            igs.output_set_int("com_1_freq", self._com_1_freq_o)

    @property
    def elevator_trim_o(self):
        return self._elevator_trim_o
    @elevator_trim_o.setter
    def elevator_trim_o(self, value):
        if hasattr(self, '_elevator_trim_o') and self._elevator_trim_o == value:
            return
        self._elevator_trim_o = value
        if self._elevator_trim_o is not None:
            igs.output_set_double("elevator_trim", self._elevator_trim_o)

    @property
    def aileron_trim_o(self):
        return self._aileron_trim_o
    @aileron_trim_o.setter
    def aileron_trim_o(self, value):
        if hasattr(self, '_aileron_trim_o') and self._aileron_trim_o == value:
            return
        self._aileron_trim_o = value
        if self._aileron_trim_o is not None:
            igs.output_set_double("aileron_trim", self._aileron_trim_o)

    @property
    def fd_pitch_deg_o(self):
        return self._fd_pitch_deg_o
    @fd_pitch_deg_o.setter
    def fd_pitch_deg_o(self, value):
        if hasattr(self, '_fd_pitch_deg_o') and self._fd_pitch_deg_o == value:
            return
        self._fd_pitch_deg_o = value
        if self._fd_pitch_deg_o is not None:
            igs.output_set_double("fd_pitch_deg", self._fd_pitch_deg_o)

    @property
    def paused_o(self):
        return self._paused_o
    @paused_o.setter
    def paused_o(self, value):
        if hasattr(self, '_paused_o') and self._paused_o == value:
            return
        self._paused_o = value
        if self._paused_o is not None:
            igs.output_set_bool("paused", self._paused_o)

    # =========================================================================

    # services
    def receive_values(self, sender_agent_name, sender_agent_uuid, boolV, integer, double, string, data, token, my_data):
        igs.info(f"Service receive_values called by {sender_agent_name} ({sender_agent_uuid}) with argument_list {boolV, integer, double, string, data} and token '{token}''")

    def send_values(self, sender_agent_name, sender_agent_uuid, token, my_data):
        print(f"Service send_values called by {sender_agent_name} ({sender_agent_uuid}), token '{token}' sending values : {self.airspeed_o, self.integerO, self.doubleO, self.stringO, self.dataO}")
        igs.info(sender_agent_uuid, "receive_values", (self.airspeed_o, self.integerO, self.doubleO, self.stringO, self.dataO), token)
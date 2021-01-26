from collections import namedtuple


patch_value = namedtuple("Field", ["name", "type"])


patch_struct = (
    # 0
    ("str_PROG", "4s"),
    ("program_name", "12s"),
    ("keyboard_octave", "B"),
    ("sub_on", "B"),
    ("edit_timbre", "B"),
    ("timbre_type", "B"),
    ("main_sub_balance", "B"),
    ("reserved1", "B"),
    ("main_sub_position", "B"),
    ("split_point", "B"),
    ("bpm", ">H"),
    ("arp_target", "B"),
    ("reserved2", "2B"),
    ("category", "B"),
    ("frequent_upper", ">H"),
    ("frequent_lower", ">H"),
    ("reserved3", "3B"),
    ("amp_velocity", "B"),
    ("portamento_mode", "B"),
    ("reserved4", "B"),
    ("program_level", "B"),
    ("mod_fx_type", "B"),
    ("mod_fx_time", ">H"),
    ("mod_fx_depth", ">H"),
    ("mod_fx_chorus", "B"),
    ("mod_fx_ensemble", "B"),
    ("mod_fx_phaser", "B"),
    ("mod_fx_flanger", "B"),
    ("mod_fx_user", "B"),
    ("micro_tuning", "B"),
    ("scale_key", "B"),
    ("program_tuning", "B"),
    ("program_transpose", "B"),
    ("arp_gate_time", "B"),
    ("arp_rate", "B"),
    ("delay_reverb_dry_wet", ">H"),
    ("reserved5", "3B"),
    ("delay_reverb_type", "B"),
    ("delay_reverb_time", ">H"),
    ("delay_reverb_depth", ">H"),
    ("reverb_sub_type", "B"),
    ("delay_sub_type", "B"),
    ("mod_fx_routing", "B"),
    ("delay_reverb_routing", "B"),
    ("mod_fx_on_off", "B"),
    ("delay_reverb_on_off", "B"),
    ("arp", "B"),
    ("arp_range", "B"),
    ("arp_type", "B"),
    ("like_upper", ">H"),
    ("like_lower", ">H"),
    #80 Timbre 1
    ("portamento_time", "B"),
    ("reserved6", "B"),
    ("voice_spread", "B"),
    ("reserved7", "B"),
    ("voice_mode_depth", ">H"),
    ("voice_mode_type", "B"),
    ("reserved8", "3B"),
    ("vco_1_wave", "B"),
    ("vco_1_octave", "B"),
    ("vco_1_pitch", ">H"),
    ("vco_1_shape", ">H"),
    ("pitch_eg_target", "B"),
    ("pitch_eg_int", ">H"),
    ("vco_2_wave", "B"),
    ("vco_2_octave", "B"),
    ("vco_2_pitch", ">H"),
    ("vco_2_shape", ">H"),
    ("ring_sync", "B"),
    ("cross_mod_depth", ">H"),
    ("multi_routing", "B"),
    ("multi_type", "B"),
    ("multi_octave", "B"),
    ("select_noise", "B"),
    ("select_vpm", "B"),
    ("select_user", "B"),
    ("shape_noise", ">H"),
    ("reserved9", "2B"),
    ("vco_1_level", ">H"),
    ("vco_2_level", ">H"),
    ("multi_level", ">H"),
    ("cutoff", ">H"),
    ("resonance", ">H"),
    ("cutoff_eg_int", ">H"),
    ("cutoff_drive", "B"),
    ("cutoff_keyboard_track", "B"),
    ("low_cut", "B"),
    ("cutoff_velocity", "B"),
    ("amp_eg_attack", ">H"),
    ("amp_eg_decay", ">H"),
    ("amp_eg_sustain", ">H"),
    ("amp_eg_release", ">H"),
    ("eg_attack", ">H"),
    ("eg_decay", ">H"),
    ("eg_sustain", ">H"),
    ("eg_release", ">H"),
    ("lfo_wave", "B"),
    ("lfo_mode", "B"),
    ("lfo_rate", ">H"),
    ("lfo_int", ">H"),
    ("lfo_target", "B"),
    ("mod_wheel_assign", "B"),
    ("e_pedal_assign", "B"),
    ("bend_range_plus", "B",),
    ("bend_range_minus", "B",),
    ("vpm_param1_feedback", "B"),
    ("reserved10", "B"),
    ("vpm_param2_noise_depth", "B"),
    ("reserved11", "B"),
    ("vpm_param3_shapemodint", "B"),
    ("reserved12", "B"),
    ("vpm_param4_mod_attack", "B"),
    ("vpm_param5_mod_decay", "B"),
    ("reserved13", "2B"),
    ("vpm_param6_modkeytrack", "B"),
    ("reserved14", "B"),
    ("user_param1", "B"),
    ("reserved15", "B"),
    ("user_param2", "B"),
    ("reserved16", "B"),
    ("user_param3", "B"),
    ("reserved17", "B"),
    ("user_param4", "B"),
    ("reserved18", "B"),
    ("user_param5", "B"),
    ("reserved19", "B"),
    ("user_param6", "B"),
    ("reserved20", "B"),
    ("user_param5_6_r_r_type", "B"),
    ("user_param1_2_3_4_type", "B"),
    ("shape_vpm", ">H"),
    ("shift_shape_vpm", ">H"),
    ("shape_user", ">H"),
    ("shift_shape_user", ">H"),
    ("mod_wheel_range", "B"),
    ("lfo_key_sync", "B"),
    ("lfo_voice_sync", "B"),
    ("lfo_target_osc", "B"),
    ("eg_legato", "B"),
    ("midi_after_touch_assign", "B"),
    ("reserved21", "5B"),
    #206 Timbre 2
    ("timbre_2", "126B"),
    #332
    ("str_PRED", "4s")
)


normalise_patch = lambda a: a


favorite_template = """\
<?xml version="1.0" encoding="UTF-8"?>

<prologue_Liveset>
  <Bank>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
  </Bank>
  <Bank>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
  </Bank>
  <Bank>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
  </Bank>
  <Bank>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
    <Data>500</Data>
  </Bank>
</prologue_Liveset>
"""

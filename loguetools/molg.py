from loguetools import common
from collections import namedtuple
import copy


patch_value = namedtuple("Field", ["name", "type"])


patch_struct = (
    # 0
    ("str_PROG", "4s"),
    ("program_name", "12s"),
    ("vco_1_pitch_b2_9", "B"),
    ("vco_1_shape_b2_9", "B"),
    ("vco_2_pitch_b2_9", "B"),
    ("vco_2_shape_b2_9", "B"),
    ("vco_1_level_b2_9", "B"),
    ("vco_2_level_b2_9", "B"),
    ("cutoff_b2_9", "B"),
    ("resonance_b2_9", "B"),
    ("eg_attack_b2_9", "B"),
    ("eg_decay_b2_9", "B"),
    ("eg_int_b2_9", "B"),
    ("lfo_rate_b2_9", "B"),
    ("lfo_int_b2_9", "B"),
    ("drive_b2_9", "B"),
    ("vco_1_pitch_shape_octave_wave", "B"),
    ("vco_2_pitch_shape_octave_wave", "B"),
    ("sync_ring_keyboard_octave", "B"),
    ("vco1_lvl_vco2_lvl_cutoff_res", "B"),
    ("eg_type_eg_attack_eg_decay_eg_target", "B"),
    ("eg_int_lfo_rate_lfo_int_drive", "B"),
    ("lfo_type_lfo_mode_lfo_target_seq_trig", "B"),
    ("program_tuning", "B"),
    ("micro_tuning", "B"),
    ("scale_key", "B"),
    ("slide_time", "B"),
    ("portamento_time", "B"),
    ("slider_assign", "B"),
    ("bend_range_plusminus", "B"),
    ("portamento_mode_lfo_bpm_sync_cutoff_velocity_cutoff_key_track", "B"),
    ("program_level", "B"),
    ("amp_velocity", "B"),
    ("reserved1", "B"),
    ("str_SEQD", "4s"),
    #48
    ("bpm", "<H"),
    ("step_length", "B"),
    ("step_resolution", "B"),
    ("swing", "B"),
    ("default_gate_time", "B"),
    ("reserved2", "6B"),
    ("step1_16", "<H"),
    ("step1_16_motion", "<H"),
    ("step1_16_slide", "<H"),
    ("reserved3", "2B"),
    ("motion_slot_1_0_parameter", "B"),
    ("motion_slot_1_1_parameter", "B"),
    ("motion_slot_2_0_parameter", "B"),
    ("motion_slot_2_1_parameter", "B"),
    ("motion_slot_3_0_parameter", "B"),
    ("motion_slot_3_1_parameter", "B"),
    ("motion_slot_4_0_parameter", "B"),
    ("motion_slot_4_1_parameter", "B"),
    ("motion_slot_1_step1_16", "<H"),
    ("motion_slot_2_step1_16", "<H"),
    ("motion_slot_3_step1_16", "<H"),
    ("motion_slot_4_step1_16", "<H"),
    ("reserved4", "8B"),
    # 128
    ("step_01_event_data", "22s"),
    ("step_02_event_data", "22s"),
    ("step_03_event_data", "22s"),
    ("step_04_event_data", "22s"),
    ("step_05_event_data", "22s"),
    ("step_06_event_data", "22s"),
    ("step_07_event_data", "22s"),
    ("step_08_event_data", "22s"),
    ("step_09_event_data", "22s"),
    ("step_10_event_data", "22s"),
    ("step_11_event_data", "22s"),
    ("step_12_event_data", "22s"),
    ("step_13_event_data", "22s"),
    ("step_14_event_data", "22s"),
    ("step_15_event_data", "22s"),
    ("step_16_event_data", "22s"),
)


patch_normalisation = (
    ("vco_1_pitch", "vco_1_pitch_b2_9_FF_2", "vco_1_pitch_shape_octave_wave_03_0"),
    ("vco_1_shape", "vco_1_shape_b2_9_FF_2", "vco_1_pitch_shape_octave_wave_0C_E"),
    ("vco_1_octave", "vco_1_pitch_shape_octave_wave_30_C"),
    ("vco_1_wave", "vco_1_pitch_shape_octave_wave_C0_A"),
    ("vco_2_pitch", "vco_2_pitch_b2_9_FF_2", "vco_2_pitch_shape_octave_wave_03_0"),
    ("vco_2_shape", "vco_2_shape_b2_9_FF_2", "vco_2_pitch_shape_octave_wave_0C_E"),
    ("vco_2_octave", "vco_2_pitch_shape_octave_wave_30_C"),
    ("vco_2_wave", "vco_2_pitch_shape_octave_wave_C0_A"),
    ("ring_sync", "sync_ring_keyboard_octave_03_0"),
    ("keyboard_octave", "sync_ring_keyboard_octave_0C_E"),
    ("vco_1_level", "vco_1_level_b2_9_FF_2", "vco1_lvl_vco2_lvl_cutoff_res_03_0"),
    ("vco_2_level", "vco_2_level_b2_9_FF_2", "vco1_lvl_vco2_lvl_cutoff_res_0C_E"),
    ("cutoff", "cutoff_b2_9_FF_2", "vco1_lvl_vco2_lvl_cutoff_res_30_C"),
    ("resonance", "resonance_b2_9_FF_2", "vco1_lvl_vco2_lvl_cutoff_res_C0_A"),
    ("eg_type", "eg_type_eg_attack_eg_decay_eg_target_03_0"),
    ("eg_attack", "eg_attack_b2_9_FF_2", "eg_type_eg_attack_eg_decay_eg_target_0C_E"),
    ("eg_decay", "eg_decay_b2_9_FF_2", "eg_type_eg_attack_eg_decay_eg_target_30_C"),
    ("eg_target", "eg_type_eg_attack_eg_decay_eg_target_C0_A"),
    ("eg_int", "eg_int_b2_9_FF_2", "eg_int_lfo_rate_lfo_int_drive_03_0"),
    ("lfo_rate", "lfo_rate_b2_9_FF_2", "eg_int_lfo_rate_lfo_int_drive_0C_E"),
    ("lfo_int", "lfo_int_b2_9_FF_2", "eg_int_lfo_rate_lfo_int_drive_30_C"),
    ("drive", "drive_b2_9_FF_2", "eg_int_lfo_rate_lfo_int_drive_C0_A"),
    ("lfo_type", "lfo_type_lfo_mode_lfo_target_seq_trig_03_0"),
    ("lfo_mode", "lfo_type_lfo_mode_lfo_target_seq_trig_0C_E"),
    ("lfo_target", "lfo_type_lfo_mode_lfo_target_seq_trig_30_C"),
    ("seq_trig", "lfo_type_lfo_mode_lfo_target_seq_trig_40_A"),
    ("bend_range_plus", "bend_range_plusminus_0F_0"),
    ("bend_range_minus", "bend_range_plusminus_F0_C"),
    ("portamento_mode", "portamento_mode_lfo_bpm_sync_cutoff_velocity_cutoff_key_track_01_0"),
    ("lfo_bpm_sync", "portamento_mode_lfo_bpm_sync_cutoff_velocity_cutoff_key_track_0C_E"),
    ("cutoff_velocity", "portamento_mode_lfo_bpm_sync_cutoff_velocity_cutoff_key_track_30_C"),
    ("cutoff_kbd_track", "portamento_mode_lfo_bpm_sync_cutoff_velocity_cutoff_key_track_C0_A"),
)


postnormalisation_deletions = (
    "vco_1_pitch_b2_9",
    "vco_1_shape_b2_9",
    "vco_1_pitch_shape_octave_wave",
    "vco_2_pitch_b2_9",
    "vco_2_shape_b2_9",
    "vco_2_pitch_shape_octave_wave",
    "sync_ring_keyboard_octave",
    "vco_1_level_b2_9",
    "vco_2_level_b2_9",
    "cutoff_b2_9",
    "resonance_b2_9",
    "vco1_lvl_vco2_lvl_cutoff_res",
    "eg_attack_b2_9",
    "eg_decay_b2_9",
    "eg_type_eg_attack_eg_decay_eg_target",
    "eg_int_b2_9",
    "lfo_rate_b2_9",
    "lfo_int_b2_9",
    "drive_b2_9",
    "eg_int_lfo_rate_lfo_int_drive",
    "lfo_type_lfo_mode_lfo_target_seq_trig",
    "bend_range_plusminus",
    "portamento_mode_lfo_bpm_sync_cutoff_velocity_cutoff_key_track",
)


def normalise_patch(patch):
    """Expand all encoded fields into a normalised form of patch object. This makes it
    printable and easier to translate. Uses the minilogue_og_patch_normalisation
    translation table:
    ("vco_1_pitch", "vco_1_pitch_b2_9_FF_2", "vco_1_pitch_shape_octave_wave_03_0"),

    Args:
        patch (Patch instance): raw minilogue og patch, read using
            minilogue_og_patch_struct

    Returns:
        Patch instance: Decoded/expanded patch

    """
    norm_patch = copy.deepcopy(patch)
    for t in patch_normalisation:
        # t has form ('dest_name', 'src1_name_XX_x', 'src2_name_XX_x', ...)
        dest_name, *srcs = t
        dest_val = 0
        for s in srcs:
            src_name, mask, shift = decode_src_string(s)
            source_val = getattr(patch, src_name) & mask
            dest_val += common.signed_shift(source_val, shift)
        setattr(norm_patch, dest_name, dest_val)

    # Delete all encoded fields that won't be used anymore
    for t in postnormalisation_deletions:
        delattr(norm_patch, t)

    return norm_patch


def decode_src_string(src_string):
    """Decodes minilogue_og_patch_normalisation tuple src strings.

    The tuples take the form (Note here N >= 1)
    ('dest_name', 'src1_name_XX_x', 'src2_name_XX_x', ..., 'srcN_name_XX_x')

    'src1_name_XX_x' contains 'src1_name', the name of a source field, a hex bit mask XX
    and a 2's-complement single-hex-digit x encoding the number of bits to shift up
    (+ve values) or down (-ve) the masked values before adding them to the destination.

    Args:
        src_string (str): A string of the form described above.

    Returns:
        str: src_name substring
        int: 8-bit bitmask defining a masked region of the src_name field
        int: number of bits by which to shift the masked bit region

    """
    src_parts = src_string.split("_")
    src_name = "_".join(src_parts[:-2])
    mask = int(src_parts[-2], base=16)
    shift = int(src_parts[-1], base=16)
    if shift > 7:
        shift = -(~shift & 7) - 1  # decode negative part of signed 2's complement
    return src_name, mask, shift

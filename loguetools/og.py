import common
import struct
import copy
from collections import namedtuple


patch_value = namedtuple("Field", ["name", "type"])


minilogue_og_patch_struct = (
    # 0
    ("str_PROG", "4s"),
    ("program_name", "12s"),
    ("reserved1", "4B"),
    ("vco_1_pitch_b2_9", "B"),
    ("vco_1_shape_b2_9", "B"),
    ("vco_2_pitch_b2_9", "B"),
    ("vco_2_shape_b2_9", "B"),
    ("cross_mod_depth_b2_9", "B"),
    ("vco_2_pitch_eg_int_b2_9", "B"),
    ("vco_1_level_b2_9", "B"),
    ("vco_2_level_b2_9", "B"),
    ("noise_level_b2_9", "B"),
    ("cutoff_b2_9", "B"),
    ("resonance_b2_9", "B"),
    ("cutoff_eg_int_b2_9", "B"),
    ("reserved2", "B"),
    ("amp_velocity", "B"),
    ("amp_eg_attack_b2_9", "B"),
    ("amp_eg_decay_b2_9", "B"),
    ("amp_eg_sustain_b2_9", "B"),
    ("amp_eg_release_b2_9", "B"),
    ("eg_attack_b2_9", "B"),
    ("eg_decay_b2_9", "B"),
    ("eg_sustain_b2_9", "B"),
    ("eg_release_b2_9", "B"),
    ("lfo_rate_b2_9", "B"),
    ("lfo_int_b2_9", "B"),
    ("reserved3", "5B"),
    ("delay_hi_pass_cutoff_b2_9", "B"),
    # 50
    ("delay_time_b2_9", "B"),
    ("delay_feedback_b2_9", "B"),
    ("vco_1_pitch_shape_octave_wave", "B"),
    ("vco_2_pitch_shape_octave_wave", "B"),
    ("xmod_vco2_pitch_vco1_lvl_vco2_lvl", "B"),
    ("sync_ring_noise_cutoff_res", "B"),
    ("cutoff_params", "B"),
    ("amp_adsr", "B"),
    ("eg_adsr", "B"),
    ("lfo_rate_int_tgt_eg", "B"),
    ("lfo_wave_dly", "B"),
    ("portamento_time", "B"),
    ("delay_b0_1", "B"),
    ("reserved4", "B"),
    ("voice_mode_and_depth_b0_1", "B"),
    ("reserved5", "B"),
    ("bend_range_plusminus", "B"),
    ("reserved6", "2B"),
    ("lfo_portamento_params", "B"),
    ("voice_mode_depth_b2_9", "B"),
    ("program_level", "B"),
    ("slider_assign", "B"),
    ("keyboard_octave", "B"),
    ("reserved7", "22B"),
    ("str_SEQD", "4s"),
    # 100
    ("bpm", "<H"),
    ("reserved8", "B"),
    ("step_length", "B"),
    ("swing", "B"),
    ("default_gate_time", "B"),
    ("step_resolution", "B"),
    ("reserved9", "B"),
    ("step1_16", "<H"),
    ("step1_16_switch", "<H"),
    ("motion_slot_1_parameter", "<H"),
    ("motion_slot_2_parameter", "<H"),
    ("motion_slot_3_parameter", "<H"),
    ("motion_slot_4_parameter", "<H"),
    ("motion_slot_1_step1_16", "<H"),
    ("motion_slot_2_step1_16", "<H"),
    ("motion_slot_3_step1_16", "<H"),
    ("motion_slot_4_step1_16", "<H"),
    # 128
    ("step_1_event_data", "20B"),
    ("step_2_event_data", "20B"),
    ("step_3_event_data", "20B"),
    ("step_4_event_data", "20B"),
    ("step_5_event_data", "20B"),
    ("step_6_event_data", "20B"),
    ("step_7_event_data", "20B"),
    ("step_8_event_data", "20B"),
    ("step_9_event_data", "20B"),
    ("step_10_event_data", "20B"),
    ("step_11_event_data", "20B"),
    ("step_12_event_data", "20B"),
    ("step_13_event_data", "20B"),
    ("step_14_event_data", "20B"),
    ("step_15_event_data", "20B"),
    ("step_16_event_data", "20B"),
)


"""
A translation table for normalising the minilogue OG patch data by combining
fields that are split across different fields. Each tuple takes the form

('dest_name', 'src1_name_XX_x', 'src2_name_XX_x', ..., 'srcN_name_XX_x'), where N >= 1.

'dest_name' is the name of the new field to be created.
'src1_name_XX_x' contains 'src1_name', the name of a source field, a hex bit mask XX and
a 2's-complement single-hex-digit x encoding the number of bits to shift up (+ve values)
or down (-ve) the masked values before adding them to the destination.

+---------------------+----------------------------+-----------------------
|                     |        offset for          |offset for lower 2bits
|  Description        |        upper 8bits         +----------+------------
|                     |                            |   Byte   |    Bit
+---------------------+----------------------------+----------+------------
| VCO 1 PITCH         |20 vco_1_pitch_b2_9         | 52 vco_1_pitch_shape_octave_wave |0~1|
| VCO 1 SHAPE         |21 vco_1_shape_b2_9         | 52 vco_1_pitch_shape_octave_wave |2~3|
| VCO 2 PITCH         |22 vco_2_pitch_b2_9         | 53 vco_2_pitch_shape_octave_wave |0~1|
| VCO 2 SHAPE         |23 vco_2_shape_b2_9         | 53 vco_2_pitch_shape_octave_wave |2~3|
| CROSS MOD DEPTH     |24 cross_mod_depth_b2_9     | 54 xmod_vco2_pitch_vco1_lvl_vco2_lvl |0~1|
| VCO 2 PITCH EG INT  |25 vco_2_pitch_eg_int_b2_9  | 54 xmod_vco2_pitch_vco1_lvl_vco2_lvl |2~3|
| VCO 1 LEVEL         |26 vco_1_level_b2_9         | 54 xmod_vco2_pitch_vco1_lvl_vco2_lvl |4~5|
| VCO 2 LEVEL         |27 vco_2_level_b2_9         | 54 xmod_vco2_pitch_vco1_lvl_vco2_lvl |6~7|
| NOISE LEVEL         |28 noise_level_b2_9         | 55 sync_ring_noise_cutoff_res |2~3|
| CUTOFF              |29 cutoff_b2_9              | 55 sync_ring_noise_cutoff_res |4~5|
| RESONANCE           |30 resonance_b2_9           | 55 sync_ring_noise_cutoff_res |6~7|
| CUTOFF EG INT       |31 cutoff_eg_int_b2_9       | 56 cutoff_params |0~1|
| AMP EG ATTACK       |34 amp_eg_attack_b2_9       | 57 amp_adsr |0~1|
| AMP EG DECAY        |35 amp_eg_decay_b2_9        | 57 amp_adsr |2~3|
| AMP EG SUSTAIN      |36 amp_eg_sustain_b2_9      | 57 amp_adsr |4~5|
| AMP EG RELEASE      |37 amp_eg_release_b2_9      | 57 amp_adsr |6~7|
| AMP ATTACK          |38 eg_attack_b2_9           | 58 eg_adsr |0~1|
| AMP DECAY           |39 eg_decay_b2_9            | 58 eg_adsr |2~3|
| AMP SUSTAIN         |40 eg_sustain_b2_9          | 58 eg_adsr |4~5|
| AMP RELEASE         |41 eg_release_b2_9          | 58 eg_adsr |6~7| !Note: Korg docs say 59
| LFO RATE            |42 lfo_rate_b2_9            | 60 lfo_wave_dly |0~1|
| LFO INT             |43 lfo_int_b2_9             | 60 lfo_wave_dly |2~3|
| DELAY HI PASS CUTOFF|49 delay_hi_pass_cutoff_b2_9| 62 delay_b0_1 |2~3|
| DELAY TIME          |50 delay_time_b2_9          | 62 delay_b0_1 |4~5|
| DELAY FEEDBACK      |51 delay_feedback_b2_9      | 62 delay_b0_1 |6~7|
| VOICE MODE DEPTH    |70 voice_mode_depth_b2_9    | 64 voice_mode |4~5|
+---------------------+----------------------------+----------+------------
"""


minilogue_og_patch_normalisation = (
    ("vco_1_pitch", "vco_1_pitch_b2_9_FF_2", "vco_1_pitch_shape_octave_wave_03_0"),
    ("vco_1_shape", "vco_1_shape_b2_9_FF_2", "vco_1_pitch_shape_octave_wave_0C_E"),
    ("vco_1_octave", "vco_1_pitch_shape_octave_wave_30_C"),
    ("vco_1_wave", "vco_1_pitch_shape_octave_wave_C0_A"),
    ("vco_2_pitch", "vco_2_pitch_b2_9_FF_2", "vco_2_pitch_shape_octave_wave_03_0"),
    ("vco_2_shape", "vco_2_shape_b2_9_FF_2", "vco_2_pitch_shape_octave_wave_0C_E"),
    ("vco_2_octave", "vco_2_pitch_shape_octave_wave_30_C"),
    ("vco_2_wave", "vco_2_pitch_shape_octave_wave_C0_A"),
    ("cross_mod_depth", "cross_mod_depth_b2_9_FF_2", "xmod_vco2_pitch_vco1_lvl_vco2_lvl_03_0"),
    ("vco_2_pitch_eg_int", "vco_2_pitch_eg_int_b2_9_FF_2", "xmod_vco2_pitch_vco1_lvl_vco2_lvl_0C_E"),
    ("vco_1_level", "vco_1_level_b2_9_FF_2", "xmod_vco2_pitch_vco1_lvl_vco2_lvl_30_C"),
    ("vco_2_level", "vco_2_level_b2_9_FF_2", "xmod_vco2_pitch_vco1_lvl_vco2_lvl_C0_A"),
    ("noise_level", "noise_level_b2_9_FF_2", "sync_ring_noise_cutoff_res_0C_E"),
    ("cutoff", "cutoff_b2_9_FF_2", "sync_ring_noise_cutoff_res_30_C"),
    ("resonance", "resonance_b2_9_FF_2", "sync_ring_noise_cutoff_res_C0_A"),
    ("sync", "sync_ring_noise_cutoff_res_01_0"),
    ("ring", "sync_ring_noise_cutoff_res_02_F"),
    ("cutoff_eg_int", "cutoff_eg_int_b2_9_FF_2", "cutoff_params_03_0"),
    ("cutoff_velocity", "cutoff_params_0C_E"),
    ("cutoff_kbd_track", "cutoff_params_30_C"),
    ("cutoff_type", "cutoff_params_40_A"),
    ("amp_eg_attack", "amp_eg_attack_b2_9_FF_2", "amp_adsr_03_0"),
    ("amp_eg_decay", "amp_eg_decay_b2_9_FF_2", "amp_adsr_0C_E"),
    ("amp_eg_sustain", "amp_eg_sustain_b2_9_FF_2", "amp_adsr_30_C"),
    ("amp_eg_release", "amp_eg_release_b2_9_FF_2", "amp_adsr_C0_A"),
    ("amp_attack", "eg_attack_b2_9_FF_2", "eg_adsr_03_0"),
    ("amp_decay", "eg_decay_b2_9_FF_2", "eg_adsr_0C_E"),
    ("amp_sustain", "eg_sustain_b2_9_FF_2", "eg_adsr_30_C"),
    ("amp_release", "eg_release_b2_9_FF_2", "eg_adsr_C0_A"),
    ("lfo_rate", "lfo_rate_b2_9_FF_2", "lfo_rate_int_tgt_eg_03_0"),
    ("lfo_int", "lfo_int_b2_9_FF_2", "lfo_rate_int_tgt_eg_0C_E"),
    ("lfo_target", "lfo_rate_int_tgt_eg_30_C"),
    ("lfo_eg", "lfo_rate_int_tgt_eg_C0_A"),
    ("lfo_wave", "lfo_wave_dly_03_0"),
    ("delay_output_routing", "lfo_wave_dly_C0_A"),
    ("delay_hi_pass_cutoff", "delay_hi_pass_cutoff_b2_9_FF_2", "delay_b0_1_0C_E"),
    ("delay_time", "delay_time_b2_9_FF_2", "delay_b0_1_30_C"),
    ("delay_feedback", "delay_feedback_b2_9_FF_2", "delay_b0_1_C0_A"),
    ("voice_mode", "voice_mode_and_depth_b0_1_07_0"),
    ("voice_mode_depth", "voice_mode_depth_b2_9_FF_2", "voice_mode_and_depth_b0_1_30_C"),
    ("bend_range_plus", "bend_range_plusminus_0F_0"),
    ("bend_range_minus", "bend_range_plusminus_F0_C"),
    ("lfo_key_sync", "lfo_portamento_params_01_0"),
    ("lfo_bpm_sync", "lfo_portamento_params_02_F"),
    ("lfo_voice_sync", "lfo_portamento_params_04_E"),
    ("portamento_bpm", "lfo_portamento_params_08_D"),
    ("portamento_mode", "lfo_portamento_params_10_C"),
)


minilogue_og_postnormalisation_deletions = (
    "vco_1_pitch_b2_9",
    "vco_1_shape_b2_9",
    "vco_1_pitch_shape_octave_wave",
    "vco_2_pitch_b2_9",
    "vco_2_shape_b2_9",
    "vco_2_pitch_shape_octave_wave",
    "cross_mod_depth_b2_9",
    "vco_2_pitch_eg_int_b2_9",
    "vco_1_level_b2_9",
    "vco_2_level_b2_9",
    "noise_level_b2_9",
    "cutoff_b2_9",
    "resonance_b2_9",
    "cutoff_eg_int_b2_9",
    "amp_eg_attack_b2_9",
    "amp_eg_decay_b2_9",
    "amp_eg_sustain_b2_9",
    "amp_eg_release_b2_9",
    "eg_attack_b2_9",
    "eg_decay_b2_9",
    "eg_sustain_b2_9",
    "eg_release_b2_9",
    "lfo_rate_b2_9",
    "lfo_int_b2_9",
    "delay_hi_pass_cutoff_b2_9",
    "delay_time_b2_9",
    "delay_feedback_b2_9",
    "delay_b0_1",
    "voice_mode_depth_b2_9",
    "voice_mode_and_depth_b0_1",
    "bend_range_plusminus",
    "xmod_vco2_pitch_vco1_lvl_vco2_lvl",
    "sync_ring_noise_cutoff_res",
    "cutoff_params",
    "amp_adsr",
    "eg_adsr",
    "lfo_rate_int_tgt_eg",
    "lfo_wave_dly",
    "lfo_portamento_params",
)


def normalise_og_patch(patch):
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
    for t in minilogue_og_patch_normalisation:
        # t has form ('dest_name', 'src1_name_XX_x', 'src2_name_XX_x', ...)
        dest_name, *srcs = t
        dest_val = 0
        for s in srcs:
            src_name, mask, shift = decode_src_string(s)
            source_val = getattr(patch, src_name) & mask
            dest_val += common.signed_shift(source_val, shift)
        setattr(norm_patch, dest_name, dest_val)

    # Delete all encoded fields that won't be used anymore
    for t in minilogue_og_postnormalisation_deletions:
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


"""
Korg's program format tables for the minilogue original (OG).
Any personal notes are designated Gn.

Minilogue OG
+-------+-------+---------+---------------------------------------------+
| Offset|  Bit  |  Range  |  Description                                |
+-------+-------+---------+---------------------------------------------+
|  0~3  |       |  ASCII  |  'PROG'                                     |
+-------+-------+---------+---------------------------------------------+
|  4~15 |       |  ASCII  |  PROGRAM NAME [12]                          |
+-------+-------+---------+---------------------------------------------+
| 16~19 |       |         |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
|  20   |  0~7  |         |  VCO 1 PITCH (bit2~9)           *note P1,P2 |
+-------+-------+---------+---------------------------------------------+
|  21   |  0~7  |         |  VCO 1 SHAPE (bit2~9)              *note P1 |
+-------+-------+---------+---------------------------------------------+
|  22   |  0~7  |         |  VCO 2 PITCH (bit2~9)           *note P1,P2 |
+-------+-------+---------+---------------------------------------------+
|  23   |  0~7  |         |  VCO 2 SHAPE (bit2~9)              *note P1 |
+-------+-------+---------+---------------------------------------------+
|  24   |  0~7  |         |  CROSS MOD DEPTH (bit2~9)          *note P1 |
+-------+-------+---------+---------------------------------------------+
|  25   |  0~7  |         |  VCO 2 PITCH EG INT (bit2~9)    *note P1,P3 |
+-------+-------+---------+---------------------------------------------+
|  26   |  0~7  |         |  VCO 1 LEVEL (bit2~9)              *note P1 |
+-------+-------+---------+---------------------------------------------+
|  27   |  0~7  |         |  VCO 2 LEVEL (bit2~9)              *note P1 |
+-------+-------+---------+---------------------------------------------+
|  28   |  0~7  |         |  NOISE LEVEL (bit2~9)              *note P1 |
+-------+-------+---------+---------------------------------------------+
|  29   |  0~7  |         |  CUTOFF (bit2~9)                   *note P1 |
+-------+-------+---------+---------------------------------------------+
|  30   |  0~7  |         |  RESONANCE (bit2~9)                *note P1 |
+-------+-------+---------+---------------------------------------------+
|  31   |  0~7  |         |  CUTOFF EG INT (bit2~9)         *note P1,P4 |
+-------+-------+---------+---------------------------------------------+
|  32   |       |         |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
|  33   |  0~7  |  0~127  |  Amp Velocity                               |
+-------+-------+---------+---------------------------------------------+
|  34   |  0~7  |         |  AMP EG ATTACK (bit2~9)            *note P1 |
+-------+-------+---------+---------------------------------------------+
|  35   |  0~7  |         |  AMP EG DECAY (bit2~9)             *note P1 |
+-------+-------+---------+---------------------------------------------+
|  36   |  0~7  |         |  AMP EG SUSTAIN (bit2~9)           *note P1 |
+-------+-------+---------+---------------------------------------------+
|  37   |  0~7  |         |  AMP EG RELEASE (bit2~9)           *note P1 |
+-------+-------+---------+---------------------------------------------+
|  38   |  0~7  |         |  EG ATTACK (bit2~9)                *note P1 |
+-------+-------+---------+---------------------------------------------+
|  39   |  0~7  |         |  EG DECAY (bit2~9)                 *note P1 |
+-------+-------+---------+---------------------------------------------+
|  40   |  0~7  |         |  EG SUSTAIN (bit2~9)               *note P1 |
+-------+-------+---------+---------------------------------------------+
|  41   |  0~7  |         |  EG RELEASE (bit2~9)               *note P1 |
+-------+-------+---------+---------------------------------------------+
|  42   |  0~7  |         |  LFO RATE (bit2~9)              *note P1,P5 |
+-------+-------+---------+---------------------------------------------+
|  43   |  0~7  |         |  LFO INT (bit2~9)                  *note P1 |
+-------+-------+---------+---------------------------------------------+
| 44~48 |       |         |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
|  49   |  0~7  |         |  DELAY HI PASS CUTOFF (bit2~9)     *note P1 |
+-------+-------+---------+---------------------------------------------+
|  50   |  0~7  |         |  DELAY TIME (bit2~9)               *note P1 |
+-------+-------+---------+---------------------------------------------+
|  51   |  0~7  |         |  DELAY FEEDBACK (bit2~9)           *note P1 |
+-------+-------+---------+---------------------------------------------+
|  52   |  0~1  |         |  VCO 1 PITCH (bit0~1)           *note P1,P2 |
|       |  2~3  |         |  VCO 1 SHAPE (bit0~1)              *note P1 |
|       |  4~5  |  0~3    |  VCO 1 OCTAVE              0~3=16',8',4',2' |
|       |  6~7  |  0~2    |  VCO 1 WAVE                        *note P6 |
+-------+-------+---------+---------------------------------------------+
|  53   |  0~1  |         |  VCO 2 PITCH (bit0~1)           *note P1,P2 |
|       |  2~3  |         |  VCO 2 SHAPE (bit0~1)              *note P1 |
|       |  4~5  |  0~3    |  VCO 2 OCTAVE              0~3=16',8',4',2' |
|       |  6~7  |  0~2    |  VCO 2 WAVE                        *note P6 |
+-------+-------+---------+---------------------------------------------+
|  54   |  0~1  |         |  CROSS MOD DEPTH (bit0~1)          *note P1 |
|       |  2~3  |         |  VCO 2 PITCH EG INT (bit0~1)    *note P1,P3 |
|       |  4~5  |         |  VCO 1 LEVEL (bit0~1)              *note P1 |
|       |  6~7  |         |  VCO 2 LEVEL (bit0~1)              *note P1 |
+-------+-------+---------+---------------------------------------------+
|  55   |   0   |  0,1    |  SYNC                            0,1=Off,On |
|       |   1   |  0,1    |  RING                            0,1=Off,On |
|       |  2~3  |         |  NOISE LEVEL (bit0~1)              *note P1 |
|       |  4~5  |         |  CUTOFF (bit0~1)                   *note P1 |
|       |  6~7  |         |  RESONANCE (bit0~1)                *note P1 |
+-------+-------+---------+---------------------------------------------+
|  56   |  0~1  |         |  CUTOFF EG INT (bit0~1)         *note P1,P4 |
|       |  2~3  |  0~2    |  CUTOFF VELOCITY                  *note P10 |
|       |  4~5  |  0~2    |  CUTOFF KEYBOARD TRACK            *note P10 |
|       |   6   |  0,1    |  CUTOFF TYPE              0,1=2-POLE,4-POLE |
|       |   7   |  0,1    |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
|  57   |  0~1  |         |  AMP EG ATTACK (bit0~1)            *note P1 |
|       |  2~3  |         |  AMP EG DECAY (bit0~1)             *note P1 |
|       |  4~5  |         |  AMP EG SUSTAIN (bit0~1)           *note P1 |
|       |  6~7  |         |  AMP EG RELEASE (bit0~1)           *note P1 |
+-------+-------+---------+---------------------------------------------+
|  58   |  0~1  |         |  EG ATTACK (bit0~1)                *note P1 |
|       |  2~3  |         |  EG DECAY (bit0~1)                 *note P1 |
|       |  4~5  |         |  EG SUSTAIN (bit0~1)               *note P1 |
|       |  6~7  |         |  EG RELEASE (bit0~1)               *note P1 |
+-------+-------+---------+---------------------------------------------+
|  59   |  0~1  |         |  LFO RATE (bit0~1)              *note P1,P5 |
|       |  2~3  |         |  LFO INT (bit0~1)                  *note P1 |
|       |  4~5  |  0~2    |  LFO TARGET                        *note P7 |
|       |  6~7  |  0~2    |  LFO EG                            *note P8 |
+-------+-------+---------+---------------------------------------------+
|  60   |  0~1  |  0~2    |  LFO WAVE                          *note P6 |
|       |  2~5  |         |  Reserved                                   |
|       |  6~7  |  0~2    |  DELAY OUTPUT ROUTING              *note P9 |
+-------+-------+---------+---------------------------------------------+
|  61   |  0~7  |  0~128  |  Portament Time          0,1~129=OFF,0~128  |
+-------+-------+---------+---------------------------------------------+
|  62   |  0~1  |         |  Reserved                                   |
|       |  2~3  |         |  DELAY HI PASS CUTOFF (bit0~1)     *note P1 |
|       |  4~5  |         |  DELAY TIME (bit0~1)               *note P1 |
|       |  6~7  |         |  DELAY FEEDBACK (bit0~1)           *note P1 |
+-------+-------+---------+---------------------------------------------+
|  63   |       |         |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
|  64   |  0~2  |  0~7    |  VOICE MODE                       *note P11 |
|       |   3   |         |  Reserved                                   |
|       |  4~5  |         |  VOICE MODE DEPTH (bit0~1)     *note P1,P12 |
|       |  6~7  |         |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
|  65   |       |         |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
|  66   |  0~3  |  1~12   |  Bend Range (+)                       1~12  |
|       |  4~7  |  1~12   |  Bend Range (-)                       1~12  |
+-------+-------+---------+---------------------------------------------+
| 67~68 |       |         |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
|  69   |   0   |  0,1    |  LFO Key Sync                    0,1=Off,On |
|       |   1   |  0,1    |  LFO BPM Sync                    0,1=Off,On |
|       |   2   |  0,1    |  LFO Voice Sync                  0,1=Off,On |
|       |   3   |  0,1    |  Portament BPM                   0,1=Off,On |
|       |   4   |  0,1    |  Portament Mode                 0,1=Auto,On |
|       |  5~7  |         |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
|  70   |  0~7  |         |  VOICE MODE DEPTH (bit2~9)     *note P1,P12 |
+-------+-------+---------+---------------------------------------------+
|  71   |  0~7  | 77~127  |  Program Level               77~127=-25~+25 |
+-------+-------+---------+---------------------------------------------+
|  72   |  0~7  |  0~79   |  Slider Assign                    *note P13 |
+-------+-------+---------+---------------------------------------------+
|  73   |  0~2  |  0~4    |  KEYBOARD OCTAVE                  0~4=-2~+2 |
+-------+-------+---------+---------------------------------------------+
| 74~95 |       |         |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
| 96~99 |       | ASCII   |  'SEQD'                                     |
+-------+-------+---------+---------------------------------------------+
|  100  | L:0~7 |100~3000 |  BPM                    100~3000=10.0~300.0 |
|  101  | H:0~3 |         |                                             |
+-------+-------+---------+---------------------------------------------+
|  102  |       |         |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
|  103  |       |  1~16   |  Step Length                                |
+-------+-------+---------+---------------------------------------------+
|  104  |       | -75~+75 |  Swing                                      |
+-------+-------+---------+---------------------------------------------+
|  105  |       |  0~72   |  Default Gate Time             0~72=0%~100% |
+-------+-------+---------+---------------------------------------------+
|  106  |       |  0~4    |  Step Resolution                   *note S1 |
+-------+-------+---------+---------------------------------------------+
|  107  |       |         |  Reserved                                   |
+-------+-------+---------+---------------------------------------------+
|  108  |   0   |   0,1   |  Step  1 Off/On                  0,1=Off,On |
|  108  |   1   |   0,1   |  Step  2 Off/On                  0,1=Off,On |
|  108  |   2   |   0,1   |  Step  3 Off/On                  0,1=Off,On |
|  108  |   3   |   0,1   |  Step  4 Off/On                  0,1=Off,On |
|  108  |   4   |   0,1   |  Step  5 Off/On                  0,1=Off,On |
|  108  |   5   |   0,1   |  Step  6 Off/On                  0,1=Off,On |
|  108  |   6   |   0,1   |  Step  7 Off/On                  0,1=Off,On |
|  108  |   7   |   0,1   |  Step  8 Off/On                  0,1=Off,On |
+-------+-------+---------+---------------------------------------------+
|  109  |   0   |   0,1   |  Step  9 Off/On                  0,1=Off,On |
|  109  |   1   |   0,1   |  Step 10 Off/On                  0,1=Off,On |
|  109  |   2   |   0,1   |  Step 11 Off/On                  0,1=Off,On |
|  109  |   3   |   0,1   |  Step 12 Off/On                  0,1=Off,On |
|  109  |   4   |   0,1   |  Step 13 Off/On                  0,1=Off,On |
|  109  |   5   |   0,1   |  Step 14 Off/On                  0,1=Off,On |
|  109  |   6   |   0,1   |  Step 15 Off/On                  0,1=Off,On |
|  109  |   7   |   0,1   |  Step 16 Off/On                  0,1=Off,On |
+-------+-------+---------+---------------------------------------------+
|  110  |       |         |  Step 1~8 Switch                   *note S2 |
+-------+-------+---------+---------------------------------------------+
|  111  |       |         |  Step 9~16 Switch                  *note S2 |
+-------+-------+---------+---------------------------------------------+
|112~113|       |         |  Motion Slot 1 Parameter           *note S3 |
+-------+-------+---------+---------------------------------------------+
|114~115|       |         |  Motion Slot 2 Parameter           *note S3 |
+-------+-------+---------+---------------------------------------------+
|116~117|       |         |  Motion Slot 3 Parameter           *note S3 |
+-------+-------+---------+---------------------------------------------+
|118~119|       |         |  Motion Slot 4 Parameter           *note S3 |
+-------+-------+---------+---------------------------------------------+
|  120  |   0   |         |  Motion Slot 1 Step  1 Off/On    0,1=Off,On |
|  120  |   1   |         |  Motion Slot 1 Step  2 Off/On    0,1=Off,On |
|  120  |   2   |         |  Motion Slot 1 Step  3 Off/On    0,1=Off,On |
|  120  |   3   |         |  Motion Slot 1 Step  4 Off/On    0,1=Off,On |
|  120  |   4   |         |  Motion Slot 1 Step  5 Off/On    0,1=Off,On |
|  120  |   5   |         |  Motion Slot 1 Step  6 Off/On    0,1=Off,On |
|  120  |   6   |         |  Motion Slot 1 Step  7 Off/On    0,1=Off,On |
|  120  |   7   |         |  Motion Slot 1 Step  8 Off/On    0,1=Off,On |
+-------+-------+---------+---------------------------------------------+
|  121  |   0   |         |  Motion Slot 1 Step  9 Off/On    0,1=Off,On |
|  121  |   1   |         |  Motion Slot 1 Step 10 Off/On    0,1=Off,On |
|  121  |   2   |         |  Motion Slot 1 Step 11 Off/On    0,1=Off,On |
|  121  |   3   |         |  Motion Slot 1 Step 12 Off/On    0,1=Off,On |
|  121  |   4   |         |  Motion Slot 1 Step 13 Off/On    0,1=Off,On |
|  121  |   5   |         |  Motion Slot 1 Step 14 Off/On    0,1=Off,On |
|  121  |   6   |         |  Motion Slot 1 Step 15 Off/On    0,1=Off,On |
|  121  |   7   |         |  Motion Slot 1 Step 16 Off/On    0,1=Off,On |
+-------+-------+---------+---------------------------------------------+
|122~123|       |         |  Motion Slot 2 Step Off/On (same as Slot 1) |
+-------+-------+---------+---------------------------------------------+
|124~125|       |         |  Motion Slot 3 Step Off/On (same as Slot 1) |
+-------+-------+---------+---------------------------------------------+
|126~127|       |         |  Motion Slot 4 Step Off/On (same as Slot 1) |
+-------+-------+---------+---------------------------------------------+
|128~147|       |         |  Step 1 Event Data                 *note S4 |
|148~167|       |         |  Step 2 Event Data                 *note S4 |
|   :   |       |         |                                             |
|   :   |       |         |                                             |
|428~447|       |         |  Step 16 Event Data                *note S4 |
+-------+-------+---------+---------------------------------------------+

"""

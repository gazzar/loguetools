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


factory_presets = """\
180c3f3e6fbdcaf6615533482088bca0 <afx acid3>
72719a57f2c949bc68eb6199edcd7152 Injection
91ef375c689f96f74cf850ad9682ff04 Anfem
27f560ed0f1c7e6bc5234b4bd481bad0 <wavetable>
f20bb671b115dd064f87da357f0cfe56 Lu-Fuki
fe63347344d218e17f1bf3781521873e Fake3OSC
22afc99dc25c701cc3e6c43b06814a35 Arc Lead   
e0cd5bcc803a964f5d37633ab00de6fb <Flute>
4df60cff635237328a91f545a6d2323c Scoooping
516922632ff1cdd7332ca7672c8015c8 Robot Empire
097afef62e22d21fe1c8b2c5007ece6d TeeVeeSaw
55468103540a342cc2463fe2a19f81bc <AFX> bAss 
6d05864ea32ef83fb9ed5aa23ff4bfdc <model 800>
644e3bfae19f3fcfd26a31ea695daa4c <epic acid>
f77dbc7568ae8cd70b7d382a211bd76e Herd Of Crab
e869d02fcfb69080d56f37be982240de Stonecold
92ca0d867eac86c6a3f117e625b3c18e Dirty Sub
03df35eb7dc4c823429cb70338dc6ade Jungle Sub
429da32166baf866661d5e6471cb6aaa <deep bass>
dc3f20417692b7c5781c1e48645608df Hoodie Bass
b95435a40c1f4925f51e95e5c85e459f StabbyBass
0c31c7a7ef861fb7d04b4cea20b0c7c1 DistortedSqr
0e8c55f4df179fd11a9c6ea9657b7c43 Werq
f88fe8afa7fb07e6ef0ae682e479beda <Ratewobble
3e0e9148ba1ecf89e1cceef989d32ec6 StomachWave
79c5735b4ec3b643561c6517830d7491 Dr.Juice
9e2dec4a010d9e71cfd78a9276135531 Rubber Duck
32034afb67701eb39b76975912769d44 <HarmonBa> 
97ece84afb73e249bb9a3b21f5a9c0c4 Dark Perc
c7f8e3a54e8d7f192617d26336c5c126 Jackathon
9147f4113d3f44912597400071ee663d Bosshog
3c9c19f7b9b78d7c784e7e63cd08f73d <Ardkore92>
2a0b7d6bc50141d0be900da23fdf5032 <aliasBass>
b8015115b65c52c6a08818f664edd9b4 <PWM envBA>
4ca712033cef3fac38af141f56835661 Disemvowel
2e94118692bed98581dfa15e456e7775 Kickin'B
f064e6f84d9836c538a647f4b53b4798 OIOI
7be3359cbe485c43ac0d65269e51b461 <akunk b>  
6212e6db045097ed725500d06927663b Dual Saw
4e0af205343b79fa3a60bec9c895fe32 BitterLead
80a988854c54a01829030c6c459e01de Syncwave
eb446a88e09fc6e5e3c2dffbbd912928 <Duophony> 
fe1545e00f6c674d7a2ce21b83df06fe Mono Brass
1d9236bdab22e344c4c030a6ca982f9f <5th brASs>
77fdf12199d8fc606b23eb7cbcb259bb Bouncy Balls
26e6ed4886d9d40bb43e8800cf3f4254 Ghost Town
e12c48184b31af53968229f0e7c7e858 Childhood
b83847e748df46718e30eaf96d7ba93d On the Moon
d83a7d2e9b2f7bdb563ef1fcdb0ba6c5 <phaseClks>
a9bc81d7de51ac7165a1cd616b10898a <SyncMtion>
0a385f731e1a29c889c4e402f25b82d3 <SyncLAM>  
be0d9e18339a8c7a0dd78927173683ce Arpme Lead
60f079ff0e7579e877a497ca99fbd22c Squelf
50151a1211f69236d18b3f6806142bc8 Milky Way
e9ee01f2816b68356105f7d0f643bb00 BrokenArcade
88a6567af77ec64a27643173f0031811 <MT-digArp>
5ba74dc530e2f6e8b132b017ecd8ed37 Chopchoon
5bd0df85ff1978ca20647238033abc2b FMod Seq
568aef3852e885b3826112f460e16520 TronIines  
dba2833ffd5b42a96b8a2c18370f35f8 Tech Stab
338e14ab201409b749238f5e38b61390 Pumpdriver
e950093ad8f6a960e1a1509aca88c22b Lfoiled
e43a98c2551c32edbbdcd31e3fcb0ac5 < Digisnd >
d9f80e8631f2debeaff1c987c639cd55 <ascension>
9165a176f1beae1756a8b48062b12590 <centipede>
702781efa069c988a174097489647278 Robotspeak
44e854b5c426a26158c1d4edab0fc7c3 Cpu Cycles
cc9b5625cfbd6613ac706844724b103c Loud Siren
0c8cb897b502d0b200af569f0cbc9704 Portrythm
9323d1669689871260e0cbeb5197f886 Dambuster
1156c0b0a17afc4c5fabab1598c38ff7 <xoc PLAY> 
1f1cbc6ce3e8afe34d30c2c976b9fefa LittleGlitch
afd746cbb3099a6ada981188cbe4cc11 Hard Run
92c54d799e62c701983b293176b66a90 <beat&bass>
7d6190780551e3532d372af97faa624a <bnsbeats1>
60136a93b193be9b5e5b3759767fc779 <bnsbeats2>
9a22e36c7774a194f9a3c455b47d901f <bnsbeats3>
2f73b823b4e9080608b1543d69b5034c <bnsbeats4>
f4fcb598813b457af78e921fcf5ebc80 <bnsbeats5>
4c39f2abcf25898fcd4cf6c22d929ce5 <afx beat> 
"""
factory_hashes = [l.split()[0] for l in factory_presets.splitlines()]
from loguetools import common
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
    # 128
    ("step_01_event_data", "20s"),
    ("step_02_event_data", "20s"),
    ("step_03_event_data", "20s"),
    ("step_04_event_data", "20s"),
    ("step_05_event_data", "20s"),
    ("step_06_event_data", "20s"),
    ("step_07_event_data", "20s"),
    ("step_08_event_data", "20s"),
    ("step_09_event_data", "20s"),
    ("step_10_event_data", "20s"),
    ("step_11_event_data", "20s"),
    ("step_12_event_data", "20s"),
    ("step_13_event_data", "20s"),
    ("step_14_event_data", "20s"),
    ("step_15_event_data", "20s"),
    ("step_16_event_data", "20s"),
)


factory_presets = """\
b4ceaf3fcc1b4663c24f1f5c605dc636 PolyLogue
78c8cda29abb09948a27e3d2729b63f2 PWM Strings
732c0d84bf9ec3343bf2942775ec3cb7 Flutter Pad
c8be8bb08eef83696b4b1909a05da3d3 TraxBass
88df7c272279a5af245a332de812ac97 Ultra Low
c13166171ad0a492c8def521622a9c8c Stardom Lead
ba8689bb2210d0912034c00808b19ede Fluctuation
917b584dbf7351f4462e512a260b39eb King Cheetah
0a2c87f36cc435d4e772753ca5c8b900 PolySeek
a5096fa8b755fdd87b64a4e704008ba4 Magic Spells
7d62870f00d8913de72e4c47d9fdccae Stabber
909a0cde6d11fb301b9e5dff5212c8d5 S.F. Key    
b2ac467dc2988c6ebda0758dd8fe2943 Late Summer
386536f45b84ffb410808dc7e484624d Scuba Diving
0965c83f5525f1e139387e6d2af4ab9e Soft Brass
8f45c792bdca6117f1f16a26f6af9196 Wah CIav
27751de67a03c305007bbdbd0a0afbed FilterMotion
3098217a4762579f5463d6bd09f062c8 Sing(bout u)
0c792e6227f87a9cf6193255ee5e6725 PluckMouse
54c20cb52ce6a083fa075a95d040aa4f PopperSynth
27596b968643e4d9a7d0cd02feadc3c6 Cosmic Love
d5eac5a9350e1aa7cb4001f0e70bb3dc Louge Pad
4b747ceb7be07dc704f4839c326cff90 Pulse Pad
0a8062f5bc65a6c93c03173a73a1d579 Liquid Pad
6f411fb3e381b3920e7669eaccd07326 Prospero
98591ae64a3da55184d79496ea360017 Burn Low
27c8e395e6e4b8fd86aabfae3ef4e8b6 Polymonk
aa86ad66e18982cd8a0b389bc0b0e233 Yes or No
547cadb29a607812a4dd171d39831f86 OuterSpace
1f282632efa7ff019481a33c5c2e6a37 Morning Gt.
5ba414907dad2c31457d2d7826516967 Ugly Ducking
bb2456b1e38a419f8724e1acc97107bd Unwilling
af63d5be7d264c20c773031a38daa782 Mountain
758ba81a6ce6bda7e5028bdbb29fa7a1 Old Elba
ad466ffd78270089916903cece3f9562 Lipstick
6ce4e3207fa3b3ecc35dc1bd5342f2c1 Rubber Band
650249bec2186132c5910bbb179edd35 Vintage Tine
e47f730f2039b18030f33cf9387f30fd Chico Synth
c2c8dd577f3c98520c5ed3658bc278c2 Dice Synth
50ca90de28b67cbe88a66169c3027338 Joyful
a624e871399e14956c4512ec63150cda Majenta
9d2dd5fded508f5ed9e32267043399b7 TriBell     
466a7ccac19a1f9c56b467cb93be4960 Pluckey
c384c3131de6ea75663b4bb057be875d Old MusicBox
ded8e1c121c641b870aea92ee5ba189a NoiseScope
00b4d7b97199ec47c010331d4ca8f25f Flutes Key
308b0bc9b4ac79b9b48dc6e38ed6125a Universe Luv
02530481b900a1e4e271ab8292179c9d Accordion   
9309c965fdd2bf567ce3165b585d7d24 Dirt Bass
d69796019c28fa4d256c5ce43f8e543c QueBass
8a3f71635eeb66bd857380bae424b548 Mega PopBass
25c7b47f3c0b48218245bb47280d1c75 OctaBass
42b3bbb8d2094dc400f0655fbd2d2068 BassRide
262f3e912c3c1526180fcd57dc46b154 Dark Bass
e33feb15dc9552d4dc218e0f2e65d5fa Detuned Acid
125c52f3256fc7130f757e5b6ad525a7 Nasal Bass
b9b236ef8f9e559bb6c58d0348f650d3 RingBase
26cbc7386ec2d355a50d2329bd312716 Housey Bass
87103392b050037d4dcf93cd30969ce6 Rhino Bass
353bf433f60e21c9ed72372959e89dbb Dungeon
6ddad499f65b630c0b8390bd384fc403 StackBass
402b8657ada4d81c843f52324ebfb8b1 Organ Bass
1f28ed55a96af3b9b452ba4c93592473 Passing Step
8675ceaf93eacaae8add0f39df85ff4f Sterlie Bass
46ddc6d752ef192d2530cfd40e7fe0c3 Hoovaaa
3699b90b8327c04983e7274408683832 Fallen Rock
e2cf7bcb684dee71648b77416b8d1976 Runaway Lead
11e82f3d86408ea7a198cb5aae489e53 G-Lead
e5b185580ddaf324cceb63d0ef20cfad Panic Lead
cd4a5763f60657ef1a12bede1e664d01 Unison Lead
924d9b7ad3ba0c80459ee1d3f547912d CutLead
0635dc3af6f4e30b7a2f27b3d5bec8ed Cyber Lead
252a0a20a8da9f5eae196d0b4afaa47c Sweep Lead
be47dd94d25a58b7c97025df5ac80a2b Jimmy Vision
0115eb4a53a04a3c210261c1d90a6c98 Vibe Lead
a7cb104c272faaadb2366d1922bb785e ManzLead
515ec6f20c6e3e4ee2ce3e893963705a Da Lead
a9de7204bd7e90ea3f3b371be782df93 Oct Uni Sync
d74824da392ad46e97cc9929f73de4ae Delay Seq_1
1ac51449fb14a2e169c223a0209d2049 Third Eye
0310ded6e48214864562210bc2126fe8 DualSonic
9dca7849b24360fbf6743a632de8f2c5 Deephit
2753a7b69197428e33d98125597b373c Halftime Hit
f226860f6b7b5a7cf2ad40d1ea27904e HarmorChord
a08b0e7b175239bcdd3b67910a40254a SunnyDetroit
7ea1d58fa85f0b5bf55a829e0f7ffd0b Crystal Band
54b9eabe64cbf6dd1f0e6ccb09044512 Foggy Morn
cdf296539e8544591c824aa0ce7218df Teleport 1-2
0f13f9b3c82860753c7c214dd4798b0f Thoth Arp
d9b88a41b43be517e9cd0af2a7088b37 BlinkyLead
40fc76735cad46ede4ad0a8b322676d6 Arp Bass
93df7263a86691e719daacd0791aad91 Password
3232a4f229df4871f2bff77cb51f02a8 Drip City
8ec9ff7dc1fe161736bc23ebc597cfdc Heeler Seq
2217603c5b6a72acd8ddfa7e1285ab5d Dream Seq
d298fa31935fbedd271831b63e39b5f0 Spark!
fe35f1f06bc1d3a92cdf08acb487ff6d Mono Growl
288f03dfcde2a26b0d695c223d62bd29 NoisyPopToms
4a681341f4d17ae042f8430b33652f41 Motion Beat
54917be8be3a95dd5e9776b027f62a68 Beat Salad
"""
factory_hashes = [l.split()[0] for l in factory_presets.splitlines()]


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
    ("eg_attack", "eg_attack_b2_9_FF_2", "eg_adsr_03_0"),
    ("eg_decay", "eg_decay_b2_9_FF_2", "eg_adsr_0C_E"),
    ("eg_sustain", "eg_sustain_b2_9_FF_2", "eg_adsr_30_C"),
    ("eg_release", "eg_release_b2_9_FF_2", "eg_adsr_C0_A"),
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


favorite_template = """\
<?xml version="1.0" encoding="UTF-8"?>

<minilogue_Favorite>
  <Bank>
    <Data>0</Data>
    <Data>35</Data>
    <Data>67</Data>
    <Data>95</Data>
    <Data>108</Data>
    <Data>136</Data>
    <Data>151</Data>
    <Data>176</Data>
  </Bank>
</minilogue_Favorite>
"""


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

This is the table of Slider Assignment destinations, in Korg's MIDI Implementation rev1 document.
It seems to be total rubbish. See the table following this one for corrected values.
*note P13 (Slider Assign)
    0 : PITCH BEND
    1 : GATE TIME
    2 : VCO 1 PITCH
    3 : VCO 1 SHAPE
    4 : VCO 2 PITCH
    5 : VCO 2 SHAPE
    6 : CROSS MOD DEPTH
    7 : VCO 2 PITCH EG INT
    8 : VCO 1 LEVEL
    9 : VCO 2 LEVEL
   10 : NOISE LEVEL
   11 : CUTOFF
   12 : RESONANCE
   13 : FILTER EG INT
   14 : AMP EG ATTACK
   15 : AMP EG DECAY
   16 : AMP EG SUSTAIN
   17 : AMP EG RELEASE
   18 : EG ATTACK
   19 : EG DECAY
   20 : EG SUSTAIN
   21 : EH RELEASE
   22 : LFO RATE
   23 : LFO INT
   24 : DELAY HI PASS CUTOFF
   25 : DELAY TIME
   26 : DELAY FEEDBACK
   27 : Portament Time
   28 : VOICE MODE DEPTH


The following table of Slider Assignment destinations is based on Jeff Kistler's implementation in
his minilogue editor here:
https://github.com/jeffkistler/minilogue-editor/blob/c864768866680f3cf958d00c20cc240df00208de/src/minilogue/display.js#L541

    77: 'Pitch Bend'
    78: 'Gate Time'
    17: 'VCO1 Pitch'
    18: 'VCO1 Shape'
    21: 'VCO2 Pitch'
    22: 'VCO2 Shape'
    25: 'Cross Mod Depth'
    26: 'VCO2 Pitch EG Int'
    29: 'VCO1 Level'
    30: 'VCO2 Level'
    31: 'Noise Level'
    32: 'Cutoff'
    33: 'Resonance'
    34: 'Filter EG Int'
    40: 'Amp EG Attack'
    41: 'Amp EG Decay'
    42: 'Amp EG Sustain'
    43: 'Amp EG Release'
    44: 'EG Attack'
    45: 'EG Decay'
    46: 'EG Sustain'
    47: 'EG Release'
    48: 'LFO Rate'
    49: 'LFO Int'
    56: 'Delay Hi Pass Cutoff'
    57: 'Delay Time'
    58: 'Delay Feedback'
    59: 'Portamento Time'
    71: 'Voice Mode Depth'

"""

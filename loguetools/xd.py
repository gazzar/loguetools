from collections import namedtuple
from math import exp, log


clip = lambda val, low, high: max(low, min(val, high))

def twos_comp(val, bits):
    """2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
      val = val - (1 << bits)        # compute negative value
    return val


og_slider_to_xd = {
    0: 12, # PITCH BEND. This is taken care of by +/-x on the xd so I default to filter EG.
    1:  0, # GATE TIME
    2:  3, # VCO 1 PITCH
    3:  4, # VCO 1 SHAPE
    4:  5, # VCO 2 PITCH
    5:  6, # VCO 2 SHAPE
    6:  7, # CROSS MOD DEPTH
    7:  5, # VCO 2 PITCH EG INT
    8:  9, # VCO 1 LEVEL
    9: 10, # VCO 2 LEVEL
   10: 11, # NOISE LEVEL
   11: 12, # CUTOFF
   12: 13, # RESONANCE
   13: 20, # FILTER EG INT
   14: 14, # AMP EG ATTACK
   15: 15, # AMP EG DECAY
   16: 16, # AMP EG SUSTAIN
   17: 17, # AMP EG RELEASE
   18: 18, # EG ATTACK
   19: 19, # EG DECAY
   20: 18, # EG SUSTAIN
   21: 19, # EH RELEASE
   22: 21, # LFO RATE
   23: 22, # LFO INT
   24: 12, # DELAY HI PASS CUTOFF
   25: 27, # DELAY TIME
   26: 28, # DELAY FEEDBACK
   27:  1, # Portament Time
   28:  2, # VOICE MODE DEPTH
   77: 12, # PITCH BEND alt.
   78:  0, # GATE TIME alt.
}

prologue_mod_wheel_to_xd = {
#    0 : # BALANCE
    1 : 1, # PORTAMENTO
#    2 : # V.SPREAD
    3 : 2, # V.M DEPTH
    4 : 3, # VCO1 PITCH
    5 : 4, # VCO1 SHAPE
    6 : 5, # VCO2 PITCH
    7 : 6, # VCO2 SHAPE
    8 : 7, # CROSS MOD
    9 : 20, # PITCH EG INT -> EG INT
    10 : 8, # MULTI SHAPE
    11 : 9, # VCO1 LEVEL
    12 : 10, # VCO2 LEVEL
    13 : 11, # MULTI LEVEL
    14 : 12, # CUTOFF
    15 : 13, # RESONANCE
    16 : 20, # CUTOFF EG INT -> EG INT
    17 : 14, # A.EG ATTACK
    18 : 15, # A.EG DECAY
    19 : 16, # A.EG SUSTAIN
    20 : 17, # A.EG RELEASE
    21 : 18, # EG ATTACK
    22 : 19, # EG DECAY
#    23 : # EG SUSTAIN
#    24 : # EG RELEASE
    25 : 21, # LFO RATE
    26 : 22, # LFO INT
    27 : 23, # MOD FX SPEED
    28 : 24, # MOD FX DEPTH
#todo: change with the patch default delay/reverb fx
    29 : 27, # DL/RV TIME -> DELAY TIME
    30 : 28, # DL/RV DEPTH -> DELAY DEPTH
    31 : 0, # GATE TIME
}

prologue_e_pedal_to_xd = {
#    0 : # OFF
#    1 : # VOLUME
#    2 : # BALANCE
    3 : 1, # PORTAMENTO
#    4 : # V.SPREAD
    5 : 2, # V.M DEPTH
    6 : 3, # VCO1 PITCH
    7 : 4, # VCO1 SHAPE
    8 : 5, # VCO2 PITCH
    9 : 6, # VCO2 SHAPE
    10 : 7, # CROSS MOD
    11 : 20, # PITCH EG INT -> EG INT
    12 : 8, # MULTI SHAPE
    13 : 9, # VCO1 LEVEL
    14 : 10, # VCO2 LEVEL
    15 : 11, # MULTI LEVEL
    16 : 12, # CUTOFF
    17 : 13, # RESONANCE
    18 : 20, # CUTOFF EG INT
    19 : 14, # A.EG ATTACK
    20 : 15, # A.EG DECAY
    21 : 16, # A.EG SUSTAIN
    22 : 17, # A.EG RELEASE
    23 : 18, # EG ATTACK
    24 : 19, # EG DECAY
#    25 : # EG SUSTAIN
#    26 : # EG RELEASE
    27 : 21, # LFO RATE
    28 : 22, # LFO INT
    29 : 23, # MOD FX SPEED
    30 : 24, # MOD FX DEPTH
#todo: change with the patch default delay/reverb fx
    31 : 27, # DL/RV TIME
    32 : 28, # DL/RV DEPTH
}

molg_slider_to_xd = {
    13:  3, # VCO 1 PITCH
    14:  4, # VCO 1 SHAPE
    17:  5, # VCO 2 PITCH
    18:  6, # VCO 2 SHAPE
    21:  9, # VCO 1 LEVEL
    22: 10, # VCO 2 LEVEL
    23: 12, # CUTOFF
    24: 13, # RESONANCE
    26: 50, # EG ATTACK
    27: 51, # EG DECAY
    28: 20, # EG INT
    31: 21, # LFO RATE
    32: 22, # LFO INT
    40:  1, # Portament Time
    56: 12, # PITCH BEND. This is taken care of by +/-x on the xd so I default to filter EG.
    57:  0, # GATE TIME
}

og_motion_to_xd = {
     0:  0,     # None
    17: 20,     # VCO 1 PITCH
    18: 21,     # VCO 1 SHAPE
    19: 18,     # : 19? VCO 1 OCTAVE **og WAVE maybe
    20: 19,     # : 18? VCO 1 OCTAVE **one of these might be WAVE
    21: 24,     # VCO 2 PITCH
    22: 25,     # VCO 2 SHAPE  *docs say VCO 1
    23: 22,     # : 23? VCO 1 OCTAVE *docs say VCO 1
    24: 23,     # : 22? VCO 1 OCTAVE *docs say VCO 1
    25: 28,     # CROSS MOD
    26:  0,     # PITCH EG INT
    27: 26,     # SYNC
    28: 27,     # RING
    29: 39,     # VCO 1 LEVEL
    30: 40,     # VCO 2 LEVEL
    31: 41,     # NOISE LEVEL * mapped to multi-engine level
    32: 42,     # CUTOFF
    33: 43,     # RESONANCE
    34:  0,     # CUTOFF EG INT
    35:  0,     # CUTOFF VELOCITY TRACK
    36: 45,     # CUTOFF KEYBOARD TRACK
    37:  0,     # CUTOFF TYPE
    40: 46,     # AMP EG ATTACK
    41: 47,     # AMP EG DECAY
    42: 48,     # AMP EG SUSTAIN
    43: 49,     # AMP EG RELEASE
    44: 50,     # EG ATTACK
    45: 51,     # EG DECAY
    46:  0,     # EG SUSTAIN
    47:  0,     # EG RELEASE
    48: 56,     # LFO RATE
    49: 57,     # LFO INT
    50: 58,     # LFO TARGET
    51: 57,     # LFO EG
    52: 54,     # LFO TYPE
    53:  0,     # DELAY OUTPUT ROUTING
    55:  0,     # DELAY HI PASS CUTOFF
    56: 70,     # DELAY TIME
    57: 71,     # DELAY FEEDBACK
    61: 126,     # PITCH BEND
    62: 129,     # GATE TIME
}

molg_motion_to_xd = {
     0:  0,     # None
    13: 20,     # VCO 1 PITCH
    14: 21,     # VCO 1 SHAPE
    15: 18,     # : 19? VCO 1 OCTAVE **og WAVE maybe
    16: 19,     # : 18? VCO 1 OCTAVE **one of these might be WAVE
    17: 24,     # VCO 2 PITCH
    18: 25,     # VCO 2 SHAPE  *docs say VCO 1
    19: 22,     # : 23? VCO 1 OCTAVE *docs say VCO 1
    20: 23,     # : 22? VCO 1 OCTAVE *docs say VCO 1
    21: 39,     # VCO 1 LEVEL
    22: 40,     # VCO 2 LEVEL
    23: 42,     # CUTOFF
    24: 43,     # RESONANCE
    25: 26,     # SYNC
#    25: 27,     # RING
    26: 50,     # EG ATTACK
    27: 51,     # EG DECAY
    28: 52,     # EG INT
    29:  0,     #EG TYPE
    30: 53,      #EG TARGET
    31: 56,     # LFO RATE
    32: 57,     # LFO INT
    33: 58,     # LFO TARGET
    34: 57,     # LFO EG
    35: 54,     # LFO TYPE
    37:  0,     # DRIVE
    56: 126,     # PITCH BEND
    57: 129,     # GATE TIME
}

fn_motion_slot_1_parameter = lambda src: og_motion_to_xd.get(src.motion_slot_1_1_parameter, 0)
fn_motion_slot_2_parameter = lambda src: og_motion_to_xd.get(src.motion_slot_2_1_parameter, 0)
fn_motion_slot_3_parameter = lambda src: og_motion_to_xd.get(src.motion_slot_3_1_parameter, 0)
fn_motion_slot_4_parameter = lambda src: og_motion_to_xd.get(src.motion_slot_4_1_parameter, 0)

fn_molg_motion_slot_1_parameter = lambda src: molg_motion_to_xd.get(src.motion_slot_1_1_parameter, 0)
fn_molg_motion_slot_2_parameter = lambda src: molg_motion_to_xd.get(src.motion_slot_2_1_parameter, 0)
fn_molg_motion_slot_3_parameter = lambda src: molg_motion_to_xd.get(src.motion_slot_3_1_parameter, 0)
fn_molg_motion_slot_4_parameter = lambda src: molg_motion_to_xd.get(src.motion_slot_4_1_parameter, 0)

fn_slider_right = lambda src: og_slider_to_xd.get(src.slider_assign, 12)
fn_slider_left = lambda src: og_slider_to_xd.get(src.slider_assign, 12)
fn_bend_range_plus = lambda src: int(100 + src.bend_range_plus * 100 / 12)
fn_bend_range_minus = lambda src: int(100 + src.bend_range_minus * 100 / 12)

fn_midi_after_touch_assign = lambda src: prologue_mod_wheel_to_xd.get(src.midi_after_touch_assign, 0)
fn_mod_wheel_assign = lambda src: prologue_mod_wheel_to_xd.get(src.mod_wheel_assign, 0)
fn_e_pedal_assign = lambda src: prologue_e_pedal_to_xd.get(src.e_pedal_assign, 0)
fn_slider = lambda src: molg_slider_to_xd.get(src.slider_assign, 0)

# Simple translation functions
fn_delay_on_off = lambda src: 0 if src.delay_output_routing == 0 else 1
fn_prologue_delay_on_off = lambda src: 1 if src.delay_reverb_on_off != 0 and src.delay_reverb_type == 1 else 0
fn_prologue_reverb_on_off = lambda src: 1 if src.delay_reverb_on_off != 0 and src.delay_reverb_type == 2 else 0

fn_sync = lambda src: 1 if src.ring_sync == 2 else 0
fn_ring = lambda src: 1 if src.ring_sync == 0 else 0

fn_str_pred = lambda src: "PRED"
fn_str_sq = lambda src: "SQ"
# XD swing encoding is 0,75,150=-75%,0,+75% but OG uses something else; maybe 2's complement?
fn_swing = lambda src: clip(twos_comp(src.swing, 8) + 75, 0, 150)
fn_cutoff_velocity = lambda src: (0, 63, 127)[src.cutoff_velocity]
fn_cutoff_kbd_track = lambda src: 2 - src.cutoff_kbd_track
fn_multi_octave = lambda src: 0 if src.vco_1_octave == 0 else src.vco_1_octave - 1
fn_voice_mode_type = lambda src: {0: 4, 1: 4, 2: 3, 3: 2, 4: 2, 5: 4, 6: 1, 7: 4}[src.voice_mode]
fn_prologue_voice_mode_type = lambda src: {0: 4, 1: 4, 2: 3, 3: 2}[src.voice_mode_type] if src.arp == 0 else 1
fn_prologue_voice_mode_depth = lambda src: {0: 0, 1: 157, 2: 313, 3: 469, 4:781, 5: 1023}[src.arp_type] if src.arp != 0 else src.voice_mode_depth
# Assumption: pitch EG is favored over cutoff eg
fn_prologue_eg_int = lambda src: src.pitch_eg_int if src.pitch_eg_int > 0 else src.cutoff_eg_int
fn_prologue_eg_target = lambda src: 2 if src.pitch_eg_int > 0 else 0
fn_prologue_lfo_mode = lambda src: {0: 3, 1: 1, 2: 1}[src.lfo_mode]
fn_vco_2_level = lambda src: src.vco_2_level if src.vco_2_wave != 0 else 0
fn_vco_2_octave = lambda src: src.vco_2_octave if src.vco_2_wave != 0 else 1
fn_vco_2_pitch = lambda src: src.vco_2_pitch if src.vco_2_wave != 0 else 0
fn_vco_2_shape = lambda src: src.vco_2_shape if src.vco_2_wave != 0 else 0
fn_multi_level = lambda src: src.vco_2_level if src.vco_2_wave == 0 else 0
fn_molg_multi_octave = lambda src: src.vco_2_octave if src.vco_2_wave == 0 else 1
fn_molg_lfo_mode = lambda src: 2 if src.lfo_bpm_sync != 0 else {0: 0, 1: 1, 2: 1}[src.lfo_mode]
fn_drive = lambda src: (src.drive * 3) >> 10
fn_amp_eg_attack = lambda src: src.eg_attack if src.eg_type != 2 else 0
fn_amp_eg_decay = lambda src: src.eg_decay if src.eg_type == 0 else 0
fn_amp_eg_sustain = lambda src: 0 if src.eg_type == 0 else 1023
fn_amp_eg_release = lambda src: src.eg_decay if src.eg_type == 1 else 0

# The following seems wrong; need more data
fn_delay_time = lambda src: int(src.delay_time * 350.0 / 654.0)
fn_bmp = lambda src: 3000 if src.bpm > 3000 else src

# Based on the SonicLabs review, the minilogue's portamento time setting encodes both
# the portamento time and the EG Legato setting. The OG midi docs say
# |  61   |  0~7  |  0~128  |  Portament Time          0,1~129=OFF,0~128  |
# I think they should say
# |  61   |  0~7  |  0~127  |  Portament Time          0,1~127=OFF,0~126  |
fn_portamento_time = lambda src: 0 if src.portamento_time == 0 else src.portamento_time - 1
fn_eg_legato = lambda src: src.portamento_time > 0


def fn_voice_mode_depth(src):
    """
    -XD-
    *note P3 (VOICE MODE TYPE)
        1:ARP, 2:CHORD (Mono verified), 3:UNISON, 4:POLY
    *note P2 (VOICE MODE DEPTH)
        [POLY] 0~255:Poly, 256~1023:Duo 0~1023
        [UNISON] 0 ~ 1023: Detune 0 Cent
        [CHORD] 0~1:Mono, 2~73:5th, 74~146:sus2, 147~219:m, 220~292:Maj, 293~365:sus4,
            366~438:m7, 439~511:7, 512~585:7sus4, 586~658:Maj7, 659~731:aug,
            732~804:dim, 805~877:m7b5, 878~950:mMaj7, 951~1023:Maj7b5
        [ARP] unchanged

    -OG-
    *note P11 (VOICE MODE)
        0:POLY, 1:DUO, 2:UNISON, 3:MONO, 4:CHORD, 5:DELAY, 6:ARP, 7:SIDECHAIN

    *note P12 (VOICE MODE DEPTH)
        [POLY] 0~1023:Invert 0~8
        [DUO],[UNISON] 0~1023:Detune 0 Cent ~ 50 Cent
        [MONO] 0~1023:Sub 0~1023
        [CHORD] unchanged for non-mono mode
        [DELAY] N/A
        [ARP] unchanged
        [SIDECHAIN] N/A
    """
    if src.voice_mode == 1:
        # DUO; this handling could well be wrong
        return clip(src.voice_mode_depth + 256, 256, 1023)
    elif src.voice_mode == 3:
        # MONO
        return 0
    else:
        return src.voice_mode_depth


def fn_translate_step_data(og_step_data):
    xd_buffer = bytearray(52 * b"\x00")
    # notes
    xd_buffer[0:4] = og_step_data[0:4]
    # note velocities
    xd_buffer[8:12] = og_step_data[4:8]
    # gates and triggers
    xd_buffer[16:20] = og_step_data[8:12]
    # motion data; xd is 10 bit and og is 8-bit; I'm not sure if I should shift them.
    # I think I will just copy across to slots 0-3.
    xd_buffer[24:26] = og_step_data[12:14]
    xd_buffer[31:33] = og_step_data[14:16]
    xd_buffer[38:40] = og_step_data[16:18]
    xd_buffer[45:47] = og_step_data[18:20]
    return xd_buffer

def fn_molg_translate_step_data(molg_step_data):
    xd_buffer = bytearray(52 * b"\x00")
    # notes
    xd_buffer[0] = molg_step_data[0]
    # note velocities
    xd_buffer[8] = molg_step_data[2]
    # gates and triggers
    xd_buffer[16] = molg_step_data[4]
    # motion data; xd is 10 bit and og is 8-bit; not I'm not sure if I should shift them
    # I think I will just copy across to slots 0-3
    xd_buffer[24:28] = molg_step_data[6:10]
    xd_buffer[31:35] = molg_step_data[10:14]
    xd_buffer[38:42] = molg_step_data[14:18]
    xd_buffer[45:49] = molg_step_data[18:22]
    return xd_buffer

fn_empty_step_data = lambda src: bytearray(52 * b"\x00")

fn_step_01_event_data = lambda src: fn_translate_step_data(src.step_01_event_data)
fn_step_02_event_data = lambda src: fn_translate_step_data(src.step_02_event_data)
fn_step_03_event_data = lambda src: fn_translate_step_data(src.step_03_event_data)
fn_step_04_event_data = lambda src: fn_translate_step_data(src.step_04_event_data)
fn_step_05_event_data = lambda src: fn_translate_step_data(src.step_05_event_data)
fn_step_06_event_data = lambda src: fn_translate_step_data(src.step_06_event_data)
fn_step_07_event_data = lambda src: fn_translate_step_data(src.step_07_event_data)
fn_step_08_event_data = lambda src: fn_translate_step_data(src.step_08_event_data)
fn_step_09_event_data = lambda src: fn_translate_step_data(src.step_09_event_data)
fn_step_10_event_data = lambda src: fn_translate_step_data(src.step_10_event_data)
fn_step_11_event_data = lambda src: fn_translate_step_data(src.step_11_event_data)
fn_step_12_event_data = lambda src: fn_translate_step_data(src.step_12_event_data)
fn_step_13_event_data = lambda src: fn_translate_step_data(src.step_13_event_data)
fn_step_14_event_data = lambda src: fn_translate_step_data(src.step_14_event_data)
fn_step_15_event_data = lambda src: fn_translate_step_data(src.step_15_event_data)
fn_step_16_event_data = lambda src: fn_translate_step_data(src.step_16_event_data)

fn_molg_step_01_event_data = lambda src: fn_molg_translate_step_data(src.step_01_event_data)
fn_molg_step_02_event_data = lambda src: fn_molg_translate_step_data(src.step_02_event_data)
fn_molg_step_03_event_data = lambda src: fn_molg_translate_step_data(src.step_03_event_data)
fn_molg_step_04_event_data = lambda src: fn_molg_translate_step_data(src.step_04_event_data)
fn_molg_step_05_event_data = lambda src: fn_molg_translate_step_data(src.step_05_event_data)
fn_molg_step_06_event_data = lambda src: fn_molg_translate_step_data(src.step_06_event_data)
fn_molg_step_07_event_data = lambda src: fn_molg_translate_step_data(src.step_07_event_data)
fn_molg_step_08_event_data = lambda src: fn_molg_translate_step_data(src.step_08_event_data)
fn_molg_step_09_event_data = lambda src: fn_molg_translate_step_data(src.step_09_event_data)
fn_molg_step_10_event_data = lambda src: fn_molg_translate_step_data(src.step_10_event_data)
fn_molg_step_11_event_data = lambda src: fn_molg_translate_step_data(src.step_11_event_data)
fn_molg_step_12_event_data = lambda src: fn_molg_translate_step_data(src.step_12_event_data)
fn_molg_step_13_event_data = lambda src: fn_molg_translate_step_data(src.step_13_event_data)
fn_molg_step_14_event_data = lambda src: fn_molg_translate_step_data(src.step_14_event_data)
fn_molg_step_15_event_data = lambda src: fn_molg_translate_step_data(src.step_15_event_data)
fn_molg_step_16_event_data = lambda src: fn_molg_translate_step_data(src.step_16_event_data)


"""
The routing possibilities for the EG and LFO are quite different in the OG and XD. In
the following one selection is possible per independent group a-e:
XD:
   a / EG INT     -> CUTOFF
   a | EG INT     -> PITCH 1 & 2
   a \ EG INT     -> PITCH 2
   b / LFO        -> CUTOFF
   b | LFO        -> SHAPE 1 & 2
   b | LFO        -> SHAPE 2
   b | LFO        -> PITCH 1 & 2
   b | LFO        -> PITCH 2
   b | LFO-1-SHOT -> CUTOFF
   b | LFO-1-SHOT -> PITCH 1 & 2
   b \ LFO-1-SHOT -> PITCH 2

OG:
   c < EG INT     -> CUTOFF
   d < EG INT     -> PITCH 2
   e / LFO        -> CUTOFF
   e | LFO        -> SHAPE 1 & 2
   e \ LFO        -> PITCH 1 & 2

    Note: The EG can be targeted to the LFO RATE and INTensity. There is no possibility
    for this on the XD so we must ignore it.

    On the XD, LFO-1-SHOT is included explicitly because it can act as a second envelope
    if the LFO is not being used. The translator follows the following principles:
    The amounts of the OG's EG INTensity and LFO INTensity will be sorted from highest
    to lowest and the two highest INTensity groups will be allocated on the XD. In case
    of a tie, the LFO group will be given lowest priority.

    In the case where we use the LFO in 1-Shot mode to act as an envelope, we don't 
    have much control. Since this is targeted to pitch, we will assume that most
    patches are using it as an attack transient. This means we can assume both that
    the sustain level is 0 and the release can be ignored, so we just need to look
    at approximating the Attack and Decay. We will choose from the following 4
    possibilities (The pulse waveform would be of limited use). We choose the saw
    if A << D and the triangle if A ~= D.
    1. Saw down _|\_    3. Tri up   _/\_
    2. Saw up   _  _    4. Tri down _  _
                 |/                  \/

    Timings (s) of the XD's EG envelope (^RISEvFALL)
    A  | 512   1023    0     0    0    0      768
    D  |  0      0   1023   512  256  768     256
    --------------------------------------------------
    (s)|^1.08 ^3.63 v31.1  v1.5 v0.28 v3.8 ^2.04v0.29

    So Attack and Decay are both nonlinear but I can't be bothered to work these out
    for now, and I don't know the OG's timings either, so I'll use the XD's.
    I fitted exponential trends to these
    attack_time_s(x) = 0.324 exp(0.00237 x)
    x = 421.5 ln(3.09 * attack_time_s)
    decay_time_s(x) = 0.0613 exp(0.00589 x)
    x = 169.8 ln(16.3 * decay_time_s

    Timings (s) of the XD's 1-shot saw/fall time
    R  |  0   512  1023
    --------------------
    (s)| 10  1.02  0.02

    fall_time_s(x) = 13.17 exp(-0.006 x)
    x = -167 ln(0.076 * fall_time_s)
"""
attack_to_s = lambda x: 0.324 * exp(0.00237 * x)
decay_to_s = lambda x: 0.0613 * exp(0.00589 * x)
s_rate = lambda x: clip(int(-167 * log(0.076 * x)), 0, 1023)


def eg_and_lfo_mapping(src):
    # Scale all EG and LFO amount from 0.0 to 1.0
    c = abs(src.cutoff_eg_int - 512) / 512.0        # (492+532)/2=512; abs(a-512)/508
    d = abs(src.vco_2_pitch_eg_int - 512) / 512.0   # abs(a-512)/508
    e = src.lfo_int / 1023.0                        # 0~1023; a/1023

    # Sort EG and LFO amounts
    resourcepool = {'eg_to_cutoff':c, 'eg_to_pitch':d, 'lfo':e}
    resources = sorted(resourcepool, key=resourcepool.get)
    # remove lowest priority, prioritising lfo lowest in the case of equality
    if resourcepool[resources[0]] == resourcepool['lfo']:
        resources.remove('lfo')
    else:
        resources.pop(0)

    # allocate our resources
    if 'lfo' in resources:
        # we need to use the XD's lfo
        # LFO -> OG target
        lfo_target = src.lfo_target
        lfo_target_osc = 0  # LFO TARGET OSC = 0:ALL, 1:VCO1+VCO2, 2:VCO2, 3:MULTI
        # LFO MODE 0~2=1-SHOT,NORMAL,BPM
        lfo_mode = 1 if src.lfo_bpm_sync == 0 else 2
        lfo_wave = src.lfo_wave
        lfo_int = 512 + int(src.lfo_int / 2)
        lfo_rate = src.lfo_rate

        # now allocate the XD's EG
        eg_int = src.cutoff_eg_int
        if 'eg_to_cutoff' in resources:
            # EG INT -> CUTOFF
            eg_target = 0      # EG TARGET 0~2=CUTOFF, PITCH2, PITCH
        else:
            # 'eg_to_pitch'
            eg_target = 1      # EG TARGET 0~2=CUTOFF, PITCH2, PITCH

    else:
        # The lfo is free; send EG INT -> CUTOFF and LFO-1-SHOT -> PITCH 2

        # LFO-1-SHOT -> PITCH 2
        lfo_target = 2     # LFO TARGET 0~2=CUTOFF,SHAPE,PITCH
        lfo_target_osc = 2 # LFO TARGET OSC = 0:ALL, 1:VCO1+VCO2, 2:VCO2, 3:MULTI
        lfo_mode = 0       # LFO MODE 0~2=1-SHOT,NORMAL,BPM
        # Translate the LFO RATE value from the EG AD values
        # Choose saw or triangle
        if (src.eg_attack + src.eg_decay) == 0 or src.eg_attack / (src.eg_attack + src.eg_decay) < 0.25:
            lfo_wave = 2    # saw
        else:
            lfo_wave = 1    # triangle
        # Choose sign of lfo_int; the og encodes -4800 cent but I'll ignore this for now
        # See minilogue OG MIDIimp_rev1p10 note P3 (VCO 2 PITCH EG Int)
        lfo_int = src.vco_2_pitch_eg_int
        eg_ad_length_s = attack_to_s(src.eg_attack) + decay_to_s(src.eg_decay)
        lfo_rate = s_rate(eg_ad_length_s)

        # EG INT -> CUTOFF
        eg_int = src.cutoff_eg_int
        eg_target = 0      # EG TARGET 0~2=CUTOFF, PITCH2, PITCH

    return lfo_target, lfo_target_osc, lfo_mode, lfo_wave, lfo_int, lfo_rate, eg_int, eg_target


# OG VCO 2 PITCH EG Int
# OG Owner's Guide says the knob encodes values from -4800 to 4800 but the midi guide
# says
#     0    ~    4 : -4800 (Cent)
#     4    ~  356 : -4800 ~ -1024 (Cent)
#     356  ~  476 : -1024 ~   -64 (Cent)
#     476  ~  492 :   -64 ~     0 (Cent)
#     492  ~  532 :     0 (Cent)
#     532  ~  548 :     0 ~    64 (Cent)
#     548  ~  668 :    64 ~  1024 (Cent)
#     668  ~ 1020 :   256 ~  1200 (Cent)
#     1020 ~ 1023 :  1200 (Cent)

# OG CUTOFF EG INT and XD EG INT
#     0   ~ 11   : -100 (%)
#     11  ~ 492  : - ((492 - value) * (492 - value) * 4641 * 100) / 0x40000000 (%)
#     492 ~ 532  : 0 (%)
#     532 ~ 1013 : ((value - 532) * (value - 532) * 4641 * 100) / 0x40000000 (%)
#     1013~1023  : 100 (%)


class ComputeOnce():
    """The fields of this class are interdependent. The first attempt to access any
    field by calling the associated method will compute all fields. Subsequent accesses
    via any of the methods just retrieve the already computed value.

    """
    def __init__(self):
        self.run = False

    def first(self, src):
        if not self.run:
            self.run = True
            (
                self.lfo_target,
                self.lfo_target_osc,
                self.lfo_mode,
                self.lfo_wave,
                self.lfo_int,
                self.lfo_rate,
                self.eg_int,
                self.eg_target,
            ) = eg_and_lfo_mapping(src)

    def fn_lfo_target(self, src):
        self.first(src)
        return self.lfo_target
    
    def fn_lfo_target_osc(self, src):
        self.first(src)
        return self.lfo_target_osc
    
    def fn_lfo_mode(self, src):
        self.first(src)
        return self.lfo_mode

    def fn_lfo_wave(self, src):
        self.first(src)
        return self.lfo_wave

    def fn_lfo_int(self, src):
        self.first(src)
        return self.lfo_int

    def fn_lfo_rate(self, src):
        self.first(src)
        return self.lfo_rate

    def fn_eg_int(self, src):
        self.first(src)
        return self.eg_int

    def fn_eg_target(self, src):
        self.first(src)
        return self.eg_target


once = ComputeOnce()

patch_translation_value = namedtuple("Field", ["name", "type", "source"])

"""
A translation table for converting from minilogue OG patch data. Each tuple takes one of
the forms

('label', 'binary-format string', 'src1_name')
('label', 'binary-format string', p), where p is an integer
('label', 'binary-format string', f), where f is a function

"""
patch_struct = {
    "og":(
    # 0
    ("str_PROG", "4s", "str_PROG"),
    ("program_name", "12s", "program_name"),
    ("octave", "B", "keyboard_octave"),
    ("portamento", "B", fn_portamento_time),
    ("key_trig", "B", 0),
    ("voice_mode_depth", "<H", fn_voice_mode_depth),
    ("voice_mode_type", "B", fn_voice_mode_type),
    ("vco_1_wave", "B", "vco_1_wave"),
    ("vco_1_octave", "B", "vco_1_octave"),
    ("vco_1_pitch", "<H", "vco_1_pitch"),
    ("vco_1_shape", "<H", "vco_1_shape"),
    ("vco_2_wave", "B", "vco_2_wave"),
    ("vco_2_octave", "B", "vco_2_octave"),
    ("vco_2_pitch", "<H", "vco_2_pitch"),
    ("vco_2_shape", "<H", "vco_2_shape"),
    ("sync", "B", "sync"),
    ("ring", "B", "ring"),
    ("cross_mod_depth", "<H", "cross_mod_depth"),
    ("multi_type", "B", 0),
    ("select_noise", "B", 1),
    ("select_vpm", "B", 6),
    ("select_user", "B", 0),
    ("shape_noise", "<H", 1),
    ("shape_vpm", "<H", 6),
    ("shape_user", "<H", 0),
    ("shift_shape_noise", "<H", 0),
    # 50
    ("shift_shape_vpm", "<H", 0),
    ("shift_shape_user", "<H", 0),
    ("vco_1_level", "<H", "vco_1_level"),
    ("vco_2_level", "<H", "vco_2_level"),
    ("multi_level", "<H", "noise_level"),
    ("cutoff", "<H", "cutoff"),
    ("resonance", "<H", "resonance"),
    ("cutoff_drive", "B", 0),
    ("cutoff_keyboard_track", "B", fn_cutoff_kbd_track),
    ("amp_eg_attack", "<H", "amp_eg_attack"),
    ("amp_eg_decay", "<H", "amp_eg_decay"),
    ("amp_eg_sustain", "<H", "amp_eg_sustain"),
    ("amp_eg_release", "<H", "amp_eg_release"),
    ("eg_attack", "<H", "eg_attack"),
    ("eg_decay", "<H", "eg_decay"),
    ("eg_int", "<H", once.fn_eg_int),
    ("eg_target", "B", once.fn_eg_target),
    ("lfo_wave", "B", once.fn_lfo_wave),
    ("lfo_mode", "B", once.fn_lfo_mode),
    ("lfo_rate", "<H", once.fn_lfo_rate),
    ("lfo_int", "<H", once.fn_lfo_int),
    ("lfo_target", "B", once.fn_lfo_target),
    ("mod_fx_on_off", "B", 0),
    ("mod_fx_type", "B", 0),
    ("mod_fx_chorus", "B", 0),
    ("mod_fx_ensemble", "B", 0),
    ("mod_fx_phaser", "B", 0),
    ("mod_fx_flanger", "B", 0),
    ("mod_fx_user", "B", 0),
    ("mod_fx_time", "<H", 0),
    ("mod_fx_depth", "<H", 0),
    ("delay_on_off", "B", fn_delay_on_off),
    # 100
    ("delay_sub_type", "B", 3),
    ("delay_time", "<H", fn_delay_time),
    ("delay_depth", "<H", "delay_feedback"),
    ("reverb_on_off", "B", 0),
    ("reverb_sub_type", "B", 0),
    ("reverb_time", "<H", 0),
    ("reverb_depth", "<H", 0),
    ("bend_range_plus", "B", "bend_range_plus"),
    ("bend_range_minus", "B", "bend_range_minus"),
    ("joystick_assign_plus", "B", fn_slider_right),
    ("joystick_range_plus", "B", fn_bend_range_plus),
    ("joystick_assign_minus", "B", fn_slider_left),
    ("joystick_range_minus", "B", fn_bend_range_minus),
    ("cv_in_mode", "B", 0),
    ("cv_in_1_assign", "B", 0),
    ("cv_in_1_range", "B", 100),
    ("cv_in_2_assign", "B", 0),
    ("cv_in_2_range", "B", 100),
    ("micro_tuning", "B", 0),
    ("scale_key", "B", 12),
    ("program_tuning", "B", 50),
    ("lfo_key_sync", "B", "lfo_key_sync"),
    ("lfo_voice_sync", "B", "lfo_voice_sync"),
    ("lfo_target_osc", "B", once.fn_lfo_target_osc),
    ("cutoff_velocity", "B", fn_cutoff_velocity),
    ("amp_velocity", "B", "amp_velocity"),
    ("multi_octave", "B", fn_multi_octave),
    ("multi_routing", "B", 0),
    ("eg_legato", "B", fn_eg_legato),
    ("portamento_mode", "B", "portamento_mode"),
    ("portamento_bpm_sync", "B", "portamento_bpm"),
    ("program_level", "B", 102),
    ("vpm_param1_feedback", "B", 199),
    ("vpm_param2_noise_depth", "B", 199),
    ("vpm_param3_shapemodint", "B", 199),
    ("vpm_param4_mod_attack", "B", 199),
    ("vpm_param5_mod_decay", "B", 199),
    ("vpm_param6_modkeytrack", "B", 199),
    ("user_param1", "B", 0),
    ("user_param2", "B", 0),
    ("user_param3", "B", 0),
    ("user_param4", "B", 0),
    ("user_param5", "B", 0),
    ("user_param6", "B", 0),
    ("user_param5_6_r_r_type", "B", 0),
    ("user_param1_2_3_4_type", "B", 0),
    # 150
    ("program_transpose", "B", 13),
    ("delay_dry_wet", "<H", 512),  # 50% wet/dry
    ("reverb_dry_wet", "<H", 512),  # 50% wet/dry
    ("midi_after_touch_assign", "B", 12),
    ("str_PRED", "4s", fn_str_pred),
    ("str_SQ", "2s", fn_str_sq),
    ("step_1_16_active_step", "<H", 65535),
    ("bpm", "<H", "bpm"),
    ("step_length", "B", "step_length"),
    ("step_resolution", "B", "step_resolution"),
    ("swing", "B", fn_swing),
    ("default_gate_time", "B", "default_gate_time"),
    ("step1_16", "<H", "step1_16"),
    ("step1_16_motion", "<H", "step1_16_switch"),  # I think this is the corresponding param
    ("motion_slot_1_0_parameter", "B", "motion_slot_1_0_parameter"),
    ("motion_slot_1_1_parameter", "B", fn_motion_slot_1_parameter),
    ("motion_slot_2_0_parameter", "B", "motion_slot_2_0_parameter"),
    ("motion_slot_2_1_parameter", "B", fn_motion_slot_2_parameter),
    ("motion_slot_3_0_parameter", "B", "motion_slot_3_0_parameter"),
    ("motion_slot_3_1_parameter", "B", fn_motion_slot_3_parameter),
    ("motion_slot_4_0_parameter", "B", "motion_slot_4_0_parameter"),
    ("motion_slot_4_1_parameter", "B", fn_motion_slot_4_parameter),
    ("motion_slot_1_step1_16", "<H", "motion_slot_1_step1_16"),
    ("motion_slot_2_step1_16", "<H", "motion_slot_2_step1_16"),
    ("motion_slot_3_step1_16", "<H", "motion_slot_3_step1_16"),
    ("motion_slot_4_step1_16", "<H", "motion_slot_4_step1_16"),
    # 1900
    ("step_01_event_data", "52s", fn_step_01_event_data),
    ("step_02_event_data", "52s", fn_step_02_event_data),
    ("step_03_event_data", "52s", fn_step_03_event_data),
    ("step_04_event_data", "52s", fn_step_04_event_data),
    ("step_05_event_data", "52s", fn_step_05_event_data),
    ("step_06_event_data", "52s", fn_step_06_event_data),
    ("step_07_event_data", "52s", fn_step_07_event_data),
    ("step_08_event_data", "52s", fn_step_08_event_data),
    ("step_09_event_data", "52s", fn_step_09_event_data),
    ("step_10_event_data", "52s", fn_step_10_event_data),
    ("step_11_event_data", "52s", fn_step_11_event_data),
    ("step_12_event_data", "52s", fn_step_12_event_data),
    ("step_13_event_data", "52s", fn_step_13_event_data),
    ("step_14_event_data", "52s", fn_step_14_event_data),
    ("step_15_event_data", "52s", fn_step_15_event_data),
    ("step_16_event_data", "52s", fn_step_16_event_data),
    # 1022
    ("arp_gate_time", "B", "default_gate_time"),
    ("arp_rate", "B", 5),   # **
# ** Seems to be off by 1 in Korg's docs; set to 5 to get 16th notes.
# Minilogue arp only plays 16th notes unless you halve the tempo?
    ),
    "prologue":(
    ("str_PROG", "4s", "str_PROG"),
    ("program_name", "12s", "program_name"),
    ("octave", "B", "keyboard_octave"),
    ("portamento", "B", "portamento_time"),
    ("key_trig", "B", 0),
    ("voice_mode_depth", "<H", fn_prologue_voice_mode_depth),
    ("voice_mode_type", "B", fn_prologue_voice_mode_type),
    ("vco_1_wave", "B", "vco_1_wave"),
    ("vco_1_octave", "B", "vco_1_octave"),
    ("vco_1_pitch", "<H", "vco_1_pitch"),
    ("vco_1_shape", "<H", "vco_1_shape"),
    ("vco_2_wave", "B", "vco_2_wave"),
    ("vco_2_octave", "B", "vco_2_octave"),
    ("vco_2_pitch", "<H", "vco_2_pitch"),
    ("vco_2_shape", "<H", "vco_2_shape"),
    ("sync", "B", fn_sync),
    ("ring", "B", fn_ring),
    ("cross_mod_depth", "<H", "cross_mod_depth"),
    ("multi_type", "B", "multi_type"),
    ("select_noise", "B", "select_noise"),
    ("select_vpm", "B", "select_vpm"),
    ("select_user", "B", "select_user"),
    ("shape_noise", "<H", "shape_noise"),
    ("shape_vpm", "<H", "shape_vpm"),
    ("shape_user", "<H", "shape_user"),
    ("shift_shape_noise", "<H", 0),
    # 50
    ("shift_shape_vpm", "<H", "shift_shape_vpm"),
    ("shift_shape_user", "<H", "shift_shape_user"),
    ("vco_1_level", "<H", "vco_1_level"),
    ("vco_2_level", "<H", "vco_2_level"),
    ("multi_level", "<H", "multi_level"),
    ("cutoff", "<H", "cutoff"),
    ("resonance", "<H", "resonance"),
    ("cutoff_drive", "B", "cutoff_drive"),
    ("cutoff_keyboard_track", "B", "cutoff_keyboard_track"),
    ("amp_eg_attack", "<H", "amp_eg_attack"),
    ("amp_eg_decay", "<H", "amp_eg_decay"),
    ("amp_eg_sustain", "<H", "amp_eg_sustain"),
    ("amp_eg_release", "<H", "amp_eg_release"),
    ("eg_attack", "<H", "eg_attack"),
    ("eg_decay", "<H", "eg_decay"),
    ("eg_int", "<H", fn_prologue_eg_int),
    ("eg_target", "B", fn_prologue_eg_target),
    ("lfo_wave", "B", "lfo_wave"),
    ("lfo_mode", "B", fn_prologue_lfo_mode),
    ("lfo_rate", "<H", "lfo_rate"),
    ("lfo_int", "<H", "lfo_int"),
    ("lfo_target", "B", "lfo_target"),
    ("mod_fx_on_off", "B", "mod_fx_on_off"),
    ("mod_fx_type", "B", "mod_fx_type"),
    ("mod_fx_chorus", "B", "mod_fx_chorus"),
    ("mod_fx_ensemble", "B", "mod_fx_ensemble"),
    ("mod_fx_phaser", "B", "mod_fx_phaser"),
    ("mod_fx_flanger", "B", "mod_fx_flanger"),
    ("mod_fx_user", "B", "mod_fx_user"),
    ("mod_fx_time", "<H", "mod_fx_time"),
    ("mod_fx_depth", "<H", "mod_fx_depth"),
    ("delay_on_off", "B", fn_prologue_delay_on_off),
    # 100
    ("delay_sub_type", "B", "delay_sub_type"),
    ("delay_time", "<H", "delay_reverb_time"),
    ("delay_depth", "<H", "delay_reverb_depth"),
    ("reverb_on_off", "B", fn_prologue_reverb_on_off),
    ("reverb_sub_type", "B", "reverb_sub_type"),
    ("reverb_time", "<H", "delay_reverb_time"),
    ("reverb_depth", "<H", "delay_reverb_depth"),
    ("bend_range_plus", "B", "bend_range_plus"),
    ("bend_range_minus", "B", "bend_range_minus"),
    ("joystick_assign_plus", "B", fn_mod_wheel_assign),
    ("joystick_range_plus", "B", 200),
    ("joystick_assign_minus", "B", fn_e_pedal_assign),
    ("joystick_range_minus", "B", 200),
    ("cv_in_mode", "B", 0),
    ("cv_in_1_assign", "B", 0),
    ("cv_in_1_range", "B", 100),
    ("cv_in_2_assign", "B", 0),
    ("cv_in_2_range", "B", 100),
    ("micro_tuning", "B", "micro_tuning"),
    ("scale_key", "B", "scale_key"),
    ("program_tuning", "B", "program_tuning"),
    ("lfo_key_sync", "B", "lfo_key_sync"),
    ("lfo_voice_sync", "B", "lfo_voice_sync"),
    ("lfo_target_osc", "B", "lfo_target_osc"),
    ("cutoff_velocity", "B", "cutoff_velocity"),
    ("amp_velocity", "B", "amp_velocity"),
    ("multi_octave", "B", "multi_octave"),
    ("multi_routing", "B", "multi_routing"),
    ("eg_legato", "B", "eg_legato"),
    ("portamento_mode", "B", "portamento_mode"),
    ("portamento_bpm_sync", "B", 0),
    ("program_level", "B", "program_level"),
    ("vpm_param1_feedback", "B", "vpm_param1_feedback"),
    ("vpm_param2_noise_depth", "B", "vpm_param2_noise_depth"),
    ("vpm_param3_shapemodint", "B", "vpm_param3_shapemodint"),
    ("vpm_param4_mod_attack", "B", "vpm_param4_mod_attack"),
    ("vpm_param5_mod_decay", "B", "vpm_param5_mod_decay"),
    ("vpm_param6_modkeytrack", "B", "vpm_param6_modkeytrack"),
    ("user_param1", "B", "user_param1"),
    ("user_param2", "B", "user_param2"),
    ("user_param3", "B", "user_param3"),
    ("user_param4", "B", "user_param4"),
    ("user_param5", "B", "user_param5"),
    ("user_param6", "B", "user_param6"),
    ("user_param1_2_3_4_type", "B", "user_param1_2_3_4_type"),
    ("user_param1_2_3_4_type", "B", "user_param1_2_3_4_type"),
    # 150
    ("program_transpose", "B", "program_transpose"),
    ("delay_dry_wet", "<H", "delay_reverb_dry_wet"),  # 50% wet/dry
    ("reverb_dry_wet", "<H", "delay_reverb_dry_wet"),  # 50% wet/dry
    ("midi_after_touch_assign", "B", fn_midi_after_touch_assign),
    ("str_PRED", "4s", fn_str_pred),
    ("str_SQ", "2s", fn_str_sq),
    ("step_1_16_active_step", "<H", 0),
#    ("bpm", "<H", fn_bmp),
    ("bpm", "<H", "bpm"),
    ("step_length", "B", 0),
    ("step_resolution", "B", 0),
    ("swing", "B", 0),
    ("default_gate_time", "B", 0),
    ("step1_16", "<H", 0),
    ("step1_16_motion", "<H", 0),
    ("motion_slot_1_0_parameter", "B", 0),
    ("motion_slot_1_1_parameter", "B", 0),
    ("motion_slot_2_0_parameter", "B", 0),
    ("motion_slot_2_1_parameter", "B", 0),
    ("motion_slot_3_0_parameter", "B", 0),
    ("motion_slot_3_1_parameter", "B", 0),
    ("motion_slot_4_0_parameter", "B", 0),
    ("motion_slot_4_1_parameter", "B", 0),
    ("motion_slot_1_step1_16", "<H", 0),
    ("motion_slot_2_step1_16", "<H", 0),
    ("motion_slot_3_step1_16", "<H", 0),
    ("motion_slot_4_step1_16", "<H", 0),
    # 1900
    ("step_01_event_data", "52s", fn_empty_step_data),
    ("step_02_event_data", "52s", fn_empty_step_data),
    ("step_03_event_data", "52s", fn_empty_step_data),
    ("step_04_event_data", "52s", fn_empty_step_data),
    ("step_05_event_data", "52s", fn_empty_step_data),
    ("step_06_event_data", "52s", fn_empty_step_data),
    ("step_07_event_data", "52s", fn_empty_step_data),
    ("step_08_event_data", "52s", fn_empty_step_data),
    ("step_09_event_data", "52s", fn_empty_step_data),
    ("step_10_event_data", "52s", fn_empty_step_data),
    ("step_11_event_data", "52s", fn_empty_step_data),
    ("step_12_event_data", "52s", fn_empty_step_data),
    ("step_13_event_data", "52s", fn_empty_step_data),
    ("step_14_event_data", "52s", fn_empty_step_data),
    ("step_15_event_data", "52s", fn_empty_step_data),
    ("step_16_event_data", "52s", fn_empty_step_data),
    # 1022
    ("arp_gate_time", "B", 0),
    ("arp_rate", "B", "arp_rate"),   # **
    ),
    "monologue":(
    # 0
    ("str_PROG", "4s", "str_PROG"),
    ("program_name", "12s", "program_name"),
    ("octave", "B", "keyboard_octave"),
    ("portamento", "B", fn_portamento_time),
    ("key_trig", "B", 0),
    ("voice_mode_depth", "<H", 0),
    ("voice_mode_type", "B", 4),
    ("vco_1_wave", "B", "vco_1_wave"),
    ("vco_1_octave", "B", "vco_1_octave"),
    ("vco_1_pitch", "<H", "vco_1_pitch"),
    ("vco_1_shape", "<H", "vco_1_shape"),
    ("vco_2_wave", "B", "vco_2_wave"),
    ("vco_2_octave", "B", fn_vco_2_octave),
    ("vco_2_pitch", "<H", fn_vco_2_pitch),
    ("vco_2_shape", "<H", fn_vco_2_shape),
    ("sync", "B", fn_sync),
    ("ring", "B", fn_ring),
    ("cross_mod_depth", "<H", 0),
    ("multi_type", "B", 0),
    ("select_noise", "B", 1),
    ("select_vpm", "B", 6),
    ("select_user", "B", 0),
    ("shape_noise", "<H", 1),
    ("shape_vpm", "<H", 6),
    ("shape_user", "<H", 0),
    ("shift_shape_noise", "<H", 0),
    # 50
    ("shift_shape_vpm", "<H", 0),
    ("shift_shape_user", "<H", 0),
    ("vco_1_level", "<H", "vco_1_level"),
    ("vco_2_level", "<H", fn_vco_2_level),
    ("multi_level", "<H", fn_multi_level),
    ("cutoff", "<H", "cutoff"),
    ("resonance", "<H", "resonance"),
    ("cutoff_drive", "B", fn_drive),
    ("cutoff_keyboard_track", "B", "cutoff_kbd_track"),
    ("amp_eg_attack", "<H", fn_amp_eg_attack),
    ("amp_eg_decay", "<H", fn_amp_eg_decay),
    ("amp_eg_sustain", "<H", fn_amp_eg_sustain),
    ("amp_eg_release", "<H", fn_amp_eg_release),
    ("eg_attack", "<H", "eg_attack"),
    ("eg_decay", "<H", "eg_decay"),
    ("eg_int", "<H", "eg_int"),
    ("eg_target", "B", "eg_target"),
    ("lfo_wave", "B", "lfo_type"),
    ("lfo_mode", "B", fn_molg_lfo_mode),
    ("lfo_rate", "<H", "lfo_rate"),
    ("lfo_int", "<H", "lfo_int"),
    ("lfo_target", "B", "lfo_target"),
    ("mod_fx_on_off", "B", 0),
    ("mod_fx_type", "B", 0),
    ("mod_fx_chorus", "B", 0),
    ("mod_fx_ensemble", "B", 0),
    ("mod_fx_phaser", "B", 0),
    ("mod_fx_flanger", "B", 0),
    ("mod_fx_user", "B", 0),
    ("mod_fx_time", "<H", 0),
    ("mod_fx_depth", "<H", 0),
    ("delay_on_off", "B", 0),
    # 100
    ("delay_sub_type", "B", 3),
    ("delay_time", "<H", 0),
    ("delay_depth", "<H", 0),
    ("reverb_on_off", "B", 0),
    ("reverb_sub_type", "B", 0),
    ("reverb_time", "<H", 0),
    ("reverb_depth", "<H", 0),
    ("bend_range_plus", "B", "bend_range_plus"),
    ("bend_range_minus", "B", "bend_range_minus"),
    ("joystick_assign_plus", "B", fn_slider),
    ("joystick_range_plus", "B", fn_bend_range_plus),
    ("joystick_assign_minus", "B", fn_slider),
    ("joystick_range_minus", "B", fn_bend_range_minus),
    ("cv_in_mode", "B", 0),
    ("cv_in_1_assign", "B", 0),
    ("cv_in_1_range", "B", 100),
    ("cv_in_2_assign", "B", 0),
    ("cv_in_2_range", "B", 100),
    ("micro_tuning", "B", 0),
    ("scale_key", "B", 12),
    ("program_tuning", "B", 50),
    ("lfo_key_sync", "B", 0),
    ("lfo_voice_sync", "B", 0),
    ("lfo_target_osc", "B", 0),
    ("cutoff_velocity", "B", fn_cutoff_velocity),
    ("amp_velocity", "B", "amp_velocity"),
    ("multi_octave", "B", fn_molg_multi_octave),
    ("multi_routing", "B", 0),
    ("eg_legato", "B", fn_eg_legato),
    ("portamento_mode", "B", "portamento_mode"),
    ("portamento_bpm_sync", "B", 0),
    ("program_level", "B", 102),
    ("vpm_param1_feedback", "B", 199),
    ("vpm_param2_noise_depth", "B", 199),
    ("vpm_param3_shapemodint", "B", 199),
    ("vpm_param4_mod_attack", "B", 199),
    ("vpm_param5_mod_decay", "B", 199),
    ("vpm_param6_modkeytrack", "B", 199),
    ("user_param1", "B", 0),
    ("user_param2", "B", 0),
    ("user_param3", "B", 0),
    ("user_param4", "B", 0),
    ("user_param5", "B", 0),
    ("user_param6", "B", 0),
    ("user_param5_6_r_r_type", "B", 0),
    ("user_param1_2_3_4_type", "B", 0),
    # 150
    ("program_transpose", "B", 13),
    ("delay_dry_wet", "<H", 512),  # 50% wet/dry
    ("reverb_dry_wet", "<H", 512),  # 50% wet/dry
    ("midi_after_touch_assign", "B", 12),
    ("str_PRED", "4s", fn_str_pred),
    ("str_SQ", "2s", fn_str_sq),
    ("step_1_16_active_step", "<H", 65535),
    ("bpm", "<H", "bpm"),
    ("step_length", "B", "step_length"),
    ("step_resolution", "B", "step_resolution"),
    ("swing", "B", "swing"),
    ("default_gate_time", "B", "default_gate_time"),
    ("step1_16", "<H", "step1_16"),
    ("step1_16_motion", "<H", "step1_16_motion"),  # I think this is the corresponding param
    ("motion_slot_1_0_parameter", "B", "motion_slot_1_0_parameter"),
    ("motion_slot_1_1_parameter", "B", fn_molg_motion_slot_1_parameter),
    ("motion_slot_2_0_parameter", "B", "motion_slot_2_0_parameter"),
    ("motion_slot_2_1_parameter", "B", fn_molg_motion_slot_2_parameter),
    ("motion_slot_3_0_parameter", "B", "motion_slot_3_0_parameter"),
    ("motion_slot_3_1_parameter", "B", fn_molg_motion_slot_3_parameter),
    ("motion_slot_4_0_parameter", "B", "motion_slot_4_0_parameter"),
    ("motion_slot_4_1_parameter", "B", fn_molg_motion_slot_4_parameter),
    ("motion_slot_1_step1_16", "<H", "motion_slot_1_step1_16"),
    ("motion_slot_2_step1_16", "<H", "motion_slot_2_step1_16"),
    ("motion_slot_3_step1_16", "<H", "motion_slot_3_step1_16"),
    ("motion_slot_4_step1_16", "<H", "motion_slot_4_step1_16"),
    # 1900
    ("step_01_event_data", "52s", fn_molg_step_01_event_data),
    ("step_02_event_data", "52s", fn_molg_step_02_event_data),
    ("step_03_event_data", "52s", fn_molg_step_03_event_data),
    ("step_04_event_data", "52s", fn_molg_step_04_event_data),
    ("step_05_event_data", "52s", fn_molg_step_05_event_data),
    ("step_06_event_data", "52s", fn_molg_step_06_event_data),
    ("step_07_event_data", "52s", fn_molg_step_07_event_data),
    ("step_08_event_data", "52s", fn_molg_step_08_event_data),
    ("step_09_event_data", "52s", fn_molg_step_09_event_data),
    ("step_10_event_data", "52s", fn_molg_step_10_event_data),
    ("step_11_event_data", "52s", fn_molg_step_11_event_data),
    ("step_12_event_data", "52s", fn_molg_step_12_event_data),
    ("step_13_event_data", "52s", fn_molg_step_13_event_data),
    ("step_14_event_data", "52s", fn_molg_step_14_event_data),
    ("step_15_event_data", "52s", fn_molg_step_15_event_data),
    ("step_16_event_data", "52s", fn_molg_step_16_event_data),
    # 1022
    ("arp_gate_time", "B", "default_gate_time"),
    ("arp_rate", "B", 5),   # **
    )
}

favorite_template = """\
<?xml version="1.0" encoding="UTF-8"?>

<xd_Favorite>
  <Bank>
    <Data>0</Data>
    <Data>1</Data>
    <Data>2</Data>
    <Data>3</Data>
    <Data>4</Data>
    <Data>5</Data>
    <Data>6</Data>
    <Data>7</Data>
  </Bank>
  <Bank>
    <Data>8</Data>
    <Data>9</Data>
    <Data>10</Data>
    <Data>11</Data>
    <Data>12</Data>
    <Data>13</Data>
    <Data>14</Data>
    <Data>15</Data>
  </Bank>
</xd_Favorite>
"""


"""
og-step-data
+-------+-------+---------+----------------------------------------------+
| Offset|  Bit  |  Range  |  Description                                 |
+-------+-------+---------+----------------------------------------------+
|   0   |       |  0~127  | Note No (1)                           0~127  |
+-------+-------+---------+----------------------------------------------+
|   1   |       |  0~127  | Note No (2)                           0~127  |
+-------+-------+---------+----------------------------------------------+
|   2   |       |  0~127  | Note No (3)                           0~127  |
+-------+-------+---------+----------------------------------------------+
|   3   |       |  0~127  | Note No (4)                           0~127  |
+-------+-------+---------+----------------------------------------------+
|   4   |       |  0~127  | Velocity No (1) 0,1~127=NoEvent,Velocity1~127|
+-------+-------+---------+----------------------------------------------+
|   5   |       |  0~127  | Velocity No (2) 0,1~127=NoEvent,Velocity1~127|
+-------+-------+---------+----------------------------------------------+
|   6   |       |  0~127  | Velocity No (3) 0,1~127=NoEvent,Velocity1~127|
+-------+-------+---------+----------------------------------------------+
|   7   |       |  0~127  | Velocity No (4) 0,1~127=NoEvent,Velocity1~127|
+-------+-------+---------+----------------------------------------------+
|   8   |  0-6  |  0~127  | Gate time (1)        0~72,73~127=0%~100%,TIE |
|   8   |   7   |   0,1   | Trigger switch (1)    0,1=Off,On  *ntoe S4-1 |
+-------+-------+---------+----------------------------------------------+
|   9   |  0-6  |  0~127  | Gate time (2)        0~72,73~127=0%~100%,TIE |
|   9   |   7   |   0,1   | Trigger switch (2)    0,1=Off,On  *ntoe S4-1 |
+-------+-------+---------+----------------------------------------------+
|  10   |  0-6  |  0~127  | Gate time (3)        0~72,73~127=0%~100%,TIE |
|  10   |   7   |   0,1   | Trigger switch (3)    0,1=Off,On  *ntoe S4-1 |
+-------+-------+---------+----------------------------------------------+
|  11   |  0-6  |  0~127  | Gate time (4)        0~72,73~127=0%~100%,TIE |
|  11   |   7   |   0,1   | Trigger switch (4)    0,1=Off,On  *ntoe S4-1 |
+-------+-------+---------+----------------------------------------------+
|  12   |       |  0~255  | Motion Slot 1 Data 1        0~255 *note S4-2 |
+-------+-------+---------+----------------------------------------------+
|  13   |       |  0~255  | Motion Slot 1 Data 2        0~255 *note S4-2 |
+-------+-------+---------+----------------------------------------------+
|  14   |       |  0~255  | Motion Slot 2 Data 1        0~255 *note S4-2 |
+-------+-------+---------+----------------------------------------------+
|  15   |       |  0~255  | Motion Slot 2 Data 2        0~255 *note S4-2 |
+-------+-------+---------+----------------------------------------------+
|  16   |       |  0~255  | Motion Slot 3 Data 1        0~255 *note S4-2 |
+-------+-------+---------+----------------------------------------------+
|  17   |       |  0~255  | Motion Slot 3 Data 2        0~255 *note S4-2 |
+-------+-------+---------+----------------------------------------------+
|  18   |       |  0~255  | Motion Slot 4 Data 1        0~255 *note S4-2 |
+-------+-------+---------+----------------------------------------------+
|  19   |       |  0~255  | Motion Slot 4 Data 2        0~255 *note S4-2 |
+-------+-------+---------+----------------------------------------------+

xd-step-data
+-------+-------+---------+-----------------------------------------------+
| Offset|  Bit  |  Range  |  Description                                  |
+-------+-------+---------+-----------------------------------------------+
|   0   |       |  0~127  | Note No (1)                            0~127  |
+-------+-------+---------+-----------------------------------------------+
|   1   |       |  0~127  | Note No (2)                            0~127  |
+-------+-------+---------+-----------------------------------------------+
|   2   |       |  0~127  | Note No (3)                            0~127  |
+-------+-------+---------+-----------------------------------------------+
|   3   |       |  0~127  | Note No (4)                            0~127  |
+-------+-------+---------+-----------------------------------------------+
|   4   |       |  0~127  | Note No (5)                            0~127  |
+-------+-------+---------+-----------------------------------------------+
|   5   |       |  0~127  | Note No (6)                            0~127  |
+-------+-------+---------+-----------------------------------------------+
|   6   |       |  0~127  | Note No (7)                            0~127  |
+-------+-------+---------+-----------------------------------------------+
|   7   |       |  0~127  | Note No (8)                            0~127  |
+-------+-------+---------+-----------------------------------------------+
|   8   |       |  0~127  | Velocity No (1) 0,1~127=NoEvent,Velocity1~127 |
+-------+-------+---------+-----------------------------------------------+
|   9   |       |  0~127  | Velocity No (2) 0,1~127=NoEvent,Velocity1~127 |
+-------+-------+---------+-----------------------------------------------+
|  10   |       |  0~127  | Velocity No (3) 0,1~127=NoEvent,Velocity1~127 |
+-------+-------+---------+-----------------------------------------------+
|  11   |       |  0~127  | Velocity No (4) 0,1~127=NoEvent,Velocity1~127 |
+-------+-------+---------+-----------------------------------------------+
|  12   |       |  0~127  | Velocity No (5) 0,1~127=NoEvent,Velocity1~127 |
+-------+-------+---------+-----------------------------------------------+
|  13   |       |  0~127  | Velocity No (6) 0,1~127=NoEvent,Velocity1~127 |
+-------+-------+---------+-----------------------------------------------+
|  14   |       |  0~127  | Velocity No (7) 0,1~127=NoEvent,Velocity1~127 |
+-------+-------+---------+-----------------------------------------------+
|  15   |       |  0~127  | Velocity No (8) 0,1~127=NoEvent,Velocity1~127 |
+-------+-------+---------+-----------------------------------------------+
|  16   |  0-6  |  0~127  | Gate time (1)         0~72,73~127=0%~100%,TIE |
|  16   |   7   |   0,1   | Trigger switch (1)     0,1=Off,On  *note S3-1 |
+-------+-------+---------+-----------------------------------------------+
|  17   |  0-6  |  0~127  | Gate time (2)         0~72,73~127=0%~100%,TIE |
|  17   |   7   |   0,1   | Trigger switch (2)     0,1=Off,On  *note S3-1 |
+-------+-------+---------+-----------------------------------------------+
|  18   |  0-6  |  0~127  | Gate time (3)         0~72,73~127=0%~100%,TIE |
|  18   |   7   |   0,1   | Trigger switch (3)     0,1=Off,On  *note S3-1 |
+-------+-------+---------+-----------------------------------------------+
|  19   |  0-6  |  0~127  | Gate time (4)         0~72,73~127=0%~100%,TIE |
|  19   |   7   |   0,1   | Trigger switch (4)     0,1=Off,On  *note S3-1 |
+-------+-------+---------+-----------------------------------------------+
|  20   |  0-6  |  0~127  | Gate time (5)         0~72,73~127=0%~100%,TIE |
|  20   |   7   |   0,1   | Trigger switch (5)     0,1=Off,On  *note S3-1 |
+-------+-------+---------+-----------------------------------------------+
|  21   |  0-6  |  0~127  | Gate time (6)         0~72,73~127=0%~100%,TIE |
|  21   |   7   |   0,1   | Trigger switch (6)     0,1=Off,On  *note S3-1 |
+-------+-------+---------+-----------------------------------------------+
|  22   |  0-6  |  0~127  | Gate time (7)         0~72,73~127=0%~100%,TIE |
|  22   |   7   |   0,1   | Trigger switch (7)     0,1=Off,On  *note S3-1 |
+-------+-------+---------+-----------------------------------------------+
|  23   |  0-6  |  0~127  | Gate time (8)         0~72,73~127=0%~100%,TIE |
|  23   |   7   |   0,1   | Trigger switch (8)     0,1=Off,On  *note S3-1 |
+-------+-------+---------+-----------------------------------------------+
| 24~30 |       |         | Motion Slot 1                      *note S3-2 |
+-------+-------+---------+-----------------------------------------------+
| 31~37 |       |         | Motion Slot 2                      *note S3-2 |
+-------+-------+---------+-----------------------------------------------+
| 38~44 |       |         | Motion Slot 3                      *note S3-2 |
+-------+-------+---------+-----------------------------------------------+
| 45~51 |       |         | Motion Slot 4                      *note S3-2 |
+-------+-------+---------+-----------------------------------------------+

+-------+-------+---------+-------------------------------------+
| Offset|  Bit  |  Range  |  Description                        |
+-------+-------+---------+-------------------------------------+
|   0   |       |  0~255  |  Motion Slot x DATA 1(bit2-9)       | 
|   1   |       |  0~255  |  Motion Slot x DATA 2(bit2-9)       | 
|   2   |       |  0~255  |  Motion Slot x DATA 3(bit2-9)       | 
|   3   |       |  0~255  |  Motion Slot x DATA 4(bit2-9)       | 
|   4   |       |  0~255  |  Motion Slot x DATA 5(bit2-9)       | 
+-------+-------+---------+-------------------------------------+
|   5   |  0-1  |   0~3   |  Motion Slot x DATA 1(bit0-1)       | 
|   5   |  2-3  |   0~3   |  Motion Slot x DATA 2(bit0-1)       | 
|   5   |  4-5  |   0~3   |  Motion Slot x DATA 3(bit0-1)       | 
|   5   |  6-7  |   0~3   |  Motion Slot x DATA 4(bit0-1)       | 
+-------+-------+---------+-------------------------------------+
|   6   |  0-1  |   0~3   |  Motion Slot x DATA 5(bit0-1)       | 
|   6   |  2~7  |         |  Reserved                           |
+-------+-------+---------+-------------------------------------+

"""


"""
Korg's program format tables for the minilogues XD.
Any personal notes are designated Gn.

Minilogue XD
+---------+-------+---------+---------------------------------------------+
|  Offset |  Bit  |  Range  |  Description                                |
+---------+-------+---------+---------------------------------------------+
|   0~3   |       |  ASCII  |  'PROG'                                     |
+---------+-------+---------+---------------------------------------------+
|   4~15  |       |  ASCII  |  PROGRAM NAME [12]                 *note P1 |
+---------+-------+---------+---------------------------------------------+
|   16    |       |  0~4    |  OCTAVE                           0~4=-2~+2 |
+---------+-------+---------+---------------------------------------------+
|   17    |       |  0~127  |  PORTAMENTO                           0~127 |
+---------+-------+---------+---------------------------------------------+
|   18    |       |  0,1    |  KEY TRIG                        0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   19    | L:0~7 |  0~1023 |  VOICE MODE DEPTH                  *note P2 |
|   20    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   21    |       |  1~4    |  VOICE MODE TYPE *note G2          *note P3 |
+---------+-------+---------+---------------------------------------------+
|   22    |       |  0~2    |  VCO 1 WAVE                        *note P4 |
+---------+-------+---------+---------------------------------------------+
|   23    |       |  0~3    |  VCO 1 OCTAVE              0~3=16',8',4',2' |
+---------+-------+---------+---------------------------------------------+
|   24    | L:0~7 |  0~1023 |  VCO 1 PITCH                       *note P5 |
|   25    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   26    | L:0~7 |  0~1023 |  VCO 1 SHAPE                                |
|   27    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   28    |       |  0~2    |  VCO 2 WAVE                        *note P4 |
+---------+-------+---------+---------------------------------------------+
|   29    |       |  0~3    |  VCO 2 OCTAVE              0~3=16',8',4',2' |
+---------+-------+---------+---------------------------------------------+
|   30    | L:0~7 |  0~1023 |  VCO 2 PITCH                       *note P5 |
|   31    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   32    | L:0~7 |  0~1023 |  VCO 2 SHAPE                                |
|   33    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   34    |       |  0,1    |  SYNC                 0,1=SYNC ON, SYNC OFF |
+---------+-------+---------+---------------------------------------------+
|   35    |       |  0,1    |  RING                 0,1=RING ON, RING OFF |
+---------+-------+---------+---------------------------------------------+
|   36    | L:0~7 |  0~1023 |  CROSS MOD DEPTH                            |
|   37    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   38    |       |  0~2    |  MULTI TYPE              0~2=NOISE,VPM,USER |
+---------+-------+---------+---------------------------------------------+
|   39    |       |  0~3    |  SELECT NOISE                      *note P6 |
+---------+-------+---------+---------------------------------------------+
|   40    |       |  0~15   |  SELECT VPM                        *note P7 |
+---------+-------+---------+---------------------------------------------+
|   41    |       |  0~15   |  SELECT USER                       *note P8 |
+---------+-------+---------+---------------------------------------------+
|   42    | L:0~7 |  0~1023 |  SHAPE NOISE                                |
|   43    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   44    | L:0~7 |  0~1023 |  SHAPE VPM                                  |
|   45    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   46    | L:0~7 |  0~1023 |  SHAPE USER                                 |
|   47    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   48    | L:0~7 |  0~1023 |  SHIFT SHAPE NOISE                          |
|   49    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   50    | L:0~7 |  0~1023 |  SHIFT SHAPE VPM                            |
|   51    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   52    | L:0~7 |  0~1023 |  SHIFT SHAPE USER                           |
|   53    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   54    | L:0~7 |  0~1023 |  VCO1 LEVEL                                 |
|   55    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   56    | L:0~7 |  0~1023 |  VCO2 LEVEL                                 |
|   57    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   58    | L:0~7 |  0~1023 |  MULTI LEVEL                                |
|   59    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   60    | L:0~7 |  0~1023 |  CUTOFF                                     |
|   61    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   62    | L:0~7 |  0~1023 |  RESONANCE                                  |
|   63    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   64    |       |  0~2    |  CUTOFF DRIVE                      *note P9 |
+---------+-------+---------+---------------------------------------------+
|   65    |       |  0~2    |  CUTOFF KEYBOARD TRACK             *note G4 |
+---------+-------+---------+---------------------------------------------+
|   66    | L:0~7 |  0~1023 |  AMP EG ATTACK                              |
|   67    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   68    | L:0~7 |  0~1023 |  AMP EG DECAY                               |
|   69    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   70    | L:0~7 |  0~1023 |  AMP EG SUSTAIN                             |
|   71    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   72    | L:0~7 |  0~1023 |  AMP EG RELEASE                             |
|   73    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   74    | L:0~7 |  0~1023 |  EG ATTACK                                  |
|   75    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   76    | L:0~7 |  0~1023 |  EG DECAY                                   |
|   77    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   78    | L:0~7 |  0~1023 |  EG INT                           *note P10 |
|   79    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   80    | H:0~7 |  0~2    |  EG TARGET        0~2=CUTOFF, PITCH2, PITCH |
+---------+-------+---------+---------------------------------------------+
|   81    |       |  0~2    |  LFO WAVE                          *note P4 |
+---------+-------+---------+---------------------------------------------+
|   82    |       |  0~2    |  LFO MODE             0~2=1-SHOT,NORMAL,BPM |
+---------+-------+---------+---------------------------------------------+
|   83    | L:0~7 |  0~1023 |  LFO RATE                         *note P11 |
|   84    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   85    | L:0~7 |  0~1023 |  LFO INT              1~1023,512=-511~511,0 |
|   86    | H:0~1 |         |            -ve range accessed by SHIFT-WAVE |
+---------+-------+---------+---------------------------------------------+
|   87    |       |  0~2    |  LFO TARGET          0~2=CUTOFF,SHAPE,PITCH |
+---------+-------+---------+---------------------------------------------+
|   88    |       |  0,1    |  MOD FX ON/OFF                   0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   89    |       |  1~5    |  MOD FX TYPE                      *note P12 |
+---------+-------+---------+---------------------------------------------+
|   90    |       |  0~7    |  MOD FX CHORUS                    *note P13 |
+---------+-------+---------+---------------------------------------------+
|   91    |       |  0~2    |  MOD FX ENSEMBLE                  *note P14 |
+---------+-------+---------+---------------------------------------------+
|   92    |       |  0~7    |  MOD FX PHASER                    *note P15 |
+---------+-------+---------+---------------------------------------------+
|   93    |       |  0~7    |  MOD FX FLANGER                   *note P16 |
+---------+-------+---------+---------------------------------------------+
|   94    |       |  0~15   |  MOD FX USER                       *note P8 |
+---------+-------+---------+---------------------------------------------+
|   95    | L:0~7 |  0~1023 |  MOD FX TIME                                |
|   96    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   97    | L:0~7 |  0~1023 |  MOD FX DEPTH                               |
|   98    | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   99    |       |  0,1    |  DELAY ON/OFF                    0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   100   |       |  0~19   |  DELAY SUB TYPE                   *note P17 |
+---------+-------+---------+---------------------------------------------+
|   101   | L:0~7 |  0~1023 |  DELAY TIME                                 |
|   102   | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   103   | L:0~7 |  0~1023 |  DELAY DEPTH                                |
|   104   | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   105   |       |  0,1    |  REVERB ON/OFF                   0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   106   |       |  0~19   |  REVERB SUB TYPE                  *note P18 |
+---------+-------+---------+---------------------------------------------+
|   107   | L:0~7 |  0~1023 |  REVERB TIME                                |
|   108   | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   109   | L:0~7 |  0~1023 |  REVERB DEPTH                               |
|   110   | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   111   |       |  0~12   |  BEND RANGE (+)                 OFF~+12Note |
+---------+-------+---------+---------------------------------------------+
|   112   |       |  0~12   |  BEND RANGE (-)                 OFF~-12Note |
+---------+-------+---------+---------------------------------------------+
|   113   |       |  0~28   |  JOYSTICK ASSIGN (+)              *note P19 |
+---------+-------+---------+---------------------------------------------+
|   114   |       |  0~200  |  JOYSTICK RANGE (+)       0~200=-100%~+100% |
+---------+-------+---------+---------------------------------------------+
|   115   |       |  0~28   |  JOYSTICK ASSIGN (-)              *note P19 |
+---------+-------+---------+---------------------------------------------+
|   116   |       |  0~200  |  JOYSTICK RANGE (-)       0~200=-100%~+100% |
+---------+-------+---------+---------------------------------------------+
|   117   |       |  0~2    |  CV IN MODE                       *note P20 |
+---------+-------+---------+---------------------------------------------+
|   118   |       |  0~28   |  CV IN 1 ASSIGN (+)               *note P19 |
+---------+-------+---------+---------------------------------------------+
|   119   |       |  0~200  |  CV IN 1 RANGE (+)        0~200=-100%~+100% |
+---------+-------+---------+---------------------------------------------+
|   120   |       |  0~28   |  CV IN 2 ASSIGN (-)               *note P19 |
+---------+-------+---------+---------------------------------------------+
|   121   |       |  0~200  |  CV IN 2 RANGE (-)        0~200=-100%~+100% |
+---------+-------+---------+---------------------------------------------+
|   122   |       |  0~139  |  MICRO TUNING                     *note P21 |
+---------+-------+---------+---------------------------------------------+
|   123   |       |  0~24   |  SCALE KEY             0~24=-12Note~+12Note |
+---------+-------+---------+---------------------------------------------+
|   124   |       |  0~100  |  PROGRAM TUNING       0~100=-50Cent~+50Cent |
+---------+-------+---------+---------------------------------------------+
|   125   |       |  0,1    |  LFO KEY SYNC                    0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   126   |       |  0,1    |  LFO VOICE SYNC                  0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   127   |       |  0~3    |  LFO TARGET OSC                   *note P22 |
+---------+-------+---------+---------------------------------------------+
|   128   |       |  0~127  |  CUTOFF VELOCITY                            |
+---------+-------+---------+---------------------------------------------+
|   129   |       |  0~127  |  AMP VELOCITY                               |
+---------+-------+---------+---------------------------------------------+
|   130   |       |  0~3    |  MULTI OCTAVE              0~3=16',8',4',2' |
+---------+-------+---------+---------------------------------------------+
|   131   |       |  0,1    |  MULTI ROUTING        0,1=Pre VCF, Post VCF |
+---------+-------+---------+---------------------------------------------+
|   132   |       |  0,1    |  EG LEGATO                       0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   133   |       |  0,1    |  PORTAMENTO MODE                0,1=Auto,On |
+---------+-------+---------+---------------------------------------------+
|   134   |       |  0,1    |  PORTAMENTO BPM SYNC             0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   135   |       | 12~132  |  PROGRAM LEVEL            12~132=-18dB~+6dB |
+---------+-------+---------+---------------------------------------------+
|   136   |       |  0~200  |  VPM PARAM1 (Feedback)    0~200=-100%~+100% |
+---------+-------+---------+---------------------------------------------+
|   137   |       |  0~200  |  VPM PARAM2 (Noise Depth) 0~200=-100%~+100% |
+---------+-------+---------+---------------------------------------------+
|   138   |       |  0~200  |  VPM PARAM3 (ShapeModInt) 0~200=-100%~+100% |
+---------+-------+---------+---------------------------------------------+
|   139   |       |  0~200  |  VPM PARAM4 (Mod Attack)  0~200=-100%~+100% |
+---------+-------+---------+---------------------------------------------+
|   140   |       |  0~200  |  VPM PARAM5 (Mod Decay)   0~200=-100%~+100% |
+---------+-------+---------+---------------------------------------------+
|   141   |       |  0~200  |  VPM PARAM6 (ModKeyTrack) 0~200=-100%~+100% |
+---------+-------+---------+---------------------------------------------+
|   142   |       |         |  USER PARAM1                      *note P23 |
+---------+-------+---------+---------------------------------------------+
|   143   |       |         |  USER PARAM2                      *note P23 |
+---------+-------+---------+---------------------------------------------+
|   144   |       |         |  USER PARAM3                      *note P23 |
+---------+-------+---------+---------------------------------------------+
|   145   |       |         |  USER PARAM4                      *note P23 |
+---------+-------+---------+---------------------------------------------+
|   146   |       |         |  USER PARAM5                      *note P23 |
+---------+-------+---------+---------------------------------------------+
|   147   |       |         |  USER PARAM6                      *note P23 |
+---------+-------+---------+---------------------------------------------+
|   148   |  0~1  |         |  USER PARAM5 TYPE                 *note P24 |
|         |  2~3  |         |  USER PARAM6 TYPE                 *note P24 |
|         |  4~5  |         |  Reserved                                   |
|         |  6~7  |         |  Reserved                                   |
+---------+-------+---------+---------------------------------------------+
|   149   |  0~1  |         |  USER PARAM1 TYPE                 *note P24 |
|         |  2~3  |         |  USER PARAM2 TYPE                 *note P24 |
|         |  4~5  |         |  USER PARAM3 TYPE                 *note P24 |
|         |  6~7  |         |  USER PARAM4 TYPE                 *note P24 |
+---------+-------+---------+---------------------------------------------+
|   150   |       | 1~25    |  PROGRAM TRANSPOSE             -12~+12 Note |
+---------+-------+---------+---------------------------------------------+
|   151   | L:0~7 | 0~1024  |  DELAY DRY WET                              |
|   152   | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   153   | L:0~7 | 0~1024  |  REVERB DRY WET                             |
|   154   | H:0~1 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   155   |       |  0~28   |  MIDI AFTER TOUCH ASSIGN          *note P19 |
+---------+-------+---------+---------------------------------------------+
| 156~159 |       |  ASCII  |  'PRED'                                     |
+---------+-------+---------+---------------------------------------------+
| 160~161 |       |  ASCII  |  'SQ'                              *note S1 |
+---------+-------+---------+---------------------------------------------+
|   162   |   0   |   0,1   |  Step  1 Active Step Off/On      0,1=Off,On |
|   162   |   1   |   0,1   |  Step  2 Active Step Off/On      0,1=Off,On |
|   162   |   2   |   0,1   |  Step  3 Active Step Off/On      0,1=Off,On |
|   162   |   3   |   0,1   |  Step  4 Active Step Off/On      0,1=Off,On |
|   162   |   4   |   0,1   |  Step  5 Active Step Off/On      0,1=Off,On |
|   162   |   5   |   0,1   |  Step  6 Active Step Off/On      0,1=Off,On |
|   162   |   6   |   0,1   |  Step  7 Active Step Off/On      0,1=Off,On |
|   162   |   7   |   0,1   |  Step  8 Active Step Off/On      0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   163   |   0   |   0,1   |  Step  9 Active Step Off/On      0,1=Off,On |
|   163   |   1   |   0,1   |  Step 10 Active Step Off/On      0,1=Off,On |
|   163   |   2   |   0,1   |  Step 11 Active Step Off/On      0,1=Off,On |
|   163   |   3   |   0,1   |  Step 12 Active Step Off/On      0,1=Off,On |
|   163   |   4   |   0,1   |  Step 13 Active Step Off/On      0,1=Off,On |
|   163   |   5   |   0,1   |  Step 14 Active Step Off/On      0,1=Off,On |
|   163   |   6   |   0,1   |  Step 15 Active Step Off/On      0,1=Off,On |
|   163   |   7   |   0,1   |  Step 16 Active Step Off/On      0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   164   | L:0~7 |100~3000 |  BPM                    100~3000=10.0~300.0 |
|   165   | H:0~3 |         |                                             |
+---------+-------+---------+---------------------------------------------+
|   166   |       |  1~16   |  Step Length                                |
+---------+-------+---------+---------------------------------------------+
|   167   |       |  0~4    |  Step Resolution 0~4 = 1/16,1/8,1/4,1/2,1/1 |
+---------+-------+---------+---------------------------------------------+
|   168   |       | -75~+75 |  Swing                                      |
+---------+-------+---------+---------------------------------------------+
|   169   |       |  0~72   |  Default Gate Time             0~72=0%~100% |
+---------+-------+---------+---------------------------------------------+
|   170   |   0   |   0,1   |  Step  1 Off/On                  0,1=Off,On |
|   170   |   1   |   0,1   |  Step  2 Off/On                  0,1=Off,On |
|   170   |   2   |   0,1   |  Step  3 Off/On                  0,1=Off,On |
|   170   |   3   |   0,1   |  Step  4 Off/On                  0,1=Off,On |
|   170   |   4   |   0,1   |  Step  5 Off/On                  0,1=Off,On |
|   170   |   5   |   0,1   |  Step  6 Off/On                  0,1=Off,On |
|   170   |   6   |   0,1   |  Step  7 Off/On                  0,1=Off,On |
|   170   |   7   |   0,1   |  Step  8 Off/On                  0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   171   |   0   |   0,1   |  Step  9 Off/On                  0,1=Off,On |
|   171   |   1   |   0,1   |  Step 10 Off/On                  0,1=Off,On |
|   171   |   2   |   0,1   |  Step 11 Off/On                  0,1=Off,On |
|   171   |   3   |   0,1   |  Step 12 Off/On                  0,1=Off,On |
|   171   |   4   |   0,1   |  Step 13 Off/On                  0,1=Off,On |
|   171   |   5   |   0,1   |  Step 14 Off/On                  0,1=Off,On |
|   171   |   6   |   0,1   |  Step 15 Off/On                  0,1=Off,On |
|   171   |   7   |   0,1   |  Step 16 Off/On                  0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   172   |   0   |   0,1   |  Step  1 Motion Off/On           0,1=Off,On |
|   172   |   1   |   0,1   |  Step  2 Motion Off/On           0,1=Off,On |
|   172   |   2   |   0,1   |  Step  3 Motion Off/On           0,1=Off,On |
|   172   |   3   |   0,1   |  Step  4 Motion Off/On           0,1=Off,On |
|   172   |   4   |   0,1   |  Step  5 Motion Off/On           0,1=Off,On |
|   172   |   5   |   0,1   |  Step  6 Motion Off/On           0,1=Off,On |
|   172   |   6   |   0,1   |  Step  7 Motion Off/On           0,1=Off,On |
|   172   |   7   |   0,1   |  Step  8 Motion Off/On           0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   173   |   0   |   0,1   |  Step  9 Motion Off/On           0,1=Off,On |
|   173   |   1   |   0,1   |  Step 10 Motion Off/On           0,1=Off,On |
|   173   |   2   |   0,1   |  Step 11 Motion Off/On           0,1=Off,On |
|   173   |   3   |   0,1   |  Step 12 Motion Off/On           0,1=Off,On |
|   173   |   4   |   0,1   |  Step 13 Motion Off/On           0,1=Off,On |
|   173   |   5   |   0,1   |  Step 14 Motion Off/On           0,1=Off,On |
|   173   |   6   |   0,1   |  Step 15 Motion Off/On           0,1=Off,On |
|   173   |   7   |   0,1   |  Step 16 Motion Off/On           0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
| 174~175 |       |         |  Motion Slot 1 Parameter           *note S2 |
+---------+-------+---------+---------------------------------------------+
| 176~177 |       |         |  Motion Slot 2 Parameter           *note S2 |
+---------+-------+---------+---------------------------------------------+
| 178~179 |       |         |  Motion Slot 3 Parameter           *note S2 |
+---------+-------+---------+---------------------------------------------+
| 180~181 |       |         |  Motion Slot 4 Parameter           *note S2 |
+---------+-------+---------+---------------------------------------------+
|   182   |   0   |         |  Motion Slot 1 Step  1 Off/On    0,1=Off,On |
|   182   |   1   |         |  Motion Slot 1 Step  2 Off/On    0,1=Off,On |
|   182   |   2   |         |  Motion Slot 1 Step  3 Off/On    0,1=Off,On |
|   182   |   3   |         |  Motion Slot 1 Step  4 Off/On    0,1=Off,On |
|   182   |   4   |         |  Motion Slot 1 Step  5 Off/On    0,1=Off,On |
|   182   |   5   |         |  Motion Slot 1 Step  6 Off/On    0,1=Off,On |
|   182   |   6   |         |  Motion Slot 1 Step  7 Off/On    0,1=Off,On |
|   182   |   7   |         |  Motion Slot 1 Step  8 Off/On    0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
|   183   |   0   |         |  Motion Slot 1 Step  9 Off/On    0,1=Off,On |
|   183   |   1   |         |  Motion Slot 1 Step 10 Off/On    0,1=Off,On |
|   183   |   2   |         |  Motion Slot 1 Step 11 Off/On    0,1=Off,On |
|   183   |   3   |         |  Motion Slot 1 Step 12 Off/On    0,1=Off,On |
|   183   |   4   |         |  Motion Slot 1 Step 13 Off/On    0,1=Off,On |
|   183   |   5   |         |  Motion Slot 1 Step 14 Off/On    0,1=Off,On |
|   183   |   6   |         |  Motion Slot 1 Step 15 Off/On    0,1=Off,On |
|   183   |   7   |         |  Motion Slot 1 Step 16 Off/On    0,1=Off,On |
+---------+-------+---------+---------------------------------------------+
| 184~185 |       |         |  Motion Slot 2 Step Off/On (same as Slot 1) |
+---------+-------+---------+---------------------------------------------+
| 186~187 |       |         |  Motion Slot 3 Step Off/On (same as Slot 1) |
+---------+-------+---------+---------------------------------------------+
| 188~189 |       |         |  Motion Slot 4 Step Off/On (same as Slot 1) |
+---------+-------+---------+---------------------------------------------+
| 190~241 |       |         |  Step 1 Event Data                 *note S3 |
| 242~293 |       |         |  Step 2 Event Data                 *note S3 |
|   :     |       |         |                                             |
|   :     |       |         |                                             |
| 426~1021|       |         |  Step 16 Event Data                *note S3 |
+---------+-------+---------+---------------------------------------------+
|  1022   |       |  0~72   |  ARP Gate Time               0~72 = 0%~100% |
+---------+-------+---------+---------------------------------------------+
|  1023   |       |  0~10   |  ARP Rate                          *note S4 |
+---------+-------+---------+---------------------------------------------+

*Note G3
Korg's note P3 table shows 1, 2, 2, 3 but should be 1, 2, 3, 4
Korg's note P2 shows 0~73:5th but it should be more like 0~1:Mono 2~73:5th
I don't know if the breakover is from 1 to 2 or greater, but I will assume that.

Delay time needs scaling: og max delay=350ms, xd high-pass max delay=654ms

"""

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


factory_presets = """\
cb01be89a2e7d6335de5ea5559850e3f Runner Brass
828a17a7ec231d643c7bc95570ab35f3 June Pad    
cce1a2df0c37f6b48309f4002e587115 In My Dream
9ed361a058ba9dc54c5ab20a7fb7bd34 Solid Bass
b4b66ba5a40e62fe71d12b2f78c15f72 Selfosc Lead
c5f5a810fd9c62da12a3f6959f6c96b4 Opal Mine
515c74cab427c45f66167936183a273b ReeceFlux
fa4a4e191bc20ae66a99714aa4d16cec Sherbet
077a6855829ad31b1ca4800687bf64f5 Raid Rush
e19bb0e77bb47c23b6130c4849a66ec4 Sparkle
2734d24b82e4c67cdaf688c0eaacf04c Poly Spread
394df5e962c94164d89b5909c447e303 Harp-like
c89d517c218463460db08b3e5af4c70d Poly Sync
58db77e6adaeb9e6df076d6d025a1cd2 Cinematica
6dafdfb1f79a70567c53923bbfc51452 Vertigo
63cf85686ef60d90c9d5be145588ee36 Frantasia
835c950536a1a9dc2ccffb44880a8207 Warm Circuit
f8650eed1eb541b011c4b4f7951130d6 Fat Bass
2ab5e2fb0e125b7cdd3b87fc2cc24acc NeuModulator
65df366ffb105801efb921ee5ef6c43f Too the Deep
36d23d6e5b657b28ce2654f189d4b9bb Stab Saw
03c47dd09b3d3fdc01965cb0a4205758 Phasepad
3723f4dd120736767e63122d21f1e380 Bright Poly 
aa26a738b5a6373594d5ac65d636c333 Marina
010a9e33798af327ab1bbcad135fbb5b Anthem Synth
58f328ef8afbc0eae59d1065c7836c1f 2 Saw Oktave
88a3b59f5446469630d825a57463a2b2 Mover
6859109029c00c25cbef5ca821020eaf Triple Saw
7ebf22b774f5945c77894ac7fc9c25d9 Prologue
cf058bb58526275e0113c1660906dd19 1973
584a33ecb5b270411b5be62a133fc6b8 TriSync
46562cfa70cff10079693612da0243bf Stella
dce6b2b15fcf781ca162693b016c7ef5 Simple Saw  
dff2e9006bd5681af8f611a44d70c2ac Simple Sqr  
69c7de312b9765cca9e1303a9f29f003 Profetique
e65ff06da784a7be134932e774719d53 Electro Funk
78cb3d2c18cd0e78191cf2ea0e685e95 Detune Comp 
0481a25b80fe12efc064d368b84d893c Krelus
aa8c958cbd2cd580000924b563f2f3aa Soft Brass
07f4d6b28b4c70a9afcfd19c02e1a995 O-Bee Brass
efe575da2a5f472df37c73e95fb499aa Prolly 800
56b7074e0ca940601276bed4cbe7faab HUGE Score!
02d006e5983702eb68afd5c6f10945fe Yacht Rock  
48cb04104a88376aed2228ea2b67c7a3 Synth Brass
8c3aeb15cc607e3aae52b19bc172d563 Cork
8307c132720d8c1a590702fb09e41ac5 Destiny
66dbedb540b08120d021215d0f906c3c Star Connect
3f264b47ec10b1428594fdbbc195f41c Sunset Synth
aaef2ef12d52100a776c6e8d86a388a4 Pole 2 pole
e3a45d4bfd3ccd8001fbaff9ee13f5eb Haunted
5e5f139cfafb749000897a9b4d0d2ca6 Steaming Pod
59eabf7102b09c317fd80f3a5e1958e7 Smooth 5th
838ce42d6b82f9ba7f144c8d3d009817 D51
2c14f151e91f413d82c91dc04f131a08 Code Snipper
000a2f31c2e7a374fc88bcac93438df8 Mod Me Sigma
06b7b66cd460c0b33c7cb87ff350b405 Sine Pad
90e00f0becdf89d5f7eae42e3d8e3ef4 Gentle Pad
1d4d4a08c9447f84dc52673fb97615c9 Winters Tale
5d4e627cb06fd4c427ec262af48b9b0e Noise Ping
1899b49580a624740cefbc93bd951fed Logue Pad
9e372d63aa9411ffe609a9d4a837851b Palmers Gone
dbcc6830bcccf752e2174643fc429468 Big Rise
33647a9b4cf4fa9e3639736900858d97 Pulse Pad
248c24d7fdb782df162135f802fe8f19 SoftPadVCFMd
16b4838a8b2b84723bbd98a4c265e84c Pad Close
6c6c413641630eb020c707f0e1e03b47 Lush Pad
4a0e18d06abd0cd69e07a93d2291e770 Pad Brass
f9c08a8f56bcb1649482569c6f9c4897 Perseus
1d4d5891d754117efcc35fd1b196a30f Chillipad
eb07baf6c544adcdee587c9ee3352ddb Pipin'Hot
17245e13b6eb68b64decaaf2ff812cda Enormous Pad
c0a587f8f92c7db23116c6713aa86c53 PWM Strings
65d6abf3a61055abe23ef3d77d52e4bf Pad Open
b83430ab76ad7022785c876a04873ff9 Warm Strings
dfe629d8c2effd94dc7da022e16a4b9a Humana
c25c9116aac60cc154307e6bb170a7a0 Archestra
34309a19ec10447754cb2f15bc3a94d4 June Morning
e8d54e459f1d9307d1a8a4e380ce0836 SolarStrings
f92fe77a2e56fe62913650e173596804 Out There
5c1909feb6b3e4b7df9175aa8182bb0a UncleaNuclea
dc48a650a103810ae477da52cfba1766 Blurry Flute
e1361ea8b44db3e01d2da39f99f6b973 Awaken Pad
9cb0d233dd0b188fb6959ab33014a9b4 Moving Pad
12bcf3d6caf27bdf4de99e082c1ebc46 AngeIique
b9cf75b7e63b4c0986cf6b5912465892 VPM Sweeper
a696bc09ef20cab7a76052509c4c18f1 Dark Ocean  
781f6c72feaa411a31abb3edfec3a75e Ghosts Choir
a5f6018954c7cc96e4884485017a7208 Vocoder Pad
d57f58831dbd40e6c4e0a3f8ffb2d2a1 Air Vox
13fb2babcfb062e0791d0e066c3ee303 Big Sweep
b175304731e1b065afbba2191b68e72a Bright Idea
6e4f02f690602ca4f1d0b2a4ef711e0f Nomad Riser
1193d3334aba2eef8b56219425c8b02a Rusty Sword
12f25bd09511a141179aec425465476d Organique
a72aea72cf814f5158c872bac8373ec1 60's Organ
d1e759cb2a09e495abc08819897641c0 Basic Organ
5c1dcd3aec590b73de7570aa0b9c065a Tonewheel
f61f72d4b847555760f1c45f5b9040e4 Perc Saws
de03af6399d4454e37cc6e65cc2158e8 Analog Clav
58866ea83413ead0050b82ac45ab7bc9 Synth Clav
2e1684a3c57f4ef01cf04f4d048e9279 EP logue
2fbb06009520dcd8114c3707d6f04e91 Synth Piano
04b360e4949eed46b69b0fdd6dcdeee0 Snow Piano
4afcc22884c75f08d11e61659973acf1 VPM Pad EP 1
2561487b7599ead282331a2bc2424cf0 VPM Pad EP 2
3e51f497a52dc4ead6aa407805ffee14 Cave Echo
3a87b13ceea2668e59751626cf19065f Gentle Ocean
4480a51f14580827100178920f018d79 Droplets
6b47c6f4a50ca03f0838badca819acbd Pop Bell    
9d0a6620364c626614dbc440d4c0d408 Glasskey
aba93bc525e06c9eb8d7caa3cbd81fc0 Warm Bells  
479b229b08843ffb402e450599bb47ee Sanctuary
d476a459481ef7811d8bdf3f4febb693 LALA Pad
dcbb19ae8a33dfd88e2218a1115aab4e Icicycles
347f970bf2dbdb34807cacd70c0ae6bf Dorf Town
c1781c81d4fcb42fa7fa6b4843f7a973 The Chapel
43b9e624752da9591cf4d11ee975dba9 Box O' Trix
3ec2456bde70f5ffced5c4f02cfc2ed8 Metal-like
a6183c2ea77e45aa200c617c556c76d2 Steely Drum
82ed26c598c606cf965c1b5d1da18759 Megaorganic
7cf474b6e6e70d4a154e611469878ddd Carillon
7a9dc2a0158a0c918a8ad468390d9324 Metabell
fdd2e21a5b821d53f576d343f1bd8217 Short Hop
ab645ba5eaf213b92649484273661fe9 Lead Attack
ecc525a9fa9022ce08d6c80d315fdacc Vel Pluck
f09750e71c8ed7880c03d4b31fdf78b3 Pizzverb
be39e63fc057f148b4036fdeefa1c3be Majesty
7b546aa430d5dafece07b15fafcd0356 Harp
f350d206ad2cfb6117577fc66b24b6f0 Mod Me Snow 
e7863009e6848f52706f2425ab439b66 Future Shape
85e48036c034ab78b139eaf9a5ec6146 Datrap Sub
5c313ac1d085fce050a1fd0478cb43f9 Kickin'Bass
af7761fec4f82ddf3595502eaf2d8328 Kickbass
f6024dba04a78dbafb1537177a92da83 Double Vase
e45aafdd9bf66244e633a3f259d4d307 Perc Bass
da1b23a6a32de64db973c8f5dbbb6231 Simple Bass
8d5c51b0172e9fc26ec9a7ad99040e35 House Bass
dbd1c0250fc01e262beb76664e98599c KameleonBass
49780046ab23de49ba2ef8ec687ddb8f Squelch Bass
6ba564dc7ed8c026f35473ba1ab77ede Bassline
36627e616036d8733dbf2aa39f85978c Drive Acid
da1b640ef03177a9da6b218fe2153450 Squ Rez Bass
a1be42945915a465b10eb9bd5404b69f 80sWireBass
0e8b5c1ab0574c9c72c234a6c477fcd8 M.G.B.
4f60d90a61c4fd3d4220a58529d26228 Glide Bass
329470bde1f2085b93ed37ea8bcd9a1a Organ Bass
a272a01c09f681f2578809a279bd6f7f Bottom Bass
6c3394b631d04aa94287fcdbb5fc9703 Chunky Bass
5422cae96f677916372273f198fc5a6e Synwave Bass
8ea14c09f9e297b7256924502eee0346 Reso Bass
b9ea4301f34d055a855c34951c82052a Trusted Guy
19008b3607effe600f81981ff9e0ca12 BigFatAnalog
d58cf4e70c883407ad4dc52e941b8117 FunctionBass
fc6d0e4aaa4959f0f1d7e4bd70742222 Sink Tank
7b05840dfa0f60e6853f8ddbcefb1bf6 Bass Stab
db29d8800df5d078a93e5a136fc9ebe8 Decode Soil
71479cf06f4a3f7862538ff0106a6972 Dawndrezz
34ceb484957372b385dda1e82c2dabe7 Bass/Lead
e435badfa3ee8a63c02d1a75d37bbe39 Buzz Freq
1d1a6dd66b08ec2cbec2e9d3e7955cb1 King Hive
0ed1d430362f99a9e6777a204e9f788a PhatSaw Bass
bc2b1f61e24b2f45b2f64db9c50b4330 Surge Bass
6e50f8fa2a762fc1c63a25554ea7a14b Light Blast
6de892402a56b7707fcb658243a42f7c Mumblebass
ebff2db76539f9346171e72c5f0c0b94 Acidwheel
16f32c5a06fe4228415a5bbe59543b5b Arp StufpH
ad0c95423bc679351cf53078c934db90 Metal Power
d15a449e184cbaec59c6d6888a517af4 Mooncontact
52b4bb9d6be558e71a6c5d976a49deea Dark Lead
55dde4b95aa5ff43ea1c7640563c35af 70s SynLead
1078cff70175418a084acdb75a4448bb Perc Lead
14026c97033fd19fffa4f99d3c468b6c Chip Lead
1cba8cd6cd47874cac9df25264d1b1ad Vintage Horn
b9975a4537abfe7fb427fab21eb65261 Classic Lead
ff8c113875c7c787e26d9b489e537a79 Sync Lead
224e9d0b8a04047746d80a1e8208648b SYNC!!
5bf2e95e4eb0adf73d737bb6dec33826 CurryFlavour
738127668af251239347edc3cf61897c Growl
e1f29f1694f36145cfd53af0d4cdcbe2 Firearm SFX
3cc5a57dd136fabb089b535ce3c3a536 Sunday Lead
e533cab8ba449dfba07aac199e374d87 Waking Beast
99b36ec3ca0c4ca65e0c369deb4aaf8d DriveMetalLd
200934adab10bf63591a8d077cc4afa1 Octave Lead
3c4541e05923525427b6040f40b8ce6c Flangie Lead
e6d34a7682725db01f2ccadff745b983 Disco Lead
df3b3249222fe4f5a8a61454eb4e7712 Detune Lead
0a1af43848a757c5da32a341481d35d4 Dream Lead
3d5d54347884edc8e9e07f85e8f3bc64 Oh Yeah!
9a07c7e37f2f1798252ca339bda375cf Weekend Hymn
e3f98db5bc76c738681ba9ff1b569701 MicroK Lead
f1aae8c07a313fc323a183c69ad7fd69 VCF Lead
1ce473fef7b5c9a3eb8686bb6a824670 Octave Dive
bac77f09a1d0e548028c9e8bc7617a8d Modern Luck
c960179acd14122c66a02edb2ff0274b Phatpluk
1210bff06b036a3265a4e7f52034b79b Dirty Pluck
32edc38c33e6cf070eef9b2bc4e99fec FerrousStab
8e7de07e0299c311b5f95e916e625f6d Spooky Sound
dcab140bae19fb71b49e24794ee9ff47 Prayer Lead
6f51857d65c125fe6ca3dd07bb91ccab Marzcontact
a94ef092fb39f43bd5d86bf8bbc8a5fa #modular
fdce182e33c698165360d994faaba893 Manoeuvers
4304d3122e690de749103f0b8c5a926b Voice Lead
c91d33223bccbf4b53862953b41e8c9a Wave Ride
9afb28fc0d255dac4721ec08ff39211b PhaseShifter
a1bbcc312af19853a79e50914c0d101f Big Five
5dd93e693883ba467aa7f599583c7d80 5 Lead
3f10f3ebfe95f554bc3cec4f92d5d1ea Stabby House
4a668be3f682f1cb2b3abb6d1bf828e7 House Chord
6b7ee3283360de58822f5f6ca31e3569 8track House
54a7bd9bf7e0c7bfe86063c8bc31bad3 Wire Code   
a1b4fc9c8662f0eebc256de7bdda970c Metal Zing
2435e9a2037ab961e3b402ab6a9b987c Resurgence
8805af0d7595ab10f1d93e36eb22610a Strobe Night
4b03ac68e6053f297e3f5117c78f8d71 Flashin' Vox
c923cea32a384ef632e616c1df2effd4 Repeat Chord
a4b6218018ef1c2057173c7b4f1ecd5e Skeletonblue
b57a0262287587c50b7d5f4e495bc652 Sign Times
96f6a25cd001f9450ab3fb62e49ea602 Soft Arppad
09fa4f335366c30aca23e0fc5519af72 Stairway
685fa9943db5a5c8322abd6aa9c0870c Exciter
fd70f69396582b495f4b6d61862e4fc9 Hangry Hound
b00d482ad0532e95a2ea04ea59743001 Arpsteroids 
19745a6abaa6deca1ee28a0a9e5580b2 Barp
50c290ad446e3684046d08c63d7b85e2 Space Arp
921c33620214b5d1ee3f347e15ffb81b Gear Goggles
99a644cca673dfabb24ba2ce2062012e Mean Deal
db5f03ed511b986b192c8d61bfd3a045 New Birth
1d726211e7ea07167b3549c16d5cd008 Arp + Pad
8944e408fdd182833ad6cff5f9644233 Specter
5a8813c48e3fe34af37af2ec71e93d79 Dedspce(hld)
9c1b1c5779c6b2ed3a1c57374f59220d Forlorn
920d9a8480ed87cda05ac581c463830f Night Drive
e22440c75045f1b438546833525d8d87 Runner Blade
4883de881854dc74764360813e451cac Epiphany
23f1748416af7e6a4cc3ca1fa23c27bc Sci-bi
1eb84661f214c1d17abbcde2874542f9 Plucky Split
e68fcab16394ddb953a2a559d5e5af9d Old Scores
decb6d5c847cc4508ab91f1192177677 Winter Wind
e51bf1b12de8353bd3a7e7c7f2ab4b0c Explosion
59b30d8305d6344510c8c6eee031f79c Fly-by
fa678f0767895cd394c6905718761d40 Blown Charge
23e792ef19149e8f74a50cff55e6e9db Sci-Fi Sweep
b6cfa4dbad368004db6805d59fe4cf0e Horror Morph
5be39bb8b70791777f3660bf012f19aa Dome Horn
a4674c72c4bb7d51c4f3a751e21758f5 TH Ex
736e3e8154aa126fa64271644a5bc5bb ShootingStar
bb4fe7f74feda58c342ab07131add298 EnergyCharge
ea9d190b5a961e62933d2daa83678a07 Doncamatic
3cdfdc1d3231b663bfbb4d474c2c743b Analog Tom
780fed8fb56e04ce845edae7e8e2ebe1 tEcHpLuNk
"""
factory_hashes = [l.split()[0] for l in factory_presets.splitlines()]
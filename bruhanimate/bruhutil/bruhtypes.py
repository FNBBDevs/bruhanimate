"""
Copyright 2023 Ethan Christensen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Literal


Font = Literal[
    "1943____",
    "1row",
    "3-d",
    "3d-ascii",
    "3d_diagonal",
    "3x5",
    "4max",
    "4x4_offr",
    "5lineoblique",
    "5x7",
    "5x8",
    "64f1____",
    "6x10",
    "6x9",
    "acrobatic",
    "advenger",
    "alligator",
    "alligator2",
    "alpha",
    "alphabet",
    "amc_3_line",
    "amc_3_liv1",
    "amc_aaa01",
    "amc_neko",
    "amc_razor",
    "amc_razor2",
    "amc_slash",
    "amc_slider",
    "amc_thin",
    "amc_tubes",
    "amc_untitled",
    "ansi_regular",
    "ansi_shadow",
    "aquaplan",
    "arrows",
    "ascii_new_roman",
    "ascii___",
    "asc_____",
    "assalt_m",
    "asslt__m",
    "atc_gran",
    "atc_____",
    "avatar",
    "a_zooloo",
    "b1ff",
    "banner",
    "banner3-D",
    "banner3",
    "banner4",
    "barbwire",
    "basic",
    "battlesh",
    "battle_s",
    "baz__bil",
    "bear",
    "beer_pub",
    "bell",
    "benjamin",
    "big",
    "bigchief",
    "bigfig",
    "big_money-ne",
    "big_money-nw",
    "big_money-se",
    "big_money-sw",
    "binary",
    "block",
    "blocks",
    "blocky",
    "bloody",
    "bolger",
    "braced",
    "bright",
    "brite",
    "briteb",
    "britebi",
    "britei",
    "broadway",
    "broadway_kb",
    "bubble",
    "bubble_b",
    "bubble__",
    "bulbhead",
    "b_m__200",
    "c1______",
    "c2______",
    "calgphy2",
    "caligraphy",
    "calvin_s",
    "cards",
    "catwalk",
    "caus_in_",
    "char1___",
    "char2___",
    "char3___",
    "char4___",
    "charact1",
    "charact2",
    "charact3",
    "charact4",
    "charact5",
    "charact6",
    "characte",
    "charset_",
    "chartr",
    "chartri",
    "chiseled",
    "chunky",
    "clb6x10",
    "clb8x10",
    "clb8x8",
    "cli8x8",
    "clr4x6",
    "clr5x10",
    "clr5x6",
    "clr5x8",
    "clr6x10",
    "clr6x6",
    "clr6x8",
    "clr7x10",
    "clr7x8",
    "clr8x10",
    "clr8x8",
    "coil_cop",
    "coinstak",
    "cola",
    "colossal",
    "computer",
    "com_sen_",
    "contessa",
    "contrast",
    "convoy__",
    "cosmic",
    "cosmike",
    "cour",
    "courb",
    "courbi",
    "couri",
    "crawford",
    "crawford2",
    "crazy",
    "cricket",
    "cursive",
    "cyberlarge",
    "cybermedium",
    "cybersmall",
    "cygnet",
    "c_ascii_",
    "c_consen",
    "danc4",
    "dancing_font",
    "dcs_bfmo",
    "decimal",
    "deep_str",
    "defleppard",
    "def_leppard",
    "delta_corps_priest_1",
    "demo_1__",
    "demo_2__",
    "demo_m__",
    "devilish",
    "diamond",
    "diet_cola",
    "digital",
    "doh",
    "doom",
    "dos_rebel",
    "dotmatrix",
    "double",
    "double_shorts",
    "drpepper",
    "druid___",
    "dwhistled",
    "d_dragon",
    "ebbs_1__",
    "ebbs_2__",
    "eca_____",
    "eftichess",
    "eftifont",
    "eftipiti",
    "eftirobot",
    "eftitalic",
    "eftiwall",
    "eftiwater",
    "efti_robot",
    "electronic",
    "elite",
    "epic",
    "etcrvs__",
    "e__fist_",
    "f15_____",
    "faces_of",
    "fairligh",
    "fair_mea",
    "fantasy_",
    "fbr12___",
    "fbr1____",
    "fbr2____",
    "fbr_stri",
    "fbr_tilt",
    "fender",
    "filter",
    "finalass",
    "fireing_",
    "fire_font-k",
    "fire_font-s",
    "flipped",
    "flower_power",
    "flyn_sh",
    "fourtops",
    "fp1_____",
    "fp2_____",
    "fraktur",
    "funky_dr",
    "fun_face",
    "fun_faces",
    "future_1",
    "future_2",
    "future_3",
    "future_4",
    "future_5",
    "future_6",
    "future_7",
    "future_8",
    "fuzzy",
    "gauntlet",
    "georgi16",
    "georgia11",
    "ghost",
    "ghost_bo",
    "ghoulish",
    "glenyn",
    "goofy",
    "gothic",
    "gothic__",
    "graceful",
    "gradient",
    "graffiti",
    "grand_pr",
    "greek",
    "green_be",
    "hades___",
    "heart_left",
    "heart_right",
    "heavy_me",
    "helv",
    "helvb",
    "helvbi",
    "helvi",
    "henry_3d",
    "heroboti",
    "hex",
    "hieroglyphs",
    "high_noo",
    "hills___",
    "hollywood",
    "home_pak",
    "horizontal_left",
    "horizontal_right",
    "house_of",
    "hypa_bal",
    "hyper___",
    "icl-1900",
    "impossible",
    "inc_raw_",
    "invita",
    "isometric1",
    "isometric2",
    "isometric3",
    "isometric4",
    "italic",
    "italics_",
    "ivrit",
    "jacky",
    "jazmine",
    "jerusalem",
    "joust___",
    "js_block_letters",
    "js_bracket_letters",
    "js_capital_curves",
    "js_cursive",
    "js_stick_letters",
    "katakana",
    "kban",
    "keyboard",
    "kgames_i",
    "kik_star",
    "knob",
    "konto",
    "konto_slant",
    "krak_out",
    "larry3d",
    "lazy_jon",
    "lcd",
    "lean",
    "letters",
    "letterw3",
    "letter_w",
    "lexible_",
    "lil_devil",
    "line_blocks",
    "linux",
    "lockergnome",
    "madrid",
    "mad_nurs",
    "magic_ma",
    "marquee",
    "master_o",
    "maxfour",
    "mayhem_d",
    "mcg_____",
    "merlin1",
    "merlin2",
    "mig_ally",
    "mike",
    "mini",
    "mirror",
    "mnemonic",
    "modern__",
    "modular",
    "morse",
    "morse2",
    "moscow",
    "mshebrew210",
    "muzzle",
    "nancyj-fancy",
    "nancyj-improved",
    "nancyj-underlined",
    "nancyj",
    "new_asci",
    "nfi1____",
    "nipples",
    "notie_ca",
    "npn_____",
    "nscript",
    "ntgreek",
    "nvscript",
    "o8",
    "octal",
    "odel_lak",
    "ogre",
    "ok_beer_",
    "old_banner",
    "os2",
    "outrun__",
    "pacos_pe",
    "panther_",
    "patorjk's_cheese",
    "patorjk-hex",
    "pawn_ins",
    "pawp",
    "peaks",
    "pebbles",
    "pepper",
    "phonix__",
    "platoon2",
    "platoon_",
    "pod_____",
    "poison",
    "puffy",
    "puzzle",
    "pyramid",
    "p_skateb",
    "p_s_h_m_",
    "r2-d2___",
    "radical_",
    "rad_phan",
    "rad_____",
    "rainbow_",
    "rally_s2",
    "rally_sp",
    "rammstein",
    "rampage_",
    "rastan__",
    "raw_recu",
    "rci_____",
    "rectangles",
    "red_phoenix",
    "relief",
    "relief2",
    "rev",
    "ripper!_",
    "road_rai",
    "rockbox_",
    "rok_____",
    "roman",
    "roman___",
    "rot13",
    "rotated",
    "rounded",
    "rowancap",
    "rozzo",
    "runic",
    "runyc",
    "sans",
    "sansb",
    "sansbi",
    "sansi",
    "santa_clara",
    "sblood",
    "sbook",
    "sbookb",
    "sbookbi",
    "sbooki",
    "script",
    "script__",
    "serifcap",
    "shadow",
    "shimrod",
    "short",
    "skateord",
    "skateroc",
    "skate_ro",
    "sketch_s",
    "slant",
    "slant_relief",
    "slide",
    "slscript",
    "sl_script",
    "small",
    "small_caps",
    "small_poison",
    "small_shadow",
    "small_slant",
    "smisome1",
    "smkeyboard",
    "smscript",
    "smshadow",
    "smslant",
    "smtengwar",
    "sm______",
    "soft",
    "space_op",
    "spc_demo",
    "speed",
    "spliff",
    "stacey",
    "stampate",
    "stampatello",
    "standard",
    "starwars",
    "star_strips",
    "star_war",
    "stealth_",
    "stellar",
    "stencil1",
    "stencil2",
    "stforek",
    "stick_letters",
    "stop",
    "straight",
    "street_s",
    "stronger_than_all",
    "sub-zero",
    "subteran",
    "super_te",
    "swamp_land",
    "swan",
    "sweet",
    "tanja",
    "tav1____",
    "taxi____",
    "tec1____",
    "tecrvs__",
    "tec_7000",
    "tengwar",
    "term",
    "test1",
    "the_edge",
    "thick",
    "thin",
    "this",
    "thorned",
    "threepoint",
    "ticks",
    "ticksslant",
    "tiles",
    "times",
    "timesofl",
    "tinker-toy",
    "ti_pan__",
    "tomahawk",
    "tombstone",
    "top_duck",
    "train",
    "trashman",
    "trek",
    "triad_st",
    "ts1_____",
    "tsalagi",
    "tsm_____",
    "tsn_base",
    "tty",
    "ttyb",
    "tubular",
    "twin_cob",
    "twisted",
    "twopoint",
    "type_set",
    "t__of_ap",
    "ucf_fan_",
    "ugalympi",
    "unarmed_",
    "univers",
    "usaflag",
    "usa_pq__",
    "usa_____",
    "utopia",
    "utopiab",
    "utopiabi",
    "utopiai",
    "varsity",
    "vortron_",
    "war_of_w",
    "wavy",
    "weird",
    "wet_letter",
    "whimsy",
    "wow",
    "xbrite",
    "xbriteb",
    "xbritebi",
    "xbritei",
    "xchartr",
    "xchartri",
    "xcour",
    "xcourb",
    "xcourbi",
    "xcouri",
    "xhelv",
    "xhelvb",
    "xhelvbi",
    "xhelvi",
    "xsans",
    "xsansb",
    "xsansbi",
    "xsansi",
    "xsbook",
    "xsbookb",
    "xsbookbi",
    "xsbooki",
    "xtimes",
    "xtty",
    "xttyb",
    "yie-ar__",
    "yie_ar_k",
    "z-pilot_",
    "zig_zag_",
    "zone7___",
]
Image = Literal[
    "bruh", "bruh_empty", "bruh_computer", "computer", "hey", "twopoint", "christmas"
]
EffectType = Literal[
    "static",
    "offset",
    "noise",
    "stars",
    "plasma",
    "gol",
    "rain",
    "matrix",
    "drawlines",
    "snow",
    "twinkle",
    "audio",
    "chat",
    "firework",
    "fire",
]
valid_effect_types = {
    "static",
    "offset",
    "noise",
    "stars",
    "plasma",
    "gol",
    "rain",
    "matrix",
    "drawlines",
    "snow",
    "twinkle",
    "audio",
    "chat",
    "firework",
    "fire",
}
PanRendererDirection = Literal["horizontal", "vertical"]
valid_pan_renderer_directions = {"horizontal", "vertical"}
FireworkType = Literal[
    "circular",
    "ring",
    "starburst",
    "cone",
    "spiral",
    "cross",
    "burst",
    "wave",
    "flower",
    "doublering",
    "heart",
    "start",
    "fireball",
    "diamond",
    "shockwave",
    "snowflake",
    "cluster",
    "comet",
    "willow",
    "dna",
    "infinity",
    "galaxy",
    "phoenix",
    "fountain",
    "butterfly",
    "dragon",
    "tornado",
    "matrix",
    "portal",
    "fractal",
    "tessellation",
    "quantum",
    "mandelbrot",
    "hypercube",
    "chaos",
    "timewarp",
    "interdimensional",
    "blackhole",
    "mtheory",
    "realitywarp",
    "noneuclidean",
    "cosmicstring",
    "fancytrailburst",
    "random",
]
valid_firework_types = [
    "circular",
    "ring",
    "starburst",
    "cone",
    "spiral",
    "cross",
    "burst",
    "wave",
    "flower",
    "doublering",
    "heart",
    "start",
    "fireball",
    "diamond",
    "shockwave",
    "snowflake",
    "cluster",
    "comet",
    "willow",
    "dna",
    "infinity",
    "galaxy",
    "phoenix",
    "fountain",
    "butterfly",
    "dragon",
    "tornado",
    "matrix",
    "portal",
    "fractal",
    "tessellation",
    "quantum",
    "mandelbrot",
    "hypercube",
    "chaos",
    "timewarp",
    "interdimensional",
    "blackhole",
    "mtheory",
    "realitywarp",
    "noneuclidean",
    "cosmicstring",
    "fancytrailburst"
]
FireworkColorType = Literal["solid", "twotone", "rainbow", "random"]
valid_firework_color_types = ["solid", "twotone", "rainbow", "random"]
two_tone_colors = [
    [12, 134],
    [124, 255],
    [220, 129],
    [255, 243],
    [146, 56],
    [231, 48],
    [152, 222],
    [93, 102],
    [160, 121],
    [218, 206],
    [156, 77],
    [169, 178],
    [145, 19],
    [108, 31],
    [22, 188],
    [200, 187],
    [6, 249],
    [92, 250],
    [43, 184],
    [92, 58],
    [130, 76],
    [216, 110],
    [249, 71],
    [100, 16],
]

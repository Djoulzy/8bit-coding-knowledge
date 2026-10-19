full_menu_lo: .byte <full_menu_0,<full_menu_1,<full_menu_2,<full_menu_3,<full_menu_4,<full_menu_5,<full_menu_6,<full_menu_7,<full_menu_8
full_menu_hi: .byte >full_menu_0,>full_menu_1,>full_menu_2,>full_menu_3,>full_menu_4,>full_menu_5,>full_menu_6,>full_menu_7,>full_menu_8
full_menu_0:
    .byte "                                        "
    .byte "                                        "
    .byte "Force: 100%    Points: 00000            "
    .byte "Pieces d'or: 00500  Main:               "
full_menu_5 = full_menu_0
full_menu_6 = full_menu_0
full_menu_7 = full_menu_0
; AUX pages bypass the HUD. Reading uses full_clue_0..3 instead.
full_menu_1 = full_menu_0
full_menu_2 = full_menu_0
full_menu_3 = full_menu_0
full_menu_4 = full_menu_0
full_menu_8 = full_menu_0

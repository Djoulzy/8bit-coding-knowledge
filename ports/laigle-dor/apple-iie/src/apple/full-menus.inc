full_menu_lo: .byte <full_menu_0,<full_menu_1,<full_menu_2,<full_menu_3,<full_menu_4,<full_menu_5,<full_menu_6,<full_menu_7,<full_menu_8
full_menu_hi: .byte >full_menu_0,>full_menu_1,>full_menu_2,>full_menu_3,>full_menu_4,>full_menu_5,>full_menu_6,>full_menu_7,>full_menu_8
full_menu_0:
    .byte "FORCES:100% POINTS:00000 OR:00500       "
    .byte "SALLE:12 X:19 Y:140 MAIN:00             "
    .byte "I INVENTAIRE L LIRE P PRENDRE O OUVRIR  "
    .byte "FLECHES A B D G S T Q 0..5 R RESET      "
full_menu_1:
    .byte "EXTERIEUR DU CHATEAU                    "
    .byte "1 ENTRER  2 DEPART  3 MARCHAND          "
    .byte "OBJECTIFS: LIVRE DIAMANT AIGLE EN OR    "
    .byte "                                        "
full_menu_2:
    .byte "MARCHAND: 1 FIOLE 360  2 TORCHE 190     "
    .byte "3 CORDE 110  4 PIED DE BICHE 230        "
    .byte "0 RETOUR                                "
    .byte "                                        "
full_menu_3:
    .byte "FIOLES:00 TORCHES:00 CORDES:00          "
    .byte "INVENTAIRE (0..5 POUR TENIR UN OBJET)   "
    .byte "0 VIDE 1 TORCHE 2 FER 3 OR 4 FIOLE      "
    .byte "5 PIED DE BICHE / ESPACE RETOUR         "
full_menu_4:
    .byte "LECTURE DES INDICES                     "
    .byte "                                       "
    .byte "UNE TOUCHE: INDICE SUIVANT              "
    .byte "                                        "
full_menu_5:
    .byte "VOUS AVEZ PERDU                         "
    .byte "VOTRE AVENTURE EST TERMINEE             "
    .byte "O OU ENTREE: NOUVEL ESSAI               "
    .byte "                                        "
full_menu_6:
    .byte "VOUS AVEZ REUNI LES TROIS OBJECTIFS     "
    .byte "VICTOIRE                                "
    .byte "O OU ENTREE: NOUVEL ESSAI               "
    .byte "                                        "
full_menu_7:
    .byte "FIN DU VOYAGE                           "
    .byte "VOUS QUITTEZ LE CHATEAU                 "
    .byte "O OU ENTREE: NOUVEL ESSAI               "
    .byte "                                        "
full_menu_8:
    .byte "L AIGLE D OR - APPLE IIE                "
    .byte "NOM: ______                             "
    .byte "SIX CARACTERES, ENTREE POUR CONTINUER   "
    .byte "RETOUR ARRIERE POUR CORRIGER            "

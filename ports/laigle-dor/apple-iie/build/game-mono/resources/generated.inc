room12_rle: .byte 0
room12_aux_rle: .byte 0
room12_grid = GRID
initial_world: .incbin "world-initial.bin"
y_map:
    .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
    .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
    .byte $FF,$FF,$FF,$00,$00,$01,$02,$03,$04,$05,$06,$07,$08,$09,$0A,$0B
    .byte $0C,$0D,$0E,$0F,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$1A,$1B
    .byte $1C,$1D,$1E,$1F,$20,$20,$21,$22,$23,$24,$25,$26,$27,$28,$29,$2A
    .byte $2B,$2C,$2D,$2E,$2F,$30,$31,$32,$33,$34,$35,$36,$37,$38,$39,$3A
    .byte $3B,$3C,$3D,$3E,$3F,$40,$40,$41,$42,$43,$44,$45,$46,$47,$48,$49
    .byte $4A,$4B,$4C,$4D,$4E,$4F,$50,$51,$52,$53,$54,$55,$56,$57,$58,$59
    .byte $5A,$5B,$5C,$5D,$5E,$5F,$60,$60,$61,$62,$63,$64,$65,$66,$67,$68
    .byte $69,$6A,$6B,$6C,$6D,$6E,$6F,$70,$71,$72,$73,$74,$75,$76,$77,$78
    .byte $79,$7A,$7B,$7C,$7D,$7E,$7F,$80,$80,$81,$82,$83,$84,$85,$86,$87
    .byte $88,$89,$8A,$8B,$8C,$8D,$8E,$8F,$90,$91,$92,$93,$94,$95,$96,$97
    .byte $98,$99,$9A,$9B,$9C,$9D,$9E,$9F
row_lo:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$80,$80,$80,$80,$80,$80,$80,$80
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$80,$80,$80,$80,$80,$80,$80,$80
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$80,$80,$80,$80,$80,$80,$80,$80
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$80,$80,$80,$80,$80,$80,$80,$80
    .byte $28,$28,$28,$28,$28,$28,$28,$28,$A8,$A8,$A8,$A8,$A8,$A8,$A8,$A8
    .byte $28,$28,$28,$28,$28,$28,$28,$28,$A8,$A8,$A8,$A8,$A8,$A8,$A8,$A8
    .byte $28,$28,$28,$28,$28,$28,$28,$28,$A8,$A8,$A8,$A8,$A8,$A8,$A8,$A8
    .byte $28,$28,$28,$28,$28,$28,$28,$28,$A8,$A8,$A8,$A8,$A8,$A8,$A8,$A8
    .byte $50,$50,$50,$50,$50,$50,$50,$50,$D0,$D0,$D0,$D0,$D0,$D0,$D0,$D0
    .byte $50,$50,$50,$50,$50,$50,$50,$50,$D0,$D0,$D0,$D0,$D0,$D0,$D0,$D0
    .byte $50,$50,$50,$50,$50,$50,$50,$50,$D0,$D0,$D0,$D0,$D0,$D0,$D0,$D0
    .byte $50,$50,$50,$50,$50,$50,$50,$50,$D0,$D0,$D0,$D0,$D0,$D0,$D0,$D0
row_hi:
    .byte $20,$24,$28,$2C,$30,$34,$38,$3C,$20,$24,$28,$2C,$30,$34,$38,$3C
    .byte $21,$25,$29,$2D,$31,$35,$39,$3D,$21,$25,$29,$2D,$31,$35,$39,$3D
    .byte $22,$26,$2A,$2E,$32,$36,$3A,$3E,$22,$26,$2A,$2E,$32,$36,$3A,$3E
    .byte $23,$27,$2B,$2F,$33,$37,$3B,$3F,$23,$27,$2B,$2F,$33,$37,$3B,$3F
    .byte $20,$24,$28,$2C,$30,$34,$38,$3C,$20,$24,$28,$2C,$30,$34,$38,$3C
    .byte $21,$25,$29,$2D,$31,$35,$39,$3D,$21,$25,$29,$2D,$31,$35,$39,$3D
    .byte $22,$26,$2A,$2E,$32,$36,$3A,$3E,$22,$26,$2A,$2E,$32,$36,$3A,$3E
    .byte $23,$27,$2B,$2F,$33,$37,$3B,$3F,$23,$27,$2B,$2F,$33,$37,$3B,$3F
    .byte $20,$24,$28,$2C,$30,$34,$38,$3C,$20,$24,$28,$2C,$30,$34,$38,$3C
    .byte $21,$25,$29,$2D,$31,$35,$39,$3D,$21,$25,$29,$2D,$31,$35,$39,$3D
    .byte $22,$26,$2A,$2E,$32,$36,$3A,$3E,$22,$26,$2A,$2E,$32,$36,$3A,$3E
    .byte $23,$27,$2B,$2F,$33,$37,$3B,$3F,$23,$27,$2B,$2F,$33,$37,$3B,$3F
actor_cell_x:
    .byte $06,$0C,$12,$18,$1E,$24,$2A,$30,$36,$3C,$42,$48,$4E,$54,$5A,$60
    .byte $66,$6C,$72,$78,$7E,$84,$8A,$90,$96,$9C,$A2,$A8,$AE,$B4,$BA,$C0
    .byte $C6,$CC,$D2,$D8,$DE,$E4,$EA,$F0
x_byte:
    .byte $03,$04,$05,$06,$07,$08,$08,$09,$0A,$0B,$0C,$0D,$0E,$0E,$0F,$10
    .byte $11,$12,$13,$14,$14,$15,$16,$17,$18,$19,$1A,$1A,$1B,$1C,$1D,$1E
    .byte $1F,$20,$20,$21,$22,$23,$24,$25
x_phase:
    .byte $05,$04,$03,$02,$01,$00,$06,$05,$04,$03,$02,$01,$00,$06,$05,$04
    .byte $03,$02,$01,$00,$06,$05,$04,$03,$02,$01,$00,$06,$05,$04,$03,$02
    .byte $01,$00,$06,$05,$04,$03,$02,$01
cell_byte:
    .byte $02,$03,$03,$03,$03,$03,$03,$03,$04,$04,$04,$04,$04,$04,$04,$05
    .byte $05,$05,$05,$05,$05,$05,$06,$06,$06,$06,$06,$06,$06,$07,$07,$07
    .byte $07,$07,$07,$07,$08,$08,$08,$08,$08,$08,$08,$09,$09,$09,$09,$09
    .byte $09,$09,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0B,$0B,$0B,$0B,$0B,$0B,$0B
    .byte $0C,$0C,$0C,$0C,$0C,$0C,$0C,$0D,$0D,$0D,$0D,$0D,$0D,$0D,$0E,$0E
    .byte $0E,$0E,$0E,$0E,$0E,$0F,$0F,$0F,$0F,$0F,$0F,$0F,$10,$10,$10,$10
    .byte $10,$10,$10,$11,$11,$11,$11,$11,$11,$11,$12,$12,$12,$12,$12,$12
    .byte $12,$13,$13,$13,$13,$13,$13,$13,$14,$14,$14,$14,$14,$14,$14,$15
    .byte $15,$15,$15,$15,$15,$15,$16,$16,$16,$16,$16,$16,$16,$17,$17,$17
    .byte $17,$17,$17,$17,$18,$18,$18,$18,$18,$18,$18,$19,$19,$19,$19,$19
    .byte $19,$19,$1A,$1A,$1A,$1A,$1A,$1A,$1A,$1B,$1B,$1B,$1B,$1B,$1B,$1B
    .byte $1C,$1C,$1C,$1C,$1C,$1C,$1C,$1D,$1D,$1D,$1D,$1D,$1D,$1D,$1E,$1E
    .byte $1E,$1E,$1E,$1E,$1E,$1F,$1F,$1F,$1F,$1F,$1F,$1F,$20,$20,$20,$20
    .byte $20,$20,$20,$21,$21,$21,$21,$21,$21,$21,$22,$22,$22,$22,$22,$22
    .byte $22,$23,$23,$23,$23,$23,$23,$23,$24,$24,$24,$24,$24,$24,$24,$25
cell_phase:
    .byte $40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01
    .byte $02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04
    .byte $08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10
    .byte $20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40
    .byte $01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02
    .byte $04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08
    .byte $10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20
    .byte $40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01
    .byte $02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04
    .byte $08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10
    .byte $20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40
    .byte $01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02
    .byte $04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08
    .byte $10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20
    .byte $40,$01,$02,$04,$08,$10,$20,$40,$01,$02,$04,$08,$10,$20,$40,$01
cell_mask_lo:
    .byte $0F,$1E,$3C,$78,$70,$60,$40
cell_mask_hi:
    .byte $00,$00,$00,$00,$01,$03,$07
cell_color_lo:
    .byte $00,$01,$02,$03,$04,$05,$06,$07,$08,$09,$0A,$0B,$0C,$0D,$0E,$0F
    .byte $00,$02,$04,$06,$08,$0A,$0C,$0E,$10,$12,$14,$16,$18,$1A,$1C,$1E
    .byte $00,$04,$08,$0C,$10,$14,$18,$1C,$20,$24,$28,$2C,$30,$34,$38,$3C
    .byte $00,$08,$10,$18,$20,$28,$30,$38,$40,$48,$50,$58,$60,$68,$70,$78
    .byte $00,$10,$20,$30,$40,$50,$60,$70,$00,$10,$20,$30,$40,$50,$60,$70
    .byte $00,$20,$40,$60,$00,$20,$40,$60,$00,$20,$40,$60,$00,$20,$40,$60
    .byte $00,$40,$00,$40,$00,$40,$00,$40,$00,$40,$00,$40,$00,$40,$00,$40
cell_color_hi:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$01,$01,$01,$01,$01,$01
    .byte $00,$00,$00,$00,$01,$01,$01,$01,$02,$02,$02,$02,$03,$03,$03,$03
    .byte $00,$00,$01,$01,$02,$02,$03,$03,$04,$04,$05,$05,$06,$06,$07,$07
sprite_status_mask:
    .byte $00,$03,$00,$03,$0C,$0F,$0C,$0F,$00,$03,$0F,$03,$0C,$0F,$0C,$0F
sprite_status_pattern:
    .byte $00,$00,$03,$03,$00,$00,$03,$03,$0C,$0C,$0F,$0F,$0C,$0C,$0F,$0F
sprite_lo: .byte <sprite_40,<sprite_41,<sprite_42,<sprite_43,<sprite_44,<sprite_45,<sprite_46,<sprite_47,<sprite_48,<sprite_49,<sprite_50,<sprite_51,<sprite_52,<sprite_53,<sprite_54,<sprite_55,<sprite_56,<sprite_57,<sprite_58,<sprite_59,<sprite_60,<sprite_61,<sprite_62,<sprite_63,<sprite_64,<sprite_65,<sprite_67,<sprite_68,<sprite_69,<sprite_70,<sprite_71,<sprite_74,<sprite_75,<sprite_76,<sprite_77,<sprite_78,<sprite_79,<sprite_80,<sprite_81,<sprite_82,<sprite_83,<sprite_84,<sprite_85,<sprite_86,<sprite_87,<sprite_88,<sprite_89,<sprite_91,<sprite_94,<sprite_95,<sprite_96,<sprite_97,<sprite_98,<sprite_99,<sprite_100,<sprite_101,<sprite_102,<sprite_103,<sprite_110,<sprite_111
sprite_hi: .byte >sprite_40,>sprite_41,>sprite_42,>sprite_43,>sprite_44,>sprite_45,>sprite_46,>sprite_47,>sprite_48,>sprite_49,>sprite_50,>sprite_51,>sprite_52,>sprite_53,>sprite_54,>sprite_55,>sprite_56,>sprite_57,>sprite_58,>sprite_59,>sprite_60,>sprite_61,>sprite_62,>sprite_63,>sprite_64,>sprite_65,>sprite_67,>sprite_68,>sprite_69,>sprite_70,>sprite_71,>sprite_74,>sprite_75,>sprite_76,>sprite_77,>sprite_78,>sprite_79,>sprite_80,>sprite_81,>sprite_82,>sprite_83,>sprite_84,>sprite_85,>sprite_86,>sprite_87,>sprite_88,>sprite_89,>sprite_91,>sprite_94,>sprite_95,>sprite_96,>sprite_97,>sprite_98,>sprite_99,>sprite_100,>sprite_101,>sprite_102,>sprite_103,>sprite_110,>sprite_111
frame_lo: .byte <frame_0,<frame_1,<frame_2,<frame_3,<frame_4,<frame_5,<frame_6,<frame_7,<frame_8,<frame_9,<frame_10,<frame_11,<frame_12,<frame_13,<frame_14,<frame_15,<frame_16,<frame_17,<frame_18,<frame_19,<frame_20,<frame_21,<frame_22,<frame_23,<frame_24,<frame_25,<frame_26,<frame_27
frame_hi: .byte >frame_0,>frame_1,>frame_2,>frame_3,>frame_4,>frame_5,>frame_6,>frame_7,>frame_8,>frame_9,>frame_10,>frame_11,>frame_12,>frame_13,>frame_14,>frame_15,>frame_16,>frame_17,>frame_18,>frame_19,>frame_20,>frame_21,>frame_22,>frame_23,>frame_24,>frame_25,>frame_26,>frame_27
frame_0:
    .byte $02,$00,$00,$C7,$06,$00,$E6
frame_1:
    .byte $02,$01,$00,$C7,$07,$00,$E6
frame_2:
    .byte $02,$02,$00,$C7,$08,$00,$E6
frame_3:
    .byte $02,$03,$FF,$C7,$09,$00,$E6
frame_4:
    .byte $02,$00,$00,$D1,$12,$FF,$F0
frame_5:
    .byte $02,$01,$00,$D1,$13,$FF,$F0
frame_6:
    .byte $02,$02,$00,$D1,$14,$FF,$F0
frame_7:
    .byte $02,$03,$FF,$D1,$15,$FF,$F0
frame_8:
    .byte $02,$00,$00,$C7,$0A,$00,$E6
frame_9:
    .byte $02,$00,$00,$C7,$0E,$00,$E6
frame_10:
    .byte $02,$01,$00,$C7,$0B,$FF,$E6
frame_11:
    .byte $02,$01,$00,$C7,$0F,$FF,$E6
frame_12:
    .byte $02,$02,$00,$C7,$0C,$00,$E6
frame_13:
    .byte $02,$02,$00,$C7,$10,$00,$E6
frame_14:
    .byte $02,$03,$FF,$C7,$0D,$00,$E6
frame_15:
    .byte $02,$03,$FF,$C7,$11,$00,$E6
frame_16:
    .byte $02,$04,$01,$D8,$13,$00,$F0
frame_17:
    .byte $02,$04,$00,$D4,$16,$FE,$EC
frame_18:
    .byte $02,$04,$00,$D4,$16,$FE,$EC
frame_19:
    .byte $02,$04,$00,$D4,$16,$FE,$EC
frame_20:
    .byte $02,$04,$01,$D8,$13,$00,$F0
frame_21:
    .byte $02,$05,$FE,$D8,$14,$FF,$F0
frame_22:
    .byte $02,$05,$FF,$D3,$17,$FF,$EB
frame_23:
    .byte $02,$05,$FF,$D3,$17,$FF,$EB
frame_24:
    .byte $02,$05,$FF,$D3,$17,$FF,$EB
frame_25:
    .byte $02,$05,$FE,$D8,$14,$FF,$F0
frame_26:
    .byte $02,$2F,$00,$D1,$15,$00,$F0
frame_27:
    .byte $02,$3A,$FD,$DA,$3B,$FF,$EE
.segment "ASSETS"
.segment "ASSETS"
sprite_40:
    .byte 30,31,2,5,5,5,5,5,5,6,2,0,0,5,0,0
    .word native_row_0
    .word native_row_1
    .word native_row_2
    .word native_row_3
    .word native_row_4
    .word native_row_5
    .word native_row_6
    .word native_row_6
    .word native_row_4
    .word native_row_7
    .word native_row_8
    .word native_row_0
    .word native_row_9
    .word native_row_10
    .word native_row_11
    .word native_row_12
    .word native_row_13
    .word native_row_14
    .word native_row_15
    .word native_row_16
    .word native_row_17
    .word native_row_18
    .word native_row_19
    .word native_row_20
    .word native_row_13
    .word native_row_12
    .word native_row_21
    .word native_row_21
    .word native_row_22
    .word native_row_23
    .word native_row_24
sprite_41:
    .byte 24,31,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_25
    .word native_row_26
    .word native_row_27
    .word native_row_28
    .word native_row_29
    .word native_row_30
    .word native_row_31
    .word native_row_32
    .word native_row_33
    .word native_row_34
    .word native_row_26
    .word native_row_35
    .word native_row_36
    .word native_row_37
    .word native_row_38
    .word native_row_39
    .word native_row_40
    .word native_row_41
    .word native_row_42
    .word native_row_43
    .word native_row_44
    .word native_row_44
    .word native_row_44
    .word native_row_44
    .word native_row_44
    .word native_row_44
    .word native_row_29
    .word native_row_29
    .word native_row_45
    .word native_row_45
    .word native_row_45
sprite_42:
    .byte 24,31,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_46
    .word native_row_47
    .word native_row_48
    .word native_row_49
    .word native_row_50
    .word native_row_51
    .word native_row_52
    .word native_row_53
    .word native_row_54
    .word native_row_55
    .word native_row_47
    .word native_row_56
    .word native_row_57
    .word native_row_58
    .word native_row_50
    .word native_row_50
    .word native_row_59
    .word native_row_60
    .word native_row_61
    .word native_row_62
    .word native_row_63
    .word native_row_64
    .word native_row_64
    .word native_row_65
    .word native_row_66
    .word native_row_67
    .word native_row_68
    .word native_row_69
    .word native_row_70
    .word native_row_71
    .word native_row_72
sprite_43:
    .byte 30,31,2,5,5,5,5,5,5,6,2,0,0,5,0,0
    .word native_row_73
    .word native_row_74
    .word native_row_75
    .word native_row_76
    .word native_row_77
    .word native_row_74
    .word native_row_78
    .word native_row_79
    .word native_row_80
    .word native_row_80
    .word native_row_80
    .word native_row_80
    .word native_row_81
    .word native_row_82
    .word native_row_83
    .word native_row_84
    .word native_row_85
    .word native_row_86
    .word native_row_87
    .word native_row_88
    .word native_row_88
    .word native_row_89
    .word native_row_90
    .word native_row_91
    .word native_row_92
    .word native_row_92
    .word native_row_93
    .word native_row_93
    .word native_row_94
    .word native_row_94
    .word native_row_95
sprite_44:
    .byte 42,24,2,6,7,7,7,7,7,7,2,0,0,6,0,0
    .word native_row_96
    .word native_row_97
    .word native_row_98
    .word native_row_99
    .word native_row_100
    .word native_row_101
    .word native_row_102
    .word native_row_103
    .word native_row_104
    .word native_row_105
    .word native_row_106
    .word native_row_107
    .word native_row_108
    .word native_row_109
    .word native_row_110
    .word native_row_111
    .word native_row_112
    .word native_row_113
    .word native_row_114
    .word native_row_115
    .word native_row_116
    .word native_row_117
    .word native_row_118
    .word native_row_119
sprite_45:
    .byte 36,24,2,6,6,6,6,6,6,6,2,0,0,6,0,0
    .word native_row_120
    .word native_row_121
    .word native_row_122
    .word native_row_123
    .word native_row_124
    .word native_row_125
    .word native_row_126
    .word native_row_127
    .word native_row_128
    .word native_row_129
    .word native_row_130
    .word native_row_131
    .word native_row_132
    .word native_row_133
    .word native_row_134
    .word native_row_135
    .word native_row_136
    .word native_row_137
    .word native_row_138
    .word native_row_139
    .word native_row_140
    .word native_row_141
    .word native_row_142
    .word native_row_143
sprite_46:
    .byte 24,26,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_144
    .word native_row_145
    .word native_row_146
    .word native_row_147
    .word native_row_49
    .word native_row_144
    .word native_row_148
    .word native_row_148
    .word native_row_148
    .word native_row_148
    .word native_row_148
    .word native_row_148
    .word native_row_149
    .word native_row_150
    .word native_row_151
    .word native_row_151
    .word native_row_144
    .word native_row_148
    .word native_row_148
    .word native_row_152
    .word native_row_151
    .word native_row_151
    .word native_row_151
    .word native_row_38
    .word native_row_153
    .word native_row_154
sprite_47:
    .byte 24,26,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_29
    .word native_row_155
    .word native_row_155
    .word native_row_28
    .word native_row_156
    .word native_row_157
    .word native_row_157
    .word native_row_157
    .word native_row_157
    .word native_row_157
    .word native_row_157
    .word native_row_157
    .word native_row_157
    .word native_row_157
    .word native_row_158
    .word native_row_159
    .word native_row_160
    .word native_row_160
    .word native_row_160
    .word native_row_161
    .word native_row_162
    .word native_row_162
    .word native_row_162
    .word native_row_158
    .word native_row_163
    .word native_row_164
sprite_48:
    .byte 24,26,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_165
    .word native_row_166
    .word native_row_166
    .word native_row_167
    .word native_row_168
    .word native_row_169
    .word native_row_169
    .word native_row_169
    .word native_row_169
    .word native_row_169
    .word native_row_170
    .word native_row_169
    .word native_row_169
    .word native_row_169
    .word native_row_171
    .word native_row_172
    .word native_row_173
    .word native_row_173
    .word native_row_173
    .word native_row_174
    .word native_row_175
    .word native_row_175
    .word native_row_175
    .word native_row_171
    .word native_row_176
    .word native_row_177
sprite_49:
    .byte 24,26,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_144
    .word native_row_146
    .word native_row_146
    .word native_row_147
    .word native_row_49
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_179
    .word native_row_179
    .word native_row_144
    .word native_row_178
    .word native_row_178
    .word native_row_180
    .word native_row_179
    .word native_row_179
    .word native_row_179
    .word native_row_181
    .word native_row_182
    .word native_row_183
sprite_50:
    .byte 24,26,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_144
    .word native_row_145
    .word native_row_146
    .word native_row_147
    .word native_row_184
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_179
    .word native_row_185
    .word native_row_179
    .word native_row_186
    .word native_row_178
    .word native_row_178
    .word native_row_187
    .word native_row_188
    .word native_row_179
    .word native_row_189
    .word native_row_190
    .word native_row_178
    .word native_row_191
    .word native_row_192
sprite_51:
    .byte 30,26,2,5,5,5,5,5,5,6,2,0,0,5,0,0
    .word native_row_193
    .word native_row_194
    .word native_row_195
    .word native_row_196
    .word native_row_197
    .word native_row_198
    .word native_row_198
    .word native_row_199
    .word native_row_200
    .word native_row_201
    .word native_row_201
    .word native_row_202
    .word native_row_203
    .word native_row_203
    .word native_row_204
    .word native_row_205
    .word native_row_206
    .word native_row_207
    .word native_row_208
    .word native_row_209
    .word native_row_210
    .word native_row_211
    .word native_row_212
    .word native_row_213
    .word native_row_214
    .word native_row_215
sprite_52:
    .byte 30,26,2,5,5,5,5,5,5,6,2,0,0,5,0,0
    .word native_row_216
    .word native_row_217
    .word native_row_218
    .word native_row_219
    .word native_row_220
    .word native_row_221
    .word native_row_221
    .word native_row_221
    .word native_row_222
    .word native_row_222
    .word native_row_223
    .word native_row_223
    .word native_row_224
    .word native_row_224
    .word native_row_225
    .word native_row_226
    .word native_row_227
    .word native_row_228
    .word native_row_229
    .word native_row_230
    .word native_row_231
    .word native_row_232
    .word native_row_233
    .word native_row_234
    .word native_row_235
    .word native_row_236
sprite_53:
    .byte 24,26,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_144
    .word native_row_146
    .word native_row_146
    .word native_row_147
    .word native_row_49
    .word native_row_237
    .word native_row_237
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_238
    .word native_row_239
    .word native_row_240
    .word native_row_241
    .word native_row_179
    .word native_row_144
    .word native_row_178
    .word native_row_178
    .word native_row_180
    .word native_row_179
    .word native_row_241
    .word native_row_242
    .word native_row_243
    .word native_row_244
    .word native_row_245
sprite_54:
    .byte 24,26,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_144
    .word native_row_145
    .word native_row_146
    .word native_row_147
    .word native_row_49
    .word native_row_246
    .word native_row_246
    .word native_row_246
    .word native_row_246
    .word native_row_246
    .word native_row_246
    .word native_row_247
    .word native_row_148
    .word native_row_248
    .word native_row_148
    .word native_row_249
    .word native_row_250
    .word native_row_251
    .word native_row_251
    .word native_row_252
    .word native_row_253
    .word native_row_161
    .word native_row_254
    .word native_row_255
    .word native_row_256
    .word native_row_257
sprite_55:
    .byte 30,26,2,5,5,5,5,5,5,6,2,0,0,5,0,0
    .word native_row_193
    .word native_row_194
    .word native_row_195
    .word native_row_196
    .word native_row_258
    .word native_row_259
    .word native_row_260
    .word native_row_261
    .word native_row_262
    .word native_row_263
    .word native_row_263
    .word native_row_264
    .word native_row_264
    .word native_row_264
    .word native_row_265
    .word native_row_205
    .word native_row_206
    .word native_row_207
    .word native_row_208
    .word native_row_209
    .word native_row_210
    .word native_row_211
    .word native_row_212
    .word native_row_213
    .word native_row_214
    .word native_row_215
sprite_56:
    .byte 30,26,2,5,5,5,5,5,5,6,2,0,0,5,0,0
    .word native_row_216
    .word native_row_217
    .word native_row_218
    .word native_row_219
    .word native_row_266
    .word native_row_267
    .word native_row_267
    .word native_row_268
    .word native_row_269
    .word native_row_10
    .word native_row_223
    .word native_row_270
    .word native_row_224
    .word native_row_271
    .word native_row_225
    .word native_row_226
    .word native_row_227
    .word native_row_228
    .word native_row_229
    .word native_row_230
    .word native_row_231
    .word native_row_232
    .word native_row_233
    .word native_row_234
    .word native_row_235
    .word native_row_236
sprite_57:
    .byte 24,26,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_144
    .word native_row_146
    .word native_row_146
    .word native_row_147
    .word native_row_49
    .word native_row_272
    .word native_row_272
    .word native_row_148
    .word native_row_148
    .word native_row_148
    .word native_row_148
    .word native_row_249
    .word native_row_273
    .word native_row_274
    .word native_row_275
    .word native_row_151
    .word native_row_148
    .word native_row_148
    .word native_row_148
    .word native_row_276
    .word native_row_151
    .word native_row_249
    .word native_row_247
    .word native_row_277
    .word native_row_278
    .word native_row_279
sprite_58:
    .byte 36,16,2,6,6,6,6,6,6,6,2,0,0,6,0,0
    .word native_row_280
    .word native_row_281
    .word native_row_282
    .word native_row_283
    .word native_row_283
    .word native_row_284
    .word native_row_285
    .word native_row_286
    .word native_row_287
    .word native_row_288
    .word native_row_289
    .word native_row_290
    .word native_row_291
    .word native_row_292
    .word native_row_293
    .word native_row_293
sprite_59:
    .byte 36,16,2,6,6,6,6,6,6,6,2,0,0,6,0,0
    .word native_row_294
    .word native_row_295
    .word native_row_296
    .word native_row_297
    .word native_row_298
    .word native_row_299
    .word native_row_300
    .word native_row_301
    .word native_row_302
    .word native_row_303
    .word native_row_304
    .word native_row_305
    .word native_row_306
    .word native_row_307
    .word native_row_308
    .word native_row_309
sprite_60:
    .byte 30,16,2,5,5,5,5,5,5,6,2,0,0,5,0,0
    .word native_row_310
    .word native_row_311
    .word native_row_312
    .word native_row_82
    .word native_row_313
    .word native_row_314
    .word native_row_315
    .word native_row_216
    .word native_row_316
    .word native_row_317
    .word native_row_318
    .word native_row_319
    .word native_row_320
    .word native_row_321
    .word native_row_80
    .word native_row_322
sprite_61:
    .byte 36,16,2,6,6,6,6,6,6,6,2,0,0,6,0,0
    .word native_row_323
    .word native_row_324
    .word native_row_325
    .word native_row_326
    .word native_row_327
    .word native_row_328
    .word native_row_329
    .word native_row_330
    .word native_row_331
    .word native_row_332
    .word native_row_333
    .word native_row_334
    .word native_row_335
    .word native_row_336
    .word native_row_337
    .word native_row_338
sprite_62:
    .byte 48,20,2,7,7,8,8,8,8,8,2,0,0,7,0,0
    .word native_row_339
    .word native_row_340
    .word native_row_341
    .word native_row_342
    .word native_row_343
    .word native_row_344
    .word native_row_345
    .word native_row_346
    .word native_row_347
    .word native_row_348
    .word native_row_349
    .word native_row_350
    .word native_row_351
    .word native_row_352
    .word native_row_353
    .word native_row_354
    .word native_row_355
    .word native_row_356
    .word native_row_357
    .word native_row_358
sprite_63:
    .byte 54,21,2,8,8,8,9,9,9,9,2,0,0,8,0,0
    .word native_row_359
    .word native_row_360
    .word native_row_361
    .word native_row_362
    .word native_row_363
    .word native_row_364
    .word native_row_365
    .word native_row_366
    .word native_row_367
    .word native_row_368
    .word native_row_369
    .word native_row_370
    .word native_row_371
    .word native_row_372
    .word native_row_373
    .word native_row_374
    .word native_row_375
    .word native_row_376
    .word native_row_377
    .word native_row_378
    .word native_row_379
sprite_64:
    .byte 12,17,2,2,2,2,3,3,3,3,2,0,0,2,0,0
    .word native_row_380
    .word native_row_381
    .word native_row_382
    .word native_row_383
    .word native_row_383
    .word native_row_383
    .word native_row_384
    .word native_row_384
    .word native_row_384
    .word native_row_385
    .word native_row_386
    .word native_row_383
    .word native_row_382
    .word native_row_381
    .word native_row_382
    .word native_row_381
    .word native_row_382
sprite_65:
    .byte 12,16,2,2,2,2,3,3,3,3,2,0,0,2,0,0
    .word native_row_387
    .word native_row_388
    .word native_row_389
    .word native_row_389
    .word native_row_390
    .word native_row_391
    .word native_row_392
    .word native_row_390
    .word native_row_389
    .word native_row_393
    .word native_row_394
    .word native_row_395
    .word native_row_390
    .word native_row_396
    .word native_row_397
    .word native_row_398
sprite_67:
    .byte 12,17,2,2,2,2,3,3,3,3,2,0,0,2,0,0
    .word native_row_399
    .word native_row_400
    .word native_row_400
    .word native_row_401
    .word native_row_401
    .word native_row_401
    .word native_row_401
    .word native_row_401
    .word native_row_401
    .word native_row_401
    .word native_row_402
    .word native_row_400
    .word native_row_401
    .word native_row_401
    .word native_row_400
    .word native_row_400
    .word native_row_399
sprite_68:
    .byte 18,25,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_403
    .word native_row_404
    .word native_row_405
    .word native_row_406
    .word native_row_407
    .word native_row_408
    .word native_row_409
    .word native_row_410
    .word native_row_409
    .word native_row_409
    .word native_row_409
    .word native_row_411
    .word native_row_412
    .word native_row_413
    .word native_row_414
    .word native_row_415
    .word native_row_416
    .word native_row_417
    .word native_row_417
    .word native_row_418
    .word native_row_419
    .word native_row_420
    .word native_row_421
    .word native_row_422
    .word native_row_423
sprite_69:
    .byte 18,26,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_403
    .word native_row_404
    .word native_row_424
    .word native_row_425
    .word native_row_426
    .word native_row_427
    .word native_row_428
    .word native_row_429
    .word native_row_430
    .word native_row_431
    .word native_row_428
    .word native_row_432
    .word native_row_433
    .word native_row_434
    .word native_row_435
    .word native_row_436
    .word native_row_437
    .word native_row_438
    .word native_row_439
    .word native_row_440
    .word native_row_441
    .word native_row_442
    .word native_row_442
    .word native_row_443
    .word native_row_444
    .word native_row_445
sprite_70:
    .byte 18,23,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_403
    .word native_row_404
    .word native_row_405
    .word native_row_446
    .word native_row_407
    .word native_row_408
    .word native_row_447
    .word native_row_448
    .word native_row_409
    .word native_row_449
    .word native_row_447
    .word native_row_450
    .word native_row_451
    .word native_row_452
    .word native_row_453
    .word native_row_454
    .word native_row_455
    .word native_row_456
    .word native_row_457
    .word native_row_458
    .word native_row_459
    .word native_row_460
    .word native_row_461
sprite_71:
    .byte 12,21,2,2,2,2,3,3,3,3,2,0,0,2,0,0
    .word native_row_462
    .word native_row_463
    .word native_row_464
    .word native_row_465
    .word native_row_466
    .word native_row_467
    .word native_row_468
    .word native_row_468
    .word native_row_468
    .word native_row_469
    .word native_row_469
    .word native_row_470
    .word native_row_470
    .word native_row_469
    .word native_row_471
    .word native_row_472
    .word native_row_473
    .word native_row_474
    .word native_row_474
    .word native_row_474
    .word native_row_402
sprite_74:
    .byte 12,17,2,2,2,2,3,3,3,3,2,0,0,2,0,0
    .word native_row_380
    .word native_row_381
    .word native_row_382
    .word native_row_383
    .word native_row_383
    .word native_row_383
    .word native_row_384
    .word native_row_384
    .word native_row_384
    .word native_row_385
    .word native_row_386
    .word native_row_383
    .word native_row_382
    .word native_row_381
    .word native_row_382
    .word native_row_475
    .word native_row_476
sprite_75:
    .byte 18,16,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_477
    .word native_row_478
    .word native_row_479
    .word native_row_479
    .word native_row_479
    .word native_row_479
    .word native_row_480
    .word native_row_481
    .word native_row_482
    .word native_row_483
    .word native_row_484
    .word native_row_485
    .word native_row_486
    .word native_row_487
    .word native_row_488
    .word native_row_489
sprite_76:
    .byte 12,7,2,2,2,2,3,3,3,3,2,0,0,2,0,0
    .word native_row_490
    .word native_row_491
    .word native_row_492
    .word native_row_493
    .word native_row_494
    .word native_row_495
    .word native_row_496
sprite_77:
    .byte 12,18,2,2,2,2,3,3,3,3,2,0,0,2,0,0
    .word native_row_399
    .word native_row_400
    .word native_row_400
    .word native_row_401
    .word native_row_401
    .word native_row_401
    .word native_row_401
    .word native_row_401
    .word native_row_401
    .word native_row_401
    .word native_row_402
    .word native_row_400
    .word native_row_401
    .word native_row_401
    .word native_row_400
    .word native_row_400
    .word native_row_474
    .word native_row_497
sprite_78:
    .byte 18,19,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_498
    .word native_row_499
    .word native_row_500
    .word native_row_501
    .word native_row_501
    .word native_row_502
    .word native_row_503
    .word native_row_504
    .word native_row_505
    .word native_row_506
    .word native_row_507
    .word native_row_508
    .word native_row_509
    .word native_row_510
    .word native_row_510
    .word native_row_510
    .word native_row_511
    .word native_row_511
    .word native_row_510
sprite_79:
    .byte 24,14,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_512
    .word native_row_512
    .word native_row_513
    .word native_row_514
    .word native_row_515
    .word native_row_516
    .word native_row_517
    .word native_row_518
    .word native_row_519
    .word native_row_520
    .word native_row_520
    .word native_row_521
    .word native_row_522
    .word native_row_523
sprite_80:
    .byte 18,11,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_501
    .word native_row_524
    .word native_row_525
    .word native_row_459
    .word native_row_526
    .word native_row_527
    .word native_row_528
    .word native_row_528
    .word native_row_529
    .word native_row_529
    .word native_row_530
sprite_81:
    .byte 18,19,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_531
    .word native_row_532
    .word native_row_532
    .word native_row_533
    .word native_row_533
    .word native_row_533
    .word native_row_444
    .word native_row_444
    .word native_row_534
    .word native_row_535
    .word native_row_536
    .word native_row_537
    .word native_row_538
    .word native_row_510
    .word native_row_510
    .word native_row_510
    .word native_row_511
    .word native_row_511
    .word native_row_510
sprite_82:
    .byte 18,18,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_539
    .word native_row_540
    .word native_row_541
    .word native_row_542
    .word native_row_543
    .word native_row_544
    .word native_row_545
    .word native_row_546
    .word native_row_547
    .word native_row_538
    .word native_row_548
    .word native_row_548
    .word native_row_549
    .word native_row_548
    .word native_row_550
    .word native_row_551
    .word native_row_551
    .word native_row_441
sprite_83:
    .byte 18,16,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_509
    .word native_row_552
    .word native_row_553
    .word native_row_554
    .word native_row_555
    .word native_row_556
    .word native_row_557
    .word native_row_558
    .word native_row_559
    .word native_row_560
    .word native_row_560
    .word native_row_561
    .word native_row_562
    .word native_row_459
    .word native_row_563
    .word native_row_564
sprite_84:
    .byte 18,17,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_498
    .word native_row_499
    .word native_row_500
    .word native_row_501
    .word native_row_501
    .word native_row_502
    .word native_row_503
    .word native_row_565
    .word native_row_566
    .word native_row_567
    .word native_row_568
    .word native_row_508
    .word native_row_509
    .word native_row_569
    .word native_row_570
    .word native_row_571
    .word native_row_572
sprite_85:
    .byte 24,17,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_512
    .word native_row_512
    .word native_row_512
    .word native_row_513
    .word native_row_514
    .word native_row_515
    .word native_row_516
    .word native_row_573
    .word native_row_574
    .word native_row_575
    .word native_row_576
    .word native_row_577
    .word native_row_578
    .word native_row_579
    .word native_row_580
    .word native_row_581
    .word native_row_582
sprite_86:
    .byte 18,8,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_501
    .word native_row_524
    .word native_row_525
    .word native_row_459
    .word native_row_583
    .word native_row_584
    .word native_row_585
    .word native_row_586
sprite_87:
    .byte 18,18,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_531
    .word native_row_532
    .word native_row_532
    .word native_row_533
    .word native_row_533
    .word native_row_533
    .word native_row_444
    .word native_row_444
    .word native_row_587
    .word native_row_588
    .word native_row_589
    .word native_row_590
    .word native_row_509
    .word native_row_510
    .word native_row_569
    .word native_row_591
    .word native_row_592
    .word native_row_537
sprite_88:
    .byte 18,26,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_531
    .word native_row_532
    .word native_row_532
    .word native_row_533
    .word native_row_533
    .word native_row_533
    .word native_row_444
    .word native_row_444
    .word native_row_534
    .word native_row_535
    .word native_row_536
    .word native_row_537
    .word native_row_593
    .word native_row_594
    .word native_row_595
    .word native_row_596
    .word native_row_597
    .word native_row_596
    .word native_row_539
    .word native_row_595
    .word native_row_530
    .word native_row_403
    .word native_row_403
    .word native_row_596
    .word native_row_596
    .word native_row_598
sprite_89:
    .byte 18,17,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_599
    .word native_row_599
    .word native_row_599
    .word native_row_599
    .word native_row_599
    .word native_row_510
    .word native_row_538
    .word native_row_538
    .word native_row_547
    .word native_row_547
    .word native_row_547
    .word native_row_600
    .word native_row_601
    .word native_row_602
    .word native_row_442
    .word native_row_443
    .word native_row_444
sprite_91:
    .byte 36,31,2,6,6,6,6,6,6,6,2,0,0,6,0,0
    .word native_row_603
    .word native_row_604
    .word native_row_605
    .word native_row_606
    .word native_row_607
    .word native_row_604
    .word native_row_608
    .word native_row_609
    .word native_row_610
    .word native_row_610
    .word native_row_610
    .word native_row_610
    .word native_row_611
    .word native_row_612
    .word native_row_613
    .word native_row_614
    .word native_row_615
    .word native_row_616
    .word native_row_616
    .word native_row_327
    .word native_row_617
    .word native_row_617
    .word native_row_618
    .word native_row_619
    .word native_row_611
    .word native_row_620
    .word native_row_611
    .word native_row_611
    .word native_row_621
    .word native_row_621
    .word native_row_621
sprite_94:
    .byte 18,13,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_569
    .word native_row_599
    .word native_row_403
    .word native_row_510
    .word native_row_509
    .word native_row_622
    .word native_row_623
    .word native_row_624
    .word native_row_625
    .word native_row_626
    .word native_row_627
    .word native_row_628
    .word native_row_623
sprite_95:
    .byte 18,13,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_403
    .word native_row_530
    .word native_row_622
    .word native_row_569
    .word native_row_509
    .word native_row_622
    .word native_row_623
    .word native_row_629
    .word native_row_630
    .word native_row_628
    .word native_row_627
    .word native_row_594
    .word native_row_631
sprite_96:
    .byte 24,7,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_632
    .word native_row_633
    .word native_row_634
    .word native_row_635
    .word native_row_636
    .word native_row_637
    .word native_row_632
sprite_97:
    .byte 24,7,2,4,4,4,4,4,5,5,2,0,0,4,0,0
    .word native_row_638
    .word native_row_639
    .word native_row_640
    .word native_row_641
    .word native_row_42
    .word native_row_642
    .word native_row_638
sprite_98:
    .byte 18,13,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_643
    .word native_row_644
    .word native_row_645
    .word native_row_646
    .word native_row_647
    .word native_row_648
    .word native_row_649
    .word native_row_650
    .word native_row_651
    .word native_row_652
    .word native_row_653
    .word native_row_654
    .word native_row_538
sprite_99:
    .byte 18,15,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_655
    .word native_row_656
    .word native_row_657
    .word native_row_658
    .word native_row_659
    .word native_row_660
    .word native_row_661
    .word native_row_662
    .word native_row_663
    .word native_row_664
    .word native_row_665
    .word native_row_666
    .word native_row_667
    .word native_row_531
    .word native_row_531
sprite_100:
    .byte 18,13,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_668
    .word native_row_669
    .word native_row_670
    .word native_row_671
    .word native_row_672
    .word native_row_673
    .word native_row_674
    .word native_row_675
    .word native_row_676
    .word native_row_677
    .word native_row_678
    .word native_row_679
    .word native_row_559
sprite_101:
    .byte 18,15,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_572
    .word native_row_680
    .word native_row_681
    .word native_row_682
    .word native_row_683
    .word native_row_684
    .word native_row_685
    .word native_row_686
    .word native_row_687
    .word native_row_688
    .word native_row_689
    .word native_row_690
    .word native_row_691
    .word native_row_691
    .word native_row_691
sprite_102:
    .byte 18,17,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_643
    .word native_row_644
    .word native_row_645
    .word native_row_646
    .word native_row_647
    .word native_row_648
    .word native_row_692
    .word native_row_693
    .word native_row_694
    .word native_row_695
    .word native_row_696
    .word native_row_697
    .word native_row_698
    .word native_row_699
    .word native_row_700
    .word native_row_701
    .word native_row_701
sprite_103:
    .byte 18,17,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_668
    .word native_row_669
    .word native_row_670
    .word native_row_671
    .word native_row_672
    .word native_row_673
    .word native_row_702
    .word native_row_703
    .word native_row_704
    .word native_row_705
    .word native_row_706
    .word native_row_696
    .word native_row_707
    .word native_row_708
    .word native_row_709
    .word native_row_710
    .word native_row_710
sprite_110:
    .byte 42,20,2,6,7,7,7,7,7,7,2,0,0,6,0,0
    .word native_row_711
    .word native_row_308
    .word native_row_712
    .word native_row_713
    .word native_row_280
    .word native_row_714
    .word native_row_715
    .word native_row_107
    .word native_row_716
    .word native_row_717
    .word native_row_718
    .word native_row_719
    .word native_row_720
    .word native_row_721
    .word native_row_722
    .word native_row_723
    .word native_row_724
    .word native_row_725
    .word native_row_726
    .word native_row_727
sprite_111:
    .byte 42,18,2,6,7,7,7,7,7,7,2,0,0,6,0,0
    .word native_row_728
    .word native_row_729
    .word native_row_730
    .word native_row_731
    .word native_row_732
    .word native_row_733
    .word native_row_734
    .word native_row_735
    .word native_row_736
    .word native_row_737
    .word native_row_737
    .word native_row_738
    .word native_row_739
    .word native_row_740
    .word native_row_741
    .word native_row_742
    .word native_row_743
    .word native_row_744
sprite_36:
    .byte 18,18,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_569
    .word native_row_569
    .word native_row_403
    .word native_row_569
    .word native_row_622
    .word native_row_510
    .word native_row_509
    .word native_row_622
    .word native_row_569
    .word native_row_622
    .word native_row_631
    .word native_row_508
    .word native_row_745
    .word native_row_628
    .word native_row_695
    .word native_row_627
    .word native_row_624
    .word native_row_745
sprite_37:
    .byte 18,18,2,3,3,3,3,4,4,4,2,0,0,3,0,0
    .word native_row_569
    .word native_row_746
    .word native_row_746
    .word native_row_530
    .word native_row_530
    .word native_row_747
    .word native_row_530
    .word native_row_748
    .word native_row_558
    .word native_row_539
    .word native_row_559
    .word native_row_749
    .word native_row_509
    .word native_row_594
    .word native_row_750
    .word native_row_593
    .word native_row_624
    .word native_row_745
sprite_72:
    .byte 6,6,2,1,1,2,2,2,2,2,2,0,0,1,0,0
    .word native_row_751
    .word native_row_752
    .word native_row_753
    .word native_row_754
    .word native_row_755
    .word native_row_756
sprite_73:
    .byte 6,6,2,1,1,2,2,2,2,2,2,0,0,1,0,0
    .word native_row_751
    .word native_row_757
    .word native_row_754
    .word native_row_753
    .word native_row_755
    .word native_row_756
.segment "ASSETS"
native_row_0:
    .byte $00,$00,$78,$78,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_1:
    .byte $00,$00,$7C,$2C,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_2:
    .byte $00,$00,$7E,$76,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_3:
    .byte $00,$00,$7E,$2A,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_4:
    .byte $00,$00,$7E,$7E,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_5:
    .byte $00,$00,$7E,$56,$03,$02,$00,$00,$00,$00
.segment "ASSETS"
native_row_6:
    .byte $00,$00,$7E,$5E,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_7:
    .byte $00,$00,$7C,$4C,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_8:
    .byte $00,$00,$7C,$7C,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_9:
    .byte $00,$00,$7E,$06,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_10:
    .byte $40,$40,$7F,$4F,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_11:
    .byte $40,$40,$7F,$5F,$3F,$2F,$00,$00,$00,$00
.segment "ASSETS"
native_row_12:
    .byte $00,$00,$7F,$5F,$7F,$77,$00,$00,$00,$00
.segment "ASSETS"
native_row_13:
    .byte $00,$00,$7F,$7F,$7F,$77,$00,$00,$00,$00
.segment "ASSETS"
native_row_14:
    .byte $40,$40,$7F,$5E,$7F,$7B,$01,$01,$00,$00
.segment "ASSETS"
native_row_15:
    .byte $40,$40,$7F,$79,$7F,$7C,$01,$01,$00,$00
.segment "ASSETS"
native_row_16:
    .byte $40,$40,$7F,$5F,$7F,$6F,$01,$01,$00,$00
.segment "ASSETS"
native_row_17:
    .byte $40,$40,$7F,$7F,$7F,$6F,$01,$01,$00,$00
.segment "ASSETS"
native_row_18:
    .byte $00,$00,$7F,$5F,$7F,$6F,$01,$01,$00,$00
.segment "ASSETS"
native_row_19:
    .byte $00,$00,$7F,$7F,$7F,$67,$01,$01,$00,$00
.segment "ASSETS"
native_row_20:
    .byte $00,$00,$7F,$5F,$7F,$37,$01,$01,$00,$00
.segment "ASSETS"
native_row_21:
    .byte $00,$00,$7F,$7F,$3F,$37,$00,$00,$00,$00
.segment "ASSETS"
native_row_22:
    .byte $00,$00,$7F,$51,$1F,$1C,$00,$00,$00,$00
.segment "ASSETS"
native_row_23:
    .byte $00,$00,$7F,$71,$1F,$18,$00,$00,$00,$00
.segment "ASSETS"
native_row_24:
    .byte $00,$00,$7F,$51,$0F,$0C,$00,$00,$00,$00
.segment "ASSETS"
native_row_25:
    .byte $00,$00,$7C,$7C,$00,$00,$00,$00
.segment "ASSETS"
native_row_26:
    .byte $00,$00,$7E,$76,$01,$01,$00,$00
.segment "ASSETS"
native_row_27:
    .byte $00,$00,$7F,$2B,$03,$03,$00,$00
.segment "ASSETS"
native_row_28:
    .byte $00,$00,$7F,$55,$03,$02,$00,$00
.segment "ASSETS"
native_row_29:
    .byte $00,$00,$7F,$7F,$01,$01,$00,$00
.segment "ASSETS"
native_row_30:
    .byte $00,$00,$7F,$3B,$01,$01,$00,$00
.segment "ASSETS"
native_row_31:
    .byte $00,$00,$7E,$7A,$03,$03,$00,$00
.segment "ASSETS"
native_row_32:
    .byte $00,$00,$7E,$76,$03,$02,$00,$00
.segment "ASSETS"
native_row_33:
    .byte $00,$00,$7E,$7E,$01,$01,$00,$00
.segment "ASSETS"
native_row_34:
    .byte $00,$00,$7E,$3A,$01,$01,$00,$00
.segment "ASSETS"
native_row_35:
    .byte $00,$00,$3E,$2E,$00,$00,$00,$00
.segment "ASSETS"
native_row_36:
    .byte $00,$00,$1E,$1E,$00,$00,$00,$00
.segment "ASSETS"
native_row_37:
    .byte $00,$00,$3E,$3E,$00,$00,$00,$00
.segment "ASSETS"
native_row_38:
    .byte $00,$00,$7F,$7F,$00,$00,$00,$00
.segment "ASSETS"
native_row_39:
    .byte $00,$00,$7F,$7D,$00,$00,$00,$00
.segment "ASSETS"
native_row_40:
    .byte $40,$40,$7F,$73,$01,$01,$00,$00
.segment "ASSETS"
native_row_41:
    .byte $40,$40,$7F,$4F,$01,$01,$00,$00
.segment "ASSETS"
native_row_42:
    .byte $40,$40,$7F,$3F,$01,$01,$00,$00
.segment "ASSETS"
native_row_43:
    .byte $40,$40,$7F,$7F,$00,$00,$00,$00
.segment "ASSETS"
native_row_44:
    .byte $40,$40,$7F,$7F,$01,$01,$00,$00
.segment "ASSETS"
native_row_45:
    .byte $00,$00,$7F,$41,$01,$01,$00,$00
.segment "ASSETS"
native_row_46:
    .byte $00,$00,$78,$78,$01,$01,$00,$00
.segment "ASSETS"
native_row_47:
    .byte $00,$00,$7C,$3C,$03,$03,$00,$00
.segment "ASSETS"
native_row_48:
    .byte $00,$00,$7E,$56,$07,$06,$00,$00
.segment "ASSETS"
native_row_49:
    .byte $00,$00,$7E,$2A,$07,$05,$00,$00
.segment "ASSETS"
native_row_50:
    .byte $00,$00,$7C,$7C,$07,$07,$00,$00
.segment "ASSETS"
native_row_51:
    .byte $00,$00,$7C,$74,$07,$06,$00,$00
.segment "ASSETS"
native_row_52:
    .byte $00,$00,$7E,$7E,$03,$02,$00,$00
.segment "ASSETS"
native_row_53:
    .byte $00,$00,$7E,$3A,$03,$03,$00,$00
.segment "ASSETS"
native_row_54:
    .byte $00,$00,$7C,$7C,$03,$03,$00,$00
.segment "ASSETS"
native_row_55:
    .byte $00,$00,$7C,$74,$03,$02,$00,$00
.segment "ASSETS"
native_row_56:
    .byte $00,$00,$70,$50,$03,$03,$00,$00
.segment "ASSETS"
native_row_57:
    .byte $00,$00,$60,$60,$03,$03,$00,$00
.segment "ASSETS"
native_row_58:
    .byte $00,$00,$70,$70,$03,$03,$00,$00
.segment "ASSETS"
native_row_59:
    .byte $00,$00,$7E,$76,$0F,$0C,$00,$00
.segment "ASSETS"
native_row_60:
    .byte $00,$00,$7E,$5E,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_61:
    .byte $00,$00,$7E,$7E,$0F,$0B,$00,$00
.segment "ASSETS"
native_row_62:
    .byte $00,$00,$7E,$56,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_63:
    .byte $00,$00,$7E,$3A,$07,$07,$00,$00
.segment "ASSETS"
native_row_64:
    .byte $00,$00,$7E,$7E,$0F,$0E,$00,$00
.segment "ASSETS"
native_row_65:
    .byte $00,$00,$7C,$3C,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_66:
    .byte $00,$00,$7C,$5C,$07,$07,$00,$00
.segment "ASSETS"
native_row_67:
    .byte $00,$00,$7C,$6C,$03,$03,$00,$00
.segment "ASSETS"
native_row_68:
    .byte $00,$00,$7C,$74,$07,$05,$00,$00
.segment "ASSETS"
native_row_69:
    .byte $00,$00,$78,$38,$07,$07,$00,$00
.segment "ASSETS"
native_row_70:
    .byte $00,$00,$7C,$1C,$07,$04,$00,$00
.segment "ASSETS"
native_row_71:
    .byte $00,$00,$7E,$1A,$07,$04,$00,$00
.segment "ASSETS"
native_row_72:
    .byte $00,$00,$7E,$0E,$07,$04,$00,$00
.segment "ASSETS"
native_row_73:
    .byte $00,$00,$00,$00,$3C,$3C,$00,$00,$00,$00
.segment "ASSETS"
native_row_74:
    .byte $00,$00,$00,$00,$7E,$56,$00,$00,$00,$00
.segment "ASSETS"
native_row_75:
    .byte $00,$00,$00,$00,$7F,$2B,$01,$01,$00,$00
.segment "ASSETS"
native_row_76:
    .byte $00,$00,$00,$00,$7F,$3D,$01,$01,$00,$00
.segment "ASSETS"
native_row_77:
    .byte $00,$00,$00,$00,$7F,$6B,$01,$01,$00,$00
.segment "ASSETS"
native_row_78:
    .byte $00,$00,$00,$00,$7F,$2D,$01,$01,$00,$00
.segment "ASSETS"
native_row_79:
    .byte $00,$00,$00,$00,$7F,$7F,$01,$01,$00,$00
.segment "ASSETS"
native_row_80:
    .byte $00,$00,$00,$00,$7E,$7E,$00,$00,$00,$00
.segment "ASSETS"
native_row_81:
    .byte $00,$00,$40,$40,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_82:
    .byte $00,$00,$70,$70,$7F,$7F,$07,$07,$00,$00
.segment "ASSETS"
native_row_83:
    .byte $00,$00,$78,$68,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_84:
    .byte $00,$00,$7C,$1C,$7F,$7F,$07,$04,$00,$00
.segment "ASSETS"
native_row_85:
    .byte $00,$00,$7C,$7C,$7F,$00,$07,$07,$00,$00
.segment "ASSETS"
native_row_86:
    .byte $00,$00,$7E,$7E,$7F,$7F,$07,$07,$00,$00
.segment "ASSETS"
native_row_87:
    .byte $00,$00,$7E,$6E,$7F,$7F,$07,$07,$00,$00
.segment "ASSETS"
native_row_88:
    .byte $00,$00,$7E,$6E,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_89:
    .byte $00,$00,$7E,$4E,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_90:
    .byte $00,$00,$7E,$56,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_91:
    .byte $00,$00,$7E,$5E,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_92:
    .byte $00,$00,$7C,$5C,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_93:
    .byte $00,$00,$78,$58,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_94:
    .byte $00,$00,$70,$50,$7F,$00,$03,$02,$00,$00
.segment "ASSETS"
native_row_95:
    .byte $00,$00,$60,$60,$7F,$00,$03,$02,$00,$00
.segment "ASSETS"
native_row_96:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$1F,$1F,$00,$00
.segment "ASSETS"
native_row_97:
    .byte $00,$00,$00,$00,$00,$00,$40,$40,$3F,$2A,$00,$00
.segment "ASSETS"
native_row_98:
    .byte $00,$00,$00,$00,$00,$00,$60,$60,$7F,$55,$00,$00
.segment "ASSETS"
native_row_99:
    .byte $00,$00,$00,$00,$00,$00,$60,$60,$7F,$6A,$00,$00
.segment "ASSETS"
native_row_100:
    .byte $00,$00,$00,$00,$00,$00,$60,$60,$3F,$3D,$00,$00
.segment "ASSETS"
native_row_101:
    .byte $00,$00,$00,$00,$00,$00,$70,$70,$3F,$2E,$00,$00
.segment "ASSETS"
native_row_102:
    .byte $00,$00,$00,$00,$00,$00,$7C,$7C,$3F,$3D,$00,$00
.segment "ASSETS"
native_row_103:
    .byte $00,$00,$00,$00,$00,$00,$7F,$7F,$3F,$3F,$00,$00
.segment "ASSETS"
native_row_104:
    .byte $00,$00,$00,$00,$60,$60,$7F,$7F,$1F,$17,$00,$00
.segment "ASSETS"
native_row_105:
    .byte $00,$00,$00,$00,$0E,$0E,$78,$20,$1F,$1E,$00,$00
.segment "ASSETS"
native_row_106:
    .byte $00,$00,$40,$40,$7F,$7F,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_107:
    .byte $00,$00,$60,$60,$7F,$7F,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_108:
    .byte $00,$00,$70,$70,$7F,$67,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_109:
    .byte $00,$00,$78,$78,$7F,$79,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_110:
    .byte $00,$00,$78,$78,$7F,$5E,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_111:
    .byte $00,$00,$7C,$3C,$7F,$3F,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_112:
    .byte $00,$00,$7C,$5C,$7F,$7F,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_113:
    .byte $00,$00,$7C,$5C,$7F,$7F,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_114:
    .byte $00,$00,$7E,$6E,$7F,$7F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_115:
    .byte $00,$00,$7E,$6E,$3F,$3F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_116:
    .byte $00,$00,$7E,$6A,$1F,$1F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_117:
    .byte $00,$00,$7E,$0E,$0F,$0C,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_118:
    .byte $00,$00,$7E,$06,$0F,$0C,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_119:
    .byte $00,$00,$7C,$0C,$0F,$0C,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_120:
    .byte $00,$00,$3E,$3E,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_121:
    .byte $00,$00,$7F,$7B,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_122:
    .byte $40,$40,$7F,$55,$01,$01,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_123:
    .byte $40,$40,$7F,$2A,$01,$01,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_124:
    .byte $00,$00,$7F,$6F,$01,$01,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_125:
    .byte $00,$00,$7F,$5D,$03,$03,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_126:
    .byte $00,$00,$7F,$6F,$0F,$0F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_127:
    .byte $00,$00,$7F,$7F,$3F,$3F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_128:
    .byte $00,$00,$7E,$7A,$7F,$7F,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_129:
    .byte $00,$00,$7E,$1E,$0F,$0F,$18,$18,$00,$00,$00,$00
.segment "ASSETS"
native_row_130:
    .byte $00,$00,$00,$00,$7F,$7F,$3F,$3F,$00,$00,$00,$00
.segment "ASSETS"
native_row_131:
    .byte $00,$00,$00,$00,$7F,$7F,$7F,$7F,$00,$00,$00,$00
.segment "ASSETS"
native_row_132:
    .byte $00,$00,$00,$00,$7E,$7E,$7F,$7F,$01,$01,$00,$00
.segment "ASSETS"
native_row_133:
    .byte $00,$00,$00,$00,$7E,$7E,$7F,$7D,$01,$01,$00,$00
.segment "ASSETS"
native_row_134:
    .byte $00,$00,$00,$00,$7E,$7E,$7F,$77,$03,$03,$00,$00
.segment "ASSETS"
native_row_135:
    .byte $00,$00,$00,$00,$7C,$74,$7F,$6F,$03,$03,$00,$00
.segment "ASSETS"
native_row_136:
    .byte $00,$00,$00,$00,$7C,$7C,$7F,$5F,$03,$03,$00,$00
.segment "ASSETS"
native_row_137:
    .byte $00,$00,$00,$00,$78,$68,$7F,$5F,$03,$03,$00,$00
.segment "ASSETS"
native_row_138:
    .byte $00,$00,$00,$00,$70,$70,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_139:
    .byte $00,$00,$00,$00,$60,$60,$7F,$5F,$03,$03,$00,$00
.segment "ASSETS"
native_row_140:
    .byte $00,$00,$00,$00,$40,$40,$7F,$5F,$01,$01,$00,$00
.segment "ASSETS"
native_row_141:
    .byte $00,$00,$00,$00,$00,$00,$7F,$63,$03,$03,$00,$00
.segment "ASSETS"
native_row_142:
    .byte $00,$00,$00,$00,$00,$00,$7F,$23,$03,$03,$00,$00
.segment "ASSETS"
native_row_143:
    .byte $00,$00,$00,$00,$00,$00,$7F,$63,$01,$01,$00,$00
.segment "ASSETS"
native_row_144:
    .byte $00,$00,$7F,$7F,$07,$07,$00,$00
.segment "ASSETS"
native_row_145:
    .byte $40,$40,$7F,$5F,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_146:
    .byte $40,$40,$7F,$7F,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_147:
    .byte $00,$00,$7F,$55,$0F,$0A,$00,$00
.segment "ASSETS"
native_row_148:
    .byte $00,$00,$7F,$6F,$07,$07,$00,$00
.segment "ASSETS"
native_row_149:
    .byte $00,$00,$7F,$2F,$07,$07,$00,$00
.segment "ASSETS"
native_row_150:
    .byte $00,$00,$7F,$6B,$07,$06,$00,$00
.segment "ASSETS"
native_row_151:
    .byte $00,$00,$7E,$6E,$03,$03,$00,$00
.segment "ASSETS"
native_row_152:
    .byte $00,$00,$7E,$5A,$03,$02,$00,$00
.segment "ASSETS"
native_row_153:
    .byte $40,$40,$7F,$7F,$07,$07,$00,$00
.segment "ASSETS"
native_row_154:
    .byte $40,$40,$7F,$2B,$07,$07,$00,$00
.segment "ASSETS"
native_row_155:
    .byte $40,$40,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_156:
    .byte $00,$00,$7F,$2B,$01,$01,$00,$00
.segment "ASSETS"
native_row_157:
    .byte $00,$00,$7F,$3F,$01,$01,$00,$00
.segment "ASSETS"
native_row_158:
    .byte $00,$00,$7F,$5F,$00,$00,$00,$00
.segment "ASSETS"
native_row_159:
    .byte $00,$00,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_160:
    .byte $40,$40,$7F,$5F,$00,$00,$00,$00
.segment "ASSETS"
native_row_161:
    .byte $00,$00,$3F,$29,$00,$00,$00,$00
.segment "ASSETS"
native_row_162:
    .byte $00,$00,$3F,$2F,$00,$00,$00,$00
.segment "ASSETS"
native_row_163:
    .byte $00,$00,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_164:
    .byte $00,$00,$7F,$7B,$03,$03,$00,$00
.segment "ASSETS"
native_row_165:
    .byte $00,$00,$78,$78,$07,$07,$00,$00
.segment "ASSETS"
native_row_166:
    .byte $00,$00,$7E,$7E,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_167:
    .byte $00,$00,$7E,$56,$0F,$0A,$00,$00
.segment "ASSETS"
native_row_168:
    .byte $00,$00,$7C,$2C,$07,$05,$00,$00
.segment "ASSETS"
native_row_169:
    .byte $00,$00,$7C,$74,$07,$07,$00,$00
.segment "ASSETS"
native_row_170:
    .byte $40,$40,$7F,$68,$07,$07,$00,$00
.segment "ASSETS"
native_row_171:
    .byte $00,$00,$78,$68,$07,$07,$00,$00
.segment "ASSETS"
native_row_172:
    .byte $00,$00,$60,$60,$07,$07,$00,$00
.segment "ASSETS"
native_row_173:
    .byte $00,$00,$78,$68,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_174:
    .byte $00,$00,$70,$50,$07,$04,$00,$00
.segment "ASSETS"
native_row_175:
    .byte $00,$00,$70,$50,$07,$07,$00,$00
.segment "ASSETS"
native_row_176:
    .byte $00,$00,$7E,$7E,$07,$07,$00,$00
.segment "ASSETS"
native_row_177:
    .byte $00,$00,$7E,$7E,$07,$06,$00,$00
.segment "ASSETS"
native_row_178:
    .byte $00,$00,$7F,$5F,$07,$07,$00,$00
.segment "ASSETS"
native_row_179:
    .byte $00,$00,$7E,$5E,$03,$03,$00,$00
.segment "ASSETS"
native_row_180:
    .byte $00,$00,$7E,$32,$03,$02,$00,$00
.segment "ASSETS"
native_row_181:
    .byte $40,$40,$7F,$5F,$07,$07,$00,$00
.segment "ASSETS"
native_row_182:
    .byte $40,$40,$7F,$5D,$07,$07,$00,$00
.segment "ASSETS"
native_row_183:
    .byte $00,$00,$7F,$5D,$03,$03,$00,$00
.segment "ASSETS"
native_row_184:
    .byte $00,$00,$7E,$0A,$07,$05,$00,$00
.segment "ASSETS"
native_row_185:
    .byte $00,$00,$7F,$4F,$03,$02,$00,$00
.segment "ASSETS"
native_row_186:
    .byte $00,$00,$7F,$4F,$03,$03,$00,$00
.segment "ASSETS"
native_row_187:
    .byte $00,$00,$7F,$5F,$07,$06,$00,$00
.segment "ASSETS"
native_row_188:
    .byte $00,$00,$7E,$4A,$03,$03,$00,$00
.segment "ASSETS"
native_row_189:
    .byte $00,$00,$78,$18,$03,$02,$00,$00
.segment "ASSETS"
native_row_190:
    .byte $00,$00,$7F,$57,$07,$07,$00,$00
.segment "ASSETS"
native_row_191:
    .byte $00,$00,$1E,$12,$00,$00,$00,$00
.segment "ASSETS"
native_row_192:
    .byte $00,$00,$1C,$1C,$00,$00,$00,$00
.segment "ASSETS"
native_row_193:
    .byte $00,$00,$40,$40,$7F,$7F,$01,$01,$00,$00
.segment "ASSETS"
native_row_194:
    .byte $00,$00,$60,$60,$7F,$7F,$01,$01,$00,$00
.segment "ASSETS"
native_row_195:
    .byte $00,$00,$60,$60,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_196:
    .byte $00,$00,$40,$40,$7F,$2A,$03,$03,$00,$00
.segment "ASSETS"
native_row_197:
    .byte $00,$00,$40,$40,$7F,$0A,$01,$01,$00,$00
.segment "ASSETS"
native_row_198:
    .byte $00,$00,$40,$40,$7F,$5F,$03,$03,$00,$00
.segment "ASSETS"
native_row_199:
    .byte $00,$00,$40,$40,$7F,$5F,$07,$07,$00,$00
.segment "ASSETS"
native_row_200:
    .byte $00,$00,$60,$60,$7F,$5F,$07,$07,$00,$00
.segment "ASSETS"
native_row_201:
    .byte $00,$00,$60,$60,$7F,$4F,$07,$07,$00,$00
.segment "ASSETS"
native_row_202:
    .byte $00,$00,$60,$60,$7F,$6F,$03,$03,$00,$00
.segment "ASSETS"
native_row_203:
    .byte $00,$00,$60,$60,$7F,$67,$03,$03,$00,$00
.segment "ASSETS"
native_row_204:
    .byte $00,$00,$70,$10,$7F,$63,$01,$01,$00,$00
.segment "ASSETS"
native_row_205:
    .byte $00,$00,$78,$78,$7F,$32,$01,$01,$00,$00
.segment "ASSETS"
native_row_206:
    .byte $00,$00,$78,$78,$7F,$7B,$03,$03,$00,$00
.segment "ASSETS"
native_row_207:
    .byte $00,$00,$60,$60,$7F,$7B,$03,$03,$00,$00
.segment "ASSETS"
native_row_208:
    .byte $00,$00,$78,$58,$7F,$7B,$03,$03,$00,$00
.segment "ASSETS"
native_row_209:
    .byte $00,$00,$78,$38,$7F,$11,$01,$01,$00,$00
.segment "ASSETS"
native_row_210:
    .byte $00,$00,$7C,$7C,$7F,$78,$00,$00,$00,$00
.segment "ASSETS"
native_row_211:
    .byte $00,$00,$7E,$1E,$7F,$78,$00,$00,$00,$00
.segment "ASSETS"
native_row_212:
    .byte $00,$00,$7E,$3E,$3F,$38,$00,$00,$00,$00
.segment "ASSETS"
native_row_213:
    .byte $00,$00,$78,$38,$7F,$78,$01,$01,$00,$00
.segment "ASSETS"
native_row_214:
    .byte $00,$00,$78,$78,$7F,$79,$07,$07,$00,$00
.segment "ASSETS"
native_row_215:
    .byte $00,$00,$70,$70,$7F,$59,$07,$07,$00,$00
.segment "ASSETS"
native_row_216:
    .byte $00,$00,$78,$78,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_217:
    .byte $00,$00,$7E,$7E,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_218:
    .byte $00,$00,$7F,$7F,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_219:
    .byte $00,$00,$7F,$57,$0F,$0A,$00,$00,$00,$00
.segment "ASSETS"
native_row_220:
    .byte $00,$00,$7E,$2A,$07,$05,$00,$00,$00,$00
.segment "ASSETS"
native_row_221:
    .byte $00,$00,$7F,$6F,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_222:
    .byte $40,$40,$7F,$6F,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_223:
    .byte $40,$40,$7F,$4F,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_224:
    .byte $00,$00,$7F,$5F,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_225:
    .byte $00,$00,$7E,$1E,$3F,$27,$00,$00,$00,$00
.segment "ASSETS"
native_row_226:
    .byte $00,$00,$7F,$3F,$7F,$7D,$00,$00,$00,$00
.segment "ASSETS"
native_row_227:
    .byte $00,$00,$7F,$3F,$7F,$7F,$00,$00,$00,$00
.segment "ASSETS"
native_row_228:
    .byte $00,$00,$7F,$3F,$1F,$1E,$00,$00,$00,$00
.segment "ASSETS"
native_row_229:
    .byte $00,$00,$7E,$12,$7F,$6E,$00,$00,$00,$00
.segment "ASSETS"
native_row_230:
    .byte $00,$00,$7C,$3C,$7F,$74,$01,$01,$00,$00
.segment "ASSETS"
native_row_231:
    .byte $00,$00,$7C,$3C,$7F,$70,$01,$01,$00,$00
.segment "ASSETS"
native_row_232:
    .byte $00,$00,$7C,$3C,$7F,$60,$03,$03,$00,$00
.segment "ASSETS"
native_row_233:
    .byte $00,$00,$78,$38,$7F,$70,$03,$03,$00,$00
.segment "ASSETS"
native_row_234:
    .byte $00,$00,$7E,$3E,$7F,$70,$00,$00,$00,$00
.segment "ASSETS"
native_row_235:
    .byte $40,$40,$7F,$3F,$7F,$7C,$00,$00,$00,$00
.segment "ASSETS"
native_row_236:
    .byte $40,$40,$7F,$37,$3F,$3C,$00,$00,$00,$00
.segment "ASSETS"
native_row_237:
    .byte $00,$00,$7F,$3F,$07,$07,$00,$00
.segment "ASSETS"
native_row_238:
    .byte $00,$00,$7F,$5F,$03,$03,$00,$00
.segment "ASSETS"
native_row_239:
    .byte $00,$00,$7F,$1F,$07,$06,$00,$00
.segment "ASSETS"
native_row_240:
    .byte $00,$00,$7F,$5F,$01,$01,$00,$00
.segment "ASSETS"
native_row_241:
    .byte $00,$00,$7E,$5E,$07,$07,$00,$00
.segment "ASSETS"
native_row_242:
    .byte $00,$00,$7E,$5E,$07,$05,$00,$00
.segment "ASSETS"
native_row_243:
    .byte $40,$40,$7F,$5F,$03,$03,$00,$00
.segment "ASSETS"
native_row_244:
    .byte $40,$40,$1F,$1D,$00,$00,$00,$00
.segment "ASSETS"
native_row_245:
    .byte $00,$00,$1F,$1D,$00,$00,$00,$00
.segment "ASSETS"
native_row_246:
    .byte $40,$40,$7F,$6F,$07,$07,$00,$00
.segment "ASSETS"
native_row_247:
    .byte $00,$00,$7F,$4D,$03,$03,$00,$00
.segment "ASSETS"
native_row_248:
    .byte $00,$00,$7F,$6F,$03,$02,$00,$00
.segment "ASSETS"
native_row_249:
    .byte $00,$00,$7F,$6F,$03,$03,$00,$00
.segment "ASSETS"
native_row_250:
    .byte $40,$40,$7F,$57,$03,$02,$00,$00
.segment "ASSETS"
native_row_251:
    .byte $40,$40,$7F,$77,$03,$03,$00,$00
.segment "ASSETS"
native_row_252:
    .byte $00,$00,$7F,$0D,$01,$01,$00,$00
.segment "ASSETS"
native_row_253:
    .byte $00,$00,$7F,$6F,$01,$01,$00,$00
.segment "ASSETS"
native_row_254:
    .byte $40,$40,$7F,$4F,$07,$07,$00,$00
.segment "ASSETS"
native_row_255:
    .byte $40,$40,$7F,$6B,$07,$07,$00,$00
.segment "ASSETS"
native_row_256:
    .byte $00,$00,$60,$20,$03,$02,$00,$00
.segment "ASSETS"
native_row_257:
    .byte $00,$00,$60,$60,$01,$01,$00,$00
.segment "ASSETS"
native_row_258:
    .byte $00,$00,$40,$40,$7F,$28,$01,$01,$00,$00
.segment "ASSETS"
native_row_259:
    .byte $00,$00,$40,$40,$7F,$7D,$03,$03,$00,$00
.segment "ASSETS"
native_row_260:
    .byte $00,$00,$40,$40,$7F,$79,$03,$03,$00,$00
.segment "ASSETS"
native_row_261:
    .byte $00,$00,$40,$40,$7F,$7B,$07,$07,$00,$00
.segment "ASSETS"
native_row_262:
    .byte $00,$00,$60,$60,$7F,$73,$07,$07,$00,$00
.segment "ASSETS"
native_row_263:
    .byte $00,$00,$60,$60,$7F,$67,$07,$07,$00,$00
.segment "ASSETS"
native_row_264:
    .byte $00,$00,$60,$60,$7F,$77,$03,$03,$00,$00
.segment "ASSETS"
native_row_265:
    .byte $00,$00,$70,$10,$7F,$73,$01,$01,$00,$00
.segment "ASSETS"
native_row_266:
    .byte $00,$00,$7E,$5A,$07,$05,$00,$00,$00,$00
.segment "ASSETS"
native_row_267:
    .byte $00,$00,$7F,$7F,$0F,$0C,$00,$00,$00,$00
.segment "ASSETS"
native_row_268:
    .byte $00,$00,$7F,$3F,$0F,$0E,$00,$00,$00,$00
.segment "ASSETS"
native_row_269:
    .byte $40,$40,$7F,$1F,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_270:
    .byte $40,$40,$7F,$5F,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_271:
    .byte $00,$00,$7F,$1F,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_272:
    .byte $00,$00,$7F,$77,$07,$07,$00,$00
.segment "ASSETS"
native_row_273:
    .byte $00,$00,$7F,$65,$07,$07,$00,$00
.segment "ASSETS"
native_row_274:
    .byte $00,$00,$7E,$6E,$01,$01,$00,$00
.segment "ASSETS"
native_row_275:
    .byte $00,$00,$7E,$6E,$07,$07,$00,$00
.segment "ASSETS"
native_row_276:
    .byte $00,$00,$7E,$22,$03,$02,$00,$00
.segment "ASSETS"
native_row_277:
    .byte $00,$00,$7E,$6E,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_278:
    .byte $00,$00,$60,$60,$0F,$0D,$00,$00
.segment "ASSETS"
native_row_279:
    .byte $00,$00,$60,$60,$07,$05,$00,$00
.segment "ASSETS"
native_row_280:
    .byte $00,$00,$40,$40,$7F,$7F,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_281:
    .byte $00,$00,$60,$20,$7F,$55,$0F,$0A,$00,$00,$00,$00
.segment "ASSETS"
native_row_282:
    .byte $00,$00,$70,$50,$7F,$2A,$1F,$15,$00,$00,$00,$00
.segment "ASSETS"
native_row_283:
    .byte $00,$00,$78,$78,$7F,$7F,$3F,$3F,$00,$00,$00,$00
.segment "ASSETS"
native_row_284:
    .byte $00,$00,$78,$78,$7F,$6E,$3F,$3D,$00,$00,$00,$00
.segment "ASSETS"
native_row_285:
    .byte $00,$00,$78,$78,$7F,$01,$3F,$3E,$00,$00,$00,$00
.segment "ASSETS"
native_row_286:
    .byte $00,$00,$70,$70,$7F,$01,$1F,$1A,$00,$00,$00,$00
.segment "ASSETS"
native_row_287:
    .byte $00,$00,$40,$40,$7F,$46,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_288:
    .byte $00,$00,$40,$40,$7F,$6B,$07,$06,$00,$00,$00,$00
.segment "ASSETS"
native_row_289:
    .byte $00,$00,$00,$00,$7E,$6E,$07,$05,$00,$00,$00,$00
.segment "ASSETS"
native_row_290:
    .byte $00,$00,$40,$40,$7F,$6F,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_291:
    .byte $00,$00,$60,$60,$7F,$2B,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_292:
    .byte $00,$00,$00,$00,$7F,$03,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_293:
    .byte $00,$00,$70,$70,$7F,$01,$1F,$1E,$00,$00,$00,$00
.segment "ASSETS"
native_row_294:
    .byte $00,$00,$40,$40,$7F,$7F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_295:
    .byte $00,$00,$60,$60,$7F,$7F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_296:
    .byte $00,$00,$60,$20,$7F,$55,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_297:
    .byte $00,$00,$60,$60,$7F,$7F,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_298:
    .byte $00,$00,$40,$40,$7F,$7F,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_299:
    .byte $00,$00,$00,$00,$7E,$7E,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_300:
    .byte $00,$00,$00,$00,$00,$00,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_301:
    .byte $00,$00,$00,$00,$60,$60,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_302:
    .byte $00,$00,$00,$00,$78,$28,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_303:
    .byte $00,$00,$00,$00,$7E,$7E,$0F,$0C,$00,$00,$00,$00
.segment "ASSETS"
native_row_304:
    .byte $00,$00,$40,$40,$7F,$7D,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_305:
    .byte $00,$00,$60,$60,$1F,$1B,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_306:
    .byte $00,$00,$60,$60,$03,$03,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_307:
    .byte $00,$00,$00,$00,$07,$07,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_308:
    .byte $00,$00,$00,$00,$3F,$3F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_309:
    .byte $00,$00,$00,$00,$3E,$3E,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_310:
    .byte $00,$00,$00,$00,$7E,$7E,$03,$03,$00,$00
.segment "ASSETS"
native_row_311:
    .byte $00,$00,$00,$00,$7F,$55,$07,$06,$00,$00
.segment "ASSETS"
native_row_312:
    .byte $00,$00,$40,$40,$7F,$2A,$07,$05,$00,$00
.segment "ASSETS"
native_row_313:
    .byte $00,$00,$78,$78,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_314:
    .byte $00,$00,$78,$78,$7F,$7F,$00,$00,$00,$00
.segment "ASSETS"
native_row_315:
    .byte $00,$00,$78,$78,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_316:
    .byte $00,$00,$70,$70,$3F,$2B,$00,$00,$00,$00
.segment "ASSETS"
native_row_317:
    .byte $00,$00,$40,$40,$7F,$7C,$00,$00,$00,$00
.segment "ASSETS"
native_row_318:
    .byte $00,$00,$40,$40,$7F,$1F,$01,$01,$00,$00
.segment "ASSETS"
native_row_319:
    .byte $00,$00,$00,$00,$78,$68,$03,$03,$00,$00
.segment "ASSETS"
native_row_320:
    .byte $00,$00,$00,$00,$60,$60,$03,$03,$00,$00
.segment "ASSETS"
native_row_321:
    .byte $00,$00,$00,$00,$70,$70,$00,$00,$00,$00
.segment "ASSETS"
native_row_322:
    .byte $00,$00,$00,$00,$3E,$3E,$00,$00,$00,$00
.segment "ASSETS"
native_row_323:
    .byte $00,$00,$60,$60,$7F,$7F,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_324:
    .byte $00,$00,$70,$30,$7F,$55,$0F,$0A,$00,$00,$00,$00
.segment "ASSETS"
native_row_325:
    .byte $00,$00,$78,$58,$7F,$52,$1F,$15,$00,$00,$00,$00
.segment "ASSETS"
native_row_326:
    .byte $00,$00,$7C,$7C,$7F,$77,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_327:
    .byte $00,$00,$7C,$7C,$7F,$77,$3F,$3F,$00,$00,$00,$00
.segment "ASSETS"
native_row_328:
    .byte $00,$00,$78,$78,$7F,$6F,$3F,$3F,$00,$00,$00,$00
.segment "ASSETS"
native_row_329:
    .byte $00,$00,$7C,$54,$7F,$47,$3F,$23,$00,$00,$00,$00
.segment "ASSETS"
native_row_330:
    .byte $00,$00,$7C,$54,$7F,$02,$1F,$15,$00,$00,$00,$00
.segment "ASSETS"
native_row_331:
    .byte $00,$00,$78,$58,$7F,$03,$3F,$3E,$00,$00,$00,$00
.segment "ASSETS"
native_row_332:
    .byte $00,$00,$70,$70,$7F,$03,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_333:
    .byte $00,$00,$60,$60,$7F,$44,$0F,$0C,$00,$00,$00,$00
.segment "ASSETS"
native_row_334:
    .byte $00,$00,$60,$20,$7F,$6F,$07,$05,$00,$00,$00,$00
.segment "ASSETS"
native_row_335:
    .byte $00,$00,$40,$40,$7F,$6F,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_336:
    .byte $00,$00,$70,$10,$7F,$00,$0F,$0C,$00,$00,$00,$00
.segment "ASSETS"
native_row_337:
    .byte $00,$00,$78,$58,$7F,$03,$1F,$1B,$00,$00,$00,$00
.segment "ASSETS"
native_row_338:
    .byte $00,$00,$78,$68,$7F,$01,$1F,$17,$00,$00,$00,$00
.segment "ASSETS"
native_row_339:
    .byte $00,$00,$00,$00,$60,$60,$7F,$7F,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_340:
    .byte $00,$00,$00,$00,$60,$20,$7F,$55,$03,$02,$00,$00,$00,$00
.segment "ASSETS"
native_row_341:
    .byte $00,$00,$00,$00,$70,$50,$7F,$2A,$3F,$3D,$00,$00,$00,$00
.segment "ASSETS"
native_row_342:
    .byte $00,$00,$00,$00,$78,$78,$7F,$7D,$7F,$7F,$01,$01,$00,$00
.segment "ASSETS"
native_row_343:
    .byte $00,$00,$00,$00,$7C,$7C,$7F,$7B,$7F,$7F,$07,$07,$00,$00
.segment "ASSETS"
native_row_344:
    .byte $00,$00,$00,$00,$7F,$7F,$7F,$77,$7F,$7F,$07,$07,$00,$00
.segment "ASSETS"
native_row_345:
    .byte $00,$00,$40,$40,$7F,$7F,$7F,$07,$7F,$7F,$07,$07,$00,$00
.segment "ASSETS"
native_row_346:
    .byte $00,$00,$00,$00,$7F,$7F,$7F,$03,$7F,$7C,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_347:
    .byte $00,$00,$70,$70,$7F,$5A,$07,$00,$7C,$70,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_348:
    .byte $00,$00,$7E,$7E,$7F,$1F,$07,$00,$7C,$60,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_349:
    .byte $00,$00,$7F,$5F,$7F,$01,$07,$00,$7C,$40,$0F,$08,$00,$00
.segment "ASSETS"
native_row_350:
    .byte $00,$00,$7F,$3F,$7F,$00,$7F,$00,$7F,$40,$1F,$1F,$00,$00
.segment "ASSETS"
native_row_351:
    .byte $00,$00,$7E,$0E,$7F,$00,$7F,$00,$7F,$40,$1F,$1F,$00,$00
.segment "ASSETS"
native_row_352:
    .byte $00,$00,$7F,$07,$7F,$00,$7F,$00,$7F,$40,$1F,$1F,$00,$00
.segment "ASSETS"
native_row_353:
    .byte $40,$40,$7F,$07,$7F,$00,$7F,$00,$7F,$00,$1F,$19,$00,$00
.segment "ASSETS"
native_row_354:
    .byte $40,$40,$7F,$03,$7F,$00,$7F,$00,$7F,$00,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_355:
    .byte $40,$40,$7F,$01,$7F,$00,$7F,$00,$7F,$00,$07,$07,$00,$00
.segment "ASSETS"
native_row_356:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$1F,$1F,$00,$00
.segment "ASSETS"
native_row_357:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$7F,$7F,$00,$00
.segment "ASSETS"
native_row_358:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$7F,$7B,$00,$00
.segment "ASSETS"
native_row_359:
    .byte $00,$00,$00,$00,$40,$40,$7F,$7F,$07,$07,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_360:
    .byte $00,$00,$00,$00,$70,$30,$7F,$55,$0F,$0A,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_361:
    .byte $00,$00,$00,$00,$7C,$5C,$7F,$2A,$1F,$15,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_362:
    .byte $00,$00,$00,$00,$7F,$7F,$7F,$7E,$3F,$3F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_363:
    .byte $00,$00,$40,$40,$7F,$7F,$7F,$7D,$3F,$3F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_364:
    .byte $00,$00,$40,$40,$7F,$7F,$7F,$7D,$7F,$7F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_365:
    .byte $00,$00,$60,$60,$7F,$7F,$7F,$73,$7F,$7F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_366:
    .byte $00,$00,$60,$60,$7F,$7F,$7F,$41,$7F,$7F,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_367:
    .byte $00,$00,$60,$60,$7F,$1F,$7F,$00,$7F,$7F,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_368:
    .byte $00,$00,$60,$60,$7F,$0F,$7F,$00,$7F,$7E,$0F,$0A,$00,$00,$00,$00
.segment "ASSETS"
native_row_369:
    .byte $00,$00,$60,$60,$7F,$07,$07,$00,$7C,$08,$3F,$2F,$00,$00,$00,$00
.segment "ASSETS"
native_row_370:
    .byte $00,$00,$60,$20,$7F,$04,$07,$00,$7C,$70,$7F,$77,$03,$03,$00,$00
.segment "ASSETS"
native_row_371:
    .byte $00,$00,$70,$70,$7F,$07,$07,$00,$7C,$70,$7F,$7B,$03,$03,$00,$00
.segment "ASSETS"
native_row_372:
    .byte $00,$00,$70,$70,$7F,$07,$7F,$00,$7F,$60,$7F,$7E,$03,$03,$00,$00
.segment "ASSETS"
native_row_373:
    .byte $00,$00,$70,$70,$7F,$07,$7F,$00,$7F,$00,$7F,$78,$01,$01,$00,$00
.segment "ASSETS"
native_row_374:
    .byte $00,$00,$60,$20,$7F,$02,$7F,$00,$7F,$00,$7F,$60,$03,$03,$00,$00
.segment "ASSETS"
native_row_375:
    .byte $00,$00,$60,$60,$7F,$03,$7F,$00,$7F,$00,$7F,$40,$07,$07,$00,$00
.segment "ASSETS"
native_row_376:
    .byte $00,$00,$60,$60,$7F,$03,$7F,$00,$7F,$00,$7F,$00,$07,$07,$00,$00
.segment "ASSETS"
native_row_377:
    .byte $00,$00,$78,$78,$7F,$03,$7F,$00,$7F,$00,$7F,$00,$07,$07,$00,$00
.segment "ASSETS"
native_row_378:
    .byte $00,$00,$7E,$7E,$7F,$03,$7F,$00,$7F,$00,$7F,$00,$07,$06,$00,$00
.segment "ASSETS"
native_row_379:
    .byte $00,$00,$7E,$3E,$03,$03,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_380:
    .byte $00,$00,$08,$08
.segment "ASSETS"
native_row_381:
    .byte $00,$00,$0C,$0C
.segment "ASSETS"
native_row_382:
    .byte $00,$00,$1C,$1C
.segment "ASSETS"
native_row_383:
    .byte $00,$00,$1E,$1E
.segment "ASSETS"
native_row_384:
    .byte $00,$00,$0E,$0E
.segment "ASSETS"
native_row_385:
    .byte $00,$00,$06,$06
.segment "ASSETS"
native_row_386:
    .byte $00,$00,$1E,$1A
.segment "ASSETS"
native_row_387:
    .byte $7E,$66,$01,$01
.segment "ASSETS"
native_row_388:
    .byte $7F,$3F,$03,$03
.segment "ASSETS"
native_row_389:
    .byte $7F,$7D,$03,$03
.segment "ASSETS"
native_row_390:
    .byte $7E,$5E,$03,$03
.segment "ASSETS"
native_row_391:
    .byte $7E,$7E,$03,$03
.segment "ASSETS"
native_row_392:
    .byte $7F,$6F,$03,$03
.segment "ASSETS"
native_row_393:
    .byte $7F,$7B,$03,$02
.segment "ASSETS"
native_row_394:
    .byte $7F,$77,$01,$01
.segment "ASSETS"
native_row_395:
    .byte $7E,$6E,$01,$01
.segment "ASSETS"
native_row_396:
    .byte $7E,$02,$03,$03
.segment "ASSETS"
native_row_397:
    .byte $7E,$42,$03,$02
.segment "ASSETS"
native_row_398:
    .byte $7E,$42,$03,$03
.segment "ASSETS"
native_row_399:
    .byte $01,$01,$00,$00
.segment "ASSETS"
native_row_400:
    .byte $03,$03,$00,$00
.segment "ASSETS"
native_row_401:
    .byte $07,$07,$00,$00
.segment "ASSETS"
native_row_402:
    .byte $06,$06,$00,$00
.segment "ASSETS"
native_row_403:
    .byte $00,$00,$04,$04,$00,$00
.segment "ASSETS"
native_row_404:
    .byte $00,$00,$1E,$12,$00,$00
.segment "ASSETS"
native_row_405:
    .byte $00,$00,$7F,$1D,$0F,$0C
.segment "ASSETS"
native_row_406:
    .byte $00,$00,$7F,$17,$07,$06
.segment "ASSETS"
native_row_407:
    .byte $00,$00,$7F,$1B,$0F,$0B
.segment "ASSETS"
native_row_408:
    .byte $00,$00,$7E,$0E,$07,$05
.segment "ASSETS"
native_row_409:
    .byte $00,$00,$7E,$0A,$0F,$0F
.segment "ASSETS"
native_row_410:
    .byte $00,$00,$7E,$0A,$0F,$0B
.segment "ASSETS"
native_row_411:
    .byte $00,$00,$7F,$0F,$07,$06
.segment "ASSETS"
native_row_412:
    .byte $00,$00,$7F,$0F,$0F,$0E
.segment "ASSETS"
native_row_413:
    .byte $40,$40,$7F,$0F,$0F,$0C
.segment "ASSETS"
native_row_414:
    .byte $40,$40,$7F,$02,$03,$03
.segment "ASSETS"
native_row_415:
    .byte $40,$40,$7F,$62,$07,$07
.segment "ASSETS"
native_row_416:
    .byte $40,$40,$7F,$63,$0F,$0F
.segment "ASSETS"
native_row_417:
    .byte $40,$40,$7F,$53,$0F,$0F
.segment "ASSETS"
native_row_418:
    .byte $00,$00,$7F,$3B,$0F,$0F
.segment "ASSETS"
native_row_419:
    .byte $00,$00,$7F,$77,$0F,$0C
.segment "ASSETS"
native_row_420:
    .byte $00,$00,$7F,$7F,$0F,$0F
.segment "ASSETS"
native_row_421:
    .byte $00,$00,$7E,$7E,$0F,$0F
.segment "ASSETS"
native_row_422:
    .byte $00,$00,$7E,$5E,$0F,$0F
.segment "ASSETS"
native_row_423:
    .byte $00,$00,$7C,$4C,$0F,$0F
.segment "ASSETS"
native_row_424:
    .byte $7F,$03,$1F,$1D,$00,$00
.segment "ASSETS"
native_row_425:
    .byte $7F,$07,$1F,$17,$00,$00
.segment "ASSETS"
native_row_426:
    .byte $7F,$0D,$1F,$1B,$00,$00
.segment "ASSETS"
native_row_427:
    .byte $7E,$0A,$0F,$0E,$00,$00
.segment "ASSETS"
native_row_428:
    .byte $7F,$07,$0F,$0A,$00,$00
.segment "ASSETS"
native_row_429:
    .byte $7F,$05,$0F,$0A,$00,$00
.segment "ASSETS"
native_row_430:
    .byte $7F,$0F,$0F,$0A,$00,$00
.segment "ASSETS"
native_row_431:
    .byte $7F,$0B,$0F,$0A,$00,$00
.segment "ASSETS"
native_row_432:
    .byte $7F,$05,$1F,$1E,$00,$00
.segment "ASSETS"
native_row_433:
    .byte $7F,$07,$1F,$1F,$00,$00
.segment "ASSETS"
native_row_434:
    .byte $7F,$01,$1F,$1F,$00,$00
.segment "ASSETS"
native_row_435:
    .byte $00,$00,$07,$05,$00,$00
.segment "ASSETS"
native_row_436:
    .byte $7F,$01,$07,$05,$00,$00
.segment "ASSETS"
native_row_437:
    .byte $7F,$43,$07,$07,$00,$00
.segment "ASSETS"
native_row_438:
    .byte $7F,$63,$07,$07,$00,$00
.segment "ASSETS"
native_row_439:
    .byte $7E,$76,$03,$03,$00,$00
.segment "ASSETS"
native_row_440:
    .byte $7F,$7B,$01,$01,$00,$00
.segment "ASSETS"
native_row_441:
    .byte $7F,$7F,$00,$00,$00,$00
.segment "ASSETS"
native_row_442:
    .byte $3F,$3F,$00,$00,$00,$00
.segment "ASSETS"
native_row_443:
    .byte $1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_444:
    .byte $0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_445:
    .byte $02,$02,$00,$00,$00,$00
.segment "ASSETS"
native_row_446:
    .byte $00,$00,$7F,$17,$0F,$0E
.segment "ASSETS"
native_row_447:
    .byte $00,$00,$7E,$0A,$0F,$0E
.segment "ASSETS"
native_row_448:
    .byte $00,$00,$7E,$0A,$0F,$0A
.segment "ASSETS"
native_row_449:
    .byte $00,$00,$7E,$0A,$0F,$0D
.segment "ASSETS"
native_row_450:
    .byte $00,$00,$7F,$0F,$0F,$0A
.segment "ASSETS"
native_row_451:
    .byte $40,$40,$7F,$0F,$0F,$0E
.segment "ASSETS"
native_row_452:
    .byte $40,$40,$7F,$0F,$0F,$08
.segment "ASSETS"
native_row_453:
    .byte $40,$40,$03,$02,$00,$00
.segment "ASSETS"
native_row_454:
    .byte $40,$40,$7F,$02,$0F,$08
.segment "ASSETS"
native_row_455:
    .byte $40,$40,$7F,$03,$0F,$0E
.segment "ASSETS"
native_row_456:
    .byte $40,$40,$7F,$07,$0F,$0E
.segment "ASSETS"
native_row_457:
    .byte $00,$00,$7F,$4F,$0F,$0A
.segment "ASSETS"
native_row_458:
    .byte $00,$00,$7E,$7E,$0F,$0E
.segment "ASSETS"
native_row_459:
    .byte $00,$00,$7C,$7C,$0F,$0E
.segment "ASSETS"
native_row_460:
    .byte $00,$00,$78,$78,$0F,$0A
.segment "ASSETS"
native_row_461:
    .byte $00,$00,$60,$20,$0F,$0C
.segment "ASSETS"
native_row_462:
    .byte $08,$08,$00,$00
.segment "ASSETS"
native_row_463:
    .byte $3C,$24,$00,$00
.segment "ASSETS"
native_row_464:
    .byte $3E,$3A,$00,$00
.segment "ASSETS"
native_row_465:
    .byte $3E,$2E,$00,$00
.segment "ASSETS"
native_row_466:
    .byte $3E,$36,$00,$00
.segment "ASSETS"
native_row_467:
    .byte $1C,$1C,$00,$00
.segment "ASSETS"
native_row_468:
    .byte $1C,$14,$00,$00
.segment "ASSETS"
native_row_469:
    .byte $3C,$3C,$00,$00
.segment "ASSETS"
native_row_470:
    .byte $38,$28,$00,$00
.segment "ASSETS"
native_row_471:
    .byte $3F,$3D,$00,$00
.segment "ASSETS"
native_row_472:
    .byte $1F,$1B,$00,$00
.segment "ASSETS"
native_row_473:
    .byte $1F,$1F,$00,$00
.segment "ASSETS"
native_row_474:
    .byte $0F,$0F,$00,$00
.segment "ASSETS"
native_row_475:
    .byte $40,$40,$1F,$17
.segment "ASSETS"
native_row_476:
    .byte $40,$40,$1F,$19
.segment "ASSETS"
native_row_477:
    .byte $7E,$66,$01,$01,$00,$00
.segment "ASSETS"
native_row_478:
    .byte $7F,$7B,$03,$03,$00,$00
.segment "ASSETS"
native_row_479:
    .byte $7F,$3B,$03,$03,$00,$00
.segment "ASSETS"
native_row_480:
    .byte $7F,$7B,$03,$02,$00,$00
.segment "ASSETS"
native_row_481:
    .byte $7F,$77,$01,$01,$00,$00
.segment "ASSETS"
native_row_482:
    .byte $7F,$6F,$03,$03,$00,$00
.segment "ASSETS"
native_row_483:
    .byte $7F,$5F,$03,$03,$00,$00
.segment "ASSETS"
native_row_484:
    .byte $7F,$3F,$07,$07,$00,$00
.segment "ASSETS"
native_row_485:
    .byte $7E,$7E,$0F,$0E,$00,$00
.segment "ASSETS"
native_row_486:
    .byte $7E,$7E,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_487:
    .byte $7E,$02,$1F,$1C,$00,$00
.segment "ASSETS"
native_row_488:
    .byte $7E,$02,$7F,$6C,$07,$07
.segment "ASSETS"
native_row_489:
    .byte $7E,$02,$7F,$3A,$07,$06
.segment "ASSETS"
native_row_490:
    .byte $00,$00,$18,$18
.segment "ASSETS"
native_row_491:
    .byte $00,$00,$0E,$0A
.segment "ASSETS"
native_row_492:
    .byte $00,$00,$1F,$13
.segment "ASSETS"
native_row_493:
    .byte $40,$40,$1F,$1B
.segment "ASSETS"
native_row_494:
    .byte $00,$00,$1F,$1D
.segment "ASSETS"
native_row_495:
    .byte $7C,$7C,$1F,$1A
.segment "ASSETS"
native_row_496:
    .byte $7C,$4C,$0F,$0E
.segment "ASSETS"
native_row_497:
    .byte $0F,$0B,$00,$00
.segment "ASSETS"
native_row_498:
    .byte $00,$00,$00,$00,$04,$04
.segment "ASSETS"
native_row_499:
    .byte $00,$00,$00,$00,$06,$06
.segment "ASSETS"
native_row_500:
    .byte $00,$00,$00,$00,$0E,$0E
.segment "ASSETS"
native_row_501:
    .byte $00,$00,$00,$00,$0F,$0F
.segment "ASSETS"
native_row_502:
    .byte $00,$00,$00,$00,$07,$07
.segment "ASSETS"
native_row_503:
    .byte $00,$00,$40,$40,$07,$07
.segment "ASSETS"
native_row_504:
    .byte $00,$00,$60,$60,$07,$06
.segment "ASSETS"
native_row_505:
    .byte $00,$00,$70,$30,$03,$03
.segment "ASSETS"
native_row_506:
    .byte $00,$00,$78,$78,$01,$01
.segment "ASSETS"
native_row_507:
    .byte $00,$00,$7C,$7C,$00,$00
.segment "ASSETS"
native_row_508:
    .byte $00,$00,$0F,$0D,$00,$00
.segment "ASSETS"
native_row_509:
    .byte $00,$00,$07,$07,$00,$00
.segment "ASSETS"
native_row_510:
    .byte $00,$00,$03,$03,$00,$00
.segment "ASSETS"
native_row_511:
    .byte $40,$40,$07,$07,$00,$00
.segment "ASSETS"
native_row_512:
    .byte $7E,$7E,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_513:
    .byte $7F,$3F,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_514:
    .byte $7F,$3D,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_515:
    .byte $7F,$7B,$03,$02,$00,$00,$00,$00
.segment "ASSETS"
native_row_516:
    .byte $7F,$7B,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_517:
    .byte $7F,$77,$7F,$7F,$00,$00,$00,$00
.segment "ASSETS"
native_row_518:
    .byte $7F,$6F,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_519:
    .byte $3F,$1F,$60,$40,$07,$07,$00,$00
.segment "ASSETS"
native_row_520:
    .byte $3F,$3F,$60,$00,$07,$06,$00,$00
.segment "ASSETS"
native_row_521:
    .byte $3F,$3F,$60,$00,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_522:
    .byte $3E,$3E,$60,$00,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_523:
    .byte $3E,$3E,$60,$00,$07,$06,$00,$00
.segment "ASSETS"
native_row_524:
    .byte $00,$00,$70,$30,$0F,$0F
.segment "ASSETS"
native_row_525:
    .byte $00,$00,$78,$78,$0F,$0E
.segment "ASSETS"
native_row_526:
    .byte $00,$00,$7C,$1C,$07,$06
.segment "ASSETS"
native_row_527:
    .byte $00,$00,$7C,$0C,$0F,$0A
.segment "ASSETS"
native_row_528:
    .byte $00,$00,$7C,$0C,$03,$02
.segment "ASSETS"
native_row_529:
    .byte $00,$00,$7E,$1E,$03,$02
.segment "ASSETS"
native_row_530:
    .byte $00,$00,$0C,$0C,$00,$00
.segment "ASSETS"
native_row_531:
    .byte $01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_532:
    .byte $03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_533:
    .byte $07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_534:
    .byte $0E,$0E,$00,$00,$00,$00
.segment "ASSETS"
native_row_535:
    .byte $1E,$1E,$00,$00,$00,$00
.segment "ASSETS"
native_row_536:
    .byte $3C,$3C,$00,$00,$00,$00
.segment "ASSETS"
native_row_537:
    .byte $30,$30,$00,$00,$00,$00
.segment "ASSETS"
native_row_538:
    .byte $40,$40,$03,$03,$00,$00
.segment "ASSETS"
native_row_539:
    .byte $00,$00,$0E,$0E,$00,$00
.segment "ASSETS"
native_row_540:
    .byte $7F,$05,$1F,$11,$00,$00
.segment "ASSETS"
native_row_541:
    .byte $7F,$4F,$1F,$10,$00,$00
.segment "ASSETS"
native_row_542:
    .byte $7F,$6B,$1F,$13,$00,$00
.segment "ASSETS"
native_row_543:
    .byte $7F,$57,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_544:
    .byte $7F,$65,$03,$03,$00,$00
.segment "ASSETS"
native_row_545:
    .byte $7F,$47,$03,$03,$00,$00
.segment "ASSETS"
native_row_546:
    .byte $7F,$41,$01,$01,$00,$00
.segment "ASSETS"
native_row_547:
    .byte $40,$40,$01,$01,$00,$00
.segment "ASSETS"
native_row_548:
    .byte $7F,$43,$03,$03,$00,$00
.segment "ASSETS"
native_row_549:
    .byte $7E,$46,$03,$03,$00,$00
.segment "ASSETS"
native_row_550:
    .byte $7F,$3F,$03,$03,$00,$00
.segment "ASSETS"
native_row_551:
    .byte $7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_552:
    .byte $40,$40,$7F,$08,$0F,$0F
.segment "ASSETS"
native_row_553:
    .byte $40,$40,$7F,$10,$0F,$0D
.segment "ASSETS"
native_row_554:
    .byte $40,$40,$7F,$70,$0F,$0E
.segment "ASSETS"
native_row_555:
    .byte $00,$00,$7F,$53,$0F,$0A
.segment "ASSETS"
native_row_556:
    .byte $00,$00,$7C,$3C,$0F,$0E
.segment "ASSETS"
native_row_557:
    .byte $00,$00,$7C,$1C,$0F,$08
.segment "ASSETS"
native_row_558:
    .byte $00,$00,$18,$18,$00,$00
.segment "ASSETS"
native_row_559:
    .byte $00,$00,$1C,$1C,$00,$00
.segment "ASSETS"
native_row_560:
    .byte $00,$00,$7C,$1C,$0F,$0E
.segment "ASSETS"
native_row_561:
    .byte $00,$00,$7C,$1C,$0F,$0B
.segment "ASSETS"
native_row_562:
    .byte $00,$00,$7C,$6C,$0F,$0E
.segment "ASSETS"
native_row_563:
    .byte $00,$00,$7C,$7C,$0F,$0A
.segment "ASSETS"
native_row_564:
    .byte $00,$00,$70,$70,$0F,$0D
.segment "ASSETS"
native_row_565:
    .byte $3C,$0C,$60,$60,$07,$06
.segment "ASSETS"
native_row_566:
    .byte $3C,$14,$60,$20,$03,$03
.segment "ASSETS"
native_row_567:
    .byte $3C,$24,$60,$60,$01,$01
.segment "ASSETS"
native_row_568:
    .byte $40,$40,$7F,$7C,$00,$00
.segment "ASSETS"
native_row_569:
    .byte $00,$00,$02,$02,$00,$00
.segment "ASSETS"
native_row_570:
    .byte $00,$00,$7C,$24,$01,$01
.segment "ASSETS"
native_row_571:
    .byte $00,$00,$78,$48,$00,$00
.segment "ASSETS"
native_row_572:
    .byte $00,$00,$30,$30,$00,$00
.segment "ASSETS"
native_row_573:
    .byte $7F,$77,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_574:
    .byte $7F,$6F,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_575:
    .byte $7F,$5F,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_576:
    .byte $7F,$3F,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_577:
    .byte $7F,$7F,$3F,$3C,$00,$00,$00,$00
.segment "ASSETS"
native_row_578:
    .byte $7F,$7F,$7F,$73,$01,$01,$00,$00
.segment "ASSETS"
native_row_579:
    .byte $3E,$3E,$60,$00,$7F,$73,$00,$00
.segment "ASSETS"
native_row_580:
    .byte $7E,$02,$7F,$03,$7F,$0F,$01,$01
.segment "ASSETS"
native_row_581:
    .byte $7E,$02,$7F,$1B,$7F,$06,$01,$01
.segment "ASSETS"
native_row_582:
    .byte $7E,$02,$7F,$63,$7F,$41,$03,$02
.segment "ASSETS"
native_row_583:
    .byte $38,$38,$60,$00,$07,$06
.segment "ASSETS"
native_row_584:
    .byte $7C,$44,$7F,$0D,$0F,$0E
.segment "ASSETS"
native_row_585:
    .byte $7C,$04,$7F,$4E,$0F,$0A
.segment "ASSETS"
native_row_586:
    .byte $7E,$0A,$7F,$3C,$07,$06
.segment "ASSETS"
native_row_587:
    .byte $3E,$0E,$60,$00,$03,$03
.segment "ASSETS"
native_row_588:
    .byte $3E,$1E,$60,$40,$03,$02
.segment "ASSETS"
native_row_589:
    .byte $3C,$3C,$60,$20,$03,$02
.segment "ASSETS"
native_row_590:
    .byte $70,$70,$0F,$0C,$00,$00
.segment "ASSETS"
native_row_591:
    .byte $7C,$14,$01,$01,$00,$00
.segment "ASSETS"
native_row_592:
    .byte $78,$48,$00,$00,$00,$00
.segment "ASSETS"
native_row_593:
    .byte $40,$40,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_594:
    .byte $00,$00,$1F,$17,$00,$00
.segment "ASSETS"
native_row_595:
    .byte $00,$00,$1E,$16,$00,$00
.segment "ASSETS"
native_row_596:
    .byte $00,$00,$1F,$15,$00,$00
.segment "ASSETS"
native_row_597:
    .byte $00,$00,$1C,$14,$00,$00
.segment "ASSETS"
native_row_598:
    .byte $00,$00,$0E,$0A,$00,$00
.segment "ASSETS"
native_row_599:
    .byte $00,$00,$01,$01,$00,$00
.segment "ASSETS"
native_row_600:
    .byte $7F,$71,$01,$01,$00,$00
.segment "ASSETS"
native_row_601:
    .byte $7F,$7B,$00,$00,$00,$00
.segment "ASSETS"
native_row_602:
    .byte $7F,$77,$00,$00,$00,$00
.segment "ASSETS"
native_row_603:
    .byte $00,$00,$00,$00,$3C,$3C,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_604:
    .byte $00,$00,$00,$00,$7E,$56,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_605:
    .byte $00,$00,$00,$00,$7F,$2B,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_606:
    .byte $00,$00,$00,$00,$7F,$3D,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_607:
    .byte $00,$00,$00,$00,$7F,$6B,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_608:
    .byte $00,$00,$00,$00,$7F,$2D,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_609:
    .byte $00,$00,$00,$00,$7F,$7F,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_610:
    .byte $00,$00,$00,$00,$7E,$7E,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_611:
    .byte $00,$00,$40,$40,$7F,$7F,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_612:
    .byte $00,$00,$70,$70,$7F,$7F,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_613:
    .byte $00,$00,$78,$68,$7F,$7F,$0F,$0B,$00,$00,$00,$00
.segment "ASSETS"
native_row_614:
    .byte $00,$00,$78,$18,$7F,$7F,$1F,$1C,$00,$00,$00,$00
.segment "ASSETS"
native_row_615:
    .byte $00,$00,$78,$78,$7F,$00,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_616:
    .byte $00,$00,$7C,$7C,$7F,$7F,$3F,$3F,$00,$00,$00,$00
.segment "ASSETS"
native_row_617:
    .byte $00,$00,$7C,$5C,$7F,$7F,$3F,$3B,$00,$00,$00,$00
.segment "ASSETS"
native_row_618:
    .byte $00,$00,$7C,$5C,$7F,$77,$3F,$3B,$00,$00,$00,$00
.segment "ASSETS"
native_row_619:
    .byte $00,$00,$78,$78,$7F,$7F,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_620:
    .byte $00,$00,$40,$40,$7F,$77,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_621:
    .byte $00,$00,$40,$40,$7F,$00,$03,$02,$00,$00,$00,$00
.segment "ASSETS"
native_row_622:
    .byte $00,$00,$06,$06,$00,$00
.segment "ASSETS"
native_row_623:
    .byte $00,$00,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_624:
    .byte $40,$40,$0F,$0D,$00,$00
.segment "ASSETS"
native_row_625:
    .byte $40,$40,$1F,$16,$00,$00
.segment "ASSETS"
native_row_626:
    .byte $40,$40,$1F,$17,$00,$00
.segment "ASSETS"
native_row_627:
    .byte $40,$40,$1F,$1D,$00,$00
.segment "ASSETS"
native_row_628:
    .byte $00,$00,$1F,$1B,$00,$00
.segment "ASSETS"
native_row_629:
    .byte $40,$40,$0F,$0E,$00,$00
.segment "ASSETS"
native_row_630:
    .byte $40,$40,$1F,$15,$00,$00
.segment "ASSETS"
native_row_631:
    .byte $00,$00,$0F,$0B,$00,$00
.segment "ASSETS"
native_row_632:
    .byte $00,$00,$40,$40,$03,$03,$00,$00
.segment "ASSETS"
native_row_633:
    .byte $00,$00,$7E,$6A,$07,$07,$00,$00
.segment "ASSETS"
native_row_634:
    .byte $00,$00,$7C,$7C,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_635:
    .byte $40,$40,$7F,$56,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_636:
    .byte $00,$00,$7E,$7A,$0F,$0F,$00,$00
.segment "ASSETS"
native_row_637:
    .byte $00,$00,$7F,$75,$07,$07,$00,$00
.segment "ASSETS"
native_row_638:
    .byte $00,$00,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_639:
    .byte $00,$00,$7F,$1F,$07,$05,$00,$00
.segment "ASSETS"
native_row_640:
    .byte $40,$40,$7F,$7F,$03,$02,$00,$00
.segment "ASSETS"
native_row_641:
    .byte $40,$40,$7F,$2F,$0F,$0B,$00,$00
.segment "ASSETS"
native_row_642:
    .byte $00,$00,$7F,$5F,$03,$02,$00,$00
.segment "ASSETS"
native_row_643:
    .byte $78,$78,$00,$00,$00,$00
.segment "ASSETS"
native_row_644:
    .byte $7C,$04,$01,$01,$00,$00
.segment "ASSETS"
native_row_645:
    .byte $7E,$02,$03,$02,$00,$00
.segment "ASSETS"
native_row_646:
    .byte $7F,$01,$07,$04,$00,$00
.segment "ASSETS"
native_row_647:
    .byte $7F,$0D,$07,$04,$00,$00
.segment "ASSETS"
native_row_648:
    .byte $7F,$3B,$0F,$08,$00,$00
.segment "ASSETS"
native_row_649:
    .byte $7F,$49,$3F,$29,$00,$00
.segment "ASSETS"
native_row_650:
    .byte $7F,$49,$7F,$4A,$01,$01
.segment "ASSETS"
native_row_651:
    .byte $00,$00,$70,$70,$00,$00
.segment "ASSETS"
native_row_652:
    .byte $00,$00,$7E,$76,$03,$03
.segment "ASSETS"
native_row_653:
    .byte $40,$40,$7F,$4F,$03,$02
.segment "ASSETS"
native_row_654:
    .byte $60,$60,$7F,$07,$01,$01
.segment "ASSETS"
native_row_655:
    .byte $60,$60,$00,$00,$00,$00
.segment "ASSETS"
native_row_656:
    .byte $70,$10,$3F,$21,$00,$00
.segment "ASSETS"
native_row_657:
    .byte $78,$08,$7F,$42,$01,$01
.segment "ASSETS"
native_row_658:
    .byte $78,$08,$7F,$74,$00,$00
.segment "ASSETS"
native_row_659:
    .byte $7C,$04,$7F,$74,$03,$03
.segment "ASSETS"
native_row_660:
    .byte $7C,$44,$7F,$48,$03,$02
.segment "ASSETS"
native_row_661:
    .byte $7E,$42,$7F,$07,$01,$01
.segment "ASSETS"
native_row_662:
    .byte $7E,$62,$03,$02,$00,$00
.segment "ASSETS"
native_row_663:
    .byte $7F,$59,$00,$00,$00,$00
.segment "ASSETS"
native_row_664:
    .byte $7F,$49,$00,$00,$00,$00
.segment "ASSETS"
native_row_665:
    .byte $0F,$0D,$00,$00,$00,$00
.segment "ASSETS"
native_row_666:
    .byte $0F,$0B,$00,$00,$00,$00
.segment "ASSETS"
native_row_667:
    .byte $0F,$09,$00,$00,$00,$00
.segment "ASSETS"
native_row_668:
    .byte $00,$00,$70,$70,$01,$01
.segment "ASSETS"
native_row_669:
    .byte $00,$00,$78,$08,$03,$02
.segment "ASSETS"
native_row_670:
    .byte $00,$00,$7C,$04,$07,$04
.segment "ASSETS"
native_row_671:
    .byte $00,$00,$7E,$02,$0F,$08
.segment "ASSETS"
native_row_672:
    .byte $00,$00,$7E,$02,$0F,$0B
.segment "ASSETS"
native_row_673:
    .byte $00,$00,$7F,$61,$0F,$0D
.segment "ASSETS"
native_row_674:
    .byte $60,$20,$7F,$19,$0F,$09
.segment "ASSETS"
native_row_675:
    .byte $78,$18,$7F,$15,$0F,$09
.segment "ASSETS"
native_row_676:
    .byte $70,$70,$00,$00,$00,$00
.segment "ASSETS"
native_row_677:
    .byte $7C,$7C,$07,$06,$00,$00
.segment "ASSETS"
native_row_678:
    .byte $7C,$14,$1F,$1F,$00,$00
.segment "ASSETS"
native_row_679:
    .byte $78,$08,$3F,$3E,$00,$00
.segment "ASSETS"
native_row_680:
    .byte $60,$20,$7F,$48,$00,$00
.segment "ASSETS"
native_row_681:
    .byte $78,$18,$7F,$04,$01,$01
.segment "ASSETS"
native_row_682:
    .byte $70,$70,$7F,$02,$01,$01
.segment "ASSETS"
native_row_683:
    .byte $7C,$7C,$7F,$02,$03,$02
.segment "ASSETS"
native_row_684:
    .byte $7C,$14,$7F,$11,$03,$02
.segment "ASSETS"
native_row_685:
    .byte $78,$08,$7F,$1E,$07,$04
.segment "ASSETS"
native_row_686:
    .byte $00,$00,$7C,$34,$07,$04
.segment "ASSETS"
native_row_687:
    .byte $00,$00,$70,$50,$0F,$09
.segment "ASSETS"
native_row_688:
    .byte $00,$00,$70,$10,$0F,$09
.segment "ASSETS"
native_row_689:
    .byte $00,$00,$00,$00,$0F,$0B
.segment "ASSETS"
native_row_690:
    .byte $00,$00,$00,$00,$0F,$0D
.segment "ASSETS"
native_row_691:
    .byte $00,$00,$00,$00,$08,$08
.segment "ASSETS"
native_row_692:
    .byte $7F,$49,$0F,$09,$00,$00
.segment "ASSETS"
native_row_693:
    .byte $7F,$49,$0F,$0A,$00,$00
.segment "ASSETS"
native_row_694:
    .byte $00,$00,$10,$10,$00,$00
.segment "ASSETS"
native_row_695:
    .byte $40,$40,$1F,$13,$00,$00
.segment "ASSETS"
native_row_696:
    .byte $60,$60,$1F,$1F,$00,$00
.segment "ASSETS"
native_row_697:
    .byte $40,$40,$3F,$3F,$00,$00
.segment "ASSETS"
native_row_698:
    .byte $00,$00,$70,$70,$03,$02
.segment "ASSETS"
native_row_699:
    .byte $00,$00,$60,$60,$01,$01
.segment "ASSETS"
native_row_700:
    .byte $00,$00,$40,$40,$00,$00
.segment "ASSETS"
native_row_701:
    .byte $00,$00,$60,$20,$01,$01
.segment "ASSETS"
native_row_702:
    .byte $00,$00,$7F,$19,$0F,$09
.segment "ASSETS"
native_row_703:
    .byte $00,$00,$7F,$15,$0F,$09
.segment "ASSETS"
native_row_704:
    .byte $40,$40,$00,$00,$00,$00
.segment "ASSETS"
native_row_705:
    .byte $40,$40,$1F,$1E,$00,$00
.segment "ASSETS"
native_row_706:
    .byte $00,$00,$3F,$3F,$00,$00
.segment "ASSETS"
native_row_707:
    .byte $7C,$74,$00,$00,$00,$00
.segment "ASSETS"
native_row_708:
    .byte $38,$38,$00,$00,$00,$00
.segment "ASSETS"
native_row_709:
    .byte $10,$10,$00,$00,$00,$00
.segment "ASSETS"
native_row_710:
    .byte $38,$28,$00,$00,$00,$00
.segment "ASSETS"
native_row_711:
    .byte $00,$00,$00,$00,$1E,$1E,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_712:
    .byte $00,$00,$00,$00,$7F,$7F,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_713:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_714:
    .byte $00,$00,$60,$60,$7F,$7F,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_715:
    .byte $00,$00,$60,$60,$7F,$7B,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_716:
    .byte $00,$00,$60,$60,$7F,$7D,$3F,$3F,$00,$00,$00,$00
.segment "ASSETS"
native_row_717:
    .byte $00,$00,$60,$60,$7F,$7B,$7F,$7F,$00,$00,$00,$00
.segment "ASSETS"
native_row_718:
    .byte $00,$00,$40,$40,$7F,$7B,$7F,$7F,$00,$00,$00,$00
.segment "ASSETS"
native_row_719:
    .byte $00,$00,$40,$40,$7F,$77,$7F,$7F,$01,$01,$00,$00
.segment "ASSETS"
native_row_720:
    .byte $00,$00,$60,$60,$7F,$77,$7F,$7F,$01,$01,$00,$00
.segment "ASSETS"
native_row_721:
    .byte $00,$00,$70,$70,$7F,$7B,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_722:
    .byte $00,$00,$78,$78,$7F,$78,$7F,$7F,$03,$03,$00,$00
.segment "ASSETS"
native_row_723:
    .byte $00,$00,$78,$38,$7F,$70,$7F,$7F,$07,$07,$00,$00
.segment "ASSETS"
native_row_724:
    .byte $00,$00,$7C,$1C,$7F,$60,$7F,$7F,$07,$07,$00,$00
.segment "ASSETS"
native_row_725:
    .byte $00,$00,$7C,$1C,$7F,$40,$7F,$01,$0F,$08,$00,$00
.segment "ASSETS"
native_row_726:
    .byte $00,$00,$7E,$0E,$7F,$40,$7F,$01,$1F,$10,$00,$00
.segment "ASSETS"
native_row_727:
    .byte $00,$00,$7E,$16,$7F,$00,$7F,$03,$1F,$10,$00,$00
.segment "ASSETS"
native_row_728:
    .byte $00,$00,$7C,$7C,$7F,$77,$01,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_729:
    .byte $00,$00,$7E,$7E,$7F,$7B,$03,$03,$00,$00,$00,$00
.segment "ASSETS"
native_row_730:
    .byte $00,$00,$7F,$7F,$7F,$7B,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_731:
    .byte $40,$40,$7F,$7F,$7F,$7D,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_732:
    .byte $40,$40,$7F,$0F,$7F,$78,$0F,$0F,$00,$00,$00,$00
.segment "ASSETS"
native_row_733:
    .byte $00,$00,$7F,$3F,$7F,$70,$1F,$1F,$00,$00,$00,$00
.segment "ASSETS"
native_row_734:
    .byte $00,$00,$7E,$7E,$7F,$41,$3F,$3F,$00,$00,$00,$00
.segment "ASSETS"
native_row_735:
    .byte $00,$00,$78,$78,$7F,$03,$3F,$3E,$00,$00,$00,$00
.segment "ASSETS"
native_row_736:
    .byte $00,$00,$60,$60,$7F,$07,$7F,$58,$01,$01,$00,$00
.segment "ASSETS"
native_row_737:
    .byte $00,$00,$00,$00,$7E,$1E,$7F,$70,$03,$03,$00,$00
.segment "ASSETS"
native_row_738:
    .byte $00,$00,$00,$00,$7C,$7C,$7F,$70,$03,$02,$00,$00
.segment "ASSETS"
native_row_739:
    .byte $00,$00,$00,$00,$7C,$5C,$7F,$00,$07,$07,$00,$00
.segment "ASSETS"
native_row_740:
    .byte $00,$00,$00,$00,$7E,$4E,$7F,$00,$07,$07,$00,$00
.segment "ASSETS"
native_row_741:
    .byte $00,$00,$00,$00,$7E,$16,$7F,$00,$0F,$0E,$00,$00
.segment "ASSETS"
native_row_742:
    .byte $00,$00,$00,$00,$7E,$0E,$7F,$00,$1F,$12,$00,$00
.segment "ASSETS"
native_row_743:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$3E,$22,$00,$00
.segment "ASSETS"
native_row_744:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$3C,$3C,$00,$00
.segment "ASSETS"
native_row_745:
    .byte $00,$00,$1F,$1F,$00,$00
.segment "ASSETS"
native_row_746:
    .byte $00,$00,$08,$08,$00,$00
.segment "ASSETS"
native_row_747:
    .byte $00,$00,$1E,$1A,$00,$00
.segment "ASSETS"
native_row_748:
    .byte $00,$00,$1F,$19,$00,$00
.segment "ASSETS"
native_row_749:
    .byte $00,$00,$1E,$1E,$00,$00
.segment "ASSETS"
native_row_750:
    .byte $40,$40,$1F,$11,$00,$00
.segment "ASSETS"
native_row_751:
    .byte $08,$08
.segment "ASSETS"
native_row_752:
    .byte $1E,$12
.segment "ASSETS"
native_row_753:
    .byte $3E,$2E
.segment "ASSETS"
native_row_754:
    .byte $3E,$3A
.segment "ASSETS"
native_row_755:
    .byte $3E,$36
.segment "ASSETS"
native_row_756:
    .byte $1C,$1C
.segment "ASSETS"
native_row_757:
    .byte $3C,$24
.segment "ASSETS"
sprite_1:
    .byte $18,$12,$07,$04,$04,$04,$04,$04,$05,$05,$01,$00,$00,$00,$00,$00
    .byte $0F,$AA,$AA,$AA,$AA,$AA,$AA,$0F,$56,$55,$55,$55,$55,$95,$0F,$9A
    .byte $99,$99,$99,$99,$A9,$0F,$58,$55,$55,$55,$55,$25,$0F,$5A,$59,$59
    .byte $96,$65,$A5,$0F,$66,$66,$66,$65,$9A,$99,$0F,$98,$65,$65,$65,$59
    .byte $26,$0F,$58,$96,$95,$59,$96,$25,$0F,$60,$96,$95,$59,$96,$09,$0F
    .byte $60,$96,$95,$59,$66,$09,$0F,$60,$59,$96,$99,$65,$09,$0F,$80,$59
    .byte $96,$99,$65,$02,$0F,$80,$59,$56,$96,$65,$02,$0F,$00,$AA,$AA,$AA
    .byte $AA,$00,$0F,$80,$55,$55,$55,$55,$02,$0F,$00,$AA,$AA,$AA,$AA,$00
    .byte $0F,$80,$55,$55,$55,$55,$02,$0F,$00,$AA,$AA,$AA,$AA,$00
sprite_2:
    .byte $18,$11,$07,$04,$04,$04,$04,$04,$05,$05,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$AA,$AA,$AA,$AA,$00,$0F,$00,$66,$66,$66,$66,$02,$0F,$80
    .byte $99,$99,$99,$99,$02,$0F,$80,$99,$99,$99,$99,$02,$0F,$80,$99,$99
    .byte $99,$99,$02,$0F,$80,$99,$99,$99,$99,$02,$0F,$00,$AA,$AA,$AA,$AA
    .byte $00,$0F,$80,$55,$55,$55,$55,$02,$0F,$60,$96,$65,$59,$96,$09,$0F
    .byte $98,$65,$65,$59,$59,$26,$0F,$98,$65,$65,$59,$59,$26,$0F,$98,$65
    .byte $65,$59,$59,$26,$0F,$A8,$AA,$AA,$AA,$AA,$2A,$0F,$56,$55,$55,$55
    .byte $55,$95,$0F,$56,$55,$55,$55,$55,$95,$0F,$56,$55,$55,$55,$55,$95
    .byte $0F,$AA,$AA,$AA,$AA,$AA,$AA
sprite_3:
    .byte $12,$18,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$A8,$AA,$00,$00,$0F,$00,$56,$95,$02,$00,$0F,$80,$65,$99
    .byte $02,$00,$0F,$80,$95,$A5,$09,$00,$0F,$80,$55,$95,$09,$00,$0F,$00
    .byte $56,$A6,$25,$00,$0F,$00,$58,$95,$26,$00,$0F,$A0,$AA,$AA,$09,$00
    .byte $0F,$58,$55,$95,$26,$00,$0F,$56,$65,$96,$26,$00,$0F,$5A,$55,$99
    .byte $09,$00,$0F,$96,$59,$95,$09,$00,$0F,$56,$55,$A6,$26,$00,$0F,$9A
    .byte $65,$95,$25,$00,$0F,$56,$55,$96,$95,$00,$0F,$56,$96,$A5,$99,$00
    .byte $0F,$66,$55,$95,$A5,$00,$0F,$68,$65,$96,$99,$00,$0F,$A0,$AA,$AA
    .byte $99,$00,$0F,$00,$00,$00,$96,$00,$0F,$00,$00,$00,$A6,$00,$0F,$00
    .byte $00,$00,$98,$00,$0F,$00,$00,$00,$98,$00,$0F,$00,$00,$00,$20,$00
sprite_4:
    .byte $12,$15,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$A0,$AA,$02,$00,$0F,$00,$68,$55,$09,$00,$0F,$00,$68,$66
    .byte $25,$00,$0F,$00,$A6,$55,$26,$00,$0F,$00,$66,$59,$09,$00,$0F,$80
    .byte $A6,$55,$02,$00,$0F,$80,$A5,$AA,$AA,$00,$0F,$80,$69,$59,$66,$02
    .byte $0F,$80,$69,$55,$55,$09,$0F,$00,$A6,$65,$59,$09,$0F,$00,$A6,$55
    .byte $66,$0A,$0F,$80,$65,$55,$55,$09,$0F,$80,$69,$99,$65,$09,$0F,$60
    .byte $A6,$55,$59,$0A,$0F,$A0,$65,$55,$55,$09,$0F,$60,$69,$59,$59,$0A
    .byte $0F,$A0,$65,$95,$55,$02,$0F,$60,$A6,$AA,$AA,$00,$0F,$60,$09,$00
    .byte $00,$00,$0F,$60,$09,$00,$00,$00,$0F,$80,$02,$00,$00,$00
sprite_5:
    .byte $2A,$47,$0C,$06,$07,$07,$07,$07,$07,$07,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$A0,$AA,$AA,$AA,$AA,$AA,$00,$00,$00,$0F,$00,$00,$60
    .byte $55,$99,$55,$59,$95,$00,$00,$00,$0F,$00,$00,$80,$55,$55,$55,$55
    .byte $25,$00,$00,$00,$0F,$00,$00,$80,$59,$56,$99,$55,$25,$00,$00,$00
    .byte $0F,$00,$00,$68,$55,$65,$55,$95,$95,$02,$00,$00,$0F,$00,$00,$96
    .byte $66,$55,$56,$59,$69,$29,$00,$00,$0F,$00,$80,$55,$56,$55,$55,$55
    .byte $59,$25,$00,$00,$0F,$00,$00,$58,$99,$96,$65,$65,$96,$95,$00,$00
    .byte $0F,$00,$60,$95,$59,$55,$59,$55,$56,$99,$00,$00,$0F,$00,$6A,$55
    .byte $65,$55,$59,$96,$95,$95,$00,$00,$0F,$80,$95,$59,$A5,$AA,$AA,$AA
    .byte $55,$A5,$02,$00,$0F,$60,$A5,$55,$5A,$55,$55,$55,$5A,$69,$09,$00
    .byte $0F,$60,$56,$96,$55,$55,$55,$55,$65,$66,$25,$00,$0F,$60,$55,$69
    .byte $55,$55,$55,$55,$95,$55,$26,$00,$0F,$80,$55,$59,$55,$55,$55,$55
    .byte $55,$66,$29,$00,$0F,$A0,$66,$56,$55,$55,$55,$55,$55,$55,$25,$00
    .byte $0F,$58,$59,$56,$55,$55,$55,$55,$55,$59,$9A,$00,$0F,$56,$A6,$55
    .byte $55,$55,$55,$55,$55,$A5,$55,$02,$0F,$66,$95,$55,$55,$55,$55,$55
    .byte $55,$65,$65,$02,$0F,$56,$55,$55,$55,$55,$55,$55,$55,$55,$56,$09
    .byte $0F,$96,$65,$55,$55,$55,$55,$55,$55,$95,$99,$09,$0F,$58,$65,$55
    .byte $55,$55,$55,$55,$55,$95,$55,$02,$0F,$A0,$6A,$55,$55,$55,$55,$55
    .byte $55,$95,$AA,$00,$0F,$58,$65,$55,$55,$55,$55,$55,$55,$95,$55,$02
    .byte $0F,$66,$66,$55,$55,$55,$55,$55,$55,$95,$59,$09,$0F,$56,$65,$55
    .byte $55,$55,$55,$55,$55,$95,$95,$09,$0F,$5A,$66,$55,$55,$55,$55,$55
    .byte $55,$95,$65,$09,$0F,$56,$65,$55,$55,$55,$55,$55,$55,$95,$59,$09
    .byte $0F,$96,$65,$55,$55,$55,$55,$55,$55,$95,$55,$09,$0F,$58,$65,$55
    .byte $55,$55,$55,$55,$55,$95,$55,$02,$0F,$A0,$6A,$55,$55,$55,$55,$55
    .byte $55,$95,$AA,$00,$0F,$58,$65,$55,$55,$55,$55,$55,$55,$95,$59,$02
    .byte $0F,$56,$6A,$55,$55,$55,$55,$55,$55,$95,$55,$09,$0F,$56,$65,$55
    .byte $55,$55,$55,$55,$55,$95,$95,$09,$0F,$66,$65,$55,$55,$55,$55,$55
    .byte $55,$95,$55,$09,$0F,$56,$66,$55,$55,$55,$55,$55,$55,$95,$99,$09
    .byte $0F,$56,$65,$55,$55,$55,$55,$55,$55,$95,$55,$09,$0F,$98,$65,$55
    .byte $55,$55,$55,$55,$55,$95,$55,$02,$0F,$A0,$6A,$55,$55,$55,$55,$55
    .byte $55,$95,$AA,$00,$0F,$58,$65,$55,$55,$55,$55,$55,$55,$95,$55,$02
    .byte $0F,$96,$65,$55,$55,$55,$55,$55,$55,$95,$65,$09,$0F,$56,$66,$55
    .byte $55,$55,$55,$55,$55,$95,$56,$09,$0F,$56,$65,$55,$55,$55,$55,$55
    .byte $55,$95,$55,$09,$0F,$66,$69,$55,$55,$55,$55,$55,$55,$95,$66,$09
    .byte $0F,$56,$65,$55,$55,$55,$55,$55,$55,$95,$55,$09,$0F,$68,$65,$55
    .byte $55,$55,$55,$55,$55,$95,$55,$02,$0F,$A0,$6A,$55,$55,$55,$55,$55
    .byte $55,$95,$AA,$00,$0F,$58,$65,$55,$55,$55,$55,$55,$55,$95,$55,$02
    .byte $0F,$56,$66,$55,$55,$55,$55,$55,$55,$95,$59,$09,$0F,$56,$65,$55
    .byte $55,$55,$55,$55,$55,$95,$55,$0A,$0F,$66,$66,$55,$55,$55,$55,$55
    .byte $55,$95,$55,$09,$0F,$56,$65,$55,$55,$55,$55,$55,$55,$95,$66,$09
    .byte $0F,$56,$65,$55,$55,$55,$55,$55,$55,$95,$55,$09,$0F,$58,$66,$55
    .byte $55,$55,$55,$55,$55,$95,$55,$02,$0F,$A0,$6A,$55,$55,$55,$55,$55
    .byte $55,$95,$AA,$00,$0F,$58,$66,$55,$55,$55,$55,$55,$55,$95,$55,$02
    .byte $0F,$56,$65,$55,$55,$55,$55,$55,$55,$95,$55,$09,$0F,$66,$65,$55
    .byte $55,$55,$55,$55,$55,$95,$59,$09,$0F,$56,$66,$55,$55,$55,$55,$55
    .byte $55,$95,$55,$0A,$0F,$56,$65,$55,$55,$55,$55,$55,$55,$95,$65,$09
    .byte $0F,$66,$65,$55,$55,$55,$55,$55,$55,$95,$55,$09,$0F,$58,$65,$55
    .byte $55,$55,$55,$55,$55,$95,$59,$02,$0F,$A0,$6A,$55,$55,$55,$55,$55
    .byte $55,$95,$AA,$00,$0F,$58,$65,$55,$55,$55,$55,$55,$55,$95,$55,$02
    .byte $0F,$66,$66,$55,$55,$55,$55,$55,$55,$95,$55,$09,$0F,$56,$65,$55
    .byte $55,$55,$55,$55,$55,$95,$69,$09,$0F,$96,$65,$55,$55,$55,$55,$55
    .byte $55,$95,$55,$0A,$0F,$5A,$65,$55,$55,$55,$55,$55,$55,$95,$56,$09
    .byte $0F,$56,$69,$55,$55,$55,$55,$55,$55,$95,$65,$09,$0F,$58,$65,$55
    .byte $55,$55,$55,$55,$55,$95,$55,$02,$0F,$A0,$6A,$55,$55,$55,$55,$55
    .byte $55,$95,$AA,$00
sprite_6:
    .byte $1E,$5A,$09,$05,$05,$05,$05,$05,$05,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$A8,$00,$00,$00,$0F,$00,$00,$00,$80,$96,$00
    .byte $00,$00,$0F,$00,$00,$00,$60,$95,$02,$00,$00,$0F,$00,$00,$00,$58
    .byte $65,$09,$00,$00,$0F,$00,$00,$00,$96,$65,$25,$00,$00,$0F,$00,$00
    .byte $80,$55,$65,$96,$00,$00,$0F,$00,$00,$60,$59,$59,$65,$02,$00,$0F
    .byte $00,$00,$58,$95,$99,$65,$02,$00,$0F,$00,$00,$58,$56,$59,$99,$09
    .byte $00,$0F,$00,$00,$60,$99,$56,$59,$09,$00,$0F,$00,$00,$6A,$65,$A9
    .byte $66,$0A,$00,$0F,$00,$80,$95,$59,$55,$96,$26,$00,$0F,$00,$00,$58
    .byte $56,$55,$59,$26,$00,$0F,$00,$60,$55,$55,$55,$A5,$25,$00,$0F,$00
    .byte $60,$A6,$55,$55,$65,$26,$00,$0F,$00,$98,$55,$55,$55,$65,$99,$00
    .byte $0F,$00,$56,$66,$55,$55,$95,$99,$00,$0F,$00,$9A,$59,$55,$55,$95
    .byte $96,$00,$0F,$00,$56,$59,$55,$55,$95,$A6,$00,$0F,$00,$60,$59,$55
    .byte $55,$95,$96,$00,$0F,$80,$56,$59,$55,$55,$95,$25,$00,$0F,$80,$69
    .byte $56,$55,$55,$95,$25,$00,$0F,$80,$95,$56,$55,$55,$95,$99,$00,$0F
    .byte $80,$65,$56,$55,$55,$95,$99,$00,$0F,$80,$59,$56,$55,$55,$95,$96
    .byte $00,$0F,$00,$00,$56,$55,$55,$95,$9A,$00,$0F,$80,$9A,$55,$55,$55
    .byte $95,$95,$00,$0F,$80,$A5,$55,$55,$55,$95,$26,$00,$0F,$80,$95,$55
    .byte $55,$55,$95,$25,$00,$0F,$80,$99,$55,$55,$55,$95,$99,$00,$0F,$80
    .byte $95,$55,$55,$55,$95,$99,$00,$0F,$00,$96,$55,$55,$55,$95,$96,$00
    .byte $0F,$80,$69,$55,$55,$55,$95,$96,$00,$0F,$80,$65,$55,$55,$55,$95
    .byte $99,$00,$0F,$80,$66,$55,$55,$55,$95,$25,$00,$0F,$80,$65,$55,$55
    .byte $55,$95,$25,$00,$0F,$80,$65,$55,$55,$55,$95,$99,$00,$0F,$60,$69
    .byte $55,$55,$55,$95,$99,$00,$0F,$60,$69,$55,$55,$55,$95,$A6,$00,$0F
    .byte $60,$66,$55,$55,$55,$95,$96,$00,$0F,$00,$66,$55,$55,$55,$95,$99
    .byte $00,$0F,$80,$65,$55,$55,$55,$95,$25,$00,$0F,$80,$65,$55,$55,$55
    .byte $95,$25,$00,$0F,$60,$69,$55,$55,$55,$95,$99,$00,$0F,$60,$65,$55
    .byte $55,$55,$95,$99,$00,$0F,$A0,$69,$55,$55,$55,$95,$96,$09,$0F,$60
    .byte $69,$55,$55,$55,$95,$96,$09,$0F,$60,$66,$55,$55,$55,$95,$59,$02
    .byte $0F,$60,$66,$55,$55,$55,$95,$95,$00,$0F,$80,$65,$55,$55,$55,$95
    .byte $96,$00,$0F,$80,$69,$55,$55,$55,$95,$25,$00,$0F,$60,$65,$55,$55
    .byte $55,$95,$25,$00,$0F,$60,$66,$55,$55,$55,$95,$09,$00,$0F,$60,$69
    .byte $55,$55,$55,$95,$09,$00,$0F,$60,$69,$55,$55,$55,$95,$02,$00,$0F
    .byte $60,$66,$55,$55,$55,$95,$00,$00,$0F,$60,$A6,$AA,$AA,$AA,$AA,$00
    .byte $00,$0F,$80,$25,$00,$00,$00,$00,$00,$00,$0F,$80,$29,$00,$00,$00
    .byte $00,$00,$00,$0F,$60,$25,$00,$00,$00,$00,$00,$00,$0F,$60,$26,$00
    .byte $00,$00,$00,$00,$00,$0F,$60,$29,$00,$00,$00,$00,$00,$00,$0F,$A0
    .byte $29,$00,$00,$00,$00,$00,$00,$0F,$60,$26,$00,$00,$00,$00,$00,$00
    .byte $0F,$60,$26,$00,$00,$00,$00,$00,$00,$0F,$80,$25,$00,$00,$00,$00
    .byte $00,$00,$0F,$80,$29,$00,$00,$00,$00,$00,$00,$0F,$60,$25,$00,$00
    .byte $00,$00,$00,$00,$0F,$60,$26,$00,$00,$00,$00,$00,$00,$0F,$60,$29
    .byte $00,$00,$00,$00,$00,$00,$0F,$60,$29,$00,$00,$00,$00,$00,$00,$0F
    .byte $60,$26,$00,$00,$00,$00,$00,$00,$0F,$60,$26,$00,$00,$00,$00,$00
    .byte $00,$0F,$80,$25,$00,$00,$00,$00,$00,$00,$0F,$80,$29,$00,$00,$00
    .byte $00,$00,$00,$0F,$60,$25,$00,$00,$00,$00,$00,$00,$0F,$60,$26,$00
    .byte $00,$00,$00,$00,$00,$0F,$60,$29,$00,$00,$00,$00,$00,$00,$0F,$A0
    .byte $29,$00,$00,$00,$00,$00,$00,$0F,$60,$26,$00,$00,$00,$00,$00,$00
    .byte $0F,$60,$26,$00,$00,$00,$00,$00,$00,$0F,$80,$25,$00,$00,$00,$00
    .byte $00,$00,$0F,$80,$29,$00,$00,$00,$00,$00,$00,$0F,$60,$25,$00,$00
    .byte $00,$00,$00,$00,$0F,$60,$26,$00,$00,$00,$00,$00,$00,$0F,$60,$09
    .byte $00,$00,$00,$00,$00,$00,$0F,$60,$09,$00,$00,$00,$00,$00,$00,$0F
    .byte $60,$02,$00,$00,$00,$00,$00,$00,$0F,$60,$02,$00,$00,$00,$00,$00
    .byte $00,$0F,$80,$00,$00,$00,$00,$00,$00,$00
sprite_7:
    .byte $1E,$5A,$09,$05,$05,$05,$05,$05,$05,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$80,$02,$00,$00,$00,$00,$0F,$00,$00,$80,$29,$00,$00
    .byte $00,$00,$0F,$00,$00,$80,$95,$00,$00,$00,$00,$0F,$00,$00,$00,$56
    .byte $02,$00,$00,$00,$0F,$00,$00,$A8,$66,$09,$00,$00,$00,$0F,$00,$00
    .byte $66,$56,$25,$00,$00,$00,$0F,$00,$80,$56,$59,$95,$00,$00,$00,$0F
    .byte $00,$60,$66,$99,$55,$02,$00,$00,$0F,$00,$98,$99,$59,$99,$09,$00
    .byte $00,$0F,$00,$5A,$59,$59,$55,$09,$00,$00,$0F,$00,$A6,$65,$69,$56
    .byte $02,$00,$00,$0F,$80,$65,$A6,$96,$65,$02,$00,$00,$0F,$80,$66,$69
    .byte $55,$56,$0A,$00,$00,$0F,$80,$95,$56,$55,$99,$25,$00,$00,$0F,$80
    .byte $59,$56,$55,$95,$95,$00,$00,$0F,$60,$96,$55,$55,$65,$99,$00,$00
    .byte $0F,$60,$96,$55,$55,$25,$00,$00,$00,$0F,$A0,$99,$55,$55,$95,$99
    .byte $00,$00,$0F,$60,$69,$55,$55,$55,$66,$02,$00,$0F,$60,$66,$55,$55
    .byte $55,$5A,$09,$00,$0F,$80,$65,$55,$55,$55,$96,$09,$00,$0F,$80,$65
    .byte $55,$55,$55,$56,$09,$00,$0F,$60,$66,$55,$55,$55,$69,$09,$00,$0F
    .byte $60,$66,$55,$55,$55,$59,$29,$00,$0F,$A0,$69,$55,$55,$55,$A9,$26
    .byte $00,$0F,$60,$69,$55,$55,$55,$59,$25,$00,$0F,$60,$66,$55,$55,$55
    .byte $59,$26,$00,$0F,$80,$65,$55,$55,$55,$65,$95,$00,$0F,$80,$69,$55
    .byte $55,$55,$A5,$95,$00,$0F,$60,$66,$55,$55,$55,$65,$0A,$00,$0F,$60
    .byte $66,$55,$55,$55,$65,$25,$00,$0F,$A0,$69,$55,$55,$55,$65,$26,$00
    .byte $0F,$60,$6A,$55,$55,$55,$65,$95,$00,$0F,$60,$65,$55,$55,$55,$65
    .byte $96,$00,$0F,$80,$65,$55,$55,$55,$95,$99,$00,$0F,$80,$65,$55,$55
    .byte $55,$95,$96,$00,$0F,$60,$66,$55,$55,$55,$95,$96,$00,$0F,$60,$66
    .byte $55,$55,$55,$95,$99,$00,$0F,$60,$69,$55,$55,$55,$95,$99,$00,$0F
    .byte $A0,$69,$55,$55,$55,$95,$25,$00,$0F,$60,$66,$55,$55,$55,$95,$25
    .byte $00,$0F,$80,$65,$55,$55,$55,$95,$95,$00,$0F,$80,$65,$55,$55,$55
    .byte $95,$99,$00,$0F,$60,$66,$55,$55,$55,$95,$96,$00,$0F,$60,$66,$55
    .byte $55,$55,$95,$A6,$00,$0F,$66,$69,$55,$55,$55,$95,$99,$00,$0F,$66
    .byte $69,$55,$55,$55,$95,$99,$00,$0F,$98,$66,$55,$55,$55,$95,$25,$00
    .byte $0F,$98,$65,$55,$55,$55,$95,$26,$00,$0F,$60,$65,$55,$55,$55,$95
    .byte $95,$00,$0F,$80,$65,$55,$55,$55,$95,$95,$00,$0F,$80,$69,$55,$55
    .byte $55,$95,$9A,$00,$0F,$00,$66,$55,$55,$55,$95,$96,$00,$0F,$00,$66
    .byte $55,$55,$55,$95,$99,$00,$0F,$00,$68,$55,$55,$55,$95,$99,$00,$0F
    .byte $00,$60,$55,$55,$55,$95,$25,$00,$0F,$00,$A0,$AA,$AA,$AA,$AA,$25
    .byte $00,$0F,$00,$00,$00,$00,$00,$80,$96,$00,$0F,$00,$00,$00,$00,$00
    .byte $80,$99,$00,$0F,$00,$00,$00,$00,$00,$80,$96,$00,$0F,$00,$00,$00
    .byte $00,$00,$80,$96,$00,$0F,$00,$00,$00,$00,$00,$80,$99,$00,$0F,$00
    .byte $00,$00,$00,$00,$80,$99,$00,$0F,$00,$00,$00,$00,$00,$80,$25,$00
    .byte $0F,$00,$00,$00,$00,$00,$80,$25,$00,$0F,$00,$00,$00,$00,$00,$80
    .byte $99,$00,$0F,$00,$00,$00,$00,$00,$80,$95,$00,$0F,$00,$00,$00,$00
    .byte $00,$80,$96,$00,$0F,$00,$00,$00,$00,$00,$80,$A6,$00,$0F,$00,$00
    .byte $00,$00,$00,$80,$99,$00,$0F,$00,$00,$00,$00,$00,$80,$99,$00,$0F
    .byte $00,$00,$00,$00,$00,$80,$25,$00,$0F,$00,$00,$00,$00,$00,$80,$25
    .byte $00,$0F,$00,$00,$00,$00,$00,$80,$95,$00,$0F,$00,$00,$00,$00,$00
    .byte $80,$A5,$00,$0F,$00,$00,$00,$00,$00,$80,$9A,$00,$0F,$00,$00,$00
    .byte $00,$00,$80,$96,$00,$0F,$00,$00,$00,$00,$00,$80,$99,$00,$0F,$00
    .byte $00,$00,$00,$00,$80,$99,$00,$0F,$00,$00,$00,$00,$00,$80,$25,$00
    .byte $0F,$00,$00,$00,$00,$00,$80,$25,$00,$0F,$00,$00,$00,$00,$00,$80
    .byte $95,$00,$0F,$00,$00,$00,$00,$00,$80,$99,$00,$0F,$00,$00,$00,$00
    .byte $00,$80,$95,$00,$0F,$00,$00,$00,$00,$00,$80,$96,$00,$0F,$00,$00
    .byte $00,$00,$00,$80,$A5,$00,$0F,$00,$00,$00,$00,$00,$00,$96,$00,$0F
    .byte $00,$00,$00,$00,$00,$00,$98,$00,$0F,$00,$00,$00,$00,$00,$00,$98
    .byte $00,$0F,$00,$00,$00,$00,$00,$00,$20,$00
sprite_8:
    .byte $1E,$3D,$09,$05,$05,$05,$05,$05,$05,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$AA,$AA,$AA,$0A,$00,$00,$0F,$00,$A0,$AA,$AA,$AA,$AA
    .byte $00,$00,$0F,$00,$A8,$AA,$A6,$6A,$AA,$02,$00,$0F,$00,$6A,$AA,$AA
    .byte $AA,$AA,$0A,$00,$0F,$80,$AA,$AA,$A6,$AA,$AA,$2A,$00,$0F,$A0,$AA
    .byte $AA,$AA,$6A,$AA,$26,$00,$0F,$A0,$6A,$AA,$AA,$AA,$AA,$AA,$00,$0F
    .byte $A8,$AA,$AA,$A6,$6A,$AA,$A6,$02,$0F,$A8,$AA,$AA,$AA,$AA,$AA,$AA
    .byte $02,$0F,$A8,$AA,$AA,$A6,$6A,$AA,$A6,$02,$0F,$A6,$AA,$AA,$AA,$AA
    .byte $AA,$AA,$0A,$0F,$AA,$6A,$A9,$5A,$AA,$96,$AA,$0A,$0F,$AA,$6A,$A9
    .byte $5A,$AA,$96,$AA,$0A,$0F,$AA,$AA,$AA,$A6,$AA,$AA,$A6,$0A,$0F,$AA
    .byte $6A,$AA,$AA,$AA,$AA,$AA,$02,$0F,$A6,$AA,$AA,$AA,$AA,$A9,$AA,$0A
    .byte $0F,$AA,$AA,$AA,$A6,$AA,$AA,$A6,$02,$0F,$AA,$AA,$AA,$AA,$AA,$A9
    .byte $AA,$0A,$0F,$AA,$6A,$AA,$AA,$AA,$AA,$AA,$0A,$0F,$AA,$AA,$AA,$A6
    .byte $AA,$AA,$A6,$02,$0F,$AA,$AA,$AA,$AA,$AA,$A9,$AA,$0A,$0F,$AA,$6A
    .byte $AA,$A6,$AA,$A9,$AA,$0A,$0F,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$09,$0F
    .byte $A6,$AA,$AA,$A6,$AA,$9A,$99,$09,$0F,$AA,$6A,$AA,$AA,$6A,$55,$95
    .byte $09,$0F,$A6,$AA,$AA,$A6,$6A,$55,$95,$09,$0F,$AA,$AA,$AA,$AA,$AA
    .byte $9A,$99,$09,$0F,$AA,$6A,$AA,$AA,$AA,$A9,$AA,$09,$0F,$AA,$AA,$AA
    .byte $AA,$AA,$AA,$AA,$0A,$0F,$A6,$A6,$6A,$A5,$A5,$A9,$A6,$0A,$0F,$AA
    .byte $95,$AA,$A9,$A9,$AA,$AA,$0A,$0F,$AA,$95,$AA,$99,$69,$AA,$A6,$02
    .byte $0F,$AA,$A6,$6A,$55,$A5,$AA,$AA,$0A,$0F,$AA,$66,$AA,$56,$6A,$AA
    .byte $A6,$02,$0F,$A6,$A6,$AA,$9A,$AA,$AA,$AA,$0A,$0F,$AA,$6A,$AA,$A6
    .byte $AA,$AA,$AA,$0A,$0F,$A6,$AA,$AA,$AA,$AA,$AA,$A6,$02,$0F,$AA,$AA
    .byte $AA,$AA,$6A,$AA,$AA,$0A,$0F,$AA,$AA,$AA,$A6,$AA,$AA,$9A,$02,$0F
    .byte $A6,$6A,$AA,$A6,$6A,$AA,$AA,$0A,$0F,$AA,$AA,$AA,$AA,$AA,$AA,$AA
    .byte $0A,$0F,$AA,$AA,$AA,$AA,$6A,$AA,$9A,$02,$0F,$AA,$6A,$AA,$AA,$AA
    .byte $AA,$AA,$0A,$0F,$A6,$AA,$AA,$A6,$AA,$A9,$A6,$0A,$0F,$AA,$6A,$AA
    .byte $AA,$AA,$AA,$AA,$0A,$0F,$AA,$AA,$AA,$A6,$AA,$AA,$A6,$02,$0F,$A6
    .byte $6A,$AA,$AA,$AA,$A9,$AA,$09,$0F,$AA,$AA,$AA,$9A,$AA,$9A,$99,$09
    .byte $0F,$A6,$AA,$AA,$AA,$6A,$55,$95,$09,$0F,$AA,$AA,$AA,$9A,$6A,$55
    .byte $95,$09,$0F,$AA,$6A,$AA,$AA,$AA,$9A,$99,$09,$0F,$AA,$AA,$AA,$AA
    .byte $AA,$A9,$AA,$09,$0F,$AA,$AA,$AA,$9A,$AA,$AA,$A6,$02,$0F,$A6,$6A
    .byte $AA,$AA,$AA,$A9,$AA,$0A,$0F,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$02,$0F
    .byte $9A,$6A,$A9,$5A,$AA,$96,$A6,$0A,$0F,$AA,$6A,$A9,$5A,$AA,$96,$AA
    .byte $0A,$0F,$9A,$AA,$AA,$9A,$AA,$A9,$A6,$02,$0F,$AA,$6A,$AA,$AA,$AA
    .byte $AA,$AA,$0A,$0F,$A6,$AA,$AA,$AA,$AA,$A9,$A6,$02,$0F,$A6,$6A,$AA
    .byte $9A,$AA,$A9,$A6,$02
sprite_9:
    .byte $1E,$3C,$09,$05,$05,$05,$05,$05,$05,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$00
    .byte $00,$00,$0F,$00,$00,$80,$55,$25,$00,$00,$00,$0F,$00,$00,$80,$55
    .byte $25,$00,$00,$00,$0F,$00,$00,$60,$56,$99,$00,$00,$00,$0F,$00,$00
    .byte $60,$56,$99,$00,$00,$00,$0F,$00,$56,$65,$56,$99,$55,$09,$00,$0F
    .byte $00,$56,$65,$56,$99,$55,$09,$00,$0F,$80,$59,$65,$56,$99,$55,$26
    .byte $00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59,$65,$56,$99
    .byte $55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59,$65
    .byte $56,$99,$55,$26,$00,$0F,$80,$5A,$A5,$56,$A9,$55,$2A,$00,$0F,$80
    .byte $A9,$6A,$AA,$9A,$AA,$A6,$0A,$0F,$80,$55,$55,$55,$55,$55,$55,$09
    .byte $0F,$80,$A9,$6A,$AA,$9A,$AA,$A6,$0A,$0F,$80,$5A,$A5,$56,$A9,$55
    .byte $2A,$00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59,$65,$56
    .byte $99,$55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59
    .byte $65,$56,$99,$55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F
    .byte $80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26
    .byte $00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59,$65,$56,$99
    .byte $55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59,$65
    .byte $56,$99,$55,$26,$00,$0F,$80,$AA,$6A,$56,$99,$55,$26,$00,$0F,$80
    .byte $55,$65,$56,$99,$55,$26,$00,$0F,$80,$95,$65,$56,$99,$55,$26,$00
    .byte $0F,$A0,$65,$65,$56,$99,$55,$26,$00,$0F,$80,$95,$65,$56,$99,$55
    .byte $26,$00,$0F,$80,$95,$65,$56,$99,$55,$26,$00,$0F,$80,$AA,$6A,$56
    .byte $99,$55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59
    .byte $65,$56,$99,$55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F
    .byte $80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26
    .byte $00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59,$65,$56,$99
    .byte $55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59,$65
    .byte $56,$99,$55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$80
    .byte $5A,$A5,$56,$A9,$55,$2A,$00,$0F,$80,$A9,$6A,$AA,$9A,$AA,$A6,$0A
    .byte $0F,$80,$55,$55,$55,$55,$55,$55,$09,$0F,$80,$A9,$6A,$AA,$9A,$AA
    .byte $A6,$0A,$0F,$80,$5A,$A5,$56,$A9,$55,$2A,$00,$0F,$80,$59,$65,$56
    .byte $99,$55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59
    .byte $65,$56,$99,$55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F
    .byte $80,$59,$65,$56,$99,$55,$26,$00,$0F,$80,$59,$65,$56,$99,$55,$26
    .byte $00,$0F,$80,$59,$65,$56,$99,$55,$26,$00,$0F,$00,$56,$95,$55,$65
    .byte $55,$09,$00,$0F,$00,$56,$95,$55,$65,$55,$09,$00
sprite_10:
    .byte $12,$4A,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$28,$00,$00,$0F,$00,$00,$AA,$0A,$00,$0F,$00,$80,$AA
    .byte $0A,$00,$0F,$00,$A0,$A9,$AA,$00,$0F,$00,$A0,$AA,$AA,$0A,$0F,$00
    .byte $A8,$A9,$9A,$02,$0F,$00,$A8,$AA,$AA,$02,$0F,$00,$AA,$A9,$A6,$0A
    .byte $0F,$00,$AA,$AA,$A5,$0A,$0F,$80,$AA,$AA,$A9,$0A,$0F,$80,$AA,$AA
    .byte $9A,$09,$0F,$80,$AA,$A5,$AA,$09,$0F,$A0,$AA,$A5,$6A,$09,$0F,$A0
    .byte $AA,$A9,$6A,$09,$0F,$A0,$AA,$AA,$56,$09,$0F,$A0,$AA,$A9,$56,$09
    .byte $0F,$A0,$A6,$AA,$96,$09,$0F,$A0,$A5,$6A,$95,$09,$0F,$A0,$A9,$6A
    .byte $A5,$0A,$0F,$A8,$AA,$59,$96,$0A,$0F,$A8,$AA,$5A,$AA,$0A,$0F,$A8
    .byte $AA,$6A,$9A,$0A,$0F,$98,$AA,$A9,$AA,$0A,$0F,$AA,$AA,$AA,$AA,$0A
    .byte $0F,$9A,$AA,$A9,$AA,$0A,$0F,$AA,$AA,$AA,$9A,$0A,$0F,$AA,$AA,$A9
    .byte $AA,$0A,$0F,$AA,$AA,$6A,$9A,$0A,$0F,$9A,$AA,$99,$AA,$0A,$0F,$AA
    .byte $AA,$9A,$AA,$0A,$0F,$AA,$9A,$9A,$9A,$0A,$0F,$AA,$6A,$9A,$AA,$09
    .byte $0F,$9A,$6A,$A6,$9A,$09,$0F,$AA,$6A,$A5,$6A,$09,$0F,$AA,$AA,$A9
    .byte $6A,$09,$0F,$9A,$AA,$AA,$56,$09,$0F,$AA,$AA,$A9,$56,$09,$0F,$AA
    .byte $AA,$AA,$56,$09,$0F,$9A,$A5,$6A,$A5,$09,$0F,$6A,$A5,$69,$A5,$0A
    .byte $0F,$AA,$A9,$5A,$A6,$0A,$0F,$AA,$A9,$59,$9A,$0A,$0F,$AA,$A9,$6A
    .byte $AA,$0A,$0F,$AA,$A9,$AA,$6A,$0A,$0F,$9A,$AA,$A9,$5A,$0A,$0F,$AA
    .byte $AA,$AA,$AA,$0A,$0F,$9A,$AA,$A9,$9A,$0A,$0F,$9A,$AA,$AA,$AA,$0A
    .byte $0F,$AA,$AA,$A9,$9A,$02,$0F,$AA,$AA,$AA,$AA,$02,$0F,$9A,$AA,$9A
    .byte $9A,$00,$0F,$AA,$AA,$96,$2A,$00,$0F,$9A,$AA,$A6,$2A,$00,$0F,$AA
    .byte $AA,$A9,$0A,$00,$0F,$AA,$AA,$AA,$02,$00,$0F,$9A,$AA,$AA,$02,$00
    .byte $0F,$AA,$AA,$A9,$00,$00,$0F,$9A,$AA,$AA,$00,$00,$0F,$AA,$AA,$2A
    .byte $00,$00,$0F,$AA,$A9,$09,$00,$00,$0F,$6A,$A9,$0A,$00,$00,$0F,$5A
    .byte $AA,$02,$00,$00,$0F,$AA,$AA,$00,$00,$00,$0F,$AA,$AA,$00,$00,$00
    .byte $0F,$9A,$2A,$00,$00,$00,$0F,$AA,$2A,$00,$00,$00,$0F,$AA,$0A,$00
    .byte $00,$00,$0F,$9A,$02,$00,$00,$00,$0F,$AA,$02,$00,$00,$00,$0F,$9A
    .byte $00,$00,$00,$00,$0F,$AA,$00,$00,$00,$00,$0F,$2A,$00,$00,$00,$00
    .byte $0F,$2A,$00,$00,$00,$00,$0F,$0A,$00,$00,$00,$00
sprite_11:
    .byte $12,$3E,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$08,$00,$0F,$00,$00,$56,$09,$00,$0F,$00,$00,$56
    .byte $26,$00,$0F,$00,$80,$59,$26,$00,$0F,$00,$80,$59,$26,$00,$0F,$00
    .byte $80,$59,$66,$09,$0F,$00,$80,$59,$6A,$0A,$0F,$00,$80,$59,$A6,$09
    .byte $0F,$00,$80,$99,$56,$09,$0F,$00,$80,$99,$55,$0A,$0F,$00,$80,$6A
    .byte $A5,$09,$0F,$00,$80,$65,$2A,$00,$0F,$80,$A5,$95,$26,$00,$0F,$80
    .byte $65,$95,$26,$00,$0F,$60,$5A,$69,$26,$00,$0F,$60,$96,$5A,$26,$00
    .byte $0F,$A0,$95,$59,$26,$00,$0F,$60,$A5,$59,$26,$00,$0F,$00,$98,$59
    .byte $26,$00,$0F,$60,$96,$59,$26,$00,$0F,$A0,$96,$59,$26,$00,$0F,$60
    .byte $96,$59,$26,$00,$0F,$60,$96,$59,$26,$00,$0F,$60,$96,$59,$26,$00
    .byte $0F,$60,$96,$59,$26,$00,$0F,$60,$96,$59,$26,$00,$0F,$60,$96,$59
    .byte $26,$00,$0F,$60,$96,$59,$26,$00,$0F,$60,$96,$59,$66,$0A,$0F,$60
    .byte $96,$59,$66,$0A,$0F,$60,$96,$59,$A6,$09,$0F,$60,$96,$59,$AA,$09
    .byte $0F,$60,$96,$59,$56,$09,$0F,$60,$96,$59,$56,$09,$0F,$60,$96,$99
    .byte $55,$0A,$0F,$60,$9A,$99,$A9,$00,$0F,$60,$9A,$69,$25,$00,$0F,$A0
    .byte $9A,$69,$25,$00,$0F,$A0,$9A,$9A,$26,$00,$0F,$A0,$9A,$95,$26,$00
    .byte $0F,$68,$AA,$65,$26,$00,$0F,$68,$5A,$65,$26,$00,$0F,$A8,$5A,$6A
    .byte $26,$00,$0F,$A0,$96,$59,$09,$00,$0F,$A0,$A5,$59,$09,$00,$0F,$60
    .byte $A5,$09,$00,$00,$0F,$60,$9A,$09,$00,$00,$0F,$60,$9A,$09,$00,$00
    .byte $0F,$A0,$96,$09,$00,$00,$0F,$60,$96,$09,$00,$00,$0F,$60,$96,$09
    .byte $00,$00,$0F,$60,$56,$02,$00,$00,$0F,$60,$56,$02,$00,$00,$0F,$60
    .byte $02,$00,$00,$00,$0F,$60,$02,$00,$00,$00,$0F,$60,$02,$00,$00,$00
    .byte $0F,$60,$02,$00,$00,$00,$0F,$60,$02,$00,$00,$00,$0F,$60,$02,$00
    .byte $00,$00,$0F,$60,$02,$00,$00,$00,$0F,$80,$00,$00,$00,$00,$0F,$80
    .byte $00,$00,$00,$00
sprite_12:
    .byte $12,$4A,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$AA,$0A,$00,$00,$0F,$80,$AA,$29,$00,$00,$0F,$A0,$AA,$A9
    .byte $00,$00,$0F,$A0,$AA,$AA,$00,$00,$0F,$68,$AA,$AA,$02,$00,$0F,$A8
    .byte $AA,$AA,$02,$00,$0F,$68,$AA,$A9,$0A,$00,$0F,$AA,$AA,$AA,$2A,$00
    .byte $0F,$AA,$AA,$A9,$2A,$00,$0F,$6A,$AA,$AA,$2A,$00,$0F,$AA,$AA,$A9
    .byte $26,$00,$0F,$6A,$AA,$AA,$AA,$00,$0F,$AA,$A6,$A9,$A6,$00,$0F,$AA
    .byte $96,$9A,$AA,$00,$0F,$AA,$9A,$5A,$AA,$00,$0F,$AA,$AA,$6A,$A6,$00
    .byte $0F,$6A,$AA,$A9,$AA,$02,$0F,$AA,$AA,$AA,$A6,$02,$0F,$6A,$AA,$AA
    .byte $9A,$02,$0F,$AA,$AA,$A9,$5A,$02,$0F,$AA,$AA,$6A,$66,$02,$0F,$6A
    .byte $AA,$6A,$AA,$02,$0F,$AA,$AA,$69,$A5,$02,$0F,$5A,$AA,$AA,$A5,$0A
    .byte $0F,$5A,$AA,$A9,$A5,$09,$0F,$6A,$AA,$AA,$96,$09,$0F,$6A,$AA,$AA
    .byte $56,$09,$0F,$6A,$9A,$A9,$56,$09,$0F,$AA,$6A,$AA,$6A,$09,$0F,$AA
    .byte $6A,$AA,$6A,$09,$0F,$6A,$6A,$A9,$A6,$09,$0F,$AA,$6A,$6A,$AA,$09
    .byte $0F,$6A,$6A,$99,$A6,$09,$0F,$AA,$6A,$95,$AA,$0A,$0F,$AA,$AA,$A5
    .byte $AA,$0A,$0F,$6A,$AA,$A9,$A6,$0A,$0F,$AA,$AA,$AA,$AA,$0A,$0F,$6A
    .byte $AA,$A9,$A6,$0A,$0F,$AA,$AA,$AA,$AA,$0A,$0F,$AA,$AA,$AA,$AA,$0A
    .byte $0F,$AA,$AA,$A9,$A6,$0A,$0F,$6A,$AA,$AA,$AA,$0A,$0F,$9A,$AA,$A9
    .byte $A6,$0A,$0F,$5A,$AA,$AA,$AA,$0A,$0F,$6A,$AA,$AA,$AA,$0A,$0F,$AA
    .byte $AA,$AA,$A6,$0A,$0F,$68,$AA,$A9,$AA,$0A,$0F,$A0,$9A,$AA,$A6,$0A
    .byte $0F,$60,$96,$A9,$AA,$0A,$0F,$80,$A6,$AA,$AA,$0A,$0F,$00,$AA,$AA
    .byte $A6,$0A,$0F,$00,$AA,$A9,$AA,$0A,$0F,$00,$A8,$6A,$A6,$0A,$0F,$00
    .byte $A8,$6A,$AA,$0A,$0F,$00,$A0,$65,$A5,$0A,$0F,$00,$A0,$A6,$A5,$0A
    .byte $0F,$00,$80,$95,$A5,$0A,$0F,$00,$80,$99,$96,$09,$0F,$00,$00,$A8
    .byte $96,$09,$0F,$00,$00,$AA,$56,$09,$0F,$00,$00,$A8,$6A,$09,$0F,$00
    .byte $00,$A0,$69,$09,$0F,$00,$00,$A0,$A5,$09,$0F,$00,$00,$80,$A6,$09
    .byte $0F,$00,$00,$80,$AA,$09,$0F,$00,$00,$00,$A6,$0A,$0F,$00,$00,$00
    .byte $A0,$0A,$0F,$00,$00,$00,$A8,$0A,$0F,$00,$00,$00,$A0,$0A,$0F,$00
    .byte $00,$00,$A0,$0A,$0F,$00,$00,$00,$80,$0A,$0F,$00,$00,$00,$00,$0A
    .byte $0F,$00,$00,$00,$00,$0A,$0F,$00,$00,$00,$00,$08
sprite_13:
    .byte $12,$41,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$02,$00,$00,$0F,$00,$00,$02,$00,$00,$0F,$80,$95,$09
    .byte $00,$00,$0F,$80,$95,$09,$00,$00,$0F,$60,$96,$09,$00,$00,$0F,$60
    .byte $96,$09,$00,$00,$0F,$60,$96,$09,$00,$00,$0F,$6A,$96,$09,$00,$00
    .byte $0F,$80,$96,$09,$00,$00,$0F,$56,$99,$09,$00,$00,$0F,$5A,$99,$09
    .byte $00,$00,$0F,$A0,$99,$59,$09,$00,$0F,$60,$95,$59,$09,$00,$0F,$A0
    .byte $A6,$5A,$26,$00,$0F,$60,$5A,$59,$26,$00,$0F,$60,$A6,$69,$26,$00
    .byte $0F,$60,$96,$65,$26,$00,$0F,$60,$96,$96,$26,$00,$0F,$60,$96,$99
    .byte $2A,$00,$0F,$60,$96,$69,$25,$00,$0F,$60,$96,$99,$26,$00,$0F,$60
    .byte $96,$99,$2A,$00,$0F,$60,$96,$59,$26,$00,$0F,$60,$96,$59,$26,$00
    .byte $0F,$60,$96,$59,$26,$00,$0F,$60,$96,$59,$26,$00,$0F,$60,$96,$59
    .byte $26,$00,$0F,$60,$96,$59,$26,$00,$0F,$60,$96,$59,$26,$00,$0F,$60
    .byte $96,$59,$26,$00,$0F,$60,$96,$59,$26,$00,$0F,$6A,$96,$59,$26,$00
    .byte $0F,$A6,$96,$59,$26,$00,$0F,$56,$96,$59,$26,$00,$0F,$5A,$9A,$A9
    .byte $26,$00,$0F,$60,$9A,$A9,$26,$00,$0F,$A0,$A5,$6A,$2A,$00,$0F,$60
    .byte $66,$69,$2A,$00,$0F,$60,$5A,$69,$25,$00,$0F,$60,$5A,$69,$A5,$0A
    .byte $0F,$60,$A6,$A5,$6A,$09,$0F,$60,$96,$96,$AA,$0A,$0F,$80,$95,$99
    .byte $26,$00,$0F,$80,$95,$69,$25,$00,$0F,$00,$80,$69,$25,$00,$0F,$00
    .byte $80,$99,$2A,$00,$0F,$00,$80,$59,$26,$00,$0F,$00,$80,$59,$26,$00
    .byte $0F,$00,$80,$59,$26,$00,$0F,$00,$80,$59,$26,$00,$0F,$00,$00,$56
    .byte $26,$00,$0F,$00,$00,$56,$26,$00,$0F,$00,$00,$00,$26,$00,$0F,$00
    .byte $00,$00,$26,$00,$0F,$00,$00,$00,$26,$00,$0F,$00,$00,$00,$26,$00
    .byte $0F,$00,$00,$00,$26,$00,$0F,$00,$00,$00,$26,$00,$0F,$00,$00,$00
    .byte $26,$00,$0F,$00,$00,$00,$26,$00,$0F,$00,$00,$00,$26,$00,$0F,$00
    .byte $00,$00,$26,$00,$0F,$00,$00,$00,$26,$00,$0F,$00,$00,$00,$08,$00
    .byte $0F,$00,$00,$00,$08,$00
sprite_14:
    .byte $0C,$12,$04,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0F,$5A,$95,$2A,$0F,$66,$95,$AA,$0F,$96,$A5,$A9,$0F,$5A,$A6,$9A
    .byte $0F,$66,$A9,$A9,$0F,$80,$99,$2A,$0F,$00,$56,$0A,$0F,$00,$58,$09
    .byte $0F,$00,$68,$02,$0F,$00,$AA,$00,$0F,$00,$2A,$00,$0F,$80,$0A,$00
    .byte $0F,$80,$0A,$00,$0F,$98,$02,$00,$0F,$26,$00,$00,$0F,$96,$00,$00
    .byte $0F,$28,$00,$00,$0F,$00,$00,$00
sprite_15:
    .byte $0C,$11,$04,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0F,$A8,$56,$A5,$0F,$AA,$55,$99,$0F,$9A,$5A,$96,$0F,$AA,$9A,$A5
    .byte $0F,$68,$6A,$99,$0F,$A8,$66,$02,$0F,$A0,$95,$00,$0F,$60,$25,$00
    .byte $0F,$80,$29,$00,$0F,$00,$AA,$00,$0F,$00,$A8,$00,$0F,$00,$A0,$02
    .byte $0F,$00,$A0,$02,$0F,$00,$80,$26,$0F,$00,$00,$98,$0F,$00,$00,$96
    .byte $0F,$00,$00,$28
sprite_16:
    .byte $1E,$0F,$09,$05,$05,$05,$05,$05,$05,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$80,$AA,$AA,$02,$00,$00,$0F,$00,$00,$6A,$66,$66,$AA
    .byte $00,$00,$0F,$00,$A0,$99,$99,$99,$59,$0A,$00,$0F,$00,$68,$66,$66
    .byte $66,$66,$26,$00,$0F,$00,$9A,$99,$99,$99,$99,$99,$00,$0F,$00,$66
    .byte $A6,$AA,$AA,$66,$A6,$00,$0F,$80,$99,$6A,$55,$55,$A9,$99,$02,$0F
    .byte $80,$A6,$55,$55,$55,$55,$6A,$02,$0F,$80,$59,$55,$55,$55,$55,$A5
    .byte $02,$0F,$00,$56,$55,$55,$55,$55,$95,$00,$0F,$00,$56,$55,$55,$55
    .byte $55,$95,$00,$0F,$00,$58,$55,$55,$55,$55,$25,$00,$0F,$00,$A0,$55
    .byte $55,$55,$55,$0A,$00,$0F,$00,$00,$6A,$55,$55,$A9,$00,$00,$0F,$00
    .byte $00,$80,$AA,$AA,$02,$00,$00
sprite_17:
    .byte $12,$37,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$08,$0F,$00,$00,$00,$00,$08,$0F,$00,$00,$00
    .byte $00,$0A,$0F,$00,$00,$00,$00,$0A,$0F,$00,$00,$00,$80,$0A,$0F,$00
    .byte $00,$00,$80,$0A,$0F,$00,$00,$00,$A0,$0A,$0F,$00,$00,$00,$A0,$0A
    .byte $0F,$00,$00,$00,$A8,$0A,$0F,$00,$00,$00,$A8,$0A,$0F,$00,$00,$00
    .byte $AA,$0A,$0F,$00,$00,$00,$AA,$0A,$0F,$00,$00,$80,$AA,$0A,$0F,$00
    .byte $00,$80,$9A,$0A,$0F,$00,$00,$A0,$9A,$0A,$0F,$00,$00,$A0,$96,$0A
    .byte $0F,$00,$00,$A8,$96,$0A,$0F,$00,$00,$A8,$95,$0A,$0F,$00,$00,$AA
    .byte $95,$0A,$0F,$00,$00,$6A,$95,$0A,$0F,$00,$80,$6A,$95,$0A,$0F,$00
    .byte $80,$6A,$95,$0A,$0F,$00,$A0,$6A,$95,$0A,$0F,$00,$A0,$6A,$95,$0A
    .byte $0F,$00,$A8,$6A,$95,$02,$0F,$00,$A8,$6A,$95,$02,$0F,$00,$AA,$6A
    .byte $95,$02,$0F,$00,$6A,$6A,$55,$02,$0F,$80,$6A,$6A,$55,$02,$0F,$80
    .byte $5A,$2A,$00,$00,$0F,$A0,$5A,$2A,$00,$00,$0F,$A0,$56,$2A,$00,$00
    .byte $0F,$A8,$56,$2A,$00,$00,$0F,$A8,$55,$2A,$00,$00,$0F,$AA,$55,$2A
    .byte $00,$00,$0F,$6A,$55,$2A,$00,$00,$0F,$6A,$55,$2A,$00,$00,$0F,$6A
    .byte $55,$2A,$00,$00,$0F,$6A,$55,$0A,$00,$00,$0F,$6A,$55,$0A,$00,$00
    .byte $0F,$6A,$55,$09,$00,$00,$0F,$6A,$55,$09,$00,$00,$0F,$6A,$55,$09
    .byte $00,$00,$0F,$2A,$00,$00,$00,$00,$0F,$2A,$00,$00,$00,$00,$0F,$2A
    .byte $00,$00,$00,$00,$0F,$2A,$00,$00,$00,$00,$0F,$2A,$00,$00,$00,$00
    .byte $0F,$2A,$00,$00,$00,$00,$0F,$0A,$00,$00,$00,$00,$0F,$0A,$00,$00
    .byte $00,$00,$0F,$08,$00,$00,$00,$00,$0F,$08,$00,$00,$00,$00,$0F,$08
    .byte $00,$00,$00,$00,$0F,$08,$00,$00,$00,$00
sprite_18:
    .byte $12,$37,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$02,$00,$00,$00,$00,$0F,$02,$00,$00,$00,$00,$0F,$0A,$00,$00
    .byte $00,$00,$0F,$0A,$00,$00,$00,$00,$0F,$2A,$00,$00,$00,$00,$0F,$2A
    .byte $00,$00,$00,$00,$0F,$AA,$00,$00,$00,$00,$0F,$AA,$00,$00,$00,$00
    .byte $0F,$AA,$02,$00,$00,$00,$0F,$AA,$02,$00,$00,$00,$0F,$AA,$0A,$00
    .byte $00,$00,$0F,$AA,$0A,$00,$00,$00,$0F,$AA,$2A,$00,$00,$00,$0F,$6A
    .byte $2A,$00,$00,$00,$0F,$6A,$AA,$00,$00,$00,$0F,$6A,$A9,$00,$00,$00
    .byte $0F,$6A,$A9,$02,$00,$00,$0F,$6A,$A5,$02,$00,$00,$0F,$6A,$A5,$0A
    .byte $00,$00,$0F,$6A,$95,$0A,$00,$00,$0F,$6A,$95,$2A,$00,$00,$0F,$6A
    .byte $95,$2A,$00,$00,$0F,$6A,$95,$AA,$00,$00,$0F,$6A,$95,$AA,$00,$00
    .byte $0F,$68,$95,$AA,$02,$00,$0F,$68,$95,$AA,$02,$00,$0F,$68,$95,$AA
    .byte $0A,$00,$0F,$58,$95,$9A,$0A,$00,$0F,$58,$95,$9A,$2A,$00,$0F,$00
    .byte $80,$5A,$2A,$00,$0F,$00,$80,$5A,$AA,$00,$0F,$00,$80,$5A,$A9,$00
    .byte $0F,$00,$80,$5A,$A9,$02,$0F,$00,$80,$5A,$A5,$02,$0F,$00,$80,$5A
    .byte $A5,$0A,$0F,$00,$80,$5A,$95,$0A,$0F,$00,$80,$5A,$95,$0A,$0F,$00
    .byte $80,$5A,$95,$0A,$0F,$00,$00,$5A,$95,$0A,$0F,$00,$00,$56,$95,$0A
    .byte $0F,$00,$00,$56,$95,$0A,$0F,$00,$00,$56,$95,$0A,$0F,$00,$00,$00
    .byte $80,$0A,$0F,$00,$00,$00,$80,$0A,$0F,$00,$00,$00,$80,$0A,$0F,$00
    .byte $00,$00,$80,$0A,$0F,$00,$00,$00,$80,$0A,$0F,$00,$00,$00,$80,$0A
    .byte $0F,$00,$00,$00,$80,$0A,$0F,$00,$00,$00,$80,$0A,$0F,$00,$00,$00
    .byte $00,$0A,$0F,$00,$00,$00,$00,$0A,$0F,$00,$00,$00,$00,$02,$0F,$00
    .byte $00,$00,$00,$02,$0F,$00,$00,$00,$00,$02
sprite_20:
    .byte $2A,$32,$0C,$06,$07,$07,$07,$07,$07,$07,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$AA,$AA,$AA,$AA,$0A,$00,$00,$00,$0F,$00,$00,$80
    .byte $55,$55,$55,$55,$25,$00,$00,$00,$0F,$00,$00,$60,$55,$55,$55,$55
    .byte $95,$00,$00,$00,$0F,$00,$00,$58,$55,$55,$55,$55,$55,$02,$00,$00
    .byte $0F,$00,$00,$56,$55,$55,$55,$55,$55,$09,$00,$00,$0F,$00,$80,$55
    .byte $55,$55,$55,$55,$55,$25,$00,$00,$0F,$00,$80,$55,$55,$55,$55,$55
    .byte $55,$25,$00,$00,$0F,$00,$60,$55,$55,$55,$55,$55,$55,$95,$00,$00
    .byte $0F,$00,$60,$55,$55,$AA,$AA,$56,$55,$95,$00,$00,$0F,$00,$58,$55
    .byte $55,$56,$55,$56,$55,$55,$02,$00,$0F,$00,$58,$55,$55,$96,$59,$56
    .byte $55,$55,$02,$00,$0F,$00,$56,$55,$55,$66,$66,$56,$55,$55,$09,$00
    .byte $0F,$00,$56,$55,$55,$56,$56,$56,$55,$55,$09,$00,$0F,$80,$55,$55
    .byte $55,$96,$59,$56,$55,$55,$25,$00,$0F,$60,$AA,$AA,$AA,$96,$5A,$AA
    .byte $AA,$AA,$9A,$00,$0F,$58,$55,$55,$55,$56,$56,$56,$55,$55,$55,$02
    .byte $0F,$AA,$AA,$AA,$AA,$99,$99,$A9,$AA,$AA,$AA,$0A,$0F,$56,$55,$55
    .byte $55,$65,$65,$55,$55,$55,$55,$09,$0F,$56,$55,$55,$55,$95,$59,$55
    .byte $55,$55,$55,$09,$0F,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$0A
    .byte $0F,$60,$55,$56,$56,$55,$55,$55,$59,$59,$95,$00,$0F,$60,$55,$56
    .byte $56,$55,$55,$55,$59,$59,$95,$00,$0F,$60,$66,$56,$56,$55,$55,$55
    .byte $59,$99,$99,$00,$0F,$60,$66,$56,$56,$55,$55,$55,$59,$99,$99,$00
    .byte $0F,$60,$66,$56,$56,$55,$55,$55,$59,$99,$99,$00,$0F,$60,$66,$56
    .byte $56,$55,$55,$55,$59,$99,$99,$00,$0F,$60,$66,$56,$56,$55,$55,$55
    .byte $59,$99,$99,$00,$0F,$60,$66,$56,$56,$55,$55,$55,$59,$99,$99,$00
    .byte $0F,$60,$66,$56,$56,$55,$55,$55,$59,$99,$99,$00,$0F,$60,$66,$56
    .byte $56,$55,$55,$55,$59,$99,$99,$00,$0F,$60,$55,$56,$56,$55,$55,$55
    .byte $59,$59,$95,$00,$0F,$60,$59,$56,$56,$55,$55,$55,$59,$59,$96,$00
    .byte $0F,$60,$66,$56,$56,$55,$55,$55,$59,$99,$99,$00,$0F,$60,$59,$56
    .byte $56,$55,$55,$55,$59,$59,$96,$00,$0F,$60,$55,$56,$56,$55,$55,$55
    .byte $59,$59,$95,$00,$0F,$60,$66,$56,$56,$55,$55,$55,$59,$99,$99,$00
    .byte $0F,$60,$66,$56,$56,$55,$55,$55,$59,$99,$99,$00,$0F,$60,$66,$56
    .byte $56,$55,$55,$55,$59,$99,$99,$00,$0F,$60,$66,$56,$56,$55,$55,$55
    .byte $59,$99,$99,$00,$0F,$60,$66,$56,$56,$55,$55,$55,$59,$99,$99,$00
    .byte $0F,$60,$66,$56,$AA,$AA,$AA,$AA,$5A,$99,$99,$00,$0F,$60,$66,$56
    .byte $55,$55,$55,$55,$65,$99,$99,$00,$0F,$60,$66,$96,$55,$55,$55,$55
    .byte $65,$59,$95,$00,$0F,$68,$55,$66,$55,$55,$55,$55,$95,$59,$95,$02
    .byte $0F,$68,$55,$66,$55,$55,$55,$55,$95,$59,$95,$02,$0F,$66,$55,$5A
    .byte $55,$55,$55,$55,$55,$5A,$95,$09,$0F,$A6,$AA,$5A,$55,$55,$55,$55
    .byte $55,$AA,$AA,$09,$0F,$56,$55,$55,$55,$55,$55,$55,$55,$55,$55,$09
    .byte $0F,$56,$55,$55,$55,$55,$55,$55,$55,$55,$55,$09,$0F,$AA,$AA,$AA
    .byte $AA,$AA,$AA,$AA,$AA,$AA,$AA,$0A
sprite_21:
    .byte $12,$1A,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$AA,$AA,$AA,$AA,$02,$0F,$56,$55,$55,$55,$02,$0F,$A6,$AA,$AA
    .byte $6A,$02,$0F,$A6,$9A,$9A,$6A,$02,$0F,$A6,$56,$56,$6A,$02,$0F,$A6
    .byte $56,$56,$6A,$02,$0F,$66,$A6,$69,$66,$02,$0F,$66,$6A,$99,$66,$02
    .byte $0F,$66,$55,$55,$65,$02,$0F,$66,$55,$55,$65,$02,$0F,$66,$65,$65
    .byte $65,$02,$0F,$66,$65,$65,$65,$02,$0F,$66,$65,$65,$65,$02,$0F,$66
    .byte $65,$65,$65,$02,$0F,$A6,$65,$65,$69,$02,$0F,$96,$69,$A5,$59,$02
    .byte $0F,$98,$6A,$A5,$9A,$00,$0F,$58,$66,$65,$96,$00,$0F,$60,$9A,$99
    .byte $26,$00,$0F,$60,$99,$99,$25,$00,$0F,$80,$A5,$69,$09,$00,$0F,$00
    .byte $96,$5A,$02,$00,$0F,$00,$58,$96,$00,$00,$0F,$00,$60,$25,$00,$00
    .byte $0F,$00,$80,$09,$00,$00,$0F,$00,$00,$02,$00,$00
sprite_22:
    .byte $12,$18,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$AA,$56,$55,$A9,$0A,$0F,$6A,$99,$99,$99,$0A,$0F,$A6,$AA,$AA
    .byte $AA,$09,$0F,$A6,$66,$66,$A6,$09,$0F,$6A,$55,$55,$95,$0A,$0F,$A0
    .byte $55,$55,$A5,$02,$0F,$68,$95,$56,$A5,$00,$0F,$A0,$95,$65,$95,$02
    .byte $0F,$68,$65,$55,$A5,$00,$0F,$A0,$95,$99,$95,$02,$0F,$68,$65,$65
    .byte $A5,$00,$0F,$A0,$65,$56,$95,$02,$0F,$68,$95,$69,$A5,$00,$0F,$A0
    .byte $59,$95,$95,$02,$0F,$68,$95,$99,$A6,$00,$0F,$A0,$99,$56,$99,$02
    .byte $0F,$68,$55,$55,$A5,$00,$0F,$A0,$59,$66,$96,$02,$0F,$68,$95,$55
    .byte $A5,$00,$0F,$A6,$55,$99,$95,$0A,$0F,$AA,$99,$99,$A9,$09,$0F,$A6
    .byte $AA,$AA,$AA,$09,$0F,$6A,$9A,$99,$99,$0A,$0F,$AA,$56,$55,$A9,$0A
sprite_23:
    .byte $12,$29,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$0F,$00,$A8,$A5,$96,$0A,$0F,$00,$98,$59
    .byte $99,$09,$0F,$00,$98,$56,$A5,$09,$0F,$00,$58,$55,$55,$09,$0F,$00
    .byte $58,$55,$55,$09,$0F,$00,$58,$AA,$6A,$09,$0F,$00,$58,$AA,$6A,$09
    .byte $0F,$00,$58,$AA,$6A,$09,$0F,$00,$58,$AA,$6A,$09,$0F,$00,$58,$AA
    .byte $6A,$09,$0F,$00,$58,$AA,$6A,$09,$0F,$00,$58,$AA,$6A,$09,$0F,$00
    .byte $58,$AA,$6A,$09,$0F,$00,$56,$AA,$6A,$09,$0F,$80,$55,$AA,$6A,$09
    .byte $0F,$60,$55,$AA,$5A,$09,$0F,$58,$59,$AA,$5A,$09,$0F,$56,$56,$AA
    .byte $56,$02,$0F,$96,$59,$AA,$95,$09,$0F,$96,$59,$AA,$65,$09,$0F,$68
    .byte $59,$96,$65,$09,$0F,$60,$59,$55,$5A,$09,$0F,$60,$59,$55,$65,$0A
    .byte $0F,$60,$96,$AA,$A6,$09,$0F,$A0,$A5,$AA,$66,$02,$0F,$60,$A9,$AA
    .byte $99,$00,$0F,$58,$56,$A5,$26,$00,$0F,$58,$55,$55,$9A,$00,$0F,$A8
    .byte $AA,$AA,$0A,$00,$0F,$00,$96,$96,$65,$02,$0F,$80,$65,$59,$66,$02
    .byte $0F,$60,$99,$65,$99,$09,$0F,$60,$96,$95,$99,$09,$0F,$98,$A9,$95
    .byte $99,$0A,$0F,$98,$55,$55,$26,$00,$0F,$66,$55,$55,$26,$00,$0F,$66
    .byte $55,$55,$99,$00,$0F,$66,$55,$55,$99,$00,$0F,$66,$55,$55,$99,$00
    .byte $0F,$6A,$55,$55,$A9,$00
sprite_24:
    .byte $12,$2A,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$0F,$00,$A8,$AA,$AA,$02,$0F,$00,$56,$55
    .byte $95,$02,$0F,$80,$55,$55,$65,$02,$0F,$60,$55,$55,$59,$02,$0F,$58
    .byte $55,$55,$96,$00,$0F,$A8,$AA,$AA,$26,$00,$0F,$58,$55,$55,$2A,$00
    .byte $0F,$A8,$AA,$AA,$0A,$00,$0F,$80,$66,$99,$09,$00,$0F,$00,$9A,$66
    .byte $02,$00,$0F,$00,$A6,$59,$02,$00,$0F,$00,$A8,$AA,$00,$00,$0F,$00
    .byte $58,$95,$00,$00,$0F,$00,$A8,$AA,$00,$00,$0F,$00,$98,$99,$00,$00
    .byte $0F,$00,$98,$99,$00,$00,$0F,$00,$98,$99,$00,$00,$0F,$00,$98,$99
    .byte $00,$00,$0F,$00,$98,$99,$00,$00,$0F,$00,$98,$99,$00,$00,$0F,$00
    .byte $98,$99,$00,$00,$0F,$00,$98,$99,$00,$00,$0F,$00,$98,$99,$00,$00
    .byte $0F,$00,$98,$99,$00,$00,$0F,$00,$98,$99,$00,$00,$0F,$00,$98,$99
    .byte $00,$00,$0F,$00,$98,$99,$00,$00,$0F,$00,$98,$99,$00,$00,$0F,$00
    .byte $A8,$AA,$00,$00,$0F,$00,$56,$55,$02,$00,$0F,$00,$56,$55,$02,$00
    .byte $0F,$00,$A8,$AA,$00,$00,$0F,$00,$56,$55,$2A,$00,$0F,$00,$66,$66
    .byte $96,$00,$0F,$00,$56,$55,$A6,$00,$0F,$80,$A9,$AA,$99,$00,$0F,$60
    .byte $55,$55,$95,$00,$0F,$A0,$AA,$AA,$25,$00,$0F,$60,$55,$95,$09,$00
    .byte $0F,$60,$55,$95,$02,$00,$0F,$A0,$AA,$AA,$00,$00
sprite_25:
    .byte $2A,$24,$0C,$06,$07,$07,$07,$07,$07,$07,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$0F,$AA,$AA,$AA
    .byte $AA,$AA,$AA,$AA,$AA,$00,$00,$00,$0F,$AA,$AA,$AA,$AA,$AA,$AA,$AA
    .byte $AA,$02,$00,$00,$0F,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$02,$00,$00
    .byte $0F,$A8,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$0A,$00,$00,$0F,$A6,$AA,$AA
    .byte $AA,$56,$55,$A9,$AA,$2A,$00,$00,$0F,$98,$56,$55,$55,$AA,$AA,$5A
    .byte $A5,$AA,$00,$00,$0F,$98,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$00,$00
    .byte $0F,$68,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$02,$00,$0F,$68,$AA,$AA
    .byte $6A,$55,$AA,$AA,$AA,$AA,$02,$00,$0F,$A8,$A9,$AA,$AA,$AA,$AA,$AA
    .byte $AA,$AA,$0A,$00,$0F,$A0,$A6,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$0A,$00
    .byte $0F,$A0,$9A,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$2A,$00,$0F,$A0,$9A,$AA
    .byte $AA,$AA,$AA,$AA,$AA,$AA,$AA,$00,$0F,$A0,$6A,$AA,$AA,$AA,$AA,$AA
    .byte $AA,$AA,$AA,$00,$0F,$A8,$AA,$55,$55,$55,$55,$55,$55,$55,$95,$00
    .byte $0F,$A8,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$00,$0F,$A8,$A9,$66
    .byte $55,$55,$55,$55,$55,$6A,$02,$00,$0F,$A8,$A5,$66,$55,$55,$55,$55
    .byte $55,$69,$02,$00,$0F,$A8,$A5,$A5,$AA,$AA,$AA,$AA,$AA,$69,$02,$00
    .byte $0F,$A8,$A6,$A9,$AA,$AA,$AA,$AA,$AA,$99,$00,$00,$0F,$A8,$A6,$A9
    .byte $AA,$AA,$AA,$AA,$AA,$99,$00,$00,$0F,$A8,$AA,$A9,$AA,$AA,$AA,$AA
    .byte $AA,$99,$00,$00,$0F,$A8,$A9,$5A,$55,$55,$55,$55,$55,$99,$00,$00
    .byte $0F,$A0,$A9,$66,$55,$55,$55,$55,$A5,$6A,$02,$00,$0F,$A0,$A5,$66
    .byte $55,$55,$55,$55,$95,$6A,$02,$00,$0F,$00,$A0,$66,$55,$55,$55,$55
    .byte $95,$6A,$02,$00,$0F,$00,$A0,$66,$55,$55,$55,$55,$55,$6A,$02,$00
    .byte $0F,$00,$A0,$66,$55,$55,$55,$55,$55,$6A,$02,$00,$0F,$00,$A0,$66
    .byte $55,$55,$55,$55,$55,$6A,$02,$00,$0F,$00,$A0,$66,$55,$55,$55,$55
    .byte $55,$6A,$02,$00,$0F,$00,$A0,$66,$55,$55,$55,$55,$55,$6A,$02,$00
    .byte $0F,$00,$80,$66,$55,$55,$55,$55,$55,$6A,$02,$00,$0F,$00,$80,$66
    .byte $55,$55,$55,$55,$55,$69,$02,$00,$0F,$00,$80,$66,$55,$55,$55,$55
    .byte $55,$69,$02,$00,$0F,$00,$00,$6A,$55,$55,$55,$55,$55,$A5,$02,$00
sprite_26:
    .byte $1E,$1E,$09,$05,$05,$05,$05,$05,$05,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$00,$00,$00,$0F,$00,$00,$A0,$0A,$00,$00
    .byte $00,$00,$0F,$00,$00,$A8,$2A,$00,$00,$00,$00,$0F,$00,$00,$AA,$AA
    .byte $00,$00,$00,$00,$0F,$00,$00,$AA,$AA,$02,$00,$00,$00,$0F,$00,$80
    .byte $AA,$AA,$0A,$00,$00,$00,$0F,$00,$80,$AA,$AA,$2A,$00,$00,$00,$0F
    .byte $00,$A0,$AA,$AA,$AA,$00,$00,$00,$0F,$00,$A0,$AA,$AA,$95,$00,$00
    .byte $00,$0F,$00,$60,$A9,$6A,$AA,$02,$00,$00,$0F,$00,$A0,$A9,$9A,$AA
    .byte $0A,$00,$00,$0F,$00,$A0,$A9,$9A,$AA,$0A,$00,$00,$0F,$00,$A0,$95
    .byte $A6,$AA,$2A,$00,$00,$0F,$00,$A0,$9A,$A6,$AA,$2A,$00,$00,$0F,$00
    .byte $A0,$5A,$A9,$AA,$AA,$00,$00,$0F,$00,$A0,$9A,$A9,$AA,$AA,$00,$00
    .byte $0F,$00,$A0,$A9,$56,$55,$95,$00,$00,$0F,$00,$A0,$A5,$A9,$AA,$AA
    .byte $00,$00,$0F,$00,$A0,$A6,$A9,$AA,$AA,$00,$00,$0F,$00,$A0,$A6,$69
    .byte $AA,$A6,$00,$00,$0F,$00,$A0,$AA,$A9,$A9,$A9,$00,$00,$0F,$00,$A0
    .byte $AA,$A9,$A9,$A9,$00,$00,$0F,$00,$A0,$AA,$A9,$56,$AA,$00,$00,$0F
    .byte $00,$00,$AA,$A9,$9A,$AA,$00,$00,$0F,$00,$00,$AA,$A9,$AA,$AA,$00
    .byte $00,$0F,$00,$00,$A8,$A9,$AA,$AA,$00,$00,$0F,$00,$00,$A0,$A9,$AA
    .byte $AA,$00,$00,$0F,$00,$00,$A0,$A9,$AA,$AA,$00,$00,$0F,$00,$00,$80
    .byte $A9,$AA,$AA,$00,$00,$0F,$00,$00,$00,$AA,$AA,$AA,$00,$00
sprite_27:
    .byte $24,$28,$0A,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$00,$00,$00,$00,$0F,$00,$00,$00,$00,$28
    .byte $00,$00,$00,$00,$0F,$00,$00,$00,$00,$98,$02,$00,$00,$00,$0F,$00
    .byte $00,$00,$00,$58,$0A,$00,$00,$00,$0F,$00,$00,$00,$00,$58,$2A,$00
    .byte $00,$00,$0F,$00,$00,$00,$00,$58,$29,$00,$00,$00,$0F,$00,$00,$00
    .byte $00,$58,$A9,$00,$00,$00,$0F,$00,$00,$00,$00,$58,$A5,$02,$00,$00
    .byte $0F,$00,$00,$00,$00,$58,$A5,$02,$00,$00,$0F,$00,$00,$00,$00,$58
    .byte $A5,$0A,$00,$00,$0F,$00,$00,$00,$00,$58,$59,$29,$00,$00,$0F,$00
    .byte $00,$00,$00,$58,$99,$02,$00,$00,$0F,$00,$00,$00,$00,$58,$96,$2A
    .byte $00,$00,$0F,$00,$00,$00,$00,$58,$96,$AA,$00,$00,$0F,$00,$00,$00
    .byte $00,$98,$95,$AA,$00,$00,$0F,$00,$A0,$AA,$AA,$66,$95,$AA,$02,$00
    .byte $0F,$00,$80,$55,$55,$59,$95,$AA,$02,$00,$0F,$00,$A0,$55,$55,$65
    .byte $95,$AA,$02,$00,$0F,$00,$A0,$55,$55,$69,$95,$AA,$02,$00,$0F,$00
    .byte $A0,$56,$55,$99,$95,$AA,$02,$00,$0F,$00,$A0,$5A,$55,$59,$96,$AA
    .byte $00,$00,$0F,$00,$A0,$5A,$55,$59,$96,$AA,$00,$00,$0F,$00,$A0,$6A
    .byte $55,$59,$99,$AA,$00,$00,$0F,$00,$A0,$6A,$55,$59,$A5,$2A,$00,$00
    .byte $0F,$00,$A0,$AA,$55,$59,$A5,$0A,$00,$00,$0F,$00,$A0,$AA,$55,$59
    .byte $95,$02,$00,$00,$0F,$00,$A0,$A9,$56,$55,$95,$00,$00,$00,$0F,$00
    .byte $A0,$A5,$A9,$AA,$AA,$00,$00,$00,$0F,$00,$A0,$A6,$A9,$AA,$AA,$00
    .byte $00,$00,$0F,$00,$A0,$A6,$69,$AA,$A6,$00,$00,$00,$0F,$00,$A0,$AA
    .byte $A9,$A9,$A9,$00,$00,$00,$0F,$00,$A0,$AA,$A9,$A9,$A9,$00,$00,$00
    .byte $0F,$00,$A0,$AA,$A9,$56,$AA,$00,$00,$00,$0F,$00,$00,$AA,$A9,$9A
    .byte $AA,$00,$00,$00,$0F,$00,$00,$AA,$A9,$AA,$AA,$00,$00,$00,$0F,$00
    .byte $00,$A8,$A9,$AA,$AA,$00,$00,$00,$0F,$00,$00,$A0,$A9,$AA,$AA,$00
    .byte $00,$00,$0F,$00,$00,$A0,$A9,$AA,$AA,$00,$00,$00,$0F,$00,$00,$80
    .byte $A9,$AA,$AA,$00,$00,$00,$0F,$00,$00,$00,$AA,$AA,$AA,$00,$00,$00
sprite_28:
    .byte $36,$10,$0F,$08,$08,$08,$09,$09,$09,$09,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$0F
    .byte $00,$00,$00,$00,$80,$95,$65,$55,$A9,$2A,$00,$00,$00,$00,$0F,$00
    .byte $00,$00,$00,$60,$55,$96,$55,$AA,$AA,$00,$00,$00,$00,$0F,$00,$00
    .byte $00,$00,$60,$59,$96,$95,$AA,$AA,$00,$00,$00,$00,$0F,$00,$00,$00
    .byte $00,$58,$65,$59,$A6,$AA,$9A,$00,$00,$00,$00,$0F,$00,$00,$00,$00
    .byte $58,$65,$59,$A6,$65,$99,$00,$00,$00,$00,$0F,$00,$00,$68,$55,$65
    .byte $65,$96,$A5,$65,$A9,$00,$00,$00,$00,$0F,$00,$00,$A0,$AA,$66,$99
    .byte $96,$A5,$AA,$2A,$00,$00,$00,$00,$0F,$00,$00,$6A,$59,$95,$99,$66
    .byte $95,$9A,$5A,$A5,$02,$00,$00,$0F,$00,$80,$56,$5A,$99,$9A,$AA,$56
    .byte $9A,$9A,$AA,$00,$00,$00,$0F,$00,$80,$55,$5A,$5A,$55,$69,$56,$AA
    .byte $56,$A5,$02,$00,$00,$0F,$00,$60,$AA,$95,$56,$55,$95,$56,$66,$02
    .byte $00,$00,$00,$00,$0F,$00,$A0,$96,$AA,$55,$55,$55,$5A,$55,$A5,$00
    .byte $00,$00,$00,$0F,$00,$00,$00,$5A,$55,$55,$55,$69,$55,$95,$2A,$00
    .byte $00,$00,$0F,$00,$00,$00,$00,$00,$00,$00,$A8,$55,$55,$29,$00,$00
    .byte $00,$0F,$00,$00,$00,$00,$00,$00,$00,$98,$00,$00,$00,$00,$00,$00
sprite_29:
    .byte $3C,$0F,$10,$09,$09,$09,$09,$0A,$0A,$0A,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$00,$A8,$6A,$55,$A9,$AA,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$60,$9A,$AA,$55,$9A,$AA,$2A,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$98,$66,$A6,$96,$66,$66,$2A,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$A6,$AA,$AA,$A6,$AA,$AA,$9A,$0A,$00,$00
    .byte $0F,$00,$00,$00,$00,$80,$69,$66,$AA,$69,$96,$A9,$A6,$09,$00,$00
    .byte $0F,$00,$00,$00,$00,$60,$AA,$AA,$69,$AA,$AA,$AA,$69,$02,$00,$00
    .byte $0F,$00,$00,$00,$00,$98,$66,$AA,$9A,$66,$69,$6A,$9A,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$A6,$AA,$A6,$A6,$AA,$AA,$9A,$26,$00,$00,$00
    .byte $0F,$00,$00,$00,$80,$55,$55,$AA,$59,$55,$A9,$A6,$09,$00,$00,$00
    .byte $0F,$00,$00,$00,$60,$AA,$AA,$69,$AA,$AA,$96,$69,$02,$00,$00,$00
    .byte $0F,$00,$00,$00,$58,$55,$55,$96,$5A,$55,$69,$9A,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$A6,$AA,$AA,$9A,$AA,$AA,$AA,$25,$00,$00,$00,$00
    .byte $0F,$00,$00,$80,$55,$55,$55,$55,$55,$55,$55,$09,$00,$00,$00,$00
    .byte $0F,$00,$00,$A0,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$02,$00,$00,$00,$00
sprite_30:
    .byte $1E,$13,$09,$05,$05,$05,$05,$05,$05,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$00
    .byte $00,$00,$0F,$00,$00,$A8,$55,$AA,$00,$00,$00,$0F,$00,$00,$98,$56
    .byte $9A,$00,$00,$00,$0F,$00,$00,$AA,$9A,$AA,$02,$00,$00,$0F,$00,$00
    .byte $5A,$9A,$96,$02,$00,$00,$0F,$00,$00,$56,$9A,$56,$02,$00,$00,$0F
    .byte $00,$00,$80,$A9,$09,$00,$00,$00,$0F,$00,$00,$AA,$66,$AA,$02,$00
    .byte $00,$0F,$00,$00,$AA,$9A,$AA,$02,$00,$00,$0F,$00,$00,$66,$66,$66
    .byte $02,$00,$00,$0F,$00,$00,$6A,$9A,$A6,$02,$00,$00,$0F,$00,$00,$56
    .byte $AA,$56,$02,$00,$00,$0F,$00,$00,$5A,$A9,$95,$02,$00,$00,$0F,$00
    .byte $00,$5A,$99,$55,$02,$00,$00,$0F,$00,$00,$56,$99,$55,$02,$00,$00
    .byte $0F,$00,$00,$56,$AA,$56,$02,$00,$00,$0F,$00,$00,$80,$9A,$0A,$00
    .byte $00,$00,$0F,$00,$00,$A0,$99,$29,$00,$00,$00
sprite_31:
    .byte $1E,$16,$09,$05,$05,$05,$05,$05,$05,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$00,$00,$00,$0F,$00,$00,$00,$20,$00,$00
    .byte $00,$00,$0F,$00,$00,$00,$20,$00,$00,$00,$00,$0F,$00,$00,$00,$98
    .byte $00,$00,$00,$00,$0F,$00,$00,$00,$98,$00,$00,$00,$00,$0F,$00,$00
    .byte $00,$9A,$02,$00,$00,$00,$0F,$00,$00,$00,$66,$02,$00,$00,$00,$0F
    .byte $00,$00,$80,$66,$0A,$00,$00,$00,$0F,$00,$00,$80,$66,$0A,$00,$00
    .byte $00,$0F,$00,$00,$60,$55,$25,$00,$00,$00,$0F,$00,$00,$A0,$A9,$29
    .byte $00,$00,$00,$0F,$00,$00,$A0,$A9,$29,$00,$00,$00,$0F,$00,$00,$A0
    .byte $A9,$29,$00,$00,$00,$0F,$00,$00,$60,$55,$25,$00,$00,$00,$0F,$00
    .byte $00,$80,$66,$0A,$00,$00,$00,$0F,$00,$00,$80,$66,$0A,$00,$00,$00
    .byte $0F,$00,$00,$00,$66,$02,$00,$00,$00,$0F,$00,$00,$00,$9A,$02,$00
    .byte $00,$00,$0F,$00,$00,$00,$98,$00,$00,$00,$00,$0F,$00,$00,$00,$98
    .byte $00,$00,$00,$00,$0F,$00,$00,$00,$20,$00,$00,$00,$00,$0F,$00,$00
    .byte $00,$20,$00,$00,$00,$00
sprite_32:
    .byte $06,$07,$03,$01,$01,$02,$02,$02,$02,$02,$01,$00,$00,$00,$00,$00
    .byte $0F,$9A,$09,$0F,$A8,$02,$0F,$80,$00,$0F,$A8,$02,$0F,$A6,$09,$0F
    .byte $9A,$0A,$0F,$A8,$02
sprite_33:
    .byte $18,$09,$07,$04,$04,$04,$04,$04,$05,$05,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$20,$00,$00,$00,$0F,$00,$00,$98,$00,$00,$00,$0F,$00
    .byte $00,$A0,$00,$00,$00,$0F,$00,$00,$00,$02,$00,$00,$0F,$00,$00,$00
    .byte $08,$00,$00,$0F,$00,$00,$00,$20,$00,$00,$0F,$00,$00,$00,$80,$00
    .byte $00,$0F,$00,$00,$00,$60,$02,$00,$0F,$00,$00,$00,$80,$00,$00
sprite_34:
    .byte $12,$0F,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$0A,$00,$00,$0F,$00,$80,$29,$00,$00,$0F,$00,$80,$29
    .byte $00,$00,$0F,$00,$00,$0A,$00,$00,$0F,$00,$00,$0A,$00,$00,$0F,$00
    .byte $00,$0A,$00,$00,$0F,$00,$80,$2A,$00,$00,$0F,$00,$80,$29,$00,$00
    .byte $0F,$00,$80,$29,$00,$00,$0F,$00,$80,$29,$00,$00,$0F,$00,$A0,$A9
    .byte $00,$00,$0F,$00,$60,$AA,$00,$00,$0F,$00,$60,$AA,$00,$00,$0F,$00
    .byte $A0,$A5,$00,$00,$0F,$00,$80,$2A,$00,$00
sprite_35:
    .byte $18,$0E,$07,$04,$04,$04,$04,$04,$05,$05,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$2A,$00,$00,$00,$0F,$00,$60,$A9,$00,$00,$00,$0F,$00
    .byte $A0,$A9,$02,$00,$00,$0F,$00,$A0,$A6,$0A,$00,$00,$0F,$00,$A0,$AA
    .byte $2A,$00,$00,$0F,$00,$80,$AA,$A9,$00,$00,$0F,$00,$80,$AA,$AA,$02
    .byte $00,$0F,$00,$00,$AA,$AA,$02,$00,$0F,$00,$00,$A8,$5A,$0A,$00,$0F
    .byte $00,$00,$98,$56,$09,$00,$0F,$00,$00,$80,$96,$09,$00,$0F,$00,$00
    .byte $80,$66,$09,$00,$0F,$00,$00,$00,$66,$09,$00,$0F,$00,$00,$00,$80
    .byte $02,$00
sprite_38:
    .byte $12,$06,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$02,$00,$00,$0F,$00,$80,$0A,$00,$00,$0F,$00,$80,$0A
    .byte $00,$00,$0F,$00,$60,$25,$00,$00,$0F,$00,$60,$25,$00,$00,$0F,$00
    .byte $80,$0A,$00,$00
sprite_90:
    .byte $12,$11,$06,$03,$03,$03,$03,$04,$04,$04,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$80,$09,$00,$00,$0F,$00,$60,$26,$00,$00,$0F,$00,$60,$26
    .byte $00,$00,$0F,$00,$00,$02,$00,$00,$0F,$00,$00,$02,$00,$00,$0F,$00
    .byte $00,$02,$00,$00,$0F,$00,$00,$02,$00,$00,$0F,$00,$00,$02,$00,$00
    .byte $0F,$00,$00,$02,$00,$00,$0F,$00,$00,$02,$00,$00,$0F,$00,$00,$02
    .byte $00,$00,$0F,$00,$00,$02,$00,$00,$0F,$00,$00,$02,$00,$00,$0F,$00
    .byte $00,$02,$00,$00,$0F,$00,$00,$02,$00,$00,$0F,$00,$00,$02,$00,$00
    .byte $0F,$00,$00,$02,$00,$00
sprite_93:
    .byte $24,$0D,$0A,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$A0,$AA,$AA,$AA,$00,$00,$00,$00,$0F,$00,$60,$55,$55,$95
    .byte $02,$00,$00,$00,$0F,$00,$60,$AA,$69,$9A,$0A,$00,$00,$00,$0F,$00
    .byte $00,$A0,$A6,$69,$0A,$00,$00,$00,$0F,$00,$80,$A5,$AA,$AA,$0A,$00
    .byte $00,$00,$0F,$00,$80,$55,$99,$95,$00,$00,$00,$00,$0F,$00,$00,$A6
    .byte $AA,$AA,$AA,$00,$00,$00,$0F,$00,$00,$58,$6A,$9A,$A6,$00,$00,$00
    .byte $0F,$00,$00,$58,$A9,$69,$9A,$02,$00,$00,$0F,$00,$00,$00,$A8,$AA
    .byte $AA,$02,$00,$00,$0F,$00,$00,$60,$59,$55,$55,$02,$00,$00,$0F,$00
    .byte $00,$80,$56,$55,$55,$02,$00,$00,$0F,$00,$00,$00,$AA,$AA,$AA,$0A
    .byte $00,$00
sprite_112:
    .byte $2A,$45,$0C,$06,$07,$07,$07,$07,$07,$07,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$80,$AA,$02,$00,$00,$00,$0F,$00,$00,$00
    .byte $00,$00,$60,$95,$02,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$58,$65
    .byte $02,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$A8,$5A,$02,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$A8,$5A,$02,$00,$00,$00,$0F,$00,$00,$00
    .byte $00,$00,$A8,$5A,$02,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$A8,$5A
    .byte $02,$00,$00,$00,$0F,$00,$00,$00,$00,$A8,$AA,$5A,$AA,$2A,$00,$00
    .byte $0F,$00,$00,$00,$00,$56,$A9,$5A,$55,$29,$00,$00,$0F,$00,$00,$00
    .byte $80,$55,$A9,$5A,$55,$26,$00,$00,$0F,$00,$00,$00,$80,$AA,$AA,$AA
    .byte $AA,$25,$00,$00,$0F,$00,$00,$00,$80,$AA,$AA,$AA,$AA,$25,$00,$00
    .byte $0F,$00,$00,$00,$80,$AA,$AA,$AA,$AA,$09,$00,$00,$0F,$00,$00,$00
    .byte $80,$AA,$AA,$AA,$AA,$09,$00,$00,$0F,$00,$00,$00,$80,$AA,$AA,$AA
    .byte $AA,$02,$00,$00,$0F,$00,$00,$00,$00,$00,$A8,$5A,$02,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$A8,$5A,$02,$00,$00,$00,$0F,$00,$00,$00
    .byte $00,$00,$A8,$5A,$02,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$A8,$5A
    .byte $02,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$A8,$5A,$02,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$A8,$5A,$02,$00,$00,$00,$0F,$00,$00,$00
    .byte $00,$00,$A8,$5A,$02,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$A8,$5A
    .byte $02,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$A8,$5A,$02,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$A8,$5A,$02,$00,$00,$00,$0F,$00,$00,$00
    .byte $00,$00,$A8,$5A,$02,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$A8,$5A
    .byte $02,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$A8,$9A,$29,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$80,$A9,$9A,$A9,$02,$00,$00,$0F,$00,$00,$00
    .byte $00,$A8,$A9,$5A,$AA,$2A,$00,$00,$0F,$00,$00,$00,$80,$AA,$59,$69
    .byte $AA,$AA,$02,$00,$0F,$00,$00,$00,$A0,$AA,$65,$96,$AA,$AA,$0A,$00
    .byte $0F,$00,$00,$00,$A0,$AA,$9A,$AA,$AA,$AA,$0A,$00,$0F,$00,$00,$00
    .byte $A8,$AA,$9A,$AA,$AA,$AA,$26,$00,$0F,$00,$00,$00,$A8,$AA,$A6,$AA
    .byte $AA,$AA,$26,$00,$0F,$00,$00,$00,$AA,$AA,$A6,$AA,$AA,$AA,$25,$00
    .byte $0F,$00,$00,$00,$AA,$AA,$A9,$AA,$AA,$AA,$25,$00,$0F,$00,$00,$80
    .byte $AA,$AA,$A9,$AA,$AA,$6A,$25,$00,$0F,$00,$00,$80,$AA,$6A,$AA,$AA
    .byte $AA,$6A,$25,$00,$0F,$00,$00,$A0,$AA,$6A,$AA,$AA,$AA,$5A,$25,$00
    .byte $0F,$00,$00,$A0,$AA,$9A,$AA,$AA,$AA,$5A,$25,$00,$0F,$00,$00,$A8
    .byte $AA,$9A,$AA,$AA,$AA,$56,$25,$00,$0F,$00,$00,$A8,$AA,$A6,$AA,$AA
    .byte $AA,$56,$09,$00,$0F,$00,$00,$AA,$AA,$A6,$AA,$AA,$AA,$55,$09,$00
    .byte $0F,$00,$00,$AA,$AA,$A9,$AA,$AA,$AA,$55,$02,$00,$0F,$00,$80,$AA
    .byte $AA,$A9,$AA,$AA,$6A,$55,$02,$00,$0F,$00,$80,$AA,$6A,$AA,$AA,$AA
    .byte $6A,$95,$00,$00,$0F,$00,$A0,$AA,$6A,$AA,$AA,$AA,$5A,$95,$00,$00
    .byte $0F,$00,$A0,$AA,$9A,$AA,$AA,$AA,$5A,$25,$00,$00,$0F,$00,$A8,$AA
    .byte $9A,$AA,$AA,$AA,$56,$25,$00,$00,$0F,$00,$A8,$AA,$A6,$AA,$AA,$AA
    .byte $56,$09,$00,$00,$0F,$00,$AA,$AA,$96,$AA,$AA,$AA,$55,$09,$00,$00
    .byte $0F,$00,$AA,$6A,$69,$A9,$AA,$AA,$55,$02,$00,$00,$0F,$80,$AA,$96
    .byte $AA,$96,$AA,$6A,$55,$02,$00,$00,$0F,$80,$6A,$A9,$AA,$6A,$A9,$6A
    .byte $95,$00,$00,$00,$0F,$A0,$96,$AA,$AA,$AA,$96,$5A,$95,$00,$00,$00
    .byte $0F,$60,$A9,$AA,$AA,$AA,$6A,$59,$25,$00,$00,$00,$0F,$A8,$AA,$AA
    .byte $AA,$AA,$AA,$56,$25,$00,$00,$00,$0F,$A8,$AA,$AA,$AA,$AA,$AA,$56
    .byte $09,$00,$00,$00,$0F,$A8,$AA,$AA,$AA,$AA,$AA,$56,$09,$00,$00,$00
    .byte $0F,$A8,$AA,$AA,$AA,$AA,$AA,$56,$02,$00,$00,$00,$0F,$A8,$AA,$AA
    .byte $AA,$AA,$AA,$56,$02,$00,$00,$00,$0F,$A8,$AA,$AA,$AA,$AA,$AA,$96
    .byte $00,$00,$00,$00,$0F,$A8,$AA,$AA,$AA,$AA,$AA,$96,$00,$00,$00,$00
    .byte $0F,$A8,$AA,$AA,$AA,$AA,$AA,$26,$00,$00,$00,$00,$0F,$A8,$AA,$AA
    .byte $AA,$AA,$AA,$26,$00,$00,$00,$00,$0F,$A8,$AA,$AA,$AA,$AA,$AA,$0A
    .byte $00,$00,$00,$00,$0F,$A8,$AA,$AA,$AA,$AA,$AA,$0A,$00,$00,$00,$00
    .byte $0F,$A8,$AA,$AA,$AA,$AA,$AA,$02,$00,$00,$00,$00
sprite_113:
    .byte $24,$31,$0A,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$00,$02,$00,$00,$00,$0F,$00,$00,$00,$00,$00
    .byte $02,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$02,$00,$00,$00,$0F,$00
    .byte $00,$00,$00,$00,$02,$00,$00,$00,$0F,$00,$00,$00,$00,$00,$02,$00
    .byte $00,$00,$0F,$00,$00,$00,$00,$80,$0A,$00,$00,$00,$0F,$00,$00,$00
    .byte $00,$80,$0A,$00,$00,$00,$0F,$00,$00,$00,$00,$80,$5A,$25,$00,$00
    .byte $0F,$00,$00,$00,$00,$A0,$6A,$25,$00,$00,$0F,$00,$00,$00,$00,$A0
    .byte $6A,$25,$00,$00,$0F,$00,$00,$00,$00,$A8,$AA,$25,$00,$00,$0F,$00
    .byte $00,$00,$60,$99,$99,$A5,$00,$00,$0F,$00,$00,$00,$60,$A5,$6A,$A9
    .byte $00,$00,$0F,$00,$00,$00,$60,$A5,$6A,$AA,$02,$00,$0F,$00,$00,$00
    .byte $60,$A5,$69,$AA,$02,$00,$0F,$00,$00,$00,$A8,$A5,$69,$A9,$00,$00
    .byte $0F,$00,$00,$00,$A8,$A5,$6A,$AA,$00,$00,$0F,$00,$00,$00,$AA,$A6
    .byte $AA,$9A,$00,$00,$0F,$00,$00,$00,$AA,$AA,$6A,$9A,$00,$00,$0F,$00
    .byte $00,$00,$98,$A9,$69,$AA,$00,$00,$0F,$00,$00,$00,$98,$AA,$A9,$2A
    .byte $00,$00,$0F,$00,$00,$00,$A8,$AA,$A9,$29,$00,$00,$0F,$00,$00,$00
    .byte $A0,$AA,$AA,$2A,$00,$00,$0F,$00,$00,$00,$A0,$66,$66,$2A,$00,$00
    .byte $0F,$00,$00,$00,$A0,$AA,$AA,$29,$00,$00,$0F,$00,$00,$00,$A0,$A9
    .byte $AA,$29,$00,$00,$0F,$00,$00,$00,$A0,$A9,$AA,$2A,$00,$00,$0F,$00
    .byte $00,$00,$A0,$A9,$AA,$2A,$00,$00,$0F,$00,$00,$00,$A0,$9A,$9A,$0A
    .byte $00,$00,$0F,$00,$00,$00,$A0,$9A,$9A,$0A,$00,$00,$0F,$00,$00,$00
    .byte $A0,$AA,$AA,$0A,$00,$00,$0F,$00,$00,$00,$A0,$AA,$A9,$0A,$00,$00
    .byte $0F,$00,$00,$00,$A0,$6A,$AA,$2A,$00,$00,$0F,$00,$00,$00,$AA,$AA
    .byte $A6,$2A,$00,$00,$0F,$00,$00,$00,$AA,$6A,$A6,$AA,$00,$00,$0F,$00
    .byte $00,$A0,$AA,$9A,$AA,$AA,$02,$00,$0F,$00,$00,$A0,$AA,$AA,$99,$AA
    .byte $02,$00,$0F,$00,$00,$A0,$AA,$AA,$6A,$A6,$02,$00,$0F,$00,$00,$A8
    .byte $AA,$AA,$AA,$AA,$0A,$00,$0F,$00,$00,$A8,$AA,$AA,$AA,$9A,$09,$00
    .byte $0F,$00,$80,$AA,$AA,$AA,$AA,$AA,$9A,$00,$0F,$00,$80,$AA,$AA,$AA
    .byte $AA,$AA,$AA,$00,$0F,$00,$80,$AA,$AA,$AA,$AA,$AA,$AA,$00,$0F,$00
    .byte $80,$AA,$AA,$AA,$AA,$AA,$AA,$02,$0F,$00,$A0,$AA,$AA,$AA,$AA,$AA
    .byte $AA,$0A,$0F,$00,$A8,$AA,$AA,$AA,$AA,$AA,$AA,$0A,$0F,$00,$AA,$AA
    .byte $AA,$AA,$AA,$AA,$AA,$2A,$0F,$A0,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$AA
    .byte $0F,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$AA,$AA
sprite_161:
    .byte $06,$08,$03,$01,$01,$02,$02,$02,$02,$02,$01,$00,$00,$00,$00,$00
    .byte $0F,$20,$00,$0F,$20,$00,$0F,$20,$00,$0F,$20,$00,$0F,$20,$00,$0F
    .byte $00,$00,$0F,$20,$00,$0F,$00,$00
sprite_162:
    .byte $06,$08,$03,$01,$01,$02,$02,$02,$02,$02,$01,$00,$00,$00,$00,$00
    .byte $0F,$88,$00,$0F,$88,$00,$0F,$88,$00,$0F,$00,$00,$0F,$00,$00,$0F
    .byte $00,$00,$0F,$00,$00,$0F,$00,$00
sprite_163:
    .byte $06,$08,$03,$01,$01,$02,$02,$02,$02,$02,$01,$00,$00,$00,$00,$00
    .byte $0F,$88,$00,$0F,$88,$00,$0F,$AA,$02,$0F,$88,$00,$0F,$AA,$02,$0F
    .byte $88,$00,$0F,$88,$00,$0F,$00,$00
sprite_164:
    .byte $06,$08,$03,$01,$01,$02,$02,$02,$02,$02,$01,$00,$00,$00,$00,$00
    .byte $0F,$20,$00,$0F,$A8,$02,$0F,$22,$00,$0F,$A8,$00,$0F,$20,$02,$0F
    .byte $AA,$00,$0F,$20,$00,$0F,$00,$00
sprite_165:
    .byte $06,$08,$03,$01,$01,$02,$02,$02,$02,$02,$01,$00,$00,$00,$00,$00
    .byte $0F,$0A,$00,$0F,$0A,$02,$0F,$80,$00,$0F,$20,$00,$0F,$08,$00,$0F
    .byte $82,$02,$0F,$80,$02,$0F,$00,$00
sprite_166:
    .byte $06,$08,$03,$01,$01,$02,$02,$02,$02,$02,$01,$00,$00,$00,$00,$00
    .byte $0F,$08,$00,$0F,$22,$00,$0F,$22,$00,$0F,$08,$00,$0F,$22,$02,$0F
    .byte $82,$00,$0F,$28,$02,$0F,$00,$00
sprite_167:
    .byte $06,$08,$03,$01,$01,$02,$02,$02,$02,$02,$01,$00,$00,$00,$00,$00
    .byte $0F,$20,$00,$0F,$20,$00,$0F,$20,$00,$0F,$00,$00,$0F,$00,$00,$0F
    .byte $00,$00,$0F,$00,$00,$0F,$00,$00
sprite_168:
    .byte $06,$08,$03,$01,$01,$02,$02,$02,$02,$02,$01,$00,$00,$00,$00,$00
    .byte $0F,$20,$00,$0F,$08,$00,$0F,$02,$00,$0F,$02,$00,$0F,$02,$00,$0F
    .byte $08,$00,$0F,$20,$00,$0F,$00,$00
sprite_169:
    .byte $06,$08,$03,$01,$01,$02,$02,$02,$02,$02,$01,$00,$00,$00,$00,$00
    .byte $0F,$20,$00,$0F,$80,$00,$0F,$00,$02,$0F,$00,$02,$0F,$00,$02,$0F
    .byte $80,$00,$0F,$20,$00,$0F,$00,$00
.segment "RODATA"
source_variation: .incbin "room-variation.bin"
atlas_lo: .byte 0,<sprite_1,<sprite_2,<sprite_3,<sprite_4,<sprite_5,<sprite_6,<sprite_7,<sprite_8,<sprite_9,<sprite_10,<sprite_11,<sprite_12,<sprite_13,<sprite_14,<sprite_15,<sprite_16,<sprite_17,<sprite_18,0,<sprite_20,<sprite_21,<sprite_22,<sprite_23,<sprite_24,<sprite_25,<sprite_26,<sprite_27,<sprite_28,<sprite_29,<sprite_30,<sprite_31,<sprite_32,<sprite_33,<sprite_34,<sprite_35,<sprite_36,<sprite_37,<sprite_38,0,<sprite_40,<sprite_41,<sprite_42,<sprite_43,<sprite_44,<sprite_45,<sprite_46,<sprite_47,<sprite_48,<sprite_49,<sprite_50,<sprite_51,<sprite_52,<sprite_53,<sprite_54,<sprite_55,<sprite_56,<sprite_57,<sprite_58,<sprite_59,<sprite_60,<sprite_61,<sprite_62,<sprite_63,<sprite_64,<sprite_65,0,<sprite_67,<sprite_68,<sprite_69,<sprite_70,<sprite_71,<sprite_72,<sprite_73,<sprite_74,<sprite_75,<sprite_76,<sprite_77,<sprite_78,<sprite_79,<sprite_80,<sprite_81,<sprite_82,<sprite_83,<sprite_84,<sprite_85,<sprite_86,<sprite_87,<sprite_88,<sprite_89,<sprite_90,<sprite_91,0,<sprite_93,<sprite_94,<sprite_95,<sprite_96,<sprite_97,<sprite_98,<sprite_99,<sprite_100,<sprite_101,<sprite_102,<sprite_103,0,0,0,0,0,0,<sprite_110,<sprite_111,<sprite_112,<sprite_113,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,<sprite_161,<sprite_162,<sprite_163,<sprite_164,<sprite_165,<sprite_166,<sprite_167,<sprite_168,<sprite_169
atlas_hi: .byte 0,>sprite_1,>sprite_2,>sprite_3,>sprite_4,>sprite_5,>sprite_6,>sprite_7,>sprite_8,>sprite_9,>sprite_10,>sprite_11,>sprite_12,>sprite_13,>sprite_14,>sprite_15,>sprite_16,>sprite_17,>sprite_18,0,>sprite_20,>sprite_21,>sprite_22,>sprite_23,>sprite_24,>sprite_25,>sprite_26,>sprite_27,>sprite_28,>sprite_29,>sprite_30,>sprite_31,>sprite_32,>sprite_33,>sprite_34,>sprite_35,>sprite_36,>sprite_37,>sprite_38,0,>sprite_40,>sprite_41,>sprite_42,>sprite_43,>sprite_44,>sprite_45,>sprite_46,>sprite_47,>sprite_48,>sprite_49,>sprite_50,>sprite_51,>sprite_52,>sprite_53,>sprite_54,>sprite_55,>sprite_56,>sprite_57,>sprite_58,>sprite_59,>sprite_60,>sprite_61,>sprite_62,>sprite_63,>sprite_64,>sprite_65,0,>sprite_67,>sprite_68,>sprite_69,>sprite_70,>sprite_71,>sprite_72,>sprite_73,>sprite_74,>sprite_75,>sprite_76,>sprite_77,>sprite_78,>sprite_79,>sprite_80,>sprite_81,>sprite_82,>sprite_83,>sprite_84,>sprite_85,>sprite_86,>sprite_87,>sprite_88,>sprite_89,>sprite_90,>sprite_91,0,>sprite_93,>sprite_94,>sprite_95,>sprite_96,>sprite_97,>sprite_98,>sprite_99,>sprite_100,>sprite_101,>sprite_102,>sprite_103,0,0,0,0,0,0,>sprite_110,>sprite_111,>sprite_112,>sprite_113,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>sprite_161,>sprite_162,>sprite_163,>sprite_164,>sprite_165,>sprite_166,>sprite_167,>sprite_168,>sprite_169
equipment_lo: .byte <equipment_0,<equipment_1,<equipment_2,<equipment_3,<equipment_4,<equipment_5,<equipment_6,<equipment_7,<equipment_8,<equipment_9,<equipment_10,<equipment_11,<equipment_12,<equipment_13,<equipment_14,<equipment_15,<equipment_16,<equipment_17,<equipment_18,<equipment_19,<equipment_20,<equipment_21,<equipment_22,<equipment_23,<equipment_24,<equipment_25
equipment_hi: .byte >equipment_0,>equipment_1,>equipment_2,>equipment_3,>equipment_4,>equipment_5,>equipment_6,>equipment_7,>equipment_8,>equipment_9,>equipment_10,>equipment_11,>equipment_12,>equipment_13,>equipment_14,>equipment_15,>equipment_16,>equipment_17,>equipment_18,>equipment_19,>equipment_20,>equipment_21,>equipment_22,>equipment_23,>equipment_24,>equipment_25
equipment_0:
    .byte $01,$18,$FF,$D5
equipment_1:
    .byte $01,$19,$01,$D6
equipment_2:
    .byte $01,$02,$00,$C7
equipment_3:
    .byte $01,$1A,$03,$D5
equipment_4:
    .byte $01,$1B,$FF,$C5
equipment_5:
    .byte $01,$1C,$02,$C5
equipment_6:
    .byte $01,$1D,$FF,$C5
equipment_7:
    .byte $01,$1E,$03,$C7
equipment_8:
    .byte $01,$1F,$FF,$D5
equipment_9:
    .byte $01,$20,$01,$D6
equipment_10:
    .byte $01,$21,$00,$DF
equipment_11:
    .byte $01,$22,$03,$D4
equipment_12:
    .byte $01,$23,$FE,$D5
equipment_13:
    .byte $01,$24,$01,$D5
equipment_14:
    .byte $01,$25,$FF,$DE
equipment_15:
    .byte $01,$26,$03,$D4
equipment_16:
    .byte $01,$27,$02,$CB
equipment_17:
    .byte $01,$28,$FF,$CC
equipment_18:
    .byte $00
equipment_19:
    .byte $01,$29,$FE,$D5
equipment_20:
    .byte $01,$2A,$01,$D5
equipment_21:
    .byte $01,$2B,$FF,$DE
equipment_22:
    .byte $01,$2C,$03,$D4
equipment_23:
    .byte $01,$2D,$03,$D5
equipment_24:
    .byte $01,$2E,$03,$CA
equipment_25:
    .byte $01,$3B,$FF,$EE
enemy_sprite_indices: .byte 48,49,50,51,52,53,54,55,56,57
full_clue_lo: .byte <full_clue_0,<full_clue_1,<full_clue_2,<full_clue_3
full_clue_hi: .byte >full_clue_0,>full_clue_1,>full_clue_2,>full_clue_3
full_clue_0:
    .byte $4D,$65,$73,$73,$61,$67,$65,$20,$31,$20,$22,$44,$65,$72,$20,$52,$65,$69,$66,$20,$77,$69,$72,$64,$20,$64,$69,$72,$20,$64,$61,$73,$20,$20,$20,$20,$20,$20,$20,$20,$55,$62,$65,$6C,$76,$65,$72,$64,$65,$63,$6B,$65,$6E,$2E,$22,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$55,$6E,$65,$20,$74,$6F,$75,$63,$68,$65,$3A,$20,$69,$6E,$64,$69,$63,$65,$20,$73,$75,$69,$76,$61,$6E,$74,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
full_clue_1:
    .byte $4D,$65,$73,$73,$61,$67,$65,$20,$32,$20,$22,$44,$65,$72,$20,$67,$6F,$6C,$64,$65,$6E,$65,$20,$77,$69,$72,$64,$20,$64,$69,$72,$20,$64,$65,$6E,$20,$20,$20,$20,$20,$46,$65,$75,$65,$72,$77,$65,$67,$20,$62,$61,$68,$6E,$65,$6E,$2E,$22,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$55,$6E,$65,$20,$74,$6F,$75,$63,$68,$65,$3A,$20,$69,$6E,$64,$69,$63,$65,$20,$73,$75,$69,$76,$61,$6E,$74,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
full_clue_2:
    .byte $4D,$65,$73,$73,$61,$67,$65,$20,$33,$20,$22,$44,$65,$72,$20,$41,$64,$6C,$65,$72,$20,$61,$75,$73,$20,$67,$65,$6D,$65,$69,$6E,$65,$6D,$20,$4D,$65,$74,$61,$6C,$6C,$77,$69,$72,$64,$20,$65,$64,$65,$6C,$20,$77,$65,$72,$64,$65,$6E,$20,$2E,$22,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$55,$6E,$65,$20,$74,$6F,$75,$63,$68,$65,$3A,$20,$69,$6E,$64,$69,$63,$65,$20,$73,$75,$69,$76,$61,$6E,$74,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
full_clue_3:
    .byte $4C,$65,$20,$4C,$69,$76,$72,$65,$20,$64,$65,$20,$6C,$61,$20,$53,$61,$67,$65,$73,$73,$65,$20,$22,$4E,$75,$72,$20,$76,$6F,$6E,$20,$64,$65,$6D,$20,$20,$20,$20,$20,$53,$74,$65,$72,$6E,$20,$77,$69,$72,$73,$74,$20,$64,$75,$20,$64,$69,$63,$68,$20,$65,$72,$68,$65,$62,$65,$6E,$2E,$22,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$55,$6E,$65,$20,$74,$6F,$75,$63,$68,$65,$3A,$20,$69,$6E,$64,$69,$63,$65,$20,$73,$75,$69,$76,$61,$6E,$74,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
geometry_0:
    .byte $01,$0C,$C7,$30,$8B,$01,$30,$8B,$CB,$8B,$01,$CB,$8B,$EF,$C7,$02,$04,$24,$7A,$01,$02,$04,$24,$69,$01,$02,$04,$24,$58,$01,$02,$04,$24,$47,$01,$02,$04,$24,$36,$01,$02,$04,$24,$25,$01,$02,$04,$24,$14,$01,$02,$03,$BF,$79,$01,$02,$03,$BF,$67,$01,$02,$03,$BF,$55,$01,$02,$03,$BF,$43,$01,$02,$03,$BF,$31,$01,$02,$03,$BF,$1F,$01,$02,$03,$BF,$0D,$01,$00
geometry_1:
    .byte $01,$0C,$C7,$3C,$77,$01,$3C,$77,$BF,$77,$01,$BF,$77,$EF,$C7,$02,$04,$30,$66,$01,$02,$04,$30,$55,$01,$02,$04,$30,$44,$01,$02,$04,$30,$33,$01,$02,$04,$30,$22,$01,$02,$04,$30,$11,$01,$02,$03,$B3,$65,$01,$02,$03,$B3,$53,$01,$02,$03,$B3,$41,$01,$02,$03,$B3,$2F,$01,$02,$03,$B3,$1D,$01,$02,$03,$B3,$0B,$01,$00
geometry_2:
    .byte $01,$0C,$C7,$3C,$77,$01,$3C,$77,$BF,$77,$01,$BF,$77,$EF,$C7,$01,$3A,$77,$3A,$13,$01,$49,$77,$49,$13,$01,$B2,$77,$B2,$13,$01,$C1,$77,$C1,$13,$02,$01,$32,$13,$00,$02,$02,$32,$70,$00,$02,$01,$A9,$13,$00,$02,$02,$A9,$70,$00,$00
geometry_left_border:
    .byte $01,$2B,$95,$2B,$27,$01,$2B,$27,$23,$1A,$01,$23,$1A,$1B,$13,$01,$1B,$13,$13,$2B,$01,$13,$2B,$0C,$53,$01,$0C,$53,$0C,$C6,$00
geometry_3:
    .byte $01,$0C,$C7,$2B,$95,$01,$2B,$95,$D0,$95,$01,$D0,$95,$EF,$C7,$01,$2B,$95,$2B,$27,$01,$2B,$27,$23,$1A,$01,$23,$1A,$1B,$13,$01,$1B,$13,$13,$2B,$01,$13,$2B,$0C,$53,$01,$0C,$53,$0C,$C6,$01,$D0,$95,$D0,$27,$01,$D0,$27,$D8,$1A,$01,$D8,$1A,$E0,$13,$01,$E0,$13,$E8,$2B,$01,$E8,$2B,$EF,$53,$01,$EF,$53,$EF,$C6,$00
geometry_lo: .byte <geometry_0,<geometry_1,<geometry_2,<geometry_3
geometry_hi: .byte >geometry_0,>geometry_1,>geometry_2,>geometry_3
hud_description_0:
    .byte $56,$6F,$75,$73,$20,$65,$74,$65,$73,$20,$00
hud_description_1:
    .byte $64,$61,$6E,$73,$20,$6C,$61,$20,$63,$72,$79,$70,$74,$65,$20,$73,$61,$63,$72,$65,$65,$2E,$00
hud_description_2:
    .byte $64,$61,$6E,$73,$20,$6C,$65,$20,$64,$6F,$6E,$6A,$6F,$6E,$2E,$00
hud_description_3:
    .byte $61,$75,$20,$73,$6F,$6D,$6D,$65,$74,$20,$64,$75,$20,$64,$6F,$6E,$6A,$6F,$6E,$2E,$00
hud_description_4:
    .byte $64,$61,$6E,$73,$20,$75,$6E,$20,$63,$6F,$75,$6C,$6F,$69,$72,$20,$00
hud_description_5:
    .byte $64,$61,$6E,$73,$20,$75,$6E,$65,$20,$73,$61,$6C,$6C,$65,$00
hud_description_6:
    .byte $64,$61,$6E,$73,$20,$75,$6E,$20,$70,$61,$73,$73,$61,$67,$65,$20,$00
hud_description_7:
    .byte $64,$61,$6E,$73,$20,$6C,$65,$73,$20,$63,$61,$74,$61,$63,$6F,$6D,$62,$65,$73,$2E,$00
hud_description_8:
    .byte $61,$75,$20,$70,$72,$65,$6D,$69,$65,$72,$20,$65,$74,$61,$67,$65,$2E,$00
hud_description_9:
    .byte $61,$75,$20,$72,$65,$7A,$2D,$64,$65,$2D,$63,$68,$61,$75,$73,$73,$65,$65,$2E,$00
hud_description_10:
    .byte $61,$75,$20,$66,$6F,$6E,$64,$20,$64,$27,$75,$6E,$65,$20,$6F,$75,$62,$6C,$69,$65,$74,$74,$65,$2E,$00
hud_hand_0:
    .byte $00
hud_hand_1:
    .byte $54,$6F,$72,$63,$68,$65,$00
hud_hand_2:
    .byte $43,$6C,$65,$66,$20,$65,$6E,$20,$66,$65,$72,$00
hud_hand_3:
    .byte $43,$6C,$65,$66,$20,$65,$6E,$20,$6F,$72,$00
hud_hand_4:
    .byte $55,$6E,$65,$20,$66,$69,$6F,$6C,$65,$00
hud_hand_5:
    .byte $50,$69,$65,$64,$20,$64,$65,$20,$62,$69,$63,$68,$65,$00
hud_description_lo: .byte <hud_description_0,<hud_description_1,<hud_description_2,<hud_description_3,<hud_description_4,<hud_description_5,<hud_description_6,<hud_description_7,<hud_description_8,<hud_description_9,<hud_description_10
hud_description_hi: .byte >hud_description_0,>hud_description_1,>hud_description_2,>hud_description_3,>hud_description_4,>hud_description_5,>hud_description_6,>hud_description_7,>hud_description_8,>hud_description_9,>hud_description_10
hud_hand_lo: .byte <hud_hand_0,<hud_hand_1,<hud_hand_0,<hud_hand_0,<hud_hand_0,<hud_hand_0,<hud_hand_5,<hud_hand_0,<hud_hand_3,<hud_hand_2,<hud_hand_4
hud_hand_hi: .byte >hud_hand_0,>hud_hand_1,>hud_hand_0,>hud_hand_0,>hud_hand_0,>hud_hand_0,>hud_hand_5,>hud_hand_0,>hud_hand_3,>hud_hand_2,>hud_hand_4
.segment "TEXTASSETS"
text_assets: .incbin "text-panels.bin"
.segment "RODATA"
text_panel_lo: .byte 0,<(text_assets+483),<(text_assets+624),<(text_assets+858),0,<(text_assets+2434),<(text_assets+2547),<(text_assets+2661),<(text_assets+1560),0,<(text_assets+1129),<(text_assets+0),<(text_assets+1714),0,0,0,<(text_assets+1941),<(text_assets+2187)
text_panel_hi: .byte 0,>(text_assets+483),>(text_assets+624),>(text_assets+858),0,>(text_assets+2434),>(text_assets+2547),>(text_assets+2661),>(text_assets+1560),0,>(text_assets+1129),>(text_assets+0),>(text_assets+1714),0,0,0,>(text_assets+1941),>(text_assets+2187)
map_room_row: .byte 55,27,27,55,83,83,83,55,27,21,21,21,21,21,21,21,41,41,41,41,41,41,41,61,61,61,61,61,61,61,81,81,81,81,81,81,81,101,101,101,101,101,101,101,121,121,121,121,121,121,121,141,141,141,141,141,141,141,27,27,27,55,55,55
map_room_column: .byte 10,10,15,15,15,10,5,5,5,35,30,25,20,15,10,5,35,30,25,20,15,10,5,35,30,25,20,15,10,5,35,30,25,20,15,10,5,35,30,25,20,15,10,5,35,30,25,20,15,10,5,35,30,25,20,15,10,5,25,30,35,25,30,35
.segment "CODE"
map_pin: .byte $1C,$3E,$63,$6B,$63,$3E,$1C,$08,$08
map_glyphs:
    .byte $0E,$11,$19,$15,$13,$11,$0E,$04,$06,$04,$04,$04,$04,$0E
    .byte $0E,$11,$10,$08,$04,$02,$1F,$0F,$10,$10,$0E,$10,$10,$0F
    .byte $08,$0C,$0A,$09,$1F,$08,$08,$1F,$01,$01,$0F,$10,$10,$0F
    .byte $0E,$01,$01,$0F,$11,$11,$0E,$1F,$10,$08,$04,$02,$02,$02
    .byte $0E,$11,$11,$0E,$11,$11,$0E,$0E,$11,$11,$1E,$10,$10,$0E
    .byte $00,$00,$00,$1F,$00,$00,$00,$11,$11,$0A,$04,$0A,$11,$11
.segment "RODATA"
title_flash_data: .incbin "title-flash.bin"

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
    .byte $0D,$10,$13,$16,$19,$1C,$1F,$22,$25,$28,$2B,$2E,$31,$34,$37,$3A
    .byte $3D,$40,$43,$46,$49,$4C,$4F,$52,$55,$58,$5B,$5E,$61,$64,$67,$6A
    .byte $6D,$70,$73,$76,$79,$7C,$7F,$82
x_byte:
    .byte $07,$09,$0A,$0C,$0E,$10,$11,$13,$15,$16,$18,$1A,$1C,$1D,$1F,$21
    .byte $22,$24,$26,$28,$29,$2B,$2D,$2E,$30,$32,$34,$35,$37,$39,$3A,$3C
    .byte $3E,$40,$41,$43,$45,$46,$48,$4A
x_phase:
    .byte $03,$01,$06,$04,$02,$00,$05,$03,$01,$06,$04,$02,$00,$05,$03,$01
    .byte $06,$04,$02,$00,$05,$03,$01,$06,$04,$02,$00,$05,$03,$01,$06,$04
    .byte $02,$00,$05,$03,$01,$06,$04,$02
cell_byte:
    .byte $00,$00,$01,$01,$02,$02,$03,$04,$04,$05,$05,$06,$06,$07,$08,$08
    .byte $09,$09,$0A,$0A,$0B,$0C,$0C,$0D,$0D,$0E,$0E,$0F,$10,$10,$11,$11
    .byte $12,$12,$13,$14,$14,$15,$15,$16,$16,$17,$18,$18,$19,$19,$1A,$1A
    .byte $1B,$1C,$1C,$1D,$1D,$1E,$1E,$1F,$20,$20,$21,$21,$22,$22,$23,$24
    .byte $24,$25,$25,$26,$26,$27,$28,$28,$29,$29,$2A,$2A,$2B,$2C,$2C,$2D
    .byte $2D,$2E,$2E,$2F,$30,$30,$31,$31,$32,$32,$33,$34,$34,$35,$35,$36
    .byte $36,$37,$38,$38,$39,$39,$3A,$3A,$3B,$3C,$3C,$3D,$3D,$3E,$3E,$3F
    .byte $40,$40,$41,$41,$42,$42,$43,$44,$44,$45,$45,$46,$46,$47,$48,$48
    .byte $49,$49,$4A,$4A,$4B,$4C,$4C,$4D,$4D,$4E,$4E,$4F
cell_phase:
    .byte $00,$40,$10,$50,$20,$60,$30,$00,$40,$10,$50,$20,$60,$30,$00,$40
    .byte $10,$50,$20,$60,$30,$00,$40,$10,$50,$20,$60,$30,$00,$40,$10,$50
    .byte $20,$60,$30,$00,$40,$10,$50,$20,$60,$30,$00,$40,$10,$50,$20,$60
    .byte $30,$00,$40,$10,$50,$20,$60,$30,$00,$40,$10,$50,$20,$60,$30,$00
    .byte $40,$10,$50,$20,$60,$30,$00,$40,$10,$50,$20,$60,$30,$00,$40,$10
    .byte $50,$20,$60,$30,$00,$40,$10,$50,$20,$60,$30,$00,$40,$10,$50,$20
    .byte $60,$30,$00,$40,$10,$50,$20,$60,$30,$00,$40,$10,$50,$20,$60,$30
    .byte $00,$40,$10,$50,$20,$60,$30,$00,$40,$10,$50,$20,$60,$30,$00,$40
    .byte $10,$50,$20,$60,$30,$00,$40,$10,$50,$20,$60,$30
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
sprite_62:
    .byte $18,$14,$07,$0E,$0E,$0E,$0F,$0F,$0F,$0F,$01,$00,$00,$00,$00,$00
    .byte $01,$00,$00,$A8,$2A,$00,$00,$01,$00,$00,$A8,$2A,$00,$00,$01,$00
    .byte $00,$A8,$AA,$02,$00,$01,$00,$00,$AA,$AA,$0A,$00,$01,$00,$00,$AA
    .byte $AA,$2A,$00,$01,$00,$80,$AA,$AA,$2A,$00,$01,$00,$A0,$AA,$A5,$2A
    .byte $00,$01,$00,$80,$AA,$95,$AA,$00,$01,$00,$A8,$6A,$40,$AA,$00,$01
    .byte $00,$AA,$5A,$40,$AA,$00,$01,$80,$AA,$55,$40,$99,$00,$01,$80,$6A
    .byte $55,$55,$A9,$00,$04,$00,$5A,$55,$55,$A9,$00,$04,$80,$56,$55,$55
    .byte $A9,$00,$04,$80,$56,$55,$55,$99,$00,$04,$80,$56,$55,$55,$A9,$00
    .byte $04,$80,$55,$55,$55,$29,$00,$04,$00,$00,$00,$00,$A8,$00,$04,$00
    .byte $00,$00,$00,$A8,$02,$04,$00,$00,$00,$00,$A8,$02
sprite_63:
    .byte $1B,$15,$08,$10,$10,$10,$10,$10,$11,$11,$01,$00,$00,$00,$00,$00
    .byte $01,$00,$00,$A0,$AA,$00,$00,$00,$01,$00,$00,$A8,$AA,$00,$00,$00
    .byte $01,$00,$00,$AA,$AA,$02,$00,$00,$01,$00,$80,$AA,$AA,$02,$00,$00
    .byte $01,$00,$A0,$AA,$AA,$02,$00,$00,$01,$00,$A0,$AA,$AA,$0A,$00,$00
    .byte $01,$00,$A0,$AA,$AA,$0A,$00,$00,$01,$00,$A0,$6A,$A9,$0A,$00,$00
    .byte $01,$00,$A0,$5A,$A5,$2A,$00,$00,$01,$00,$A0,$56,$A5,$AA,$00,$00
    .byte $01,$00,$A0,$56,$80,$A9,$02,$00,$01,$00,$60,$56,$40,$AA,$0A,$00
    .byte $01,$00,$A8,$56,$40,$AA,$0A,$00,$04,$00,$A8,$56,$55,$AA,$0A,$00
    .byte $04,$00,$A8,$56,$55,$95,$0A,$00,$04,$00,$A0,$55,$55,$55,$0A,$00
    .byte $04,$00,$A0,$55,$55,$55,$2A,$00,$04,$00,$A0,$55,$55,$55,$29,$00
    .byte $04,$00,$A8,$55,$55,$55,$29,$00,$04,$00,$AA,$55,$55,$55,$29,$00
    .byte $04,$00,$AA,$00,$00,$00,$00,$00
sprite_64:
    .byte $06,$11,$04,$04,$04,$04,$04,$04,$05,$05,$00,$00,$00,$00,$00,$00
    .byte $06,$00,$00,$30,$06,$00,$00,$3C,$06,$00,$00,$AC,$06,$00,$00,$AA
    .byte $06,$00,$00,$AA,$06,$00,$00,$AA,$06,$00,$00,$3A,$06,$00,$00,$3A
    .byte $06,$00,$00,$3A,$06,$00,$00,$0A,$0D,$00,$00,$A7,$0D,$00,$00,$AA
    .byte $0D,$00,$00,$AC,$0D,$00,$00,$3C,$0D,$00,$00,$AC,$0D,$00,$00,$3C
    .byte $0D,$00,$00,$AC
sprite_65:
    .byte $06,$10,$04,$04,$04,$04,$04,$04,$05,$05,$00,$00,$00,$00,$00,$00
    .byte $06,$7C,$AD,$00,$06,$AA,$DA,$03,$06,$A7,$AF,$03,$06,$A7,$FA,$03
    .byte $06,$FC,$A7,$03,$06,$FC,$FA,$03,$06,$AA,$FD,$03,$06,$FC,$A7,$03
    .byte $06,$A7,$AA,$03,$06,$DA,$7F,$03,$06,$7A,$AA,$00,$0D,$AC,$AD,$00
    .byte $0D,$AC,$A7,$03,$0D,$5C,$D5,$03,$0D,$5C,$75,$03,$0D,$5C,$A5,$03
sprite_67:
    .byte $06,$11,$04,$04,$04,$04,$04,$04,$05,$05,$00,$00,$00,$00,$00,$00
    .byte $06,$03,$00,$00,$06,$0A,$00,$00,$06,$0A,$00,$00,$06,$3A,$00,$00
    .byte $06,$3A,$00,$00,$06,$3A,$00,$00,$06,$3A,$00,$00,$06,$3A,$00,$00
    .byte $06,$3A,$00,$00,$06,$3A,$00,$00,$0D,$3C,$00,$00,$0D,$0A,$00,$00
    .byte $0D,$3A,$00,$00,$0D,$3A,$00,$00,$0D,$0A,$00,$00,$0D,$0A,$00,$00
    .byte $0D,$03,$00,$00
sprite_68:
    .byte $09,$19,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $04,$00,$02,$00,$04,$00,$0A,$00,$04,$80,$5A,$02,$04,$80,$9A,$02
    .byte $04,$80,$9A,$02,$04,$00,$9A,$02,$04,$00,$9A,$02,$04,$00,$9A,$02
    .byte $04,$00,$9A,$02,$04,$00,$9A,$02,$04,$00,$9A,$02,$04,$80,$9A,$02
    .byte $04,$80,$9A,$02,$04,$80,$5A,$02,$04,$80,$96,$00,$04,$80,$A6,$02
    .byte $04,$80,$A6,$02,$04,$80,$AA,$02,$04,$80,$AA,$02,$04,$80,$AA,$02
    .byte $04,$80,$6A,$02,$04,$80,$AA,$02,$04,$00,$AA,$02,$04,$00,$AA,$02
    .byte $04,$00,$AA,$02
sprite_69:
    .byte $09,$1A,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $04,$00,$02,$00,$04,$00,$0A,$00,$04,$96,$0A,$00,$04,$9A,$0A,$00
    .byte $04,$9A,$0A,$00,$04,$5A,$0A,$00,$04,$5A,$0A,$00,$04,$5A,$0A,$00
    .byte $04,$5A,$0A,$00,$04,$5A,$0A,$00,$04,$5A,$0A,$00,$04,$5A,$0A,$00
    .byte $04,$9A,$0A,$00,$04,$96,$0A,$00,$04,$80,$02,$00,$04,$96,$02,$00
    .byte $04,$96,$02,$00,$04,$A6,$02,$00,$04,$AA,$02,$00,$04,$AA,$00,$00
    .byte $04,$AA,$00,$00,$04,$2A,$00,$00,$04,$2A,$00,$00,$04,$2A,$00,$00
    .byte $04,$0A,$00,$00,$04,$02,$00,$00
sprite_70:
    .byte $09,$17,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $04,$00,$02,$00,$04,$00,$0A,$00,$04,$80,$5A,$02,$04,$80,$9A,$02
    .byte $04,$80,$9A,$02,$04,$00,$9A,$02,$04,$00,$9A,$02,$04,$00,$9A,$02
    .byte $04,$00,$9A,$02,$04,$00,$9A,$02,$04,$00,$9A,$02,$04,$80,$9A,$02
    .byte $04,$80,$9A,$02,$04,$80,$5A,$02,$04,$80,$02,$00,$04,$80,$56,$02
    .byte $04,$80,$96,$02,$04,$80,$96,$02,$04,$80,$AA,$02,$04,$00,$AA,$02
    .byte $04,$00,$AA,$02,$04,$00,$A8,$02,$04,$00,$60,$02
sprite_71:
    .byte $06,$15,$03,$04,$04,$04,$04,$04,$05,$05,$01,$00,$00,$00,$00,$00
    .byte $04,$08,$00,$04,$28,$00,$04,$2A,$00,$04,$2A,$00,$04,$2A,$00,$04
    .byte $28,$00,$04,$28,$00,$04,$28,$00,$04,$28,$00,$04,$28,$00,$04,$28
    .byte $00,$04,$28,$00,$04,$28,$00,$04,$28,$00,$04,$2A,$00,$04,$2A,$00
    .byte $04,$2A,$00,$04,$0A,$00,$04,$0A,$00,$04,$0A,$00,$04,$0A,$00
sprite_74:
    .byte $06,$11,$03,$04,$04,$04,$04,$04,$05,$05,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$08,$05,$00,$0A,$05,$00,$0A,$05,$00,$0A,$05,$00,$0A,$05
    .byte $00,$0A,$05,$00,$0A,$05,$00,$0A,$05,$00,$0A,$05,$00,$02,$05,$00
    .byte $0A,$05,$00,$0A,$05,$00,$0A,$05,$00,$0A,$05,$00,$0A,$05,$80,$0A
    .byte $05,$80,$09
sprite_75:
    .byte $09,$10,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$AA,$00,$00,$05,$AA,$02,$00,$05,$AA,$02,$00,$05,$AA,$02,$00
    .byte $05,$AA,$02,$00,$05,$AA,$02,$00,$05,$AA,$02,$00,$05,$AA,$00,$00
    .byte $05,$AA,$02,$00,$05,$AA,$02,$00,$05,$AA,$02,$00,$05,$AA,$0A,$00
    .byte $05,$AA,$0A,$00,$05,$56,$0A,$00,$05,$56,$AA,$02,$05,$56,$AA,$02
sprite_76:
    .byte $06,$07,$03,$04,$04,$04,$04,$04,$05,$05,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$08,$05,$00,$0A,$05,$80,$0A,$05,$80,$0A,$05,$80,$0A,$05
    .byte $A8,$0A,$05,$98,$0A
sprite_77:
    .byte $06,$12,$03,$04,$04,$04,$04,$04,$05,$05,$01,$00,$00,$00,$00,$00
    .byte $05,$02,$00,$05,$02,$00,$05,$02,$00,$05,$0A,$00,$05,$0A,$00,$05
    .byte $0A,$00,$05,$0A,$00,$05,$0A,$00,$05,$0A,$00,$05,$0A,$00,$05,$0A
    .byte $00,$05,$02,$00,$05,$0A,$00,$05,$0A,$00,$05,$02,$00,$05,$02,$00
    .byte $05,$0A,$00,$05,$0A,$00
sprite_78:
    .byte $09,$13,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0D,$00,$00,$02,$0D,$00,$80,$02,$0D,$00,$80,$02,$0D,$00,$80,$02
    .byte $0D,$00,$80,$02,$0D,$00,$80,$02,$0D,$00,$A0,$02,$0D,$00,$A0,$02
    .byte $0D,$00,$A8,$00,$0D,$00,$A8,$00,$0D,$00,$2A,$00,$0D,$80,$0A,$00
    .byte $0D,$80,$02,$00,$0D,$80,$02,$00,$0D,$80,$02,$00,$0D,$80,$02,$00
    .byte $0D,$80,$02,$00,$0D,$80,$02,$00,$0D,$80,$02,$00
sprite_79:
    .byte $0C,$0E,$04,$07,$07,$08,$08,$08,$08,$08,$01,$00,$00,$00,$00,$00
    .byte $0D,$AA,$00,$00,$0D,$AA,$00,$00,$0D,$AA,$02,$00,$0D,$AA,$02,$00
    .byte $0D,$AA,$02,$00,$0D,$AA,$00,$00,$0D,$AA,$2A,$00,$0D,$AA,$AA,$00
    .byte $0D,$2A,$A0,$02,$0D,$2A,$90,$02,$0D,$2A,$90,$02,$0D,$2A,$90,$02
    .byte $0D,$2A,$90,$02,$0D,$2A,$90,$02
sprite_80:
    .byte $09,$0B,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0D,$00,$80,$02,$0D,$00,$A8,$02,$0D,$00,$A8,$02,$0D,$00,$AA,$02
    .byte $0D,$00,$9A,$02,$0D,$00,$9A,$02,$0D,$00,$9A,$00,$0D,$00,$9A,$00
    .byte $0D,$00,$9A,$00,$0D,$00,$9A,$00,$0D,$00,$0A,$00
sprite_81:
    .byte $09,$13,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0D,$02,$00,$00,$0D,$02,$00,$00,$0D,$02,$00,$00,$0D,$0A,$00,$00
    .byte $0D,$0A,$00,$00,$0D,$0A,$00,$00,$0D,$0A,$00,$00,$0D,$0A,$00,$00
    .byte $0D,$0A,$00,$00,$0D,$2A,$00,$00,$0D,$28,$00,$00,$0D,$20,$00,$00
    .byte $0D,$80,$02,$00,$0D,$80,$02,$00,$0D,$80,$02,$00,$0D,$80,$02,$00
    .byte $0D,$80,$02,$00,$0D,$80,$02,$00,$0D,$80,$02,$00
sprite_82:
    .byte $09,$12,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0D,$00,$0A,$00,$0D,$9A,$09,$00,$0D,$9A,$09,$00,$0D,$AA,$0A,$00
    .byte $0D,$AA,$0A,$00,$0D,$AA,$02,$00,$0D,$9A,$02,$00,$0D,$96,$00,$00
    .byte $0D,$80,$00,$00,$0D,$80,$02,$00,$0D,$96,$02,$00,$0D,$96,$02,$00
    .byte $0D,$9A,$02,$00,$0D,$96,$02,$00,$0D,$AA,$02,$00,$0D,$AA,$02,$00
    .byte $0D,$AA,$02,$00,$0D,$AA,$00,$00
sprite_83:
    .byte $09,$10,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0D,$80,$02,$00,$0D,$80,$99,$02,$0D,$80,$99,$02,$0D,$80,$A9,$02
    .byte $0D,$80,$AA,$02,$0D,$00,$AA,$02,$0D,$00,$5A,$02,$0D,$00,$08,$00
    .byte $0D,$00,$0A,$00,$0D,$00,$9A,$02,$0D,$00,$9A,$02,$0D,$00,$9A,$02
    .byte $0D,$00,$AA,$02,$0D,$00,$AA,$02,$0D,$00,$AA,$02,$0D,$00,$A8,$02
sprite_84:
    .byte $09,$11,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$00,$02,$05,$00,$80,$02,$05,$00,$80,$02,$05,$00,$80,$02
    .byte $05,$00,$80,$02,$05,$00,$80,$02,$05,$00,$A0,$02,$05,$18,$A0,$02
    .byte $05,$28,$A0,$00,$05,$28,$A0,$00,$05,$80,$2A,$00,$05,$80,$0A,$00
    .byte $05,$80,$02,$00,$05,$00,$02,$00,$05,$00,$A6,$00,$05,$00,$28,$00
    .byte $05,$00,$28,$00
sprite_85:
    .byte $0C,$11,$04,$07,$07,$08,$08,$08,$08,$08,$01,$00,$00,$00,$00,$00
    .byte $05,$AA,$00,$00,$05,$AA,$00,$00,$05,$AA,$00,$00,$05,$AA,$02,$00
    .byte $05,$AA,$02,$00,$05,$AA,$02,$00,$05,$AA,$00,$00,$05,$AA,$02,$00
    .byte $05,$AA,$02,$00,$05,$AA,$0A,$00,$05,$AA,$0A,$00,$05,$AA,$2A,$00
    .byte $05,$AA,$AA,$00,$05,$2A,$90,$29,$05,$96,$96,$26,$05,$96,$9A,$26
    .byte $05,$96,$A6,$A5
sprite_86:
    .byte $09,$08,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$80,$02,$05,$00,$A8,$02,$05,$00,$A8,$02,$05,$00,$AA,$02
    .byte $05,$28,$90,$02,$05,$98,$9A,$02,$05,$58,$AA,$02,$05,$5A,$AA,$02
sprite_87:
    .byte $09,$12,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$02,$00,$00,$05,$02,$00,$00,$05,$02,$00,$00,$05,$0A,$00,$00
    .byte $05,$0A,$00,$00,$05,$0A,$00,$00,$05,$0A,$00,$00,$05,$0A,$00,$00
    .byte $05,$1A,$90,$00,$05,$2A,$A0,$00,$05,$28,$A0,$00,$05,$A0,$0A,$00
    .byte $05,$80,$02,$00,$05,$80,$02,$00,$05,$00,$02,$00,$05,$A8,$00,$00
    .byte $05,$98,$00,$00,$05,$20,$00,$00
sprite_88:
    .byte $09,$1A,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$02,$00,$00,$05,$02,$00,$00,$05,$02,$00,$00,$05,$0A,$00,$00
    .byte $05,$0A,$00,$00,$05,$0A,$00,$00,$05,$0A,$00,$00,$05,$0A,$00,$00
    .byte $05,$0A,$00,$00,$05,$2A,$00,$00,$05,$28,$00,$00,$05,$20,$00,$00
    .byte $05,$80,$0A,$00,$05,$80,$0A,$00,$05,$00,$0A,$00,$05,$80,$0A,$00
    .byte $05,$00,$0A,$00,$05,$80,$0A,$00,$05,$00,$0A,$00,$05,$00,$0A,$00
    .byte $05,$00,$0A,$00,$05,$00,$02,$00,$05,$00,$02,$00,$05,$80,$0A,$00
    .byte $05,$80,$0A,$00,$05,$00,$0A,$00
sprite_89:
    .byte $09,$11,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$80,$00,$00,$05,$80,$00,$00,$05,$80,$00,$00,$05,$80,$00,$00
    .byte $05,$80,$00,$00,$05,$80,$02,$00,$05,$80,$02,$00,$05,$80,$02,$00
    .byte $05,$80,$00,$00,$05,$80,$00,$00,$05,$80,$00,$00,$05,$A6,$00,$00
    .byte $05,$AA,$00,$00,$05,$AA,$00,$00,$05,$2A,$00,$00,$05,$2A,$00,$00
    .byte $05,$0A,$00,$00
sprite_91:
    .byte $12,$1F,$06,$0B,$0B,$0B,$0B,$0B,$0B,$0C,$01,$00,$00,$00,$00,$00
    .byte $0E,$00,$00,$0A,$00,$00,$0E,$00,$80,$2A,$00,$00,$0E,$00,$80,$2A
    .byte $00,$00,$0E,$00,$80,$2A,$00,$00,$0E,$00,$80,$2A,$00,$00,$0D,$00
    .byte $80,$2A,$00,$00,$0D,$00,$80,$2A,$00,$00,$0D,$00,$80,$2A,$00,$00
    .byte $0D,$00,$80,$2A,$00,$00,$0D,$00,$80,$2A,$00,$00,$0D,$00,$80,$2A
    .byte $00,$00,$06,$00,$80,$2A,$00,$00,$06,$00,$A0,$AA,$00,$00,$06,$00
    .byte $A8,$AA,$02,$00,$06,$00,$A8,$AA,$02,$00,$06,$00,$98,$AA,$02,$00
    .byte $06,$00,$68,$A5,$02,$00,$06,$00,$AA,$AA,$0A,$00,$06,$00,$AA,$AA
    .byte $0A,$00,$06,$00,$AA,$AA,$0A,$00,$06,$00,$AA,$AA,$0A,$00,$06,$00
    .byte $AA,$AA,$0A,$00,$06,$00,$AA,$AA,$0A,$00,$06,$00,$A8,$AA,$02,$00
    .byte $06,$00,$A0,$AA,$00,$00,$06,$00,$A0,$AA,$00,$00,$06,$00,$A0,$AA
    .byte $00,$00,$06,$00,$A0,$AA,$00,$00,$06,$00,$60,$95,$00,$00,$06,$00
    .byte $60,$95,$00,$00,$06,$00,$60,$95,$00,$00
sprite_94:
    .byte $09,$0D,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$02,$00,$05,$80,$00,$00,$05,$00,$02,$00,$05,$80,$02,$00
    .byte $05,$80,$02,$00,$05,$00,$02,$00,$05,$80,$0A,$00,$05,$80,$0A,$00
    .byte $05,$80,$0A,$00,$05,$80,$0A,$00,$05,$80,$0A,$00,$05,$80,$0A,$00
    .byte $05,$80,$0A,$00
sprite_95:
    .byte $09,$0D,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$02,$00,$05,$00,$0A,$00,$05,$00,$02,$00,$05,$00,$02,$00
    .byte $05,$80,$02,$00,$05,$00,$02,$00,$05,$80,$0A,$00,$05,$80,$0A,$00
    .byte $05,$80,$0A,$00,$05,$80,$0A,$00,$05,$80,$0A,$00,$05,$80,$0A,$00
    .byte $05,$80,$0A,$00
sprite_96:
    .byte $0C,$07,$04,$07,$07,$08,$08,$08,$08,$08,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$A0,$00,$05,$00,$AA,$02,$05,$00,$AA,$02,$05,$80,$AA,$02
    .byte $05,$00,$AA,$02,$05,$80,$AA,$02,$05,$00,$A0,$00
sprite_97:
    .byte $0C,$07,$04,$07,$07,$08,$08,$08,$08,$08,$01,$00,$00,$00,$00,$00
    .byte $05,$80,$02,$00,$05,$80,$9A,$02,$05,$80,$AA,$00,$05,$80,$AA,$02
    .byte $05,$80,$AA,$00,$05,$80,$AA,$00,$05,$80,$02,$00
sprite_98:
    .byte $09,$0D,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$A8,$00,$00,$05,$98,$00,$00,$05,$56,$02,$00,$05,$56,$02,$00
    .byte $05,$5A,$02,$00,$05,$6A,$09,$00,$05,$9A,$29,$00,$05,$9A,$AA,$00
    .byte $05,$00,$28,$00,$05,$00,$AA,$00,$05,$80,$AA,$00,$05,$A0,$96,$00
    .byte $05,$80,$02,$00
sprite_99:
    .byte $09,$0F,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$A0,$00,$00,$05,$A0,$25,$00,$05,$58,$A6,$00,$05,$58,$2A,$00
    .byte $05,$58,$AA,$00,$05,$98,$A9,$00,$05,$96,$96,$00,$05,$A6,$02,$00
    .byte $05,$AA,$00,$00,$05,$9A,$00,$00,$05,$0A,$00,$00,$05,$0A,$00,$00
    .byte $05,$0A,$00,$00,$05,$02,$00,$00,$05,$02,$00,$00
sprite_100:
    .byte $09,$0D,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$A8,$00,$05,$00,$98,$00,$05,$00,$56,$02,$05,$00,$56,$02
    .byte $05,$00,$96,$02,$05,$80,$A5,$02,$05,$A0,$99,$02,$05,$A8,$9A,$02
    .byte $05,$A0,$00,$00,$05,$A8,$02,$00,$05,$A8,$0A,$00,$05,$58,$2A,$00
    .byte $05,$00,$0A,$00
sprite_101:
    .byte $09,$0F,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$28,$00,$05,$60,$29,$00,$05,$68,$96,$00,$05,$A0,$96,$00
    .byte $05,$A8,$96,$00,$05,$A8,$99,$00,$05,$58,$5A,$02,$05,$00,$6A,$02
    .byte $05,$00,$A8,$02,$05,$00,$98,$02,$05,$00,$80,$02,$05,$00,$80,$02
    .byte $05,$00,$00,$02,$05,$00,$00,$02,$05,$00,$00,$02
sprite_102:
    .byte $09,$11,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$A8,$00,$00,$05,$98,$00,$00,$05,$56,$02,$00,$05,$56,$02,$00
    .byte $05,$5A,$02,$00,$05,$6A,$09,$00,$05,$9A,$09,$00,$05,$9A,$0A,$00
    .byte $05,$00,$08,$00,$05,$80,$0A,$00,$05,$A0,$0A,$00,$05,$80,$2A,$00
    .byte $05,$00,$A8,$00,$05,$00,$A0,$00,$05,$00,$20,$00,$05,$00,$A0,$00
    .byte $05,$00,$A0,$00
sprite_103:
    .byte $09,$11,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$A8,$00,$05,$00,$98,$00,$05,$00,$56,$02,$05,$00,$56,$02
    .byte $05,$00,$96,$02,$05,$80,$A5,$02,$05,$80,$99,$02,$05,$80,$9A,$02
    .byte $05,$80,$00,$00,$05,$80,$0A,$00,$05,$80,$2A,$00,$05,$A0,$0A,$00
    .byte $05,$A8,$00,$00,$05,$28,$00,$00,$05,$20,$00,$00,$05,$28,$00,$00
    .byte $05,$28,$00,$00
sprite_110:
    .byte $15,$14,$07,$0C,$0D,$0D,$0D,$0D,$0D,$0D,$01,$00,$00,$00,$00,$00
    .byte $0E,$00,$80,$0A,$00,$00,$00,$0E,$00,$80,$0A,$00,$00,$00,$0E,$00
    .byte $80,$2A,$00,$00,$00,$0E,$00,$00,$00,$00,$00,$00,$0E,$00,$A0,$AA
    .byte $00,$00,$00,$0D,$00,$A0,$AA,$02,$00,$00,$0D,$00,$A0,$AA,$02,$00
    .byte $00,$0D,$00,$A0,$AA,$02,$00,$00,$0D,$00,$A0,$AA,$0A,$00,$00,$0D
    .byte $00,$A0,$AA,$0A,$00,$00,$0D,$00,$A0,$AA,$0A,$00,$00,$06,$00,$A0
    .byte $AA,$2A,$00,$00,$06,$00,$A0,$AA,$2A,$00,$00,$06,$00,$A8,$AA,$2A
    .byte $00,$00,$06,$00,$68,$AA,$2A,$00,$00,$06,$00,$68,$A9,$AA,$00,$00
    .byte $06,$00,$5A,$A9,$AA,$00,$00,$06,$00,$5A,$65,$95,$00,$00,$06,$00
    .byte $5A,$65,$55,$02,$00,$06,$00,$5A,$A5,$55,$02,$00
sprite_111:
    .byte $15,$12,$07,$0C,$0D,$0D,$0D,$0D,$0D,$0D,$01,$00,$00,$00,$00,$00
    .byte $01,$00,$AA,$2A,$00,$00,$00,$01,$00,$AA,$AA,$00,$00,$00,$01,$80
    .byte $AA,$AA,$00,$00,$00,$01,$80,$AA,$AA,$02,$00,$00,$01,$80,$5A,$AA
    .byte $02,$00,$00,$01,$80,$6A,$A9,$02,$00,$00,$01,$00,$AA,$A5,$0A,$00
    .byte $00,$01,$00,$A8,$95,$0A,$00,$00,$01,$00,$A0,$56,$2A,$00,$00,$01
    .byte $00,$80,$5A,$2A,$00,$00,$04,$00,$80,$5A,$2A,$00,$00,$04,$00,$00
    .byte $6A,$2A,$00,$00,$04,$00,$00,$6A,$A5,$00,$00,$04,$00,$80,$66,$A5
    .byte $00,$00,$04,$00,$80,$5A,$A5,$00,$00,$04,$00,$80,$56,$65,$02,$00
    .byte $04,$00,$00,$00,$60,$02,$00,$04,$00,$00,$00,$80,$02,$00
.segment "ASSETS"
sprite_40:
    .byte 15,31,2,9,9,9,9,10,10,10,2,0,0,9,0,0
    .word native_row_0
    .word native_row_1
    .word native_row_1
    .word native_row_1
    .word native_row_1
    .word native_row_2
    .word native_row_3
    .word native_row_3
    .word native_row_4
    .word native_row_5
    .word native_row_6
    .word native_row_7
    .word native_row_8
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
    .word native_row_12
    .word native_row_11
    .word native_row_20
    .word native_row_20
    .word native_row_21
    .word native_row_22
    .word native_row_23
sprite_41:
    .byte 12,31,2,7,7,8,8,8,8,8,2,0,0,7,0,0
    .word native_row_24
    .word native_row_25
    .word native_row_26
    .word native_row_26
    .word native_row_26
    .word native_row_27
    .word native_row_28
    .word native_row_29
    .word native_row_30
    .word native_row_31
    .word native_row_32
    .word native_row_33
    .word native_row_34
    .word native_row_35
    .word native_row_36
    .word native_row_37
    .word native_row_38
    .word native_row_39
    .word native_row_40
    .word native_row_41
    .word native_row_42
    .word native_row_42
    .word native_row_42
    .word native_row_42
    .word native_row_42
    .word native_row_42
    .word native_row_43
    .word native_row_43
    .word native_row_44
    .word native_row_44
    .word native_row_44
sprite_42:
    .byte 12,31,2,7,7,8,8,8,8,8,2,0,0,7,0,0
    .word native_row_45
    .word native_row_25
    .word native_row_46
    .word native_row_46
    .word native_row_46
    .word native_row_47
    .word native_row_48
    .word native_row_49
    .word native_row_48
    .word native_row_48
    .word native_row_50
    .word native_row_51
    .word native_row_52
    .word native_row_53
    .word native_row_54
    .word native_row_54
    .word native_row_55
    .word native_row_56
    .word native_row_57
    .word native_row_58
    .word native_row_59
    .word native_row_60
    .word native_row_60
    .word native_row_61
    .word native_row_62
    .word native_row_63
    .word native_row_64
    .word native_row_65
    .word native_row_66
    .word native_row_67
    .word native_row_68
sprite_43:
    .byte 15,31,2,9,9,9,9,10,10,10,2,0,0,9,0,0
    .word native_row_69
    .word native_row_70
    .word native_row_70
    .word native_row_70
    .word native_row_70
    .word native_row_70
    .word native_row_70
    .word native_row_70
    .word native_row_70
    .word native_row_71
    .word native_row_71
    .word native_row_71
    .word native_row_72
    .word native_row_73
    .word native_row_74
    .word native_row_75
    .word native_row_76
    .word native_row_77
    .word native_row_78
    .word native_row_79
    .word native_row_79
    .word native_row_80
    .word native_row_81
    .word native_row_82
    .word native_row_83
    .word native_row_83
    .word native_row_84
    .word native_row_84
    .word native_row_85
    .word native_row_85
    .word native_row_86
sprite_44:
    .byte 21,24,2,12,13,13,13,13,13,13,2,0,0,12,0,0
    .word native_row_87
    .word native_row_88
    .word native_row_89
    .word native_row_89
    .word native_row_88
    .word native_row_90
    .word native_row_91
    .word native_row_92
    .word native_row_93
    .word native_row_94
    .word native_row_95
    .word native_row_96
    .word native_row_97
    .word native_row_97
    .word native_row_98
    .word native_row_99
    .word native_row_99
    .word native_row_100
    .word native_row_100
    .word native_row_101
    .word native_row_101
    .word native_row_102
    .word native_row_103
    .word native_row_102
sprite_45:
    .byte 18,24,2,11,11,11,11,11,11,12,2,0,0,11,0,0
    .word native_row_104
    .word native_row_105
    .word native_row_106
    .word native_row_106
    .word native_row_106
    .word native_row_107
    .word native_row_108
    .word native_row_109
    .word native_row_110
    .word native_row_111
    .word native_row_112
    .word native_row_113
    .word native_row_114
    .word native_row_114
    .word native_row_114
    .word native_row_115
    .word native_row_115
    .word native_row_115
    .word native_row_116
    .word native_row_116
    .word native_row_117
    .word native_row_118
    .word native_row_118
    .word native_row_118
sprite_46:
    .byte 12,26,2,7,7,8,8,8,8,8,2,0,0,7,0,0
    .word native_row_119
    .word native_row_120
    .word native_row_119
    .word native_row_119
    .word native_row_121
    .word native_row_119
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_123
    .word native_row_124
    .word native_row_124
    .word native_row_125
    .word native_row_126
    .word native_row_126
    .word native_row_127
    .word native_row_128
    .word native_row_128
    .word native_row_128
    .word native_row_129
    .word native_row_125
    .word native_row_130
sprite_47:
    .byte 12,26,2,7,7,8,8,8,8,8,2,0,0,7,0,0
    .word native_row_131
    .word native_row_131
    .word native_row_131
    .word native_row_131
    .word native_row_132
    .word native_row_133
    .word native_row_133
    .word native_row_133
    .word native_row_133
    .word native_row_133
    .word native_row_133
    .word native_row_133
    .word native_row_133
    .word native_row_133
    .word native_row_134
    .word native_row_135
    .word native_row_129
    .word native_row_129
    .word native_row_129
    .word native_row_136
    .word native_row_137
    .word native_row_137
    .word native_row_137
    .word native_row_129
    .word native_row_138
    .word native_row_139
sprite_48:
    .byte 12,26,2,7,7,8,8,8,8,8,2,0,0,7,0,0
    .word native_row_140
    .word native_row_121
    .word native_row_121
    .word native_row_121
    .word native_row_141
    .word native_row_141
    .word native_row_141
    .word native_row_141
    .word native_row_141
    .word native_row_141
    .word native_row_142
    .word native_row_141
    .word native_row_141
    .word native_row_141
    .word native_row_140
    .word native_row_143
    .word native_row_144
    .word native_row_144
    .word native_row_144
    .word native_row_145
    .word native_row_146
    .word native_row_146
    .word native_row_146
    .word native_row_144
    .word native_row_147
    .word native_row_148
sprite_49:
    .byte 12,26,2,7,7,8,8,8,8,8,2,0,0,7,0,0
    .word native_row_119
    .word native_row_119
    .word native_row_119
    .word native_row_119
    .word native_row_121
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_149
    .word native_row_149
    .word native_row_125
    .word native_row_150
    .word native_row_150
    .word native_row_127
    .word native_row_151
    .word native_row_151
    .word native_row_151
    .word native_row_150
    .word native_row_152
    .word native_row_153
sprite_50:
    .byte 12,26,2,7,7,8,8,8,8,8,2,0,0,7,0,0
    .word native_row_119
    .word native_row_120
    .word native_row_119
    .word native_row_119
    .word native_row_154
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_149
    .word native_row_131
    .word native_row_149
    .word native_row_131
    .word native_row_150
    .word native_row_150
    .word native_row_155
    .word native_row_127
    .word native_row_151
    .word native_row_156
    .word native_row_150
    .word native_row_150
    .word native_row_157
    .word native_row_157
sprite_51:
    .byte 15,26,2,9,9,9,9,10,10,10,2,0,0,9,0,0
    .word native_row_158
    .word native_row_158
    .word native_row_159
    .word native_row_160
    .word native_row_161
    .word native_row_162
    .word native_row_162
    .word native_row_162
    .word native_row_162
    .word native_row_162
    .word native_row_162
    .word native_row_162
    .word native_row_159
    .word native_row_159
    .word native_row_163
    .word native_row_164
    .word native_row_165
    .word native_row_166
    .word native_row_167
    .word native_row_168
    .word native_row_169
    .word native_row_170
    .word native_row_171
    .word native_row_172
    .word native_row_173
    .word native_row_174
sprite_52:
    .byte 15,26,2,9,9,9,9,10,10,10,2,0,0,9,0,0
    .word native_row_175
    .word native_row_176
    .word native_row_177
    .word native_row_177
    .word native_row_176
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_178
    .word native_row_179
    .word native_row_179
    .word native_row_180
    .word native_row_180
    .word native_row_181
    .word native_row_182
    .word native_row_183
    .word native_row_184
    .word native_row_185
    .word native_row_169
    .word native_row_186
    .word native_row_187
    .word native_row_188
    .word native_row_186
    .word native_row_189
    .word native_row_190
sprite_53:
    .byte 12,26,2,7,7,8,8,8,8,8,2,0,0,7,0,0
    .word native_row_119
    .word native_row_119
    .word native_row_119
    .word native_row_119
    .word native_row_121
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_120
    .word native_row_133
    .word native_row_120
    .word native_row_133
    .word native_row_154
    .word native_row_149
    .word native_row_125
    .word native_row_150
    .word native_row_150
    .word native_row_127
    .word native_row_151
    .word native_row_191
    .word native_row_192
    .word native_row_193
    .word native_row_194
    .word native_row_194
sprite_54:
    .byte 12,26,2,7,7,8,8,8,8,8,2,0,0,7,0,0
    .word native_row_119
    .word native_row_120
    .word native_row_119
    .word native_row_119
    .word native_row_121
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_132
    .word native_row_122
    .word native_row_195
    .word native_row_122
    .word native_row_195
    .word native_row_138
    .word native_row_196
    .word native_row_196
    .word native_row_153
    .word native_row_196
    .word native_row_136
    .word native_row_125
    .word native_row_130
    .word native_row_197
    .word native_row_197
sprite_55:
    .byte 15,26,2,9,9,9,9,10,10,10,2,0,0,9,0,0
    .word native_row_158
    .word native_row_158
    .word native_row_159
    .word native_row_160
    .word native_row_198
    .word native_row_199
    .word native_row_159
    .word native_row_200
    .word native_row_200
    .word native_row_159
    .word native_row_159
    .word native_row_200
    .word native_row_200
    .word native_row_200
    .word native_row_163
    .word native_row_164
    .word native_row_165
    .word native_row_166
    .word native_row_167
    .word native_row_168
    .word native_row_169
    .word native_row_170
    .word native_row_171
    .word native_row_172
    .word native_row_173
    .word native_row_174
sprite_56:
    .byte 15,26,2,9,9,9,9,10,10,10,2,0,0,9,0,0
    .word native_row_175
    .word native_row_176
    .word native_row_177
    .word native_row_177
    .word native_row_201
    .word native_row_202
    .word native_row_202
    .word native_row_177
    .word native_row_203
    .word native_row_177
    .word native_row_179
    .word native_row_180
    .word native_row_180
    .word native_row_180
    .word native_row_181
    .word native_row_182
    .word native_row_183
    .word native_row_184
    .word native_row_185
    .word native_row_169
    .word native_row_186
    .word native_row_187
    .word native_row_188
    .word native_row_186
    .word native_row_189
    .word native_row_190
sprite_57:
    .byte 12,26,2,7,7,8,8,8,8,8,2,0,0,7,0,0
    .word native_row_119
    .word native_row_119
    .word native_row_119
    .word native_row_119
    .word native_row_121
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_122
    .word native_row_195
    .word native_row_122
    .word native_row_124
    .word native_row_141
    .word native_row_124
    .word native_row_126
    .word native_row_126
    .word native_row_126
    .word native_row_128
    .word native_row_128
    .word native_row_196
    .word native_row_139
    .word native_row_204
    .word native_row_205
    .word native_row_205
sprite_58:
    .byte 18,16,2,11,11,11,11,11,11,12,2,0,0,11,0,0
    .word native_row_206
    .word native_row_207
    .word native_row_208
    .word native_row_209
    .word native_row_209
    .word native_row_210
    .word native_row_211
    .word native_row_212
    .word native_row_213
    .word native_row_214
    .word native_row_215
    .word native_row_216
    .word native_row_217
    .word native_row_218
    .word native_row_219
    .word native_row_219
sprite_59:
    .byte 18,16,2,11,11,11,11,11,11,12,2,0,0,11,0,0
    .word native_row_220
    .word native_row_220
    .word native_row_220
    .word native_row_206
    .word native_row_207
    .word native_row_221
    .word native_row_222
    .word native_row_223
    .word native_row_224
    .word native_row_221
    .word native_row_225
    .word native_row_226
    .word native_row_227
    .word native_row_228
    .word native_row_229
    .word native_row_229
sprite_60:
    .byte 15,16,2,9,9,9,9,10,10,10,2,0,0,9,0,0
    .word native_row_230
    .word native_row_230
    .word native_row_159
    .word native_row_231
    .word native_row_231
    .word native_row_232
    .word native_row_233
    .word native_row_175
    .word native_row_234
    .word native_row_198
    .word native_row_158
    .word native_row_235
    .word native_row_236
    .word native_row_237
    .word native_row_238
    .word native_row_239
sprite_61:
    .byte 18,16,2,11,11,11,11,11,11,12,2,0,0,11,0,0
    .word native_row_206
    .word native_row_240
    .word native_row_241
    .word native_row_242
    .word native_row_243
    .word native_row_244
    .word native_row_245
    .word native_row_246
    .word native_row_247
    .word native_row_248
    .word native_row_249
    .word native_row_216
    .word native_row_216
    .word native_row_250
    .word native_row_251
    .word native_row_252
sprite_36:
    .byte 9,18,2,6,6,6,6,6,6,6,2,0,0,6,0,0
    .word native_row_253
    .word native_row_253
    .word native_row_253
    .word native_row_253
    .word native_row_253
    .word native_row_254
    .word native_row_254
    .word native_row_253
    .word native_row_253
    .word native_row_253
    .word native_row_255
    .word native_row_255
    .word native_row_256
    .word native_row_257
    .word native_row_256
    .word native_row_257
    .word native_row_257
    .word native_row_256
sprite_37:
    .byte 9,18,2,6,6,6,6,6,6,6,2,0,0,6,0,0
    .word native_row_253
    .word native_row_258
    .word native_row_258
    .word native_row_259
    .word native_row_259
    .word native_row_259
    .word native_row_259
    .word native_row_255
    .word native_row_258
    .word native_row_259
    .word native_row_259
    .word native_row_259
    .word native_row_260
    .word native_row_256
    .word native_row_257
    .word native_row_256
    .word native_row_257
    .word native_row_256
sprite_72:
    .byte 3,6,2,2,2,2,3,3,3,3,2,0,0,2,0,0
    .word native_row_261
    .word native_row_262
    .word native_row_263
    .word native_row_262
    .word native_row_262
    .word native_row_264
sprite_73:
    .byte 3,6,2,2,2,2,3,3,3,3,2,0,0,2,0,0
    .word native_row_261
    .word native_row_264
    .word native_row_262
    .word native_row_263
    .word native_row_262
    .word native_row_264
.segment "ASSETEXTRA"
native_row_0:
    .byte $00,$00,$00,$00,$40,$00,$7F,$77,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_1:
    .byte $00,$00,$00,$00,$7C,$38,$7F,$77,$0F,$0E,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_2:
    .byte $00,$00,$00,$00,$7C,$34,$7F,$66,$0F,$0C,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_3:
    .byte $00,$00,$00,$00,$7C,$74,$7F,$66,$0F,$0D,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_4:
    .byte $00,$00,$00,$00,$7C,$74,$7F,$6E,$0F,$0D,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_5:
    .byte $00,$00,$00,$00,$70,$70,$7F,$60,$03,$01,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_6:
    .byte $00,$00,$00,$00,$70,$70,$7F,$6E,$03,$01,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_7:
    .byte $00,$00,$00,$00,$40,$40,$7F,$6E,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_8:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$00,$0F,$06,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_9:
    .byte $00,$00,$60,$40,$7F,$19,$7F,$21,$7F,$66,$01,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_10:
    .byte $00,$00,$60,$40,$7F,$19,$7F,$23,$7F,$66,$1F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_11:
    .byte $00,$00,$00,$00,$7F,$19,$7F,$23,$7F,$26,$7F,$4C,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_12:
    .byte $00,$00,$00,$00,$7F,$19,$7F,$33,$7F,$26,$7F,$4C,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_13:
    .byte $00,$00,$60,$40,$7F,$18,$7F,$23,$7F,$46,$7F,$4C,$03,$01,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_14:
    .byte $00,$00,$60,$40,$7F,$01,$7F,$33,$7F,$60,$7F,$4C,$03,$01,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_15:
    .byte $00,$00,$60,$40,$7F,$19,$7F,$23,$7F,$66,$7F,$48,$03,$01,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_16:
    .byte $00,$00,$60,$40,$7F,$19,$7F,$33,$7F,$66,$7F,$48,$03,$01,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_17:
    .byte $00,$00,$00,$00,$7F,$19,$7F,$23,$7F,$66,$7F,$48,$03,$01,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_18:
    .byte $00,$00,$00,$00,$7F,$19,$7F,$33,$7F,$26,$7F,$48,$03,$01,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_19:
    .byte $00,$00,$00,$00,$7F,$19,$7F,$23,$7F,$26,$7F,$0C,$03,$01,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_20:
    .byte $00,$00,$00,$00,$7F,$19,$7F,$33,$7F,$26,$1F,$0C,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_21:
    .byte $00,$00,$00,$00,$7F,$01,$7F,$22,$7F,$60,$07,$04,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_22:
    .byte $00,$00,$00,$00,$7F,$01,$7F,$32,$7F,$40,$07,$04,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_23:
    .byte $00,$00,$00,$00,$7F,$01,$7F,$22,$7F,$60,$01,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_24:
    .byte $00,$00,$00,$00,$7C,$38,$7F,$77,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_25:
    .byte $00,$00,$00,$00,$7C,$38,$7F,$77,$0F,$0E,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_26:
    .byte $00,$00,$60,$40,$7F,$3B,$7F,$77,$0F,$0E,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_27:
    .byte $00,$00,$00,$00,$7F,$47,$7F,$0E,$03,$01,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_28:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$6E,$0F,$0D,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_29:
    .byte $00,$00,$00,$00,$7C,$34,$7F,$6E,$0F,$0C,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_30:
    .byte $00,$00,$00,$00,$7C,$74,$7F,$6E,$03,$01,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_31:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$0E,$03,$01,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_32:
    .byte $00,$00,$00,$00,$7C,$34,$7F,$6E,$03,$01,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_33:
    .byte $00,$00,$00,$00,$7C,$74,$1F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_34:
    .byte $00,$00,$00,$00,$7C,$74,$07,$06,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_35:
    .byte $00,$00,$00,$00,$7C,$18,$1F,$13,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_36:
    .byte $00,$00,$00,$00,$7F,$19,$7F,$33,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_37:
    .byte $00,$00,$00,$00,$7F,$11,$7F,$33,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_38:
    .byte $00,$00,$60,$40,$7F,$09,$7F,$32,$03,$02,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_39:
    .byte $00,$00,$60,$40,$7F,$19,$7F,$21,$03,$02,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_40:
    .byte $00,$00,$60,$40,$7F,$19,$7F,$13,$03,$02,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_41:
    .byte $00,$00,$60,$40,$7F,$19,$7F,$33,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_42:
    .byte $00,$00,$60,$40,$7F,$19,$7F,$33,$03,$02,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_43:
    .byte $00,$00,$00,$00,$7F,$19,$7F,$33,$03,$02,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_44:
    .byte $00,$00,$00,$00,$7F,$01,$7F,$20,$03,$02,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_45:
    .byte $00,$00,$00,$00,$40,$00,$7F,$77,$0F,$0E,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_46:
    .byte $00,$00,$00,$00,$7C,$38,$7F,$77,$7F,$6E,$01,$01,$00,$00
.segment "ASSETEXTRA"
native_row_47:
    .byte $00,$00,$00,$00,$7C,$74,$7F,$6E,$7F,$5D,$01,$01,$00,$00
.segment "ASSETEXTRA"
native_row_48:
    .byte $00,$00,$00,$00,$7C,$74,$7F,$6E,$0F,$0D,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_49:
    .byte $00,$00,$00,$00,$7C,$34,$7F,$68,$0F,$0D,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_50:
    .byte $00,$00,$00,$00,$7C,$40,$7F,$6E,$0F,$0D,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_51:
    .byte $00,$00,$00,$00,$40,$40,$7F,$6E,$0F,$0D,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_52:
    .byte $00,$00,$00,$00,$00,$00,$78,$68,$0F,$0D,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_53:
    .byte $00,$00,$00,$00,$00,$00,$7E,$32,$0F,$06,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_54:
    .byte $00,$00,$00,$00,$70,$10,$7F,$33,$3F,$26,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_55:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$32,$7F,$60,$01,$00,$00,$00
.segment "ASSETEXTRA"
native_row_56:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$23,$7F,$66,$01,$00,$00,$00
.segment "ASSETEXTRA"
native_row_57:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$33,$7F,$46,$01,$00,$00,$00
.segment "ASSETEXTRA"
native_row_58:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$22,$7F,$66,$01,$00,$00,$00
.segment "ASSETEXTRA"
native_row_59:
    .byte $00,$00,$00,$00,$7C,$08,$7F,$13,$3F,$26,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_60:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$33,$7F,$64,$01,$00,$00,$00
.segment "ASSETEXTRA"
native_row_61:
    .byte $00,$00,$00,$00,$70,$10,$7F,$13,$7F,$66,$01,$00,$00,$00
.segment "ASSETEXTRA"
native_row_62:
    .byte $00,$00,$00,$00,$70,$10,$7F,$23,$3F,$26,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_63:
    .byte $00,$00,$00,$00,$70,$10,$7F,$31,$0F,$06,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_64:
    .byte $00,$00,$00,$00,$70,$10,$7F,$32,$3F,$22,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_65:
    .byte $00,$00,$00,$00,$40,$00,$7F,$13,$3F,$26,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_66:
    .byte $00,$00,$00,$00,$70,$10,$7F,$03,$3F,$20,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_67:
    .byte $00,$00,$00,$00,$7C,$08,$7F,$03,$3F,$20,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_68:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$01,$3F,$20,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_69:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$70,$60,$1F,$1D,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_70:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$6E,$7F,$5D,$03,$03,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_71:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7C,$5C,$7F,$3B,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_72:
    .byte $00,$00,$00,$00,$00,$00,$60,$20,$7F,$66,$7F,$4C,$0F,$09,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_73:
    .byte $00,$00,$00,$00,$00,$00,$7E,$32,$7F,$66,$7F,$4C,$3F,$19,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_74:
    .byte $00,$00,$00,$00,$40,$00,$7F,$31,$7F,$66,$7F,$4C,$0F,$09,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_75:
    .byte $00,$00,$00,$00,$70,$10,$7F,$03,$7F,$66,$7F,$4C,$3F,$10,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_76:
    .byte $00,$00,$00,$00,$70,$10,$7F,$33,$7F,$00,$7F,$00,$3F,$19,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_77:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$33,$7F,$66,$7F,$4C,$3F,$19,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_78:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$31,$7F,$66,$7F,$4C,$3F,$19,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_79:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$31,$7F,$66,$7F,$4C,$0F,$09,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_80:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$21,$7F,$66,$7F,$4C,$0F,$09,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_81:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$22,$7F,$66,$7F,$4C,$0F,$09,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_82:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$23,$7F,$66,$7F,$4C,$0F,$09,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_83:
    .byte $00,$00,$00,$00,$70,$10,$7F,$23,$7F,$66,$7F,$4C,$0F,$09,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_84:
    .byte $00,$00,$00,$00,$40,$00,$7F,$23,$7F,$66,$7F,$4C,$0F,$09,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_85:
    .byte $00,$00,$00,$00,$00,$00,$7E,$22,$7F,$00,$7F,$00,$0F,$08,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_86:
    .byte $00,$00,$00,$00,$00,$00,$78,$30,$7F,$00,$7F,$00,$0F,$08,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_87:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$7F,$6E,$1F,$1D,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_88:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$78,$70,$7F,$6E,$1F,$1D,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_89:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$78,$70,$7F,$6E,$7F,$5D,$03,$03,$00,$00
.segment "ASSETEXTRA"
native_row_90:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$40,$40,$7F,$6E,$7F,$5D,$1F,$1B,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_91:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$7C,$74,$7F,$6E,$7F,$5D,$1F,$1B,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_92:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$60,$20,$7F,$77,$7F,$6E,$7F,$5D,$1F,$1B,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_93:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$7E,$3A,$7F,$77,$7F,$6E,$7F,$5D,$1F,$1B,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_94:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$5D,$01,$01,$40,$00,$7F,$68,$7F,$5D,$1F,$1B,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_95:
    .byte $00,$00,$00,$00,$00,$00,$78,$68,$7F,$5D,$7F,$3B,$7F,$77,$07,$06,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_96:
    .byte $00,$00,$00,$00,$00,$00,$78,$30,$7F,$66,$7F,$4C,$7F,$19,$07,$03,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_97:
    .byte $00,$00,$00,$00,$40,$00,$7F,$33,$7F,$66,$7F,$4C,$7F,$19,$07,$03,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_98:
    .byte $00,$00,$00,$00,$40,$00,$7F,$33,$7F,$66,$7F,$4C,$3F,$19,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_99:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$33,$7F,$66,$7F,$4C,$3F,$19,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_100:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$33,$7F,$66,$7F,$4C,$03,$01,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_101:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$33,$7F,$66,$1F,$0C,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_102:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$03,$7F,$60,$01,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_103:
    .byte $00,$00,$00,$00,$7C,$18,$7F,$00,$7F,$60,$01,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_104:
    .byte $00,$00,$00,$00,$7C,$38,$7F,$77,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_105:
    .byte $00,$00,$60,$40,$7F,$3B,$7F,$77,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_106:
    .byte $00,$00,$60,$40,$7F,$3B,$7F,$77,$0F,$0E,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_107:
    .byte $00,$00,$60,$20,$7F,$77,$7F,$6E,$0F,$0D,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_108:
    .byte $00,$00,$60,$20,$7F,$77,$7F,$6E,$7F,$5D,$01,$01,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_109:
    .byte $00,$00,$60,$20,$7F,$77,$7F,$6E,$7F,$5D,$1F,$1B,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_110:
    .byte $00,$00,$00,$00,$7C,$74,$7F,$6E,$7F,$5D,$7F,$3B,$3F,$37,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_111:
    .byte $00,$00,$00,$00,$7C,$74,$7F,$06,$7F,$5D,$01,$01,$40,$40,$07,$06,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_112:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$5D,$7F,$3B,$7F,$77,$7F,$6E,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_113:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$66,$7F,$4C,$7F,$19,$7F,$33,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_114:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$66,$7F,$4C,$7F,$19,$7F,$33,$0F,$06,$00,$00,$00,$00
.segment "ASSETS"
native_row_115:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$70,$60,$7F,$4C,$7F,$19,$7F,$33,$0F,$06,$00,$00,$00,$00
.segment "ASSETS"
native_row_116:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$7E,$4C,$7F,$19,$7F,$33,$0F,$06,$00,$00,$00,$00
.segment "ASSETS"
native_row_117:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$60,$40,$7F,$19,$7F,$33,$0F,$06,$00,$00,$00,$00
.segment "ASSETS"
native_row_118:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$60,$40,$7F,$19,$7F,$30,$0F,$06,$00,$00,$00,$00
.segment "ASSETS"
native_row_119:
    .byte $00,$00,$60,$20,$7F,$44,$7F,$08,$7F,$11,$01,$00,$00,$00
.segment "ASSETS"
native_row_120:
    .byte $00,$00,$60,$20,$7F,$44,$7F,$00,$7F,$11,$01,$00,$00,$00
.segment "ASSETS"
native_row_121:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$08,$7F,$11,$01,$00,$00,$00
.segment "ASSETS"
native_row_122:
    .byte $00,$00,$60,$20,$7F,$04,$7F,$08,$7F,$11,$01,$00,$00,$00
.segment "ASSETS"
native_row_123:
    .byte $00,$00,$60,$20,$7F,$40,$7F,$08,$7F,$10,$01,$00,$00,$00
.segment "ASSETS"
native_row_124:
    .byte $00,$00,$00,$00,$7C,$04,$7F,$08,$0F,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_125:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$22,$7F,$44,$01,$00,$00,$00
.segment "ASSETS"
native_row_126:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$20,$7F,$44,$01,$00,$00,$00
.segment "ASSETS"
native_row_127:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$22,$0F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_128:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$20,$0F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_129:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$22,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_130:
    .byte $00,$00,$60,$00,$7F,$01,$7F,$22,$7F,$44,$01,$00,$00,$00
.segment "ASSETS"
native_row_131:
    .byte $00,$00,$60,$20,$7F,$44,$7F,$08,$0F,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_132:
    .byte $00,$00,$60,$20,$7F,$40,$7F,$08,$0F,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_133:
    .byte $00,$00,$60,$20,$7F,$44,$7F,$00,$0F,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_134:
    .byte $00,$00,$60,$20,$7F,$44,$7F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_135:
    .byte $00,$00,$60,$20,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_136:
    .byte $00,$00,$60,$00,$7F,$01,$7F,$22,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_137:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$20,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_138:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$22,$0F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_139:
    .byte $00,$00,$60,$00,$7F,$01,$7F,$22,$0F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_140:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$11,$01,$00,$00,$00
.segment "ASSETS"
native_row_141:
    .byte $00,$00,$00,$00,$7C,$04,$7F,$08,$7F,$11,$01,$00,$00,$00
.segment "ASSETS"
native_row_142:
    .byte $00,$00,$60,$20,$7F,$40,$7F,$08,$7F,$11,$01,$00,$00,$00
.segment "ASSETS"
native_row_143:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$11,$01,$00,$00,$00
.segment "ASSETS"
native_row_144:
    .byte $00,$00,$00,$00,$40,$00,$7F,$22,$7F,$44,$01,$00,$00,$00
.segment "ASSETS"
native_row_145:
    .byte $00,$00,$00,$00,$40,$00,$7F,$22,$7F,$40,$01,$00,$00,$00
.segment "ASSETS"
native_row_146:
    .byte $00,$00,$00,$00,$40,$00,$7F,$02,$7F,$44,$01,$00,$00,$00
.segment "ASSETS"
native_row_147:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$22,$7F,$44,$01,$00,$00,$00
.segment "ASSETS"
native_row_148:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$22,$7F,$40,$01,$00,$00,$00
.segment "ASSETS"
native_row_149:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$00,$0F,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_150:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$02,$7F,$44,$01,$00,$00,$00
.segment "ASSETS"
native_row_151:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$02,$0F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_152:
    .byte $00,$00,$60,$00,$7F,$01,$7F,$02,$7F,$44,$01,$00,$00,$00
.segment "ASSETS"
native_row_153:
    .byte $00,$00,$60,$00,$7F,$01,$7F,$02,$0F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_154:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$00,$7F,$11,$01,$00,$00,$00
.segment "ASSETS"
native_row_155:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$22,$7F,$40,$01,$00,$00,$00
.segment "ASSETS"
native_row_156:
    .byte $00,$00,$00,$00,$40,$00,$7F,$02,$0F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_157:
    .byte $00,$00,$00,$00,$7C,$10,$07,$02,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_158:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$11,$7F,$22,$03,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_159:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$11,$7F,$22,$3F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_160:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$11,$7F,$02,$3F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_161:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$11,$7F,$20,$03,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_162:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$11,$7F,$20,$3F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_163:
    .byte $00,$00,$00,$00,$40,$40,$7F,$00,$7F,$01,$7F,$22,$03,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_164:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$01,$7F,$22,$03,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_165:
    .byte $00,$00,$00,$00,$40,$00,$7F,$22,$7F,$04,$7F,$08,$3F,$11,$00,$00,$00,$00
.segment "ASSETS"
native_row_166:
    .byte $00,$00,$00,$00,$00,$00,$78,$20,$7F,$04,$7F,$08,$3F,$11,$00,$00,$00,$00
.segment "ASSETS"
native_row_167:
    .byte $00,$00,$00,$00,$40,$00,$7F,$02,$7F,$04,$7F,$08,$3F,$11,$00,$00,$00,$00
.segment "ASSETS"
native_row_168:
    .byte $00,$00,$00,$00,$40,$00,$7F,$02,$7F,$04,$7F,$08,$03,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_169:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$22,$7F,$40,$7F,$08,$03,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_170:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$02,$7F,$40,$7F,$08,$03,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_171:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$22,$7F,$40,$1F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_172:
    .byte $00,$00,$00,$00,$40,$00,$7F,$22,$7F,$40,$7F,$08,$03,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_173:
    .byte $00,$00,$00,$00,$40,$00,$7F,$22,$7F,$44,$7F,$08,$3F,$11,$00,$00,$00,$00
.segment "ASSETS"
native_row_174:
    .byte $00,$00,$00,$00,$40,$00,$7F,$22,$7F,$44,$7F,$00,$3F,$11,$00,$00,$00,$00
.segment "ASSETS"
native_row_175:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$11,$01,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_176:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$08,$7F,$11,$01,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_177:
    .byte $00,$00,$60,$20,$7F,$44,$7F,$08,$7F,$11,$01,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_178:
    .byte $00,$00,$60,$20,$7F,$04,$7F,$08,$7F,$11,$01,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_179:
    .byte $00,$00,$60,$20,$7F,$44,$7F,$08,$7F,$11,$1F,$02,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_180:
    .byte $00,$00,$60,$20,$7F,$44,$7F,$00,$7F,$11,$1F,$02,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_181:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$00,$7F,$11,$1F,$02,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_182:
    .byte $00,$00,$60,$20,$7F,$44,$7F,$00,$7F,$11,$7F,$22,$03,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_183:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$02,$7F,$44,$7F,$08,$03,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_184:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$22,$7F,$44,$1F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_185:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$02,$7F,$44,$7F,$00,$03,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_186:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$22,$7F,$00,$7F,$08,$03,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_187:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$22,$7F,$00,$7F,$08,$3F,$11,$00,$00,$00,$00
.segment "ASSETS"
native_row_188:
    .byte $00,$00,$00,$00,$40,$00,$7F,$22,$7F,$00,$7F,$08,$3F,$11,$00,$00,$00,$00
.segment "ASSETS"
native_row_189:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$22,$7F,$40,$7F,$08,$03,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_190:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$20,$7F,$40,$1F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_191:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$02,$7F,$44,$01,$00,$00,$00
.segment "ASSETS"
native_row_192:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$02,$7F,$40,$01,$00,$00,$00
.segment "ASSETS"
native_row_193:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$02,$0F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_194:
    .byte $00,$00,$60,$00,$7F,$01,$07,$02,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_195:
    .byte $00,$00,$60,$20,$7F,$04,$7F,$08,$0F,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_196:
    .byte $00,$00,$60,$00,$7F,$11,$7F,$20,$0F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_197:
    .byte $00,$00,$00,$00,$00,$00,$78,$20,$0F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_198:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$10,$7F,$22,$03,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_199:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$10,$7F,$22,$3F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_200:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$01,$7F,$22,$3F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_201:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$00,$7F,$10,$01,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_202:
    .byte $00,$00,$60,$20,$7F,$44,$7F,$08,$7F,$10,$01,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_203:
    .byte $00,$00,$60,$20,$7F,$44,$7F,$00,$7F,$11,$01,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_204:
    .byte $00,$00,$00,$00,$7C,$10,$7F,$20,$7F,$44,$01,$00,$00,$00
.segment "ASSETS"
native_row_205:
    .byte $00,$00,$00,$00,$00,$00,$78,$20,$7F,$40,$01,$00,$00,$00
.segment "ASSETS"
native_row_206:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$11,$7F,$22,$3F,$04,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_207:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$11,$7F,$22,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_208:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$11,$7F,$22,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_209:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$11,$7F,$22,$7F,$44,$7F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_210:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$10,$7F,$20,$7F,$40,$7F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_211:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$01,$7F,$00,$7F,$44,$7F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_212:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$01,$7F,$00,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_213:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$10,$7F,$20,$3F,$04,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_214:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$11,$7F,$00,$3F,$04,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_215:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$11,$7F,$20,$3F,$04,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_216:
    .byte $00,$00,$00,$00,$00,$00,$78,$20,$7F,$44,$7F,$00,$3F,$11,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_217:
    .byte $00,$00,$00,$00,$00,$00,$78,$20,$7F,$44,$7F,$08,$7F,$10,$07,$02,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_218:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$04,$7F,$00,$3F,$11,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_219:
    .byte $00,$00,$00,$00,$40,$00,$7F,$22,$7F,$04,$7F,$00,$7F,$10,$07,$02,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_220:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$11,$7F,$22,$03,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_221:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$11,$7F,$22,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_222:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$60,$20,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_223:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$7E,$22,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_224:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$70,$10,$7F,$02,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_225:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$10,$7F,$22,$3F,$04,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_226:
    .byte $00,$00,$00,$00,$00,$00,$78,$20,$7F,$04,$1F,$08,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_227:
    .byte $00,$00,$00,$00,$00,$00,$78,$20,$0F,$04,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_228:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$44,$01,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_229:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$44,$1F,$08,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_230:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$11,$7F,$22,$3F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_231:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$11,$7F,$22,$3F,$04,$00,$00,$00,$00
.segment "ASSETS"
native_row_232:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$11,$7F,$22,$03,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_233:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$0F,$01,$00,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_234:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$11,$1F,$02,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_235:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$70,$40,$7F,$00,$3F,$11,$00,$00,$00,$00
.segment "ASSETS"
native_row_236:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$7E,$08,$3F,$11,$00,$00,$00,$00
.segment "ASSETS"
native_row_237:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$7E,$08,$03,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_238:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$44,$7F,$08,$03,$01,$00,$00,$00,$00
.segment "ASSETS"
native_row_239:
    .byte $00,$00,$00,$00,$00,$00,$00,$00,$7F,$44,$1F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_240:
    .byte $00,$00,$00,$00,$40,$40,$7F,$00,$7F,$11,$7F,$22,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_241:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$01,$7F,$22,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_242:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$08,$7F,$01,$7F,$22,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_243:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$08,$7F,$01,$7F,$22,$7F,$44,$7F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_244:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$11,$7F,$20,$7F,$44,$7F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_245:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$00,$7F,$11,$7F,$20,$7F,$04,$7F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_246:
    .byte $00,$00,$00,$00,$7C,$44,$7F,$08,$7F,$01,$7F,$20,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_247:
    .byte $00,$00,$00,$00,$40,$40,$7F,$00,$7F,$01,$7F,$00,$7F,$44,$7F,$08,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_248:
    .byte $00,$00,$00,$00,$40,$40,$7F,$08,$7F,$01,$7F,$20,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_249:
    .byte $00,$00,$00,$00,$00,$00,$78,$08,$7F,$10,$7F,$20,$7F,$44,$07,$00,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_250:
    .byte $00,$00,$00,$00,$40,$00,$7F,$02,$7F,$00,$7F,$00,$7F,$10,$07,$02,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_251:
    .byte $00,$00,$00,$00,$40,$00,$7F,$02,$7F,$04,$7F,$00,$7F,$01,$07,$02,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_252:
    .byte $00,$00,$00,$00,$40,$00,$7F,$22,$7F,$04,$7F,$00,$7F,$11,$07,$02,$00,$00,$00,$00,$00,$00
.segment "ASSETEXTRA"
native_row_253:
    .byte $00,$00,$00,$00,$3C,$38,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_254:
    .byte $00,$00,$60,$40,$3F,$3B,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_255:
    .byte $00,$00,$60,$40,$7F,$03,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_256:
    .byte $00,$00,$60,$00,$7F,$33,$07,$06,$00,$00,$00,$00
.segment "ASSETS"
native_row_257:
    .byte $00,$00,$60,$00,$7F,$03,$07,$06,$00,$00,$00,$00
.segment "ASSETS"
native_row_258:
    .byte $00,$00,$00,$00,$40,$00,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_259:
    .byte $00,$00,$00,$00,$7C,$38,$07,$07,$00,$00,$00,$00
.segment "ASSETS"
native_row_260:
    .byte $00,$00,$60,$00,$3F,$33,$00,$00,$00,$00,$00,$00
.segment "ASSETS"
native_row_261:
    .byte $70,$40,$01,$01
.segment "ASSETS"
native_row_262:
    .byte $7F,$0C,$1F,$18
.segment "ASSETS"
native_row_263:
    .byte $7F,$4C,$1F,$19
.segment "ASSETS"
native_row_264:
    .byte $70,$40,$1F,$19
.segment "ASSETS"
sprite_1:
    .byte $0C,$12,$04,$07,$07,$08,$08,$08,$08,$08,$01,$00,$00,$00,$00,$00
    .byte $0F,$AA,$AA,$AA,$0F,$56,$55,$95,$0F,$AA,$AA,$9A,$0F,$56,$55,$95
    .byte $0F,$66,$A6,$99,$0F,$AA,$9A,$AA,$0F,$9A,$99,$A6,$0F,$A6,$69,$9A
    .byte $0F,$A8,$69,$2A,$0F,$A8,$69,$2A,$0F,$68,$AA,$29,$0F,$68,$AA,$29
    .byte $0F,$68,$A6,$29,$0F,$A0,$AA,$0A,$0F,$58,$55,$25,$0F,$A0,$AA,$0A
    .byte $0F,$58,$55,$25,$0F,$A0,$AA,$0A
sprite_2:
    .byte $0C,$11,$04,$07,$07,$08,$08,$08,$08,$08,$01,$00,$00,$00,$00,$00
    .byte $0F,$A0,$AA,$0A,$0F,$A0,$AA,$2A,$0F,$A8,$AA,$26,$0F,$A8,$AA,$26
    .byte $0F,$A8,$AA,$26,$0F,$A8,$AA,$26,$0F,$A0,$AA,$0A,$0F,$58,$55,$25
    .byte $0F,$A8,$69,$2A,$0F,$9A,$69,$A6,$0F,$9A,$69,$A6,$0F,$9A,$69,$A6
    .byte $0F,$AA,$AA,$AA,$0F,$56,$55,$95,$0F,$56,$55,$95,$0F,$56,$55,$95
    .byte $0F,$AA,$AA,$AA
sprite_3:
    .byte $09,$18,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$A0,$0A,$00,$0F,$60,$29,$00,$0F,$98,$26,$00,$0F,$98,$29,$00
    .byte $0F,$58,$29,$00,$0F,$60,$9A,$00,$0F,$60,$99,$00,$0F,$A8,$2A,$00
    .byte $0F,$56,$99,$00,$0F,$96,$9A,$00,$0F,$56,$2A,$00,$0F,$6A,$29,$00
    .byte $0F,$56,$9A,$00,$0F,$9A,$99,$00,$0F,$56,$9A,$00,$0F,$A6,$A9,$00
    .byte $0F,$5A,$99,$00,$0F,$9A,$AA,$00,$0F,$A8,$AA,$00,$0F,$00,$A0,$00
    .byte $0F,$00,$A0,$00,$0F,$00,$A0,$00,$0F,$00,$A0,$00,$0F,$00,$80,$00
sprite_4:
    .byte $09,$15,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0F,$80,$2A,$00,$0F,$A0,$25,$00,$0F,$60,$9A,$00,$0F,$A0,$A5,$00
    .byte $0F,$A0,$26,$00,$0F,$98,$25,$00,$0F,$98,$AA,$00,$0F,$98,$A6,$02
    .byte $0F,$98,$55,$02,$0F,$A0,$69,$02,$0F,$A0,$A5,$02,$0F,$98,$55,$02
    .byte $0F,$98,$9A,$02,$0F,$A8,$65,$02,$0F,$98,$55,$02,$0F,$A8,$66,$02
    .byte $0F,$98,$59,$02,$0F,$A8,$AA,$00,$0F,$28,$00,$00,$0F,$28,$00,$00
    .byte $0F,$28,$00,$00
sprite_5:
    .byte $15,$47,$07,$0C,$0D,$0D,$0D,$0D,$0D,$0D,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$A8,$AA,$AA,$00,$00,$05,$00,$58,$5A,$96,$00,$00,$05,$00
    .byte $58,$55,$95,$00,$00,$05,$00,$68,$A6,$95,$00,$00,$05,$00,$5A,$59
    .byte $99,$02,$00,$05,$00,$9A,$65,$A6,$0A,$00,$05,$80,$65,$55,$65,$09
    .byte $00,$05,$00,$66,$9A,$A9,$09,$00,$05,$80,$69,$65,$65,$0A,$00,$05
    .byte $A0,$95,$65,$9A,$09,$00,$05,$98,$96,$AA,$5A,$29,$00,$05,$98,$65
    .byte $55,$65,$2A,$00,$05,$68,$5A,$55,$95,$9A,$00,$05,$58,$5A,$55,$95
    .byte $A5,$00,$05,$58,$56,$55,$55,$AA,$00,$05,$98,$56,$55,$55,$95,$00
    .byte $05,$66,$56,$55,$55,$A6,$00,$05,$A6,$55,$55,$55,$59,$02,$05,$9A
    .byte $55,$55,$55,$99,$02,$05,$56,$55,$55,$55,$65,$02,$05,$9A,$55,$55
    .byte $55,$A9,$02,$05,$96,$55,$55,$55,$59,$02,$05,$A8,$55,$55,$55,$A9
    .byte $00,$05,$96,$55,$55,$55,$59,$02,$05,$AA,$55,$55,$55,$69,$02,$05
    .byte $96,$55,$55,$55,$99,$02,$05,$A6,$55,$55,$55,$99,$02,$05,$96,$55
    .byte $55,$55,$69,$02,$05,$9A,$55,$55,$55,$59,$02,$05,$96,$55,$55,$55
    .byte $59,$02,$05,$A8,$55,$55,$55,$A9,$00,$05,$96,$55,$55,$55,$69,$02
    .byte $05,$A6,$55,$55,$55,$59,$02,$05,$96,$55,$55,$55,$99,$02,$05,$9A
    .byte $55,$55,$55,$59,$02,$05,$A6,$55,$55,$55,$A9,$02,$05,$96,$55,$55
    .byte $55,$59,$02,$05,$9A,$55,$55,$55,$59,$02,$05,$A8,$55,$55,$55,$A9
    .byte $00,$05,$96,$55,$55,$55,$59,$02,$05,$9A,$55,$55,$55,$99,$02,$05
    .byte $A6,$55,$55,$55,$69,$02,$05,$96,$55,$55,$55,$59,$02,$05,$AA,$55
    .byte $55,$55,$99,$02,$05,$96,$55,$55,$55,$59,$02,$05,$9A,$55,$55,$55
    .byte $59,$02,$05,$A8,$55,$55,$55,$A9,$00,$05,$96,$55,$55,$55,$59,$02
    .byte $05,$A6,$55,$55,$55,$69,$02,$05,$96,$55,$55,$55,$59,$02,$05,$AA
    .byte $55,$55,$55,$59,$02,$05,$96,$55,$55,$55,$99,$02,$05,$96,$55,$55
    .byte $55,$59,$02,$05,$A6,$55,$55,$55,$59,$02,$05,$A8,$55,$55,$55,$A9
    .byte $00,$05,$A6,$55,$55,$55,$59,$02,$05,$96,$55,$55,$55,$59,$02,$05
    .byte $9A,$55,$55,$55,$69,$02,$05,$A6,$55,$55,$55,$59,$02,$05,$96,$55
    .byte $55,$55,$99,$02,$05,$9A,$55,$55,$55,$59,$02,$05,$96,$55,$55,$55
    .byte $69,$02,$05,$A8,$55,$55,$55,$A9,$00,$05,$96,$55,$55,$55,$59,$02
    .byte $05,$AA,$55,$55,$55,$59,$02,$05,$96,$55,$55,$55,$99,$02,$05,$9A
    .byte $55,$55,$55,$59,$02,$05,$96,$55,$55,$55,$69,$02,$05,$A6,$55,$55
    .byte $55,$99,$02,$05,$96,$55,$55,$55,$59,$02,$05,$A8,$55,$55,$55,$A9
    .byte $00
sprite_6:
    .byte $0F,$5A,$05,$09,$09,$09,$09,$0A,$0A,$0A,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$00,$0A,$00,$05,$00,$80,$0A,$00,$05,$00,$80,$29,$00,$05
    .byte $00,$60,$29,$00,$05,$00,$A0,$99,$00,$05,$00,$58,$A9,$00,$05,$00
    .byte $68,$96,$02,$05,$00,$96,$9A,$02,$05,$00,$66,$A6,$02,$05,$00,$68
    .byte $66,$02,$05,$00,$9A,$9A,$02,$05,$80,$69,$A5,$09,$05,$00,$66,$65
    .byte $0A,$05,$80,$55,$95,$09,$05,$80,$5A,$95,$0A,$05,$A0,$55,$95,$0A
    .byte $05,$60,$5A,$95,$0A,$05,$A0,$56,$95,$0A,$05,$60,$56,$95,$09,$05
    .byte $80,$56,$95,$0A,$05,$68,$56,$95,$09,$05,$58,$56,$95,$09,$05,$98
    .byte $56,$95,$0A,$05,$98,$56,$95,$0A,$05,$68,$56,$95,$0A,$05,$00,$56
    .byte $95,$0A,$05,$A8,$55,$95,$09,$05,$98,$55,$95,$09,$05,$98,$55,$95
    .byte $09,$05,$A8,$55,$95,$0A,$05,$98,$55,$95,$0A,$05,$A0,$55,$95,$0A
    .byte $05,$98,$55,$95,$0A,$05,$98,$55,$95,$0A,$05,$98,$55,$95,$09,$05
    .byte $98,$55,$95,$09,$05,$98,$55,$95,$0A,$05,$A8,$55,$95,$0A,$05,$A8
    .byte $55,$95,$09,$05,$A8,$55,$95,$0A,$05,$A0,$55,$95,$0A,$05,$98,$55
    .byte $95,$09,$05,$98,$55,$95,$09,$05,$A8,$55,$95,$0A,$05,$98,$55,$95
    .byte $0A,$05,$98,$55,$95,$2A,$05,$A8,$55,$95,$2A,$05,$A8,$55,$95,$26
    .byte $05,$A8,$55,$95,$09,$05,$98,$55,$95,$0A,$05,$98,$55,$95,$09,$05
    .byte $98,$55,$95,$09,$05,$A8,$55,$95,$02,$05,$A8,$55,$95,$02,$05,$A8
    .byte $55,$95,$02,$05,$A8,$55,$95,$00,$05,$A8,$AA,$AA,$00,$05,$98,$00
    .byte $00,$00,$05,$98,$00,$00,$00,$05,$98,$00,$00,$00,$05,$A8,$00,$00
    .byte $00,$05,$A8,$00,$00,$00,$05,$98,$00,$00,$00,$05,$A8,$00,$00,$00
    .byte $05,$A8,$00,$00,$00,$05,$98,$00,$00,$00,$05,$98,$00,$00,$00,$05
    .byte $98,$00,$00,$00,$05,$A8,$00,$00,$00,$05,$A8,$00,$00,$00,$05,$A8
    .byte $00,$00,$00,$05,$A8,$00,$00,$00,$05,$A8,$00,$00,$00,$05,$98,$00
    .byte $00,$00,$05,$98,$00,$00,$00,$05,$98,$00,$00,$00,$05,$A8,$00,$00
    .byte $00,$05,$A8,$00,$00,$00,$05,$98,$00,$00,$00,$05,$A8,$00,$00,$00
    .byte $05,$A8,$00,$00,$00,$05,$98,$00,$00,$00,$05,$98,$00,$00,$00,$05
    .byte $98,$00,$00,$00,$05,$A8,$00,$00,$00,$05,$28,$00,$00,$00,$05,$28
    .byte $00,$00,$00,$05,$28,$00,$00,$00,$05,$28,$00,$00,$00,$05,$08,$00
    .byte $00,$00
sprite_7:
    .byte $0F,$5A,$05,$09,$09,$09,$09,$0A,$0A,$0A,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$28,$00,$00,$05,$00,$98,$00,$00,$05,$00,$98,$00,$00,$05
    .byte $00,$60,$02,$00,$05,$00,$9A,$02,$00,$05,$00,$6A,$09,$00,$05,$80
    .byte $66,$09,$00,$05,$80,$AA,$25,$00,$05,$A0,$6A,$2A,$00,$05,$60,$66
    .byte $25,$00,$05,$A0,$69,$26,$00,$05,$98,$AA,$29,$00,$05,$98,$5A,$26
    .byte $00,$05,$98,$56,$9A,$00,$05,$68,$56,$99,$00,$05,$A8,$55,$A9,$00
    .byte $05,$A8,$55,$09,$00,$05,$A8,$55,$A9,$00,$05,$A8,$55,$A5,$02,$05
    .byte $A8,$55,$65,$02,$05,$98,$55,$A5,$02,$05,$98,$55,$65,$02,$05,$A8
    .byte $55,$A5,$02,$05,$A8,$55,$65,$0A,$05,$98,$55,$A5,$09,$05,$A8,$55
    .byte $65,$09,$05,$A8,$55,$65,$0A,$05,$98,$55,$95,$09,$05,$98,$55,$95
    .byte $09,$05,$A8,$55,$95,$02,$05,$A8,$55,$95,$09,$05,$98,$55,$95,$0A
    .byte $05,$A8,$55,$95,$09,$05,$98,$55,$95,$0A,$05,$98,$55,$95,$0A,$05
    .byte $98,$55,$95,$0A,$05,$A8,$55,$95,$0A,$05,$A8,$55,$95,$0A,$05,$A8
    .byte $55,$95,$0A,$05,$98,$55,$95,$09,$05,$A8,$55,$95,$09,$05,$98,$55
    .byte $95,$09,$05,$98,$55,$95,$0A,$05,$A8,$55,$95,$0A,$05,$A8,$55,$95
    .byte $09,$05,$AA,$55,$95,$0A,$05,$AA,$55,$95,$0A,$05,$96,$55,$95,$09
    .byte $05,$9A,$55,$95,$09,$05,$98,$55,$95,$09,$05,$98,$55,$95,$09,$05
    .byte $98,$55,$95,$0A,$05,$A0,$55,$95,$0A,$05,$A0,$55,$95,$0A,$05,$A0
    .byte $55,$95,$0A,$05,$80,$55,$95,$09,$05,$80,$AA,$AA,$09,$05,$00,$00
    .byte $80,$0A,$05,$00,$00,$80,$0A,$05,$00,$00,$80,$0A,$05,$00,$00,$80
    .byte $0A,$05,$00,$00,$80,$0A,$05,$00,$00,$80,$0A,$05,$00,$00,$80,$09
    .byte $05,$00,$00,$80,$09,$05,$00,$00,$80,$0A,$05,$00,$00,$80,$09,$05
    .byte $00,$00,$80,$0A,$05,$00,$00,$80,$09,$05,$00,$00,$80,$0A,$05,$00
    .byte $00,$80,$0A,$05,$00,$00,$80,$09,$05,$00,$00,$80,$09,$05,$00,$00
    .byte $80,$09,$05,$00,$00,$80,$09,$05,$00,$00,$80,$0A,$05,$00,$00,$80
    .byte $0A,$05,$00,$00,$80,$0A,$05,$00,$00,$80,$0A,$05,$00,$00,$80,$09
    .byte $05,$00,$00,$80,$09,$05,$00,$00,$80,$09,$05,$00,$00,$80,$0A,$05
    .byte $00,$00,$80,$09,$05,$00,$00,$80,$0A,$05,$00,$00,$80,$09,$05,$00
    .byte $00,$00,$0A,$05,$00,$00,$00,$0A,$05,$00,$00,$00,$0A,$05,$00,$00
    .byte $00,$08
sprite_8:
    .byte $0F,$3D,$05,$09,$09,$09,$09,$0A,$0A,$0A,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$AA,$2A,$00,$05,$80,$AA,$AA,$00,$05,$A0,$9A,$A6,$02,$05
    .byte $60,$AA,$AA,$02,$05,$A8,$9A,$AA,$0A,$05,$A8,$AA,$A6,$09,$05,$68
    .byte $AA,$AA,$0A,$05,$AA,$9A,$A6,$29,$05,$AA,$AA,$AA,$2A,$05,$AA,$9A
    .byte $A6,$29,$05,$AA,$AA,$AA,$2A,$05,$AA,$6A,$AA,$2A,$05,$AA,$6A,$AA
    .byte $2A,$05,$AA,$9A,$AA,$29,$05,$6A,$AA,$AA,$2A,$05,$AA,$AA,$9A,$2A
    .byte $05,$AA,$9A,$AA,$29,$05,$AA,$AA,$9A,$2A,$05,$6A,$AA,$AA,$2A,$05
    .byte $AA,$9A,$AA,$29,$05,$AA,$AA,$9A,$2A,$05,$6A,$9A,$9A,$2A,$05,$AA
    .byte $AA,$AA,$2A,$05,$AA,$9A,$AA,$2A,$05,$6A,$AA,$5A,$29,$05,$AA,$9A
    .byte $5A,$29,$05,$AA,$AA,$AA,$2A,$05,$6A,$AA,$9A,$2A,$05,$AA,$AA,$AA
    .byte $2A,$05,$9A,$9A,$99,$29,$05,$9A,$9A,$A9,$2A,$05,$9A,$AA,$A5,$29
    .byte $05,$9A,$5A,$A9,$2A,$05,$9A,$6A,$A6,$29,$05,$9A,$6A,$AA,$2A,$05
    .byte $6A,$9A,$AA,$2A,$05,$AA,$AA,$AA,$29,$05,$AA,$AA,$A6,$2A,$05,$AA
    .byte $9A,$AA,$26,$05,$6A,$9A,$A6,$2A,$05,$AA,$AA,$AA,$2A,$05,$AA,$AA
    .byte $A6,$26,$05,$6A,$AA,$AA,$2A,$05,$AA,$9A,$9A,$29,$05,$6A,$AA,$AA
    .byte $2A,$05,$AA,$9A,$AA,$29,$05,$6A,$AA,$9A,$2A,$05,$AA,$6A,$AA,$2A
    .byte $05,$AA,$AA,$5A,$29,$05,$AA,$6A,$5A,$29,$05,$6A,$AA,$AA,$2A,$05
    .byte $AA,$AA,$9A,$2A,$05,$AA,$6A,$AA,$29,$05,$6A,$AA,$9A,$2A,$05,$AA
    .byte $AA,$AA,$2A,$05,$A6,$6A,$AA,$29,$05,$AA,$6A,$AA,$2A,$05,$A6,$6A
    .byte $9A,$29,$05,$6A,$AA,$AA,$2A,$05,$AA,$AA,$9A,$29,$05,$6A,$6A,$9A
    .byte $29
sprite_9:
    .byte $0F,$3C,$05,$09,$09,$09,$09,$0A,$0A,$0A,$01,$0E,$01,$00,$00,$00
    .byte $0F,$00,$00,$00,$00,$0F,$00,$00,$00,$00,$0F,$00,$58,$09,$00,$0F
    .byte $00,$58,$09,$00,$0F,$00,$58,$09,$00,$0F,$00,$58,$09,$00,$0F,$60
    .byte $59,$59,$02,$0F,$60,$59,$59,$02,$0F,$64,$59,$59,$06,$0F,$64,$59
    .byte $59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59,$59
    .byte $06,$0F,$64,$59,$59,$06,$0F,$A8,$AA,$AA,$2A,$0F,$A8,$AA,$AA,$2A
    .byte $0F,$64,$59,$59,$16,$0F,$64,$59,$59,$06,$0F,$64,$59,$59,$06,$0F
    .byte $64,$59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64
    .byte $59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59
    .byte $59,$06,$0F,$F4,$59,$59,$06,$0F,$5C,$5B,$59,$06,$0F,$5C,$5B,$59
    .byte $06,$0F,$FC,$5B,$59,$06,$0F,$FC,$5B,$59,$06,$0F,$7C,$5B,$59,$06
    .byte $0F,$7C,$5B,$59,$06,$0F,$7C,$5B,$59,$06,$0F,$FC,$5B,$59,$06,$0F
    .byte $FC,$5B,$59,$06,$0F,$FC,$5B,$59,$06,$0F,$64,$59,$59,$06,$0F,$64
    .byte $59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59
    .byte $59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59,$59
    .byte $06,$0F,$64,$59,$59,$06,$0F,$A8,$AA,$AA,$0A,$0F,$A8,$AA,$AA,$2A
    .byte $0F,$64,$59,$59,$16,$0F,$64,$59,$59,$16,$0F,$64,$59,$59,$06,$0F
    .byte $64,$59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64
    .byte $59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59,$59,$06,$0F,$64,$59
    .byte $59,$06,$0F,$60,$59,$59,$02,$0F,$60,$59,$59,$02
sprite_10:
    .byte $09,$4A,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$0A,$00,$05,$00,$2A,$00,$05,$80,$2A,$00,$05,$80,$A9,$00
    .byte $05,$80,$AA,$02,$05,$A0,$69,$02,$05,$A0,$AA,$02,$05,$A0,$99,$02
    .byte $05,$A0,$9A,$02,$05,$A8,$9A,$02,$05,$A8,$AA,$02,$05,$A8,$A9,$02
    .byte $05,$A8,$A9,$02,$05,$A8,$A9,$02,$05,$A8,$6A,$02,$05,$A8,$69,$02
    .byte $05,$98,$AA,$02,$05,$98,$9A,$02,$05,$98,$9A,$02,$05,$AA,$A6,$02
    .byte $05,$AA,$A6,$02,$05,$AA,$66,$02,$05,$A6,$A9,$02,$05,$AA,$AA,$02
    .byte $05,$A6,$A9,$02,$05,$AA,$6A,$02,$05,$AA,$A9,$02,$05,$AA,$66,$02
    .byte $05,$A6,$A6,$02,$05,$AA,$A6,$02,$05,$6A,$66,$02,$05,$6A,$A6,$02
    .byte $05,$66,$AA,$02,$05,$AA,$A9,$02,$05,$AA,$A9,$02,$05,$A6,$6A,$02
    .byte $05,$AA,$69,$02,$05,$AA,$6A,$02,$05,$9A,$9A,$02,$05,$9A,$99,$02
    .byte $05,$9A,$A6,$02,$05,$9A,$66,$02,$05,$9A,$A6,$02,$05,$9A,$6A,$02
    .byte $05,$A6,$69,$02,$05,$AA,$AA,$02,$05,$A6,$69,$02,$05,$A6,$AA,$02
    .byte $05,$AA,$69,$02,$05,$AA,$AA,$02,$05,$A6,$A6,$00,$05,$AA,$AA,$00
    .byte $05,$A6,$A9,$00,$05,$AA,$29,$00,$05,$AA,$2A,$00,$05,$A6,$2A,$00
    .byte $05,$AA,$09,$00,$05,$A6,$0A,$00,$05,$AA,$0A,$00,$05,$9A,$02,$00
    .byte $05,$AA,$02,$00,$05,$A6,$02,$00,$05,$AA,$00,$00,$05,$AA,$00,$00
    .byte $05,$A6,$00,$00,$05,$AA,$00,$00,$05,$2A,$00,$00,$05,$26,$00,$00
    .byte $05,$2A,$00,$00,$05,$0A,$00,$00,$05,$0A,$00,$00,$05,$0A,$00,$00
    .byte $05,$0A,$00,$00,$05,$02,$00,$00
sprite_11:
    .byte $09,$3E,$04,$06,$06,$06,$06,$06,$06,$06,$01,$0E,$01,$00,$00,$00
    .byte $0F,$00,$10,$00,$0F,$00,$16,$00,$0F,$00,$96,$00,$0F,$40,$96,$00
    .byte $0F,$40,$96,$00,$0F,$40,$96,$01,$0F,$40,$96,$01,$0F,$40,$96,$02
    .byte $0F,$40,$96,$02,$0F,$40,$96,$01,$0F,$40,$A6,$01,$0F,$40,$A6,$00
    .byte $0F,$58,$9A,$00,$0F,$58,$9A,$00,$0F,$58,$96,$00,$0F,$98,$96,$00
    .byte $0F,$98,$96,$00,$0F,$68,$96,$00,$0F,$60,$96,$00,$0F,$58,$96,$00
    .byte $0F,$58,$96,$00,$0F,$58,$96,$00,$0F,$58,$96,$00,$0F,$58,$96,$00
    .byte $0F,$58,$96,$00,$0F,$58,$96,$00,$0F,$58,$96,$00,$0F,$58,$96,$00
    .byte $0F,$58,$96,$01,$0F,$58,$96,$01,$0F,$F8,$96,$02,$0F,$5C,$97,$02
    .byte $0F,$5C,$97,$01,$0F,$FC,$A7,$01,$0F,$FC,$A7,$01,$0F,$7C,$9B,$00
    .byte $0F,$7C,$9B,$00,$0F,$7C,$97,$00,$0F,$FC,$97,$00,$0F,$FC,$97,$00
    .byte $0F,$FD,$97,$00,$0F,$69,$96,$00,$0F,$69,$96,$00,$0F,$58,$16,$00
    .byte $0F,$58,$16,$00,$0F,$58,$02,$00,$0F,$58,$02,$00,$0F,$58,$02,$00
    .byte $0F,$58,$02,$00,$0F,$58,$02,$00,$0F,$58,$02,$00,$0F,$58,$02,$00
    .byte $0F,$58,$02,$00,$0F,$18,$00,$00,$0F,$18,$00,$00,$0F,$18,$00,$00
    .byte $0F,$18,$00,$00,$0F,$18,$00,$00,$0F,$18,$00,$00,$0F,$18,$00,$00
    .byte $0F,$08,$00,$00,$0F,$08,$00,$00
sprite_12:
    .byte $09,$4A,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$A0,$02,$00,$05,$A8,$09,$00,$05,$A8,$09,$00,$05,$A8,$0A,$00
    .byte $05,$A6,$2A,$00,$05,$AA,$2A,$00,$05,$A6,$29,$00,$05,$AA,$AA,$00
    .byte $05,$AA,$A9,$00,$05,$A6,$AA,$00,$05,$AA,$99,$00,$05,$A6,$AA,$00
    .byte $05,$9A,$99,$00,$05,$AA,$A6,$00,$05,$6A,$A6,$00,$05,$AA,$A6,$00
    .byte $05,$A6,$A9,$02,$05,$AA,$9A,$02,$05,$A6,$6A,$02,$05,$AA,$69,$02
    .byte $05,$AA,$A6,$02,$05,$A6,$A6,$02,$05,$AA,$99,$02,$05,$A6,$9A,$02
    .byte $05,$A6,$99,$02,$05,$A6,$AA,$02,$05,$A6,$6A,$02,$05,$A6,$69,$02
    .byte $05,$6A,$AA,$02,$05,$6A,$AA,$02,$05,$A6,$9A,$02,$05,$6A,$A6,$02
    .byte $05,$A6,$96,$02,$05,$AA,$A9,$02,$05,$AA,$A9,$02,$05,$A6,$99,$02
    .byte $05,$AA,$AA,$02,$05,$A6,$99,$02,$05,$AA,$AA,$02,$05,$AA,$AA,$02
    .byte $05,$AA,$99,$02,$05,$A6,$AA,$02,$05,$A6,$99,$02,$05,$A6,$AA,$02
    .byte $05,$A6,$AA,$02,$05,$AA,$9A,$02,$05,$A6,$A9,$02,$05,$68,$9A,$02
    .byte $05,$A8,$A9,$02,$05,$98,$AA,$02,$05,$A0,$9A,$02,$05,$A0,$A9,$02
    .byte $05,$A0,$A6,$02,$05,$A0,$A6,$02,$05,$80,$99,$02,$05,$80,$99,$02
    .byte $05,$80,$99,$02,$05,$80,$A6,$02,$05,$00,$AA,$02,$05,$00,$6A,$02
    .byte $05,$00,$AA,$02,$05,$00,$98,$02,$05,$00,$98,$02,$05,$00,$98,$02
    .byte $05,$00,$A8,$02,$05,$00,$A0,$02,$05,$00,$80,$02,$05,$00,$A0,$02
    .byte $05,$00,$80,$02,$05,$00,$80,$02,$05,$00,$80,$02,$05,$00,$00,$02
    .byte $05,$00,$00,$02,$05,$00,$00,$02
sprite_13:
    .byte $09,$41,$04,$06,$06,$06,$06,$06,$06,$06,$01,$0E,$01,$00,$00,$00
    .byte $0F,$00,$02,$00,$0F,$00,$02,$00,$0F,$58,$02,$00,$0F,$58,$02,$00
    .byte $0F,$58,$02,$00,$0F,$58,$02,$00,$0F,$58,$02,$00,$0F,$59,$02,$00
    .byte $0F,$58,$02,$00,$0F,$5A,$02,$00,$0F,$59,$02,$00,$0F,$68,$16,$00
    .byte $0F,$A8,$16,$00,$0F,$98,$96,$00,$0F,$58,$96,$00,$0F,$58,$9A,$00
    .byte $0F,$58,$9A,$00,$0F,$58,$A6,$00,$0F,$58,$A6,$00,$0F,$58,$96,$00
    .byte $0F,$58,$96,$00,$0F,$58,$96,$00,$0F,$58,$96,$00,$0F,$58,$96,$00
    .byte $0F,$58,$96,$00,$0F,$58,$96,$00,$0F,$58,$96,$00,$0F,$58,$96,$00
    .byte $0F,$58,$96,$00,$0F,$7C,$96,$00,$0F,$D7,$96,$00,$0F,$D7,$96,$00
    .byte $0F,$FF,$96,$00,$0F,$FF,$96,$00,$0F,$DF,$96,$00,$0F,$DF,$96,$00
    .byte $0F,$DF,$96,$00,$0F,$FF,$96,$00,$0F,$FF,$96,$00,$0F,$FF,$9A,$01
    .byte $0F,$58,$9A,$01,$0F,$58,$A6,$01,$0F,$58,$A6,$00,$0F,$58,$96,$00
    .byte $0F,$40,$96,$00,$0F,$40,$96,$00,$0F,$40,$96,$00,$0F,$40,$96,$00
    .byte $0F,$40,$96,$00,$0F,$40,$96,$00,$0F,$00,$96,$00,$0F,$00,$96,$00
    .byte $0F,$00,$90,$00,$0F,$00,$90,$00,$0F,$00,$90,$00,$0F,$00,$90,$00
    .byte $0F,$00,$90,$00,$0F,$00,$90,$00,$0F,$00,$90,$00,$0F,$00,$90,$00
    .byte $0F,$00,$90,$00,$0F,$00,$90,$00,$0F,$00,$90,$00,$0F,$00,$10,$00
    .byte $0F,$00,$10,$00
sprite_14:
    .byte $06,$12,$03,$04,$04,$04,$04,$04,$05,$05,$01,$00,$00,$00,$00,$00
    .byte $04,$96,$0A,$04,$9A,$0A,$04,$9A,$09,$04,$A6,$0A,$04,$AA,$09,$04
    .byte $68,$0A,$04,$60,$02,$04,$60,$02,$04,$60,$02,$04,$A0,$00,$04,$A0
    .byte $00,$04,$28,$00,$04,$28,$00,$04,$26,$00,$04,$0A,$00,$04,$0A,$00
    .byte $04,$0A,$00,$04,$00,$00
sprite_15:
    .byte $06,$11,$03,$04,$04,$04,$04,$04,$05,$05,$01,$00,$00,$00,$00,$00
    .byte $04,$6A,$09,$04,$5A,$0A,$04,$66,$0A,$04,$AA,$09,$04,$A6,$0A,$04
    .byte $9A,$02,$04,$98,$00,$04,$98,$00,$04,$98,$00,$04,$A0,$00,$04,$A0
    .byte $00,$04,$80,$02,$04,$80,$02,$04,$80,$09,$04,$00,$0A,$04,$00,$0A
    .byte $04,$00,$0A
sprite_16:
    .byte $0F,$0F,$05,$09,$09,$09,$09,$0A,$0A,$0A,$01,$00,$00,$00,$00,$00
    .byte $04,$00,$A8,$2A,$00,$04,$00,$A6,$AA,$00,$04,$80,$AA,$6A,$02,$04
    .byte $60,$AA,$AA,$0A,$04,$A0,$AA,$AA,$0A,$04,$A0,$AA,$9A,$0A,$04,$68
    .byte $5A,$A5,$26,$04,$98,$55,$55,$26,$04,$68,$55,$55,$29,$04,$60,$55
    .byte $55,$09,$04,$60,$55,$55,$09,$04,$60,$55,$55,$09,$04,$80,$55,$55
    .byte $02,$04,$00,$5A,$A5,$00,$04,$00,$A8,$2A,$00
sprite_17:
    .byte $09,$37,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$00,$02,$05,$00,$00,$02,$05,$00,$00,$02,$05,$00,$00,$02
    .byte $05,$00,$80,$02,$05,$00,$80,$02,$05,$00,$80,$02,$05,$00,$80,$02
    .byte $05,$00,$A0,$02,$05,$00,$A0,$02,$05,$00,$A0,$02,$05,$00,$A0,$02
    .byte $05,$00,$A8,$02,$05,$00,$68,$02,$05,$00,$68,$02,$05,$00,$A8,$02
    .byte $05,$00,$AA,$02,$05,$00,$9A,$02,$05,$00,$9A,$02,$05,$00,$9A,$02
    .byte $05,$80,$9A,$02,$05,$80,$9A,$02,$05,$80,$9A,$02,$05,$80,$9A,$02
    .byte $05,$A0,$9A,$02,$05,$A0,$9A,$02,$05,$A0,$9A,$02,$05,$60,$5A,$02
    .byte $05,$68,$5A,$02,$05,$68,$0A,$00,$05,$68,$0A,$00,$05,$68,$0A,$00
    .byte $05,$6A,$0A,$00,$05,$5A,$0A,$00,$05,$5A,$0A,$00,$05,$5A,$0A,$00
    .byte $05,$5A,$0A,$00,$05,$5A,$0A,$00,$05,$5A,$02,$00,$05,$5A,$02,$00
    .byte $05,$5A,$02,$00,$05,$5A,$02,$00,$05,$5A,$02,$00,$05,$0A,$00,$00
    .byte $05,$0A,$00,$00,$05,$0A,$00,$00,$05,$0A,$00,$00,$05,$0A,$00,$00
    .byte $05,$0A,$00,$00,$05,$02,$00,$00,$05,$02,$00,$00,$05,$02,$00,$00
    .byte $05,$02,$00,$00,$05,$02,$00,$00,$05,$02,$00,$00
sprite_18:
    .byte $09,$37,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $05,$02,$00,$00,$05,$02,$00,$00,$05,$02,$00,$00,$05,$02,$00,$00
    .byte $05,$0A,$00,$00,$05,$0A,$00,$00,$05,$0A,$00,$00,$05,$0A,$00,$00
    .byte $05,$2A,$00,$00,$05,$2A,$00,$00,$05,$2A,$00,$00,$05,$2A,$00,$00
    .byte $05,$AA,$00,$00,$05,$A6,$00,$00,$05,$A6,$00,$00,$05,$AA,$00,$00
    .byte $05,$AA,$02,$00,$05,$9A,$02,$00,$05,$9A,$02,$00,$05,$9A,$02,$00
    .byte $05,$9A,$0A,$00,$05,$9A,$0A,$00,$05,$9A,$0A,$00,$05,$9A,$0A,$00
    .byte $05,$9A,$2A,$00,$05,$9A,$2A,$00,$05,$9A,$2A,$00,$05,$96,$26,$00
    .byte $05,$96,$A6,$00,$05,$80,$A6,$00,$05,$80,$A6,$00,$05,$80,$A6,$00
    .byte $05,$80,$A6,$02,$05,$80,$96,$02,$05,$80,$96,$02,$05,$80,$96,$02
    .byte $05,$80,$96,$02,$05,$80,$96,$02,$05,$00,$96,$02,$05,$00,$96,$02
    .byte $05,$00,$96,$02,$05,$00,$96,$02,$05,$00,$80,$02,$05,$00,$80,$02
    .byte $05,$00,$80,$02,$05,$00,$80,$02,$05,$00,$80,$02,$05,$00,$80,$02
    .byte $05,$00,$80,$02,$05,$00,$80,$02,$05,$00,$00,$02,$05,$00,$00,$02
    .byte $05,$00,$00,$02,$05,$00,$00,$02,$05,$00,$00,$02
sprite_20:
    .byte $15,$32,$07,$0C,$0D,$0D,$0D,$0D,$0D,$0D,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$A0,$AA,$2A,$00,$00,$05,$00,$58,$55,$95,$00,$00,$05,$00
    .byte $58,$55,$95,$00,$00,$05,$00,$56,$55,$55,$02,$00,$05,$00,$56,$55
    .byte $55,$02,$00,$05,$80,$55,$55,$55,$09,$00,$05,$80,$55,$55,$55,$09
    .byte $00,$05,$80,$55,$55,$55,$09,$00,$05,$80,$55,$AA,$56,$09,$00,$05
    .byte $60,$55,$56,$56,$25,$00,$05,$60,$55,$6A,$56,$25,$00,$05,$60,$55
    .byte $AA,$56,$25,$00,$05,$60,$55,$66,$56,$25,$00,$05,$58,$55,$6A,$56
    .byte $95,$00,$05,$A8,$AA,$6A,$AA,$AA,$00,$05,$56,$55,$66,$56,$55,$02
    .byte $05,$AA,$AA,$AA,$A9,$AA,$02,$05,$56,$55,$99,$55,$55,$02,$05,$56
    .byte $55,$69,$55,$55,$02,$05,$AA,$AA,$AA,$AA,$AA,$02,$05,$58,$66,$55
    .byte $65,$96,$00,$05,$58,$66,$55,$65,$96,$00,$05,$A8,$66,$55,$65,$AA
    .byte $00,$05,$A8,$66,$55,$65,$AA,$00,$05,$A8,$66,$55,$65,$AA,$00,$05
    .byte $A8,$66,$55,$65,$AA,$00,$05,$A8,$66,$55,$65,$AA,$00,$05,$A8,$66
    .byte $55,$65,$AA,$00,$05,$A8,$66,$55,$65,$AA,$00,$05,$A8,$66,$55,$65
    .byte $AA,$00,$05,$58,$66,$55,$65,$96,$00,$05,$68,$66,$55,$65,$A6,$00
    .byte $05,$A8,$66,$55,$65,$AA,$00,$05,$68,$66,$55,$65,$A6,$00,$05,$58
    .byte $66,$55,$65,$96,$00,$05,$A8,$66,$55,$65,$AA,$00,$05,$A8,$66,$55
    .byte $65,$AA,$00,$05,$A8,$66,$55,$65,$AA,$00,$05,$A8,$66,$55,$65,$AA
    .byte $00,$05,$A8,$66,$55,$65,$AA,$00,$05,$A8,$A6,$AA,$6A,$AA,$00,$05
    .byte $A8,$56,$55,$95,$AA,$00,$05,$A8,$5A,$55,$95,$96,$00,$05,$5A,$5A
    .byte $55,$95,$96,$02,$05,$5A,$5A,$55,$95,$96,$02,$05,$5A,$56,$55,$55
    .byte $96,$02,$05,$AA,$56,$55,$55,$AA,$02,$05,$56,$55,$55,$55,$55,$02
    .byte $05,$56,$55,$55,$55,$55,$02,$05,$AA,$AA,$AA,$AA,$AA,$02
sprite_21:
    .byte $09,$1A,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0E,$AA,$AA,$02,$0E,$56,$55,$02,$0E,$AA,$6A,$02,$0E,$6A,$66,$02
    .byte $0E,$6A,$66,$02,$0E,$6A,$66,$02,$0E,$AA,$A5,$02,$0E,$AA,$96,$02
    .byte $0E,$5A,$95,$02,$0E,$5A,$95,$02,$0E,$9A,$99,$02,$0E,$9A,$99,$02
    .byte $0E,$9A,$99,$02,$0E,$9A,$99,$02,$0E,$9A,$69,$02,$0E,$9A,$69,$02
    .byte $0E,$A6,$A9,$00,$0E,$A6,$A9,$00,$0E,$A8,$96,$00,$0E,$A8,$9A,$00
    .byte $0E,$98,$29,$00,$0E,$A0,$26,$00,$0E,$60,$0A,$00,$0E,$80,$09,$00
    .byte $0E,$80,$02,$00,$0E,$00,$02,$00
sprite_22:
    .byte $09,$18,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0E,$6A,$A5,$02,$0E,$AA,$6A,$02,$0E,$AA,$AA,$02,$0E,$9A,$AA,$02
    .byte $0E,$5A,$95,$02,$0E,$58,$95,$02,$0E,$9A,$96,$00,$0E,$98,$99,$02
    .byte $0E,$9A,$95,$00,$0E,$98,$9A,$02,$0E,$9A,$99,$00,$0E,$98,$96,$02
    .byte $0E,$9A,$99,$00,$0E,$68,$99,$02,$0E,$9A,$96,$00,$0E,$68,$66,$02
    .byte $0E,$5A,$95,$00,$0E,$68,$AA,$02,$0E,$9A,$95,$00,$0E,$5A,$9A,$02
    .byte $0E,$AA,$9A,$02,$0E,$AA,$AA,$02,$0E,$A6,$6A,$02,$0E,$6A,$A5,$02
sprite_23:
    .byte $09,$29,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $04,$00,$00,$00,$04,$A0,$A9,$02,$04,$A0,$A6,$02,$04,$60,$96,$02
    .byte $04,$60,$55,$02,$04,$60,$55,$02,$04,$60,$AA,$02,$04,$60,$AA,$02
    .byte $04,$60,$AA,$02,$04,$60,$AA,$02,$04,$60,$AA,$02,$04,$60,$AA,$02
    .byte $04,$60,$AA,$02,$04,$60,$AA,$02,$04,$60,$AA,$02,$04,$58,$AA,$02
    .byte $04,$58,$6A,$02,$04,$66,$6A,$02,$04,$66,$6A,$02,$04,$6A,$9A,$02
    .byte $04,$6A,$9A,$02,$04,$6A,$9A,$02,$04,$68,$65,$02,$04,$68,$95,$02
    .byte $04,$A8,$9A,$02,$04,$98,$9A,$02,$04,$A8,$AA,$00,$04,$66,$99,$00
    .byte $04,$56,$A5,$00,$04,$AA,$2A,$00,$04,$A0,$9A,$02,$04,$98,$A6,$02
    .byte $04,$A8,$A9,$02,$04,$A8,$A9,$02,$04,$9A,$69,$02,$04,$5A,$A5,$00
    .byte $04,$5A,$A5,$00,$04,$5A,$A5,$00,$04,$5A,$A5,$00,$04,$5A,$A5,$00
    .byte $04,$5A,$A5,$00
sprite_24:
    .byte $09,$2A,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $04,$00,$00,$00,$04,$A0,$AA,$02,$04,$60,$95,$02,$04,$58,$95,$02
    .byte $04,$58,$65,$02,$04,$56,$A5,$00,$04,$AA,$9A,$00,$04,$56,$A5,$00
    .byte $04,$AA,$2A,$00,$04,$98,$2A,$00,$04,$60,$29,$00,$04,$A0,$26,$00
    .byte $04,$A0,$0A,$00,$04,$60,$09,$00,$04,$A0,$0A,$00,$04,$A0,$0A,$00
    .byte $04,$A0,$0A,$00,$04,$A0,$0A,$00,$04,$A0,$0A,$00,$04,$A0,$0A,$00
    .byte $04,$A0,$0A,$00,$04,$A0,$0A,$00,$04,$A0,$0A,$00,$04,$A0,$0A,$00
    .byte $04,$A0,$0A,$00,$04,$A0,$0A,$00,$04,$A0,$0A,$00,$04,$A0,$0A,$00
    .byte $04,$A0,$0A,$00,$04,$A0,$0A,$00,$04,$60,$25,$00,$04,$60,$25,$00
    .byte $04,$A0,$0A,$00,$04,$60,$A5,$00,$04,$A0,$AA,$00,$04,$60,$A5,$00
    .byte $04,$98,$AA,$00,$04,$58,$95,$00,$04,$A8,$9A,$00,$04,$58,$29,$00
    .byte $04,$58,$29,$00,$04,$A8,$0A,$00
sprite_25:
    .byte $15,$24,$07,$0C,$0D,$0D,$0D,$0D,$0D,$0D,$01,$00,$00,$00,$00,$00
    .byte $04,$00,$00,$00,$00,$00,$00,$04,$AA,$AA,$AA,$AA,$00,$00,$04,$AA
    .byte $AA,$AA,$AA,$02,$00,$04,$AA,$AA,$AA,$AA,$02,$00,$04,$AA,$AA,$AA
    .byte $AA,$02,$00,$04,$AA,$AA,$56,$AA,$0A,$00,$04,$66,$55,$AA,$96,$0A
    .byte $00,$04,$A6,$AA,$AA,$AA,$0A,$00,$04,$A6,$AA,$AA,$AA,$2A,$00,$04
    .byte $A6,$AA,$A5,$AA,$2A,$00,$04,$9A,$AA,$AA,$AA,$2A,$00,$04,$98,$AA
    .byte $AA,$AA,$2A,$00,$04,$68,$AA,$AA,$AA,$AA,$00,$04,$68,$AA,$AA,$AA
    .byte $AA,$00,$04,$68,$AA,$AA,$AA,$AA,$00,$04,$AA,$55,$55,$55,$95,$00
    .byte $04,$AA,$AA,$AA,$AA,$AA,$00,$04,$9A,$59,$55,$55,$26,$00,$04,$9A
    .byte $59,$55,$55,$26,$00,$04,$9A,$A9,$AA,$AA,$25,$00,$04,$9A,$A9,$AA
    .byte $AA,$0A,$00,$04,$9A,$A9,$AA,$AA,$0A,$00,$04,$AA,$A9,$AA,$AA,$0A
    .byte $00,$04,$9A,$56,$55,$55,$0A,$00,$04,$98,$59,$55,$95,$26,$00,$04
    .byte $98,$59,$55,$95,$26,$00,$04,$80,$59,$55,$95,$26,$00,$04,$80,$59
    .byte $55,$55,$26,$00,$04,$80,$59,$55,$55,$26,$00,$04,$80,$59,$55,$55
    .byte $26,$00,$04,$80,$59,$55,$55,$26,$00,$04,$80,$59,$55,$55,$26,$00
    .byte $04,$80,$59,$55,$55,$26,$00,$04,$80,$59,$55,$55,$26,$00,$04,$80
    .byte $59,$55,$55,$26,$00,$04,$00,$5A,$55,$55,$29,$00
sprite_26:
    .byte $0F,$1E,$05,$09,$09,$09,$09,$0A,$0A,$0A,$01,$00,$00,$00,$00,$00
    .byte $04,$00,$00,$00,$00,$04,$00,$28,$00,$00,$04,$00,$AA,$00,$00,$04
    .byte $00,$AA,$00,$00,$04,$00,$AA,$02,$00,$04,$80,$AA,$02,$00,$04,$80
    .byte $AA,$0A,$00,$04,$80,$AA,$0A,$00,$04,$80,$AA,$09,$00,$04,$80,$6A
    .byte $2A,$00,$04,$80,$69,$2A,$00,$04,$80,$69,$2A,$00,$04,$80,$99,$AA
    .byte $00,$04,$80,$96,$AA,$00,$04,$80,$A6,$AA,$00,$04,$80,$9A,$AA,$00
    .byte $04,$80,$69,$95,$00,$04,$80,$99,$AA,$00,$04,$80,$99,$AA,$00,$04
    .byte $80,$59,$9A,$00,$04,$80,$9A,$99,$00,$04,$80,$9A,$99,$00,$04,$80
    .byte $9A,$A6,$00,$04,$00,$9A,$A6,$00,$04,$00,$9A,$AA,$00,$04,$00,$9A
    .byte $AA,$00,$04,$00,$98,$AA,$00,$04,$00,$98,$AA,$00,$04,$00,$98,$AA
    .byte $00,$04,$00,$A0,$AA,$00
sprite_27:
    .byte $12,$28,$06,$0B,$0B,$0B,$0B,$0B,$0B,$0C,$01,$00,$00,$00,$00,$00
    .byte $04,$00,$00,$00,$00,$00,$04,$00,$00,$0A,$00,$00,$04,$00,$00,$26
    .byte $00,$00,$04,$00,$00,$26,$00,$00,$04,$00,$00,$A6,$00,$00,$04,$00
    .byte $00,$A6,$00,$00,$04,$00,$00,$A6,$00,$00,$04,$00,$00,$96,$02,$00
    .byte $04,$00,$00,$96,$02,$00,$04,$00,$00,$96,$02,$00,$04,$00,$00,$66
    .byte $0A,$00,$04,$00,$00,$66,$02,$00,$04,$00,$00,$A6,$0A,$00,$04,$00
    .byte $00,$A6,$0A,$00,$04,$00,$00,$9A,$0A,$00,$04,$80,$AA,$99,$2A,$00
    .byte $04,$80,$55,$96,$2A,$00,$04,$80,$55,$99,$2A,$00,$04,$80,$55,$9A
    .byte $2A,$00,$04,$80,$56,$9A,$2A,$00,$04,$80,$56,$A6,$0A,$00,$04,$80
    .byte $56,$A6,$0A,$00,$04,$80,$5A,$66,$0A,$00,$04,$80,$5A,$96,$0A,$00
    .byte $04,$80,$5A,$96,$02,$00,$04,$80,$5A,$96,$02,$00,$04,$80,$69,$95
    .byte $00,$00,$04,$80,$99,$AA,$00,$00,$04,$80,$99,$AA,$00,$00,$04,$80
    .byte $59,$9A,$00,$00,$04,$80,$9A,$99,$00,$00,$04,$80,$9A,$99,$00,$00
    .byte $04,$80,$9A,$A6,$00,$00,$04,$00,$9A,$A6,$00,$00,$04,$00,$9A,$AA
    .byte $00,$00,$04,$00,$9A,$AA,$00,$00,$04,$00,$98,$AA,$00,$00,$04,$00
    .byte $98,$AA,$00,$00,$04,$00,$98,$AA,$00,$00,$04,$00,$A0,$AA,$00,$00
sprite_28:
    .byte $1B,$10,$08,$10,$10,$10,$10,$10,$11,$11,$01,$00,$00,$00,$00,$00
    .byte $0E,$00,$00,$00,$00,$00,$00,$00,$0E,$00,$00,$98,$59,$AA,$00,$00
    .byte $0E,$00,$00,$58,$5A,$AA,$00,$00,$0E,$00,$00,$68,$9A,$AA,$00,$00
    .byte $0E,$00,$00,$96,$A6,$AA,$00,$00,$0E,$00,$00,$96,$A6,$A9,$00,$00
    .byte $0E,$00,$5A,$99,$9A,$A9,$00,$00,$0E,$00,$A8,$69,$9A,$AA,$00,$00
    .byte $0E,$00,$6A,$69,$99,$66,$29,$00,$0E,$80,$66,$66,$6A,$66,$0A,$00
    .byte $0E,$80,$65,$56,$66,$6A,$29,$00,$0E,$80,$9A,$56,$69,$2A,$00,$00
    .byte $0E,$80,$AA,$55,$65,$95,$00,$00,$0E,$00,$60,$55,$A5,$95,$0A,$00
    .byte $0E,$00,$00,$00,$A0,$55,$0A,$00,$0E,$00,$00,$00,$A0,$00,$00,$00
sprite_29:
    .byte $1E,$0F,$09,$12,$12,$12,$12,$12,$12,$12,$01,$00,$00,$00,$00,$00
    .byte $0E,$00,$00,$00,$00,$00,$00,$00,$00,$0E,$00,$00,$00,$AA,$A5,$0A
    .byte $00,$00,$0E,$00,$00,$80,$A6,$65,$AA,$00,$00,$0E,$00,$00,$60,$A9
    .byte $9A,$AA,$00,$00,$0E,$00,$00,$A0,$AA,$A9,$6A,$02,$00,$0E,$00,$00
    .byte $58,$AA,$A5,$99,$02,$00,$0E,$00,$00,$A8,$5A,$AA,$5A,$02,$00,$0E
    .byte $00,$00,$96,$6A,$69,$A6,$00,$00,$0E,$00,$00,$AA,$99,$AA,$96,$00
    .byte $00,$0E,$00,$80,$55,$6A,$A5,$29,$00,$00,$0E,$00,$80,$AA,$A5,$AA
    .byte $25,$00,$00,$0E,$00,$60,$55,$6A,$65,$0A,$00,$00,$0E,$00,$A0,$AA
    .byte $A6,$AA,$09,$00,$00,$0E,$00,$58,$55,$55,$55,$02,$00,$00,$0E,$00
    .byte $A8,$AA,$AA,$AA,$02,$00,$00
sprite_30:
    .byte $0F,$13,$05,$09,$09,$09,$09,$0A,$0A,$0A,$01,$00,$00,$00,$00,$00
    .byte $0E,$00,$00,$00,$00,$0E,$00,$00,$00,$00,$0E,$00,$5A,$0A,$00,$0E
    .byte $00,$66,$0A,$00,$0E,$00,$6A,$2A,$00,$0E,$00,$66,$2A,$00,$0E,$00
    .byte $66,$26,$00,$0E,$00,$98,$02,$00,$0E,$00,$9A,$2A,$00,$0E,$00,$6A
    .byte $2A,$00,$0E,$00,$AA,$2A,$00,$0E,$00,$66,$29,$00,$0E,$00,$A6,$26
    .byte $00,$0E,$00,$A6,$29,$00,$0E,$00,$A6,$25,$00,$0E,$00,$A6,$25,$00
    .byte $0E,$00,$A6,$26,$00,$0E,$00,$68,$02,$00,$0E,$00,$A8,$09,$00
sprite_31:
    .byte $0F,$16,$05,$09,$09,$09,$09,$0A,$0A,$0A,$01,$00,$00,$00,$00,$00
    .byte $03,$00,$00,$00,$00,$03,$00,$80,$00,$00,$03,$00,$80,$00,$00,$03
    .byte $00,$A0,$00,$00,$03,$00,$A0,$00,$00,$03,$00,$60,$02,$00,$03,$00
    .byte $A0,$02,$00,$03,$00,$98,$02,$00,$03,$00,$98,$02,$00,$03,$00,$58
    .byte $09,$00,$03,$00,$98,$09,$00,$03,$00,$98,$09,$00,$03,$00,$98,$09
    .byte $00,$03,$00,$58,$09,$00,$03,$00,$98,$02,$00,$03,$00,$98,$02,$00
    .byte $03,$00,$A0,$02,$00,$03,$00,$60,$02,$00,$03,$00,$A0,$00,$00,$03
    .byte $00,$A0,$00,$00,$03,$00,$80,$00,$00,$03,$00,$80,$00,$00
sprite_32:
    .byte $03,$07,$02,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0E,$2A,$0E,$2A,$0E,$08,$0E,$2A,$0E,$2A,$0E,$26,$0E,$2A
sprite_33:
    .byte $0C,$09,$04,$07,$07,$08,$08,$08,$08,$08,$01,$00,$00,$00,$00,$00
    .byte $05,$00,$08,$00,$05,$00,$0A,$00,$05,$00,$08,$00,$05,$00,$20,$00
    .byte $05,$00,$20,$00,$05,$00,$80,$00,$05,$00,$80,$00,$05,$00,$80,$02
    .byte $05,$00,$80,$00
sprite_34:
    .byte $09,$0F,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0D,$00,$02,$00,$0D,$80,$09,$00,$0D,$80,$09,$00,$0D,$00,$02,$00
    .byte $0D,$00,$02,$00,$0D,$00,$02,$00,$0D,$80,$0A,$00,$0D,$80,$09,$00
    .byte $0D,$80,$09,$00,$0D,$80,$09,$00,$0D,$80,$09,$00,$0D,$80,$0A,$00
    .byte $0D,$80,$0A,$00,$0D,$80,$09,$00,$0D,$80,$0A,$00
sprite_35:
    .byte $0C,$0E,$04,$07,$07,$08,$08,$08,$08,$08,$01,$00,$00,$00,$00,$00
    .byte $0E,$00,$0A,$00,$0E,$80,$0A,$00,$0E,$80,$29,$00,$0E,$80,$29,$00
    .byte $0E,$80,$AA,$00,$0E,$80,$9A,$00,$0E,$80,$AA,$02,$0E,$00,$AA,$02
    .byte $0E,$00,$6A,$02,$0E,$00,$66,$02,$0E,$00,$A8,$02,$0E,$00,$98,$02
    .byte $0E,$00,$A0,$02,$0E,$00,$80,$02
sprite_38:
    .byte $09,$06,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $0E,$00,$02,$00,$0E,$80,$02,$00,$0E,$80,$02,$00,$0E,$80,$09,$00
    .byte $0E,$80,$09,$00,$0E,$80,$02,$00
sprite_90:
    .byte $09,$11,$04,$06,$06,$06,$06,$06,$06,$06,$01,$00,$00,$00,$00,$00
    .byte $04,$80,$02,$00,$04,$80,$0A,$00,$04,$80,$0A,$00,$04,$00,$02,$00
    .byte $04,$00,$02,$00,$04,$00,$02,$00,$04,$00,$02,$00,$04,$00,$02,$00
    .byte $04,$00,$02,$00,$04,$00,$02,$00,$04,$00,$02,$00,$04,$00,$02,$00
    .byte $04,$00,$02,$00,$04,$00,$02,$00,$04,$00,$02,$00,$04,$00,$02,$00
    .byte $04,$00,$02,$00
sprite_93:
    .byte $12,$0D,$06,$0B,$0B,$0B,$0B,$0B,$0B,$0C,$01,$00,$00,$00,$00,$00
    .byte $04,$80,$AA,$0A,$00,$00,$04,$80,$55,$29,$00,$00,$04,$80,$5A,$26
    .byte $00,$00,$04,$00,$98,$25,$00,$00,$04,$80,$A9,$2A,$00,$00,$04,$80
    .byte $A5,$09,$00,$00,$04,$00,$AA,$AA,$00,$00,$04,$00,$66,$96,$00,$00
    .byte $04,$00,$A6,$65,$02,$00,$04,$00,$A0,$AA,$02,$00,$04,$00,$68,$55
    .byte $02,$00,$04,$00,$68,$55,$02,$00,$04,$00,$A0,$AA,$02,$00
sprite_112:
    .byte $15,$45,$07,$0C,$0D,$0D,$0D,$0D,$0D,$0D,$01,$00,$00,$00,$00,$00
    .byte $0E,$00,$00,$80,$2A,$00,$00,$0E,$00,$00,$80,$29,$00,$00,$0E,$00
    .byte $00,$60,$29,$00,$00,$0E,$00,$00,$A0,$26,$00,$00,$0E,$00,$00,$A0
    .byte $26,$00,$00,$0E,$00,$00,$A0,$26,$00,$00,$0E,$00,$00,$A0,$26,$00
    .byte $00,$0E,$00,$00,$AA,$A6,$0A,$00,$0E,$00,$00,$A6,$56,$0A,$00,$0E
    .byte $00,$80,$A5,$56,$0A,$00,$0E,$00,$80,$AA,$AA,$09,$00,$0E,$00,$80
    .byte $AA,$AA,$09,$00,$0E,$00,$80,$AA,$AA,$02,$00,$0E,$00,$80,$AA,$AA
    .byte $02,$00,$0E,$00,$80,$AA,$AA,$02,$00,$0E,$00,$00,$A0,$26,$00,$00
    .byte $0E,$00,$00,$A0,$26,$00,$00,$0E,$00,$00,$A0,$26,$00,$00,$0E,$00
    .byte $00,$A0,$26,$00,$00,$0E,$00,$00,$A0,$26,$00,$00,$0E,$00,$00,$A0
    .byte $26,$00,$00,$0E,$00,$00,$A0,$26,$00,$00,$0E,$00,$00,$A0,$26,$00
    .byte $00,$0E,$00,$00,$A0,$26,$00,$00,$0E,$00,$00,$A0,$26,$00,$00,$0E
    .byte $00,$00,$A0,$26,$00,$00,$0E,$00,$00,$A0,$26,$00,$00,$0E,$00,$00
    .byte $A0,$9A,$00,$00,$0E,$00,$00,$98,$9A,$02,$00,$0E,$00,$00,$9A,$A6
    .byte $0A,$00,$0E,$00,$80,$6A,$A6,$2A,$00,$0E,$00,$80,$9A,$AA,$2A,$00
    .byte $0E,$00,$80,$6A,$AA,$2A,$00,$0E,$00,$A0,$6A,$AA,$9A,$00,$0E,$00
    .byte $A0,$9A,$AA,$9A,$00,$0E,$00,$A0,$9A,$AA,$9A,$00,$0E,$00,$A0,$9A
    .byte $AA,$9A,$00,$0E,$00,$A8,$9A,$AA,$9A,$00,$0E,$00,$A8,$A6,$AA,$9A
    .byte $00,$0E,$00,$A8,$A6,$AA,$96,$00,$0E,$00,$A8,$A6,$AA,$96,$00,$0E
    .byte $00,$AA,$A6,$AA,$96,$00,$0E,$00,$AA,$A9,$AA,$26,$00,$0E,$00,$AA
    .byte $A9,$AA,$25,$00,$0E,$00,$AA,$A9,$AA,$25,$00,$0E,$80,$AA,$A9,$AA
    .byte $25,$00,$0E,$80,$6A,$AA,$AA,$09,$00,$0E,$80,$6A,$AA,$6A,$09,$00
    .byte $0E,$80,$6A,$AA,$6A,$09,$00,$0E,$A0,$6A,$AA,$6A,$09,$00,$0E,$A0
    .byte $9A,$AA,$6A,$02,$00,$0E,$A0,$AA,$AA,$5A,$02,$00,$0E,$A0,$AA,$AA
    .byte $5A,$02,$00,$0E,$A8,$AA,$AA,$5A,$02,$00,$0E,$A8,$AA,$AA,$9A,$00
    .byte $00,$0E,$A8,$AA,$AA,$96,$00,$00,$0E,$A8,$AA,$AA,$96,$00,$00,$0E
    .byte $AA,$AA,$AA,$96,$00,$00,$0E,$AA,$AA,$AA,$26,$00,$00,$0E,$AA,$AA
    .byte $AA,$26,$00,$00,$0E,$AA,$AA,$AA,$26,$00,$00,$0E,$AA,$AA,$AA,$26
    .byte $00,$00,$0E,$AA,$AA,$AA,$0A,$00,$00,$0E,$AA,$AA,$AA,$0A,$00,$00
    .byte $0E,$AA,$AA,$AA,$09,$00,$00,$0E,$AA,$AA,$AA,$09,$00,$00,$0E,$AA
    .byte $AA,$AA,$02,$00,$00,$0E,$AA,$AA,$AA,$02,$00,$00,$0E,$AA,$AA,$AA
    .byte $02,$00,$00
sprite_113:
    .byte $12,$31,$06,$0B,$0B,$0B,$0B,$0B,$0B,$0C,$01,$00,$00,$00,$00,$00
    .byte $0E,$00,$00,$20,$00,$00,$0E,$00,$00,$20,$00,$00,$0E,$00,$00,$20
    .byte $00,$00,$0E,$00,$00,$20,$00,$00,$0E,$00,$00,$20,$00,$00,$0E,$00
    .byte $00,$28,$00,$00,$0E,$00,$00,$28,$00,$00,$0E,$00,$00,$68,$09,$00
    .byte $0E,$00,$00,$A8,$09,$00,$0E,$00,$00,$A8,$09,$00,$0E,$00,$00,$AA
    .byte $09,$00,$0E,$00,$80,$AA,$09,$00,$0E,$00,$80,$A9,$0A,$00,$0E,$00
    .byte $80,$69,$2A,$00,$0E,$00,$80,$59,$2A,$00,$0E,$00,$A0,$99,$0A,$00
    .byte $0E,$00,$A0,$69,$0A,$00,$0E,$00,$A0,$A9,$0A,$00,$0E,$00,$A0,$6A
    .byte $0A,$00,$0E,$00,$A0,$59,$0A,$00,$0E,$00,$60,$9A,$0A,$00,$0E,$00
    .byte $A0,$9A,$09,$00,$0E,$00,$80,$AA,$0A,$00,$0E,$00,$80,$A9,$0A,$00
    .byte $0E,$00,$80,$AA,$09,$00,$0E,$00,$80,$A9,$09,$00,$0E,$00,$80,$A9
    .byte $0A,$00,$0E,$00,$80,$A9,$0A,$00,$0E,$00,$80,$66,$02,$00,$0E,$00
    .byte $80,$66,$02,$00,$0E,$00,$80,$AA,$02,$00,$0E,$00,$80,$9A,$02,$00
    .byte $0E,$00,$80,$A6,$0A,$00,$0E,$00,$A0,$9A,$0A,$00,$0E,$00,$A0,$A6
    .byte $0A,$00,$0E,$00,$A8,$A6,$2A,$00,$0E,$00,$A8,$6A,$2A,$00,$0E,$00
    .byte $A8,$6A,$2A,$00,$0E,$00,$AA,$AA,$2A,$00,$0E,$00,$AA,$AA,$2A,$00
    .byte $0E,$80,$AA,$AA,$AA,$00,$0E,$80,$AA,$AA,$AA,$00,$0E,$80,$AA,$AA
    .byte $AA,$00,$0E,$80,$AA,$AA,$AA,$02,$0E,$80,$AA,$AA,$AA,$02,$0E,$A0
    .byte $AA,$AA,$AA,$02,$0E,$A0,$AA,$AA,$AA,$0A,$0E,$A8,$AA,$AA,$AA,$0A
    .byte $0E,$AA,$AA,$AA,$AA,$0A
sprite_200:
    .byte $04,$07,$02,$03,$03,$03,$03,$03,$03,$04,$01,$00,$00,$00,$00,$00
    .byte $05,$AA,$05,$96,$05,$55,$05,$55,$05,$55,$05,$96,$05,$AA
sprite_161:
    .byte $03,$08,$02,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0E,$08,$0E,$08,$0E,$08,$0E,$08,$0E,$08,$0E,$00,$0E,$08,$0E,$00
sprite_162:
    .byte $03,$08,$02,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0E,$0A,$0E,$0A,$0E,$0A,$0E,$00,$0E,$00,$0E,$00,$0E,$00,$0E,$00
sprite_163:
    .byte $03,$08,$02,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0E,$0A,$0E,$0A,$0E,$2A,$0E,$0A,$0E,$2A,$0E,$0A,$0E,$0A,$0E,$00
sprite_164:
    .byte $03,$08,$02,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0E,$08,$0E,$2A,$0E,$0A,$0E,$0A,$0E,$28,$0E,$0A,$0E,$08,$0E,$00
sprite_165:
    .byte $03,$08,$02,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0E,$02,$0E,$22,$0E,$08,$0E,$08,$0E,$02,$0E,$2A,$0E,$28,$0E,$00
sprite_166:
    .byte $03,$08,$02,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0E,$02,$0E,$0A,$0E,$0A,$0E,$02,$0E,$2A,$0E,$0A,$0E,$2A,$0E,$00
sprite_167:
    .byte $03,$08,$02,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0E,$08,$0E,$08,$0E,$08,$0E,$00,$0E,$00,$0E,$00,$0E,$00,$0E,$00
sprite_168:
    .byte $03,$08,$02,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0E,$08,$0E,$02,$0E,$02,$0E,$02,$0E,$02,$0E,$02,$0E,$08,$0E,$00
sprite_169:
    .byte $03,$08,$02,$02,$02,$02,$03,$03,$03,$03,$01,$00,$00,$00,$00,$00
    .byte $0E,$08,$0E,$08,$0E,$20,$0E,$20,$0E,$20,$0E,$08,$0E,$08,$0E,$00
.segment "RODATA"
source_variation: .incbin "room-variation.bin"
atlas_lo: .byte 0,<sprite_1,<sprite_2,<sprite_3,<sprite_4,<sprite_5,<sprite_6,<sprite_7,<sprite_8,<sprite_9,<sprite_10,<sprite_11,<sprite_12,<sprite_13,<sprite_14,<sprite_15,<sprite_16,<sprite_17,<sprite_18,0,<sprite_20,<sprite_21,<sprite_22,<sprite_23,<sprite_24,<sprite_25,<sprite_26,<sprite_27,<sprite_28,<sprite_29,<sprite_30,<sprite_31,<sprite_32,<sprite_33,<sprite_34,<sprite_35,<sprite_36,<sprite_37,<sprite_38,0,<sprite_40,<sprite_41,<sprite_42,<sprite_43,<sprite_44,<sprite_45,<sprite_46,<sprite_47,<sprite_48,<sprite_49,<sprite_50,<sprite_51,<sprite_52,<sprite_53,<sprite_54,<sprite_55,<sprite_56,<sprite_57,<sprite_58,<sprite_59,<sprite_60,<sprite_61,<sprite_62,<sprite_63,<sprite_64,<sprite_65,0,<sprite_67,<sprite_68,<sprite_69,<sprite_70,<sprite_71,<sprite_72,<sprite_73,<sprite_74,<sprite_75,<sprite_76,<sprite_77,<sprite_78,<sprite_79,<sprite_80,<sprite_81,<sprite_82,<sprite_83,<sprite_84,<sprite_85,<sprite_86,<sprite_87,<sprite_88,<sprite_89,<sprite_90,<sprite_91,0,<sprite_93,<sprite_94,<sprite_95,<sprite_96,<sprite_97,<sprite_98,<sprite_99,<sprite_100,<sprite_101,<sprite_102,<sprite_103,0,0,0,0,0,0,<sprite_110,<sprite_111,<sprite_112,<sprite_113,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,<sprite_161,<sprite_162,<sprite_163,<sprite_164,<sprite_165,<sprite_166,<sprite_167,<sprite_168,<sprite_169,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,<sprite_200
atlas_hi: .byte 0,>sprite_1,>sprite_2,>sprite_3,>sprite_4,>sprite_5,>sprite_6,>sprite_7,>sprite_8,>sprite_9,>sprite_10,>sprite_11,>sprite_12,>sprite_13,>sprite_14,>sprite_15,>sprite_16,>sprite_17,>sprite_18,0,>sprite_20,>sprite_21,>sprite_22,>sprite_23,>sprite_24,>sprite_25,>sprite_26,>sprite_27,>sprite_28,>sprite_29,>sprite_30,>sprite_31,>sprite_32,>sprite_33,>sprite_34,>sprite_35,>sprite_36,>sprite_37,>sprite_38,0,>sprite_40,>sprite_41,>sprite_42,>sprite_43,>sprite_44,>sprite_45,>sprite_46,>sprite_47,>sprite_48,>sprite_49,>sprite_50,>sprite_51,>sprite_52,>sprite_53,>sprite_54,>sprite_55,>sprite_56,>sprite_57,>sprite_58,>sprite_59,>sprite_60,>sprite_61,>sprite_62,>sprite_63,>sprite_64,>sprite_65,0,>sprite_67,>sprite_68,>sprite_69,>sprite_70,>sprite_71,>sprite_72,>sprite_73,>sprite_74,>sprite_75,>sprite_76,>sprite_77,>sprite_78,>sprite_79,>sprite_80,>sprite_81,>sprite_82,>sprite_83,>sprite_84,>sprite_85,>sprite_86,>sprite_87,>sprite_88,>sprite_89,>sprite_90,>sprite_91,0,>sprite_93,>sprite_94,>sprite_95,>sprite_96,>sprite_97,>sprite_98,>sprite_99,>sprite_100,>sprite_101,>sprite_102,>sprite_103,0,0,0,0,0,0,>sprite_110,>sprite_111,>sprite_112,>sprite_113,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>sprite_161,>sprite_162,>sprite_163,>sprite_164,>sprite_165,>sprite_166,>sprite_167,>sprite_168,>sprite_169,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>sprite_200
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

; Full-screen, 40-column Apple TEXT for exterior and modal panels.
.segment "LOWCODE"
.export full_text_draw, full_dark_text_draw
full_text_draw:
    jsr full_text_clear
    ldx game_mode
    lda text_panel_hi,x
    beq @compact
    sta src_ptr+1
    lda text_panel_lo,x
    sta src_ptr
    jmp full_panel_draw
@compact:
    ; Reuse the dynamic formatter, then deinterleave its four 80-column rows
    ; into centered 40-column MAIN text. The original HUD rows are erased.
    jsr full_hud_draw
    lda #0
    sta hud_row
@row:
    jsr full_hud_address
    lda dst_ptr
    sta src_ptr
    lda dst_ptr+1
    sta src_ptr+1
.if HGR_MONO
    ldy #39
@save:
    lda (src_ptr),y
    sta HUD_BUFFER,y
    dey
    bpl @save
.else
    ldx #0
    ldy #0
@save:
    jsr aux_read_src
    sta HUD_BUFFER,x
    inx
    lda (src_ptr),y
    sta HUD_BUFFER,x
    inx
    iny
    cpy #20
    bne @save
.endif
    lda #$A0
    ldy #39
@erase:
    sta (src_ptr),y
    dey
    bpl @erase
    lda hud_row
    clc
    adc #8
    jsr full_text_address
    ldy #39
@put:
    lda HUD_BUFFER,y
    sta (dst_ptr),y
    dey
    bpl @put
    inc hud_row
    lda hud_row
    cmp #4
    bne @row
    lda #4
    jsr full_text_address
    lda #<text_heading
    sta menu_ptr
    lda #>text_heading
    sta menu_ptr+1
    ldy #0
@heading:
    lda (menu_ptr),y
    ora #$80
    sta (dst_ptr),y
    iny
    cpy #40
    bne @heading
    lda gold
    sta word_tmp
    lda gold+1
    sta word_tmp+1
    ldy #28
    jmp full_decimal5
full_dark_text_draw:
    ; Full-screen darkness keeps the gameplay HUD at rows 20..23. TEXT column
    ; count matches the lit edition, including the DHGR right-edge feedback.
    jsr full_text_clear
    jsr full_hud_draw
    lda #11
    jsr full_text_address
    ldx #0
.if HGR_MONO
    ldy #11
@message:
    lda dark_message,x
    beq @done
    ora #$80
    sta (dst_ptr),y
    inx
    iny
    bne @message
.else
    ldy #15                ; logical column 31: MAIN, then AUX at next byte
@message:
    lda dark_message,x
    beq @done
    ora #$80
    sta (dst_ptr),y
    inx
    lda dark_message,x
    beq @done
    ora #$80
    iny
    sta $C005
    sta (dst_ptr),y
    sta $C004
    inx
    bne @message
.endif
@done:
    rts
full_text_address:
    tax
    lda text_row_lo,x
    sta dst_ptr
    lda text_row_hi,x
    ldx render_page_index
    beq :+
    clc
    adc #4
:
    sta dst_ptr+1
    rts
.segment "CODE"
full_text_clear:
    lda #0
    sta dst_ptr
    lda #4
    ldx render_page_index
    beq :+
    lda #8
:
    sta dst_ptr+1
    ldx #4
    ldy #0
    lda #$A0
@clear:
    sta (dst_ptr),y
.if !HGR_MONO
    sta $C005
    sta (dst_ptr),y
    sta $C004
.endif
    iny
    bne @clear
    inc dst_ptr+1
    dex
    bne @clear
    rts
.include "full-panels.inc"
text_heading: .byte "L'Aigle d'Or             Or:00000       "
dark_message: .asciiz "Il fait noir ici !"
text_row_lo:
    .byte $00,$80,$00,$80,$00,$80,$00,$80,$28,$A8,$28,$A8
    .byte $28,$A8,$28,$A8,$50,$D0,$50,$D0,$50,$D0,$50,$D0
text_row_hi:
    .byte $04,$04,$05,$05,$06,$06,$07,$07,$04,$04,$05,$05
    .byte $06,$06,$07,$07,$04,$04,$05,$05,$06,$06,$07,$07

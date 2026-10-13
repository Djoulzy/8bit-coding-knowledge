; Full-screen, 40-column Apple TEXT for exterior and modal panels.
.segment "LOWCODE"
.export full_text_draw, full_dark_text_draw
full_text_draw:
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
    iny
    bne @clear
    inc dst_ptr+1
    dex
    bne @clear
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
    ; Draw a fresh hidden TEXT page; never expose the previous merchant panel.
    jsr full_text_draw
    lda #14
    jsr full_text_address
    ldy #0
@message:
    lda dark_message,y
    beq @help
    ora #$80
    sta (dst_ptr),y
    iny
    bne @message
@help:
    lda #15
    jsr full_text_address
    ldy #0
@instruction:
    lda dark_instruction,y
    beq @done
    ora #$80
    sta (dst_ptr),y
    iny
    bne @instruction
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
text_heading: .byte "L'AIGLE D'OR             OR:00000       "
dark_message: .asciiz "           IL FAIT NOIR ICI !"
dark_instruction: .asciiz "      1:TORCHE   I:INVENTAIRE"
text_row_lo:
    .byte $00,$80,$00,$80,$00,$80,$00,$80,$28,$A8,$28,$A8
    .byte $28,$A8,$28,$A8,$50,$D0,$50,$D0,$50,$D0,$50,$D0
text_row_hi:
    .byte $04,$04,$05,$05,$06,$06,$07,$07,$04,$04,$05,$05
    .byte $06,$06,$07,$07,$04,$04,$05,$05,$06,$06,$07,$07

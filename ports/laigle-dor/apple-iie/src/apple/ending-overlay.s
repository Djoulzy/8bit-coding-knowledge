; Loaded only for MODE_DEAD / MODE_WIN, replacing the disposable room baseline.
; MAIN code/data remain readable while draw_cell writes the hidden AUX bank.
.setcpu "6502"
.macpack longbranch
FULL_GAME = 1
DHGR = 1
.include "memory.inc"
.include "ending-symbols.inc"
.segment "ENDING"
ending_entry:
    ; Clear every scanline and address hole in the hidden frame pair.
    lda draw_page_hi
    sta dst_ptr+1
    lda #0
    sta dst_ptr
    ldx #32
    ldy #0
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
    lda #<ending_data
    sta frame_ptr
    lda #>ending_data
    sta frame_ptr+1
    lda #0
    sta ending_y
@row:
    jsr ending_address
    lda #0
    sta cell_x
@run:
    jsr ending_read
    sta ending_count
    jsr ending_read
    sta cell_color
@cell:
    lda cell_color
    beq :+
    jsr draw_cell
:
    inc cell_x
    dec ending_count
    bne @cell
    lda cell_x
    cmp #CELL_LIMIT
    bne @run
    inc ending_y
    lda ending_y
    cmp #192
    bne @row
    lda game_mode
    cmp #MODE_DEAD
    jne @done
    lda #0
    sta ending_person
@person:
    lda ending_person
    asl a
    clc
    adc ending_person
    asl a
    sta ending_name_index
    lda #0
    sta ending_character
@letter:
    ldx ending_name_index
    lda $1380,x            ; six typed name characters per session attempt
    and #$7F
    ldx #0
    stx src_ptr+1
    asl a
    rol src_ptr+1
    asl a
    rol src_ptr+1
    asl a
    rol src_ptr+1
    clc
    adc #<ending_font
    sta src_ptr
    lda src_ptr+1
    adc #>ending_font
    sta src_ptr+1
    lda #164
    sta ending_y
@glyph_row:
    jsr ending_address
    lda ending_y
    sec
    sbc #164
    tay
    lda (src_ptr),y
    sta ending_bits
    ldx ending_person
    lda ending_positions,x
.if !HGR_MONO
    lsr a
    clc
    adc #10
.endif
    sta cell_x
    lda ending_character
.if HGR_MONO
    asl a
    clc
    adc ending_character
    asl a
.else
    asl a
    clc
    adc ending_character
.endif
    clc
    adc cell_x
    sta cell_x
    lda #6/(2-HGR_MONO)
    sta ending_count
@dot:
    lda ending_bits
.if HGR_MONO
    and #$20
.else
    and #$30
.endif
    beq :+
    lda #15
:
    sta cell_color
    jsr draw_cell
    asl ending_bits
.if !HGR_MONO
    asl ending_bits
.endif
    inc cell_x
    dec ending_count
    bne @dot
    inc ending_y
    lda ending_y
    cmp #172
    bne @glyph_row
    inc ending_name_index
    inc ending_character
    lda ending_character
    cmp #6
    jne @letter
    inc ending_person
    lda ending_person
    cmp session_attempt
    jne @person
@done:
    ldx render_page_index
    lda #0
    sta dirty_valid,x
    rts
ending_read:
    ldy #0
    lda (frame_ptr),y
    inc frame_ptr
    bne :+
    inc frame_ptr+1
:
    rts
ending_address:
    ldx ending_y
    lda row_lo,x
    sta dst_ptr
    lda row_hi,x
    and #$1F
    ora draw_page_hi
    sta dst_ptr+1
    rts
ending_y: .byte 0
ending_count: .byte 0
ending_person: .byte 0
ending_character: .byte 0
ending_name_index: .byte 0
ending_bits: .byte 0
ending_font: .incbin "ending-font.bin"
ending_positions: .incbin "ending-positions.bin"
ending_data:                 ; selected scene's row-bounded RLE follows the code

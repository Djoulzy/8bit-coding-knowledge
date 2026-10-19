; Native seven-bit rows shared in AUX. Each row is an AUX pointer to
; interleaved mask/pixel bytes, aligned at phase zero. Shift once per byte,
; then compose once per destination byte. No CPU beyond documented NMOS 6502.
.export draw_native_sprite
.exportzp static_draw, scene_additive
draw_native_sprite:
    ; A seven-bit rotation table for this horizontal phase. Modulo 127
    ; generates the rotations without shifting every source byte at runtime.
    ; MAIN $0200 is disk scratch: rebuild on each call, including after maps.
    lda #1
    ldx phase
    beq :+
@power:
    asl a
    dex
    bne @power
:
    sta native_step
    sec
    sbc #1
    sta native_carry
    eor #$7F
    sta native_keep
    ldx #0
    txa
@table:
    sta NATIVE_ROTATE,x
    clc
    adc native_step
    cmp #128
    bcc :+
    sbc #127
:
    inx
    bpl @table
@row:
    jsr clock_sample
    ldx row_y
    cpx #200
    jcs @done
    lda y_map,x
    cmp #$FF
    jeq @advance
    ldy static_draw
    beq :+
    cmp y_map+1,x           ; retain static last-source-row sampling policy
    jeq @advance
:
    tax
    lda row_lo,x
    sta dst_ptr
    lda row_hi,x
    and #$1F
    ora draw_page_hi
    sta dst_ptr+1
    ldy #0
    jsr aux_read_src
    sta native_row_lo
    iny
    jsr aux_read_src
    tax
    lda src_ptr
    sta native_table
    lda src_ptr+1
    sta native_table+1
    stx src_ptr+1
    lda native_row_lo
    sta src_ptr
    lda native_width
    asl a
    tay
    dey
    jsr aux_read_row
    lda x_column
    sta serial_col
    lda #0
    sta native_mask_carry
    sta native_pixel_carry
    sta data_cursor
    lda native_width
    sta native_left
@byte:
    ldy data_cursor
    ldx NATIVE_ROW,y
    lda NATIVE_ROTATE,x
    sta raw_mask
    and native_keep
    ora native_mask_carry
    sta mask
    lda raw_mask
    and native_carry
    sta native_mask_carry
    iny
    ldx NATIVE_ROW,y
    lda NATIVE_ROTATE,x
    sta raw_pixel
    and native_keep
    ora native_pixel_carry
    sta pixel
    lda raw_pixel
    and native_carry
    sta native_pixel_carry
    iny
    sty data_cursor
    jsr native_emit
    inc serial_col
    dec native_left
    bne @byte
    lda native_mask_carry
    sta mask
    lda native_pixel_carry
    sta pixel
    jsr native_emit
    lda native_table
    sta src_ptr
    lda native_table+1
    sta src_ptr+1
@advance:
    clc
    lda src_ptr
    adc #2
    sta src_ptr
    bcc :+
    inc src_ptr+1
:
    inc row_y
    dec sprite_h
    jne @row
@done:
    rts

native_emit:
.if HGR_MONO
    ; The centered source viewport ends at native x=260: byte 37, bit 0.
    lda serial_col
    cmp #38
    bcs @done
    cmp #37
    bne :+
    lda mask
    and #1
    sta mask
    lda pixel
    and #1
    sta pixel
:
    lda mask
    beq @done
    eor #$FF
    ldy serial_col
    and (dst_ptr),y
    ora pixel
    sta (dst_ptr),y
.else
    lda serial_col
    cmp #80
    bcs @done
    lda mask
    beq @done
    jmp write_fragment
.endif
@done:
    rts

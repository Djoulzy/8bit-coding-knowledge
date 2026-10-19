; Native mixed DHGR has 80-column text: aux char, main char, at each byte column.
dhgr_hud_init_aux:
    lda #$A0
    sta $C005
    ldx #0
@clear:
    sta $0400,x
    sta $0500,x
    sta $0600,x
    sta $0700,x
    sta $0800,x
    sta $0900,x
    sta $0A00,x
    sta $0B00,x
    inx
    bne @clear
    sta $C004
    rts

; hud_draw first builds its compact 40-character line in hidden main text RAM.
; Convert via a main-RAM buffer before overwriting that compact line.
dhgr_hud_finish:
.if HGR_MONO
    rts
.else
    lda #0
    sta hud_row
@row:
.if FULL_GAME
    jsr clock_sample
.endif
    ldx hud_row
    lda hud_row_lo,x
    sta dst_ptr
    lda hud_row_hi,x
    ldx render_page_index
    beq :+
    clc
    adc #4
:
    sta dst_ptr+1
    ldy #39
@save:
    lda (dst_ptr),y
    sta HUD_BUFFER,y
    dey
    bpl @save
    ldy #0
@pair:
    cpy #20
    bcs @blank
    tya
    asl a
    tax
    lda HUD_BUFFER,x
    sta $C005
    sta (dst_ptr),y
    sta $C004
    inx
    lda HUD_BUFFER,x
    jmp @main
@blank:
    lda #$A0
    sta $C005
    sta (dst_ptr),y
    sta $C004
@main:
    sta (dst_ptr),y
    iny
    cpy #40
    bne @pair
    inc hud_row
    lda hud_row
    cmp #4
    bne @row
.if FULL_GAME
    jmp full_wide_feedback
.else
    rts
.endif
.endif

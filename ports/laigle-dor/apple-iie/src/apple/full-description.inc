; B2 4150-4170: retain source priority, geometry and room-number bands.
; full_hud_draw already blanked both description rows on the hidden page.
full_room_description:
    lda #0
    sta hud_row
    jsr full_hud_address
    ldx #0
    ldy #0
    jsr full_hud_description
    ldx #1
    lda current_room
    cmp #1
    beq @phrase
    ldx #10
    lda in_pit
    bne @phrase
    ldx #3
    lda current_room
    cmp #63
    beq @phrase
    ldx #2
    cmp #62
    beq @phrase
    cmp #33
    beq @phrase
    ldx room_geometry
    cpx #2
    beq @floor             ; source has no SP=2 phrase
    lda hud_geometry_phrase,x
    tax
    jsr full_hud_description
@floor:
    lda #1
    sta hud_row
    jsr full_hud_address
    ldy #0
    ldx #7
    lda current_room
    cmp #9
    bcc @phrase
    ldx #8
    cmp #58
    bcs @phrase
    ldx #9
@phrase:
    ; Special-room phrases can exceed 30 columns with the prefix. Keep the
    ; prefix on row 0 and move their complete phrase to row 1 during feedback.
    lda hud_row
    bne full_hud_description
    jsr full_feedback_index
    bcc full_hud_description
.if !HGR_MONO
    jsr full_is_dark
    bcc full_hud_description ; 80-column HUD has room for the complete phrase
.endif
    txa
    pha
    inc hud_row
    jsr full_hud_address
    pla
    tax
    ldy #0
    ; Y retains the prefix length on row 0; row 1 starts at column zero.
full_hud_description:
    lda hud_description_lo,x
    sta menu_ptr
    lda hud_description_hi,x
    sta menu_ptr+1
full_hud_string:
    ldx #0
@char:
    lda (menu_ptr,x)
    beq @done
    ora #$80
    sta (dst_ptr),y
    iny
    inc menu_ptr
    bne @char
    inc menu_ptr+1
    bne @char
@done:
    rts

; Right-align the gameplay numbers without zero padding; keep a final zero.
.segment "LOWCODE"
full_hud_trim:
    dex
    beq @done
@digit:
    lda (dst_ptr),y
    cmp #$B0
    bne @done
    lda #$A0
    sta (dst_ptr),y
    iny
    dex
    bne @digit
@done:
    rts
.segment "RODATA"
hud_geometry_phrase: .byte 4,5,0,6
.segment "CODE"

; Four 40-column rows (20..23), written only on the hidden text page.
.export hud_init, hud_draw
hud_init:
.if DHGR
    jsr dhgr_hud_init_aux
.endif
    ; Boot sector has transferred control: both text pages are ours.
    lda #$A0
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
    rts
hud_draw:
.if FULL_GAME
    jmp full_hud_draw
.endif
    lda #0
    sta hud_row
@row:
    ldx hud_row
    lda hud_text_lo,x
    sta hud_ptr
    lda hud_text_hi,x
    sta hud_ptr+1
    lda hud_row_lo,x
    sta dst_ptr
    lda hud_row_hi,x
    ldx render_page_index
    beq :+
    clc
    adc #4
:
    sta dst_ptr+1
    ldy #0
@character:
    lda (hud_ptr),y
    ora #$80
    sta (dst_ptr),y
    iny
    cpy #40
    bne @character
    inc hud_row
    lda hud_row
    cmp #4
    bne @row
    lda #$D0
    sta dst_ptr
    lda #6
    ldx render_page_index
    beq :+
    clc
    adc #4
:
    sta dst_ptr+1
    lda actor_x
    ldy #11
    jsr hud_decimal2
    lda actor_y
    ldy #16
    jsr hud_decimal3
    lda #$50
    sta dst_ptr
    inc dst_ptr+1           ; row 22 $0750 or $0B50
    ldx #0
    lda pose
    cmp #4
    bcc :+
    ldx #2
:
    lda walking
    beq :+
    ldx #1
:
    lda last_event
    cmp #EVENT_EXIT
    bne :+
    lda pose
    cmp #4
    bcs :+
    lda walking
    bne :+
    ldx #3
:
    lda hud_status_lo,x
    sta hud_ptr
    lda hud_status_hi,x
    sta hud_ptr+1
    ldy #0
@status:
    lda (hud_ptr),y
    ora #$80
    sta (dst_ptr),y
    iny
    cpy #8
    bne @status
.if DHGR
    jmp dhgr_hud_finish
.else
    rts
.endif
hud_decimal3:
    ldx #0
@hundreds:
    cmp #100
    bcc @hundreds_ready
    sec
    sbc #100
    inx
    bne @hundreds
@hundreds_ready:
    sta tmp
    txa
    ora #$B0
    sta (dst_ptr),y
    iny
    lda tmp
hud_decimal2:
    ldx #0
@tens:
    cmp #10
    bcc @tens_ready
    sec
    sbc #10
    inx
    bne @tens
@tens_ready:
    sta tmp
    txa
    ora #$B0
    sta (dst_ptr),y
    iny
    lda tmp
    ora #$B0
    sta (dst_ptr),y
    rts
hud_row_lo: .byte $50,$D0,$50,$D0
hud_row_hi: .byte $06,$06,$07,$07
hud_text_lo: .byte <hud_line0,<hud_line1,<hud_line2,<hud_line3
hud_text_hi: .byte >hud_line0,>hud_line1,>hud_line2,>hud_line3
hud_line0: .byte "FORCES:100% POINTS:00000 OR:00500       "
hud_line1: .byte "SALLE:12 X:19 Y:140 MAIN:VIDE           "
hud_line2: .byte "IMMOBILE                                "
hud_line3: .byte "FLECHES:MARCHE A:ACCROUPI ESPACE:STOP   "
hud_status_lo: .byte <hud_idle,<hud_walk,<hud_crouch,<hud_exit
hud_status_hi: .byte >hud_idle,>hud_walk,>hud_crouch,>hud_exit
hud_idle: .byte "IMMOBILE"
hud_walk: .byte "MARCHE  "
hud_crouch: .byte "ACCROUPI"
hud_exit: .byte "PASSAGE "

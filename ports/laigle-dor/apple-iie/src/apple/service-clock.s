; Sample IIe RDVBLBAR at bounded rendering intervals. Only periodic strength
; loss and torch wear use this timebase; collision/action rules stay immediate.
; 18 refreshes approximate the previous warm-room ~300 ms at 60 Hz.
.export clock_sample, clock_reset, clock_vbls, clock_last_vbl
SERVICE_REFRESHES = 18
clock_reset:
    lda #0
    sta clock_vbls
    lda $C019
    and #$80
    sta clock_last_vbl
    rts
clock_sample:
    pha
    lda game_mode
    beq :+
    lda #0
    sta clock_vbls          ; menus/help pause wear, with no accumulated debt
:
    lda $C019
    and #$80
    cmp clock_last_vbl
    beq @done
    sta clock_last_vbl
    cmp #0
    bne @done              ; count entry into blank, not both transitions
    lda game_mode
    bne @done
    lda clock_vbls
    cmp #(SERVICE_REFRESHES*2-1)
    bcs @done              ; bounded pending time, no runaway catch-up
    inc clock_vbls
@done:
    pla
    rts

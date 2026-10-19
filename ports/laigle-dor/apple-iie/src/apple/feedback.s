; The compact HUD occupies the left 40 columns in DHGR. Put refusal feedback
; at the actual right edge (columns 70-79), after the normal bank interleave.
; Full-screen darkness is 40-column TEXT and uses the compact formatter instead.
.if !HGR_MONO
.segment "EXTRACODE"
full_wide_feedback:
    lda game_mode
    bne @done
    lda message_id
    cmp #1
    bne @done
    jsr full_is_dark
    bcs @done
    lda #0
    sta hud_row
    jsr full_hud_address
    ldy #35
    ldx #0
@pair:
    lda hud_impossible,x
    sta $C005
    sta (dst_ptr),y
    sta $C004
    inx
    lda hud_impossible,x
    sta (dst_ptr),y
    inx
    iny
    cpy #40
    bne @pair
@done:
    rts
.segment "CODE"
.endif

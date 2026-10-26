; Returns C set and game_tmp = ten-column field offset for a visible outcome.
; IDs 2..6 are successful actions with no transient text. Preserve X and Y:
; description formatting keeps its phrase index and prefix length there.
.segment "LOWCODE"
full_feedback_index:
    lda message_id
    cmp #MSG_IMPOSSIBLE
    beq @first
    sec
    sbc #MSG_EMPTY-1
    beq @none
    bcc @none
    cmp #(MSG_FOUND_LEAD-MSG_EMPTY+2)
    bcs @none
    sta game_tmp
    asl a
    asl a
    adc game_tmp
    asl a
    bcc @offset            ; maximum index 13: 130 bytes, no carry
@first:
    lda #0
@offset:
    sta game_tmp
    sec
    rts
@none:
    clc
    rts

full_compact_feedback:
.if !HGR_MONO
    rts                    ; DHGR keeps its 80-column HUD even in darkness TEXT
.else
    jsr full_feedback_index
    bcc @done
    lda #0
    sta hud_row
    jsr full_hud_address
    ldx game_tmp
    ldy #30
@char:
    lda hud_feedback,x
    sta (dst_ptr),y
    inx
    iny
    cpy #40
    bne @char
@done:
    rts
.endif

; The compact HUD occupies the left 40 columns in DHGR. Put outcome feedback
; at the actual right edge (columns 70-79), after the normal bank interleave.
; Full-screen darkness retains these same 80-column positions.
.if !HGR_MONO
.segment "EXTRACODE"
full_wide_feedback:
    lda game_mode
    bne @done
    jsr full_feedback_index
    bcc @done
    lda #0
    sta hud_row
    jsr full_hud_address
    ldy #35
    ldx game_tmp
@pair:
    lda hud_feedback,x
    sta $C005
    sta (dst_ptr),y
    sta $C004
    inx
    lda hud_feedback,x
    sta (dst_ptr),y
    inx
    iny
    cpy #40
    bne @pair
@done:
    rts
.endif
.segment "CODE"

; Grow the two interleaved columns of the original shared grille atlas from
; the ceiling. Immutable terrain stays unchanged until the animation completes.
.segment "CODE"
scene_gate_rows:
    ldx action_kind
    cpx #ACTION_GATE
    bne @done
    cmp action_phase
    bcc @done
    lda action_phase
@done:
    rts

full_draw_gate:
    lda action_kind
    cmp #ACTION_GATE
    bne @done
    lda actor_x
    pha
    lda actor_y
    pha
    jsr scene_gate_bars
    lda #0
    sta static_draw
    sta scene_additive
    pla
    sta actor_y
    pla
    sta actor_x
    ; Both banks/pages restore the whole falling effect before the next stage.
    ldx render_page_index
    lda #0
    sta dirty_left,x
    sta dirty_top,x
    lda #RENDER_COLUMNS
    sta dirty_right,x
    lda #VIEW_HEIGHT
    sta dirty_bottom,x
    lda #1
    sta dirty_valid,x
@done:
    rts

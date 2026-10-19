; Conservative per-page reuse of an idle, empty-handed actor. The central
; region cannot overlap either wall flame. Moving actors, equipment, enemies,
; hazards, pits and new terrain always use the ordinary compositor.
.export actor_cache, cache_frame
actor_cache:
    ldx render_page_index
    lda game_mode
    ora held_item
    ora action_kind
    ora enemy_kind
    ora hazard_active
    ora in_pit
    ora walking
    bne @invalidate
    jsr full_is_dark
    bcs @invalidate
    lda actor_x
    cmp #8
    bcc @invalidate
    cmp #28
    bcs @invalidate
    lda terrain_pending
    and title_page_bits,x
    bne @remember
    lda dirty_valid,x
    beq @remember
    lda actor_x
    cmp cache_x,x
    bne @remember
    lda actor_y
    cmp cache_y,x
    bne @remember
    lda facing
    cmp cache_facing,x
    bne @remember
    lda frame_id
    cmp cache_frame,x
    bne @remember
    sec
    rts
@invalidate:
    lda #$FF
    sta cache_frame,x
    clc
    rts
@remember:
    lda actor_x
    sta cache_x,x
    lda actor_y
    sta cache_y,x
    lda facing
    sta cache_facing,x
    lda frame_id
    sta cache_frame,x
    clc
    rts

; Source B2 $40C8-$411F: flames 36/37 at x=4/35,y=64 (DEC x before draw),
; hand flames 72/73 after the equipment-position transform at $3EF8.
; Cadence is native: two controller ticks per frame, no game RNG calls.
.export full_draw_torches
full_draw_torches:
    lda actor_x
    pha
    lda actor_y
    pha
    lda in_pit
    jne @done
    lda room_light
    beq @done
    cmp #3
    bne @local
    lda current_room
    asl a
    asl a
    tax
    lda WORLD,x
    and #3
    cmp #3
    beq @both              ; relighting one lamp cannot freeze the other
@local:
    ldx current_room
    lda lamp_history,x
    beq @done
    bne @fixtures          ; transient one-fixture lighting remains one flame
@both:
    lda #3
    bne @fixtures
@fixtures:
    pha
    and #1
    beq @right
    lda #12                ; serial byte-column bounds, cells 22..30
    sta repair_left
    lda #18
    sta repair_right
    jsr @restore
    lda #18                ; CURSET anchor -> source left 24
    sta scene_x
    jsr @flame
@right:
    pla
    and #2
    beq @done
    lda #65                ; cells 115..123
    sta repair_left
    lda #71
    sta repair_right
    jsr @restore
    lda #204               ; CURSET anchor -> source left 210
    sta scene_x
    jsr @flame
@done:
    lda #0
    sta static_draw
    sta scene_additive
    pla
    sta actor_y
    pla
    sta actor_x
    rts
@restore:
    lda y_map+64
    sta repair_y
    lda y_map+81
    clc
    adc #1
    sta repair_bottom
    jmp repair_rectangle
@flame:
    lda #64
    sta scene_y
    lda tick_lo
    lsr a
    and #1
    clc
    adc #36
    sta scene_id
    lda #0
    sta scene_additive
    jmp scene_stamp         ; static_draw avoids expanding actor dirty bounds

full_draw_hand_flame:
    lda held_item
    cmp #1
    bne @done
    lda #0
    sta static_draw
    sta scene_additive
    lda tick_lo
    lsr a
    and #1
    clc
    adc #72
    tax
    lda atlas_lo,x
    sta src_ptr
    lda atlas_hi,x
    sta src_ptr+1
    ldx pose
    cpx #8
    bcc :+
    ldx facing            ; walking uses standing equipment positions
:
    lda hand_flame_x,x
    sta dx
    lda hand_flame_y,x
    sta dy
    jmp draw_sprite_pointer
@done:
    rts
; B2 $4120-$412F and $3EF8. Signed y offsets retained from source.
hand_flame_x: .byte $FF,2,$FF,2,$FF,2,$FF,2 ; DEC x at $40B2
hand_flame_y: .byte 197,197,197,199,207,207,207,209

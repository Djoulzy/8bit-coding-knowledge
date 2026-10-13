; Apple target adaptation, not a claim of original Oric collision equivalence.
; Retain the source semantic grid, sample proposed feet rather than a broad
; 4/5-cell look-ahead. Five-row motion uses nearest 140/160/180 depth bands.
.segment "LOWCODE"
.export full_collision_probe, full_pickup_probe, full_fixture_reach
.export move_x, move_y
full_collision_probe:
    lda #0
    sta blocked
    sta object_status
    lda #4
    sta door_status
    lda actor_x
    sta move_x
    cmp #2
    jcc @blocked
    cmp #35
    jcs @blocked
    lda actor_y
    sta move_y
    cmp #181
    jcs @blocked
    ldx room_geometry
    cmp geometry_far,x
    jcc @blocked
    lda facing
    cmp #1
    beq @right
    cmp #2
    beq @left
    cmp #3
    beq @up
    lda actor_y
    cmp #180
    jeq @blocked
    clc
    adc #5
    cmp #181
    bcc :+
    lda #180
:
    sta move_y
    jmp @sample
@right:
    lda actor_x
    cmp #34
    bne @right_step
    lda actor_y
    cmp #175
    jcc @blocked
    lda room_fields+2
    jmp @door
@right_step:
    inc move_x
    bne @sample
@left:
    lda actor_x
    cmp #2
    bne @left_step
    lda actor_y
    cmp #175
    jcc @blocked
    lda room_fields+1
    jmp @door
@left_step:
    dec move_x
    jmp @sample
@up:
    lda actor_y
    ldx room_geometry
    cmp geometry_far,x
    bne @up_step
    lda actor_x
    cmp #18
    bcc @blocked
    cmp #21
    bcs @blocked
    lda room_fields
@door:
    sta door_status
    cmp #3
    bcc @blocked
    rts
@up_step:
    sec
    sbc #5
    cmp geometry_far,x
    bcs :+
    lda geometry_far,x       ; clamp irregular action heights to the foot plane
:
    sta move_y
@sample:
    jsr full_floor_envelope
    bcc @blocked
    jsr full_grid_feet
    lda GRID,x
    cmp #1
    bne :+
    sta object_status
:
    ; Source side-wall sentinels are replaced by the explicit portal planes.
    cpx #3
    beq @clear
    cpx #37
    beq @clear
    lda GRID,x
    bpl @clear
@blocked:
    lda #1
    sta blocked
@clear:
    rts

; Input move_x/move_y -> X=bounded semantic cell under the center of the feet.
full_grid_feet:
    lda move_x
    clc
    adc #2
    tax
    lda move_y
    cmp #171
    bcs @done
    txa
    clc
    adc #40
    tax
    lda move_y
    cmp #151
    bcs @done
    txa
    clc
    adc #40
    tax
@done:
    rts

; Perspective floor corridor. Without this, narrowing the source probes can
; slip through gaps between its isolated wall sentinels. Side-door lanes begin
; at y=175; elsewhere keep the proposed feet inside the shared wall geometry.
full_floor_envelope:
    lda move_y
    cmp #175
    bcs @inside
    sec
    sbc #125
    ldx #0
@depth:
    cmp #5
    bcc @band
    sbc #5
    inx
    bne @depth
@band:
    txa
    ldx room_geometry
    clc
    adc floor_table_offset,x
    tax
    lda floor_min_x,x
    cmp move_x
    beq :+
    bcs @outside
:
    sta game_tmp
    lda #36
    sec
    sbc game_tmp
    cmp move_x
    bcc @outside
@inside:
    sec
    rts
@outside:
    clc
    rts
floor_table_offset: .byte 0,10,10,20
floor_min_x:
    .byte 6,6,6,6,6,6,5,5,4,4  ; geometry 0, only y>=145 is reachable
    .byte 8,7,7,6,6,6,5,5,4,4  ; geometries 1/2
    .byte 5,5,5,5,5,5,5,5,4,4  ; geometry 3, only y>=155 is reachable

; P picks the adjacent cell in front of the feet; crouch/held guards in rules.
full_pickup_probe:
    lda actor_x
    sta move_x
    lda actor_y
    sta move_y
    ldx facing
    lda actor_x
    clc
    adc step_x,x
    sta move_x
    lda actor_y
    clc
    adc step_y,x
    sta move_y
    jsr full_grid_feet
    cpx #120
    bcs @deny
    lda GRID,x
    cmp #160
    beq @done
@deny:
    lda #0
@done:
    rts

; Table/chest/quest anchor remains source x=27,y=160, with a small approach
; window so reduced clearance cannot leave the exact source pose behind.
; Carry set when within x=27..30,y=155..165; facing/held/pose checked by caller.
full_fixture_reach:
    lda actor_x
    cmp #27
    bcc @no
    cmp #31
    bcs @no
    lda actor_y
    cmp #155
    bcc @no
    cmp #166
    bcs @no
    sec
    rts
@no:
    clc
    rts
.segment "CODE"

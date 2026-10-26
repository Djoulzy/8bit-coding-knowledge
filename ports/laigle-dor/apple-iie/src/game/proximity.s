; Apple target adaptation, not a claim of original Oric collision equivalence.
; Retain the source semantic grid, sample proposed feet rather than a broad
; 4/5-cell look-ahead. Five-row motion uses nearest 140/160/180 depth bands.
.segment "LOWCODE"
.export full_collision_probe, full_pickup_probe, full_fixture_reach, full_chest_reach
.export move_x, move_y
full_collision_probe:
    lda #0
    sta blocked
    sta object_status
    lda #4
    sta door_status
    lda in_pit
    beq full_room_collision
    jmp full_pit_collision
full_room_collision:
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
    ; x=17 puts the 12-dot feet at 114..125, inside atlas 5's far arch.
    ; Retain the existing right-side tolerance and source arrival x=19.
    cmp #17
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
    jsr full_furniture_overlap
    bcs @blocked
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
    ; Furnishings with a geometric barrier do not use their coarse depth band.
    ; Keep the historical grid intact for other semantic consumers.
    lda GRID,x
    cmp #151
    bne @table
    ldy room_furnishing
    cpy #4
    beq @clear
@table:
    cmp #153
    bne @chest
    ldy room_furnishing
    cpy #5
    beq @clear
@chest:
    cmp #154
    bne @obstacle
    ldy room_furnishing
    cpy #7
    beq @clear
@obstacle:
    lda GRID,x
    bpl @clear
@blocked:
    lda #1
    sta blocked
@clear:
    rts

; Dedicated pit floor, B2 7030-7040 outline (target foot-envelope adaptation).
; Do not use the ordinary room's portals, geometry-3 envelope or coarse GRID.
; Stable feet span [(x+2)*6,(x+4)*6), not the full animated sprite silhouette.
full_pit_collision:
    ldx facing
    lda actor_x
    clc
    adc step_x,x
    sta move_x
    lda actor_y
    clc
    adc step_y,x
    sta move_y
full_pit_envelope:           ; A=move_y; blocked was cleared by the caller
    sec
    sbc #160
    cmp #36                 ; floor y=160..195; unsigned rejects both ends
    bcs @blocked
    ldx #0
@depth:
    cmp #5
    bcc @band
    sbc #5
    inx
    bne @depth
@band:
    lda move_x
    cmp pit_min_x,x
    bcc @blocked
    cmp pit_limit_x,x
    bcs @blocked
    rts                     ; blocked=0 and door_status=4 from the entry point
@blocked:
    inc blocked
    rts
; Conservative bounds at the back edge of each five-row band, inside the
; source trapezoid: (104,159)-(134,159)-(157,179)-(166,199)-(72,199)-(81,179).
.segment "CODE"
pit_min_x: .byte 16,15,14,13,12,12,11,11
pit_limit_x: .byte 19,20,21,22,23,23,24,24
.segment "LOWCODE"

; Check the horizontal jump's landing at the original foot depth. Airborne
; y is visual height and must not be mistaken for walking into the back wall.
full_pit_jump_guard:
    ldy #0
    sty blocked
    ldx facing
    lda step_x,x
    asl a
    asl a
    asl a
    clc
    adc actor_x
    sta move_x
    lda actor_y
    sta move_y
    jmp full_pit_envelope

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

; Quest pedestal anchor remains source x=27,y=160, with a small approach
; window so reduced clearance cannot leave the exact source pose behind.
; Carry set when within x=27..30,y=155..165; facing/held/pose checked by caller.
; Chest access uses full_chest_reach instead: its front must stay reachable.
.segment "CODE"
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

; Carry set when the proposed 12-dot foot base crosses a furnishing barrier.
; The barrier reaches the rear floor plane: with scenery baked into the room
; baseline, passing behind furniture would incorrectly draw the actor over it.
; Chair 4 / atlas 23: x=[168,186), front=97+41 or 120+41.
; Table 5 / atlas 25: x=[168,210), front=130+36 in geometry 0;
;                   x=[162,204), front=107+36 in the other geometries.
; Chest 7 / atlas 26/27: stable body x=[180,210), front=136+30=126+40=166.
; Stable feet [(move_x+2)*6,(move_x+4)*6) give the actor-x intervals below.
; This replaces only matching 151/153/154 marks; the semantic grid is retained.
full_furniture_overlap:
    ldx room_geometry
    lda room_furnishing
    cmp #7
    beq @chest
    cmp #5
    beq @table
    cmp #4
    bne @clear
    beq @check
@chest:
    ldx #8                  ; same body/front for all geometries, open or closed
    bne @check
@table:
    txa
    clc
    adc #4
    tax
@check:
    lda move_x
    cmp furniture_min_x,x
    bcc @clear
    cmp furniture_limit_x,x
    bcs @clear
    lda move_y
    cmp furniture_front_y,x
    bcs @clear
    sec
    rts
@clear:
    clc
    rts
; Geometry 0/1/2/3 for chair/table, then one shared chest. Front y exclusive.
furniture_min_x:   .byte 25,25,25,25, 25,24,24,24, 27
furniture_limit_x: .byte 29,29,29,29, 33,32,32,32, 33
furniture_front_y: .byte 161,138,138,161, 166,143,143,143, 166

; Carry set for chest O/P within x=26..32,y=155..175. The left approach x=26
; and front y=170/175 remain outside its barrier; original x=27,y=160 is kept.
; The caller checks furnishing 7, open state and held-item rules as needed.
full_chest_reach:
    lda actor_x
    cmp #26
    bcc @no
    cmp #33
    bcs @no
    lda actor_y
    cmp #155
    bcc @no
    cmp #176
    bcs @no
    sec
    rts
@no:
    clc
    rts

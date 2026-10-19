; Translated B2 10000–10510, 5030; restricted to room 12, empty hand.
; No Apple I/O here. key_action = 0..3 direction,4 stop,5 crouch,$FF no key.
; Host oracle: model/movement.py. W07 consumes EVENT_EXIT; W06 stops at portal.
.export game_reset, game_tick, collision_probe
.export actor_x, actor_y, facing, pose, walking, walk_phase, tick_lo, tick_hi
.export last_event, event_head, event_count, event_overflow, frame_id
.export blocked, door_status, object_status, key_action

game_reset:
    lda #0
    ldx #16
@clear:
    sta STATE,x
    dex
    bpl @clear
    lda #19
    sta actor_x
    lda #140
    sta actor_y
    lda #$FF
    sta key_action
.if FULL_GAME
    jmp full_reset
.else
    rts
.endif

game_tick:
.if FULL_GAME
    jsr full_ui_key
    bcc :+
    rts
:
.endif
    inc tick_lo
    bne :+
    inc tick_hi
:
.if FULL_GAME
    jsr full_dispatch
    bcc :+
    jmp update_frame
:
.endif
    lda key_action
    cmp #4
    bcs @other
    lda walking
    beq @direction
    lda #EVENT_STOP
    jsr log_event
    jmp stop_actor
@direction:
    lda pose
    cmp #4
    bcc @standing
    lda key_action
    sta facing
    clc
    adc #4
    sta pose
    jmp update_frame
@standing:
    lda key_action
    cmp facing
    beq @walk
    sta facing
    sta pose
    jmp update_frame
@walk:
    lda #1
    sta walking
    sta walk_phase
    jmp continue_walk
@other:
    cmp #4
    bne @crouch
    lda walking
    beq stop_actor
    lda #EVENT_STOP
    jsr log_event
    jmp stop_actor
@crouch:
    cmp #5
    bne continue_walk
    lda #0
    sta walking
    sta walk_phase
    lda facing
    clc
    adc #4
    sta pose
    jmp update_frame

stop_actor:
    lda #0
    sta walking
    sta walk_phase
    lda facing
    sta pose
    jmp update_frame

continue_walk:
    lda walking
    beq update_frame
    jsr collision_probe
    lda blocked
    beq @allowed
    lda #EVENT_BLOCKED
    jsr log_event
    jmp stop_actor
@allowed:
    lda door_status
    cmp #3
    bne @move
    lda #EVENT_EXIT
    jsr log_event
.if FULL_GAME
    jsr full_transition
.endif
    jmp stop_actor
@move:
.if FULL_GAME
    lda move_x
    sta actor_x
    lda move_y
    sta actor_y
.else
    ldx facing
    lda actor_x
    clc
    adc step_x,x
    sta actor_x
    lda actor_y
    clc
    adc step_y,x
    sta actor_y
.endif
    lda walk_phase
    eor #1
    sta walk_phase
    lda #EVENT_WALK
    jsr log_event
update_frame:
.if FULL_GAME
    jsr full_action_frame
    bcc :+
    rts
:
.endif
    lda walking
    beq @static
    lda facing
    asl a
    clc
    adc #8
    clc
    adc walk_phase
    sta frame_id
    rts
@static:
    lda pose
    sta frame_id
    rts

; Bounded semantic map. A zero virtual cell replaces out-of-grid hardware reads
; during y=150/170 transitions; this is an explicit provisional policy.
collision_probe:
.if FULL_GAME
    jmp full_collision_probe
.else
    lda #0
    sta blocked
    sta object_status
    lda #4
    sta door_status
    lda actor_x
    cmp #40
    bcs block_actor
    lda actor_y
    cmp #140
    bcc block_actor
    cmp #181
    bcs block_actor
    lda actor_x
    sta grid_base
    lda actor_y
    cmp #140
    bne :+
    lda grid_base
    clc
    adc #80
    sta grid_base
:
    lda actor_y
    cmp #160
    bne :+
    lda grid_base
    clc
    adc #40
    sta grid_base
:
    lda facing
    beq probe_down
    cmp #1
    beq probe_right
    cmp #2
    beq probe_left
    jmp probe_up
block_actor:
    lda #1
    sta blocked
    rts
probe_down:
    lda actor_y
    cmp #180
    beq block_actor
    lda grid_base
    sec
    sbc #40
    tax
    lda #3
    jmp scan_cells
probe_right:
    lda actor_x
    cmp #31
    bne @ordinary
    lda grid_base
    cmp #40
    bcs @ordinary
    lda #3                 ; room 12 $0484 = 3
.if FULL_GAME
    lda room_fields+2
.endif
    jmp set_door
@ordinary:
    lda grid_base
    clc
    adc #3
    tax
    lda #5
    jmp scan_cells
probe_left:
    lda actor_x
    cmp #7
    bne @ordinary
    lda grid_base
    cmp #40
    bcs @ordinary
    lda #0                 ; room 12 $0483 = 0
.if FULL_GAME
    lda room_fields+1
.endif
    jmp set_door
@ordinary:
    lda grid_base
    sec
    sbc #4
    tax
    lda #4
    jmp scan_cells
probe_up:
    lda actor_y
.if FULL_GAME
    ldx room_geometry
    cmp geometry_far,x
.else
    cmp #140               ; geometry 1 far wall
.endif
    bne @ordinary
    lda actor_x
    cmp #19
    bne block_actor
    lda #1                 ; room 12 $0482 = 1 locked far door
.if FULL_GAME
    lda room_fields
.endif
    jmp set_door
@ordinary:
    lda grid_base
    clc
    adc #40
    tax
    lda #4
    jmp scan_cells
set_door:
    sta door_status
    cmp #3
.if FULL_GAME
    jcc block_actor
.else
    bcc block_actor
.endif
    rts
scan_cells:
    sta run_count
@cell:
    cpx #120
    bcs @next              ; virtual empty cell; never read I/O
    lda room12_grid,x
    bpl @object
    lda #1
    sta blocked
@object:
    lda room12_grid,x
    cmp #1
    bne @next
    sta object_status
@next:
    inx
    dec run_count
    bne @cell
    rts
.endif
.if FULL_GAME
step_x: .byte 0,1,$FF,0
step_y: .byte 5,0,0,$FB
; Target foot planes: five source rows below the visible floor/back-wall seam.
geometry_far: .byte 145,125,125,155
.else
step_x: .byte 0,2,$FE,0
step_y: .byte 10,0,0,$F6
.endif

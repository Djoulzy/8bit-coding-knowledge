; Source-backed target rules, original B2 BASIC line numbers in each section.
; Integer hundredths for strength/drain; target LFSR replaces ROM RND/timer.
; One service opportunity per target tick is an explicit cadence adaptation.
.export full_reset, full_dispatch, full_clock, full_transition, full_action_frame
.export world_decode, world_scene_flags, full_pickup, full_open, full_purchase
.export current_room, game_mode, room_dirty, held_item, vials, torches, ropes, crowbars
.export possessions, scrolls, objectives, poison, gold, points, energy, drain
.export torch_life, bar_life, in_pit, passage, action_kind, action_phase, rng_state
.export room_geometry, room_light, room_features, room_fields, room_treasure
.export room_furnishing, scene_flags, enemy_kind, enemy_x, enemy_y, hazard_active
.export enemy_direction, enemy_contact, enemy_life, hazard_x, raw_key, message_id
.export pit_wait,pit_room,pit_x,title_tick,title_stage,title_pages_ready
.export chest_open
.export terrain_pending
.export enemy_phase, reading_page, player_name, name_count

full_reset:
    jsr clock_reset
    lda #0
    ldx #43
@state:
    sta GAME_STATE,x
    dex
    bpl @state
    sta enemy_kind
    sta enemy_contact
    sta enemy_contact_cue
    sta hazard_x
    sta terrain_pending
    sta ui_skip_clock
    sta help_return_mode
    sta name_count
    sta debug_input
    sta debug_count
    sta debug_status
    ldx #63
@lamps:
    sta lamp_history,x
    dex
    bpl @lamps
    ldx #0
@world:
    lda initial_world,x
    sta WORLD,x
    lda initial_world+$100,x
    sta WORLD+$100,x
    inx
    bne @world
    lda #12
    sta current_room
    lda #7
    sta objectives
    lda #$F4
    sta gold
    lda #1
    sta gold+1
    sta drain
    sta room_dirty
    lda #$10
    sta energy
    lda #$27
    sta energy+1
    lda #$E1
    sta rng_state
    lda #$AC
    sta rng_state+1
    lda #MODE_NAME
    sta game_mode
    lda session_attempt
    cmp #5
    bcc :+
    lda #0
:
    clc
    adc #1
    sta session_attempt
    lda #' '
    ldx #5
@name:
    sta player_name,x
    dex
    bpl @name
    jsr world_decode
    rts

world_decode:
    ldx current_room
    lda source_variation,x
    sta room_variation
    txa
    asl a
    asl a
    tax
    lda WORLD,x
    pha
    and #3
    sta room_light
    pla
    pha
    lsr a
    lsr a
    and #15
    sta room_features
    pla
    lsr a
    lsr a
    lsr a
    lsr a
    lsr a
    lsr a
    sta room_geometry
    ldy #0
    inx
    lda #3
    sta game_tmp
@byte:
    lda WORLD,x
    sta game_tmp2
    lda #4
    sta math_count
@field:
    lda game_tmp2
    and #3
    sta room_fields,y
    iny
    lsr game_tmp2
    lsr game_tmp2
    dec math_count
    bne @field
    inx
    dec game_tmp
    bne @byte
    lda current_room
    asl a
    asl a
    tax
    lda WORLD+$100,x
    pha
    and #7
    sta room_furnishing
    pla
    pha
    lsr a
    lsr a
    lsr a
    and #7
    sta room_treasure
    pla
    pha
    and #$80
    sta room_gate
    pla
    and #$40
    sta room_floor
    lda #0
    sta chest_open
    lda room_furnishing
    cmp #7
    bne :+
    lda room_fields+10
    cmp #3
    bne :+
    lda #1
    sta chest_open
:
    lda #0
    sta gate_side
    lda room_features
    and #2
    beq @done
    lda room_gate
    bne @done
    lda room_fields+3
    cmp #2
    bcs @done
    lda #11
    ldx room_variation
    cpx #201
    bcc :+
    lda #27
:
    sta gate_side
@done:
    rts

world_scene_flags:
    lda #0
    sta scene_flags
    lda room_treasure
    bne :+
    inc scene_flags
:
    lda chest_open
    beq :+
    lda scene_flags
    ora #2
    sta scene_flags
:
    lda room_gate
    beq :+
    lda scene_flags
    ora #4
    sta scene_flags
:
    lda room_floor
    beq :+
    lda scene_flags
    ora #8
    sta scene_flags
:
    lda room_light
    cmp #3
    bne :+
    lda scene_flags
    ora #16
    sta scene_flags
:
    ldx #0
    lda current_room
    cmp #1
    beq @quest
    inx
    cmp #62
    beq @quest
    inx
    cmp #63
    bne @ring
@quest:
    lda objectives
    and objective_bits,x
    bne @ring
    lda scene_flags
    ora #32
    sta scene_flags
@ring:
    lda possessions
    and #4
    beq :+
    lda scene_flags
    ora #64
    sta scene_flags
:
    ldx current_room
    lda scene_flags
    and #$7F
    sta scene_flags
    rts

; Carry set consumes this tick before ordinary walking; menus pause services.
full_dispatch:
    lda game_mode
    beq @play
    cmp #MODE_TITLE
    bne :+
    jsr title_tick_update
    sec
    rts
:
    jsr full_menu_key
    sec
    rts
@play:
    lda raw_key
    bmi :+                  ; $FF means no key; all accepted keys are 7-bit
    lda #0
    sta message_id           ; retain feedback while idle; next command replaces it
:
    lda pit_wait
    beq :+
    lda raw_key
    cmp #'A'
    jne @handled
    lda #0
    sta pit_wait
:
    lda action_kind
    beq @idle
    jsr full_action_tick
    sec
    rts
@idle:
    jsr full_secret_enter
    jcs @handled
    lda raw_key
    cmp #'0'
    bcc @letter
    cmp #'7'
    bcs @letter
    sec
    sbc #'0'
    cmp #6
    bne :+
    lda #5
:
    jsr full_select_item
    sec
    rts
@letter:
    cmp #'I'
    bne :+
    lda #MODE_INVENTORY
    sta game_mode
    jne @handled
:
    cmp #'L'
    bne :+
    lda #0
    sta reading_page
    jsr full_next_clue
    jcs @handled
    jmp full_denied
:
    cmp #'P'
    bne :+
    jsr full_pickup
    jmp @handled
:
    cmp #'O'
    bne :+
    jsr full_open
    jmp @handled
:
    cmp #'B'
    bne :+
    lda vials
    beq @deny
    lda held_item
    cmp #10
    bne @deny
    lda #1
    sta action_kind
    lda #0
    sta action_phase
    lda facing
    and #1
    bne @handled
    lda #1
    sta facing
    sta pose
    jmp @handled
:
    cmp #'D'
    bne :+
    lda hazard_active
    bne @deny
    lda #2
    sta action_kind
    lda #0
    sta action_phase
    jmp @handled
:
    cmp #'S'
    bne :+
    jsr full_start_jump
    jmp @handled
:
    cmp #'G'
    bne :+
    jsr full_start_climb
    jmp @handled
:
    cmp #'T'
    bne :+
    jsr full_request_light
    jmp @handled
:
    cmp #'Q'
    bne @ordinary
    lda #0
    sta energy
    sta energy+1           ; B2 12200, death only after subsequent drain
    jmp @handled
@ordinary:
    clc
    rts
@deny:
    jsr full_denied
@handled:
    lda #0
    sta walking
    sta walk_phase
    sec
    rts
full_denied:
    lda #1
    sta message_id
    lda #EVENT_DENIED
    jsr log_event
    sec
    rts

full_menu_key:
    lda game_mode
    cmp #MODE_NAME
    jne @exterior
    lda raw_key
    cmp #13
    beq @name_done
    cmp #8
    bne :+
    lda name_count
    jeq @done
    dec name_count
    ldx name_count
    lda #' '
    sta player_name,x
    rts
:
    cmp #32
    jcc @done
    cmp #127
    jcs @done
    ldx name_count
    cpx #6
    jcs @done
    sta player_name,x
    inc name_count
    rts
@name_done:
    lda session_attempt
    sec
    sbc #1
    sta game_tmp
    asl a
    clc
    adc game_tmp
    asl a
    tax
    ldy #0
@save_name:
    lda player_name,y
    sta attempt_names,x
    inx
    iny
    cpy #6
    bne @save_name
    lda #MODE_EXTERIOR
    sta game_mode
    rts
@exterior:
    cmp #MODE_EXTERIOR
    bne @merchant
    lda raw_key
    cmp #'1'
    bne :+
    lda #0
    sta game_mode
    sta held_item
    sta action_kind
    sta message_id
    lda #12
    sta current_room
    lda #19
    sta actor_x
    lda #140
    sta actor_y
    lda #1
    sta room_dirty
    rts
:
    cmp #'3'
    bne :+
    lda #MODE_MERCHANT
    sta game_mode
    lda #0
    sta message_id
    rts
:
    cmp #'2'
    bne @done
    lda #MODE_DEPART
    sta game_mode
    rts
@merchant:
    cmp #MODE_MERCHANT
    bne @overlay
    lda raw_key
    cmp #'0'
    bne :+
    lda #MODE_EXTERIOR
    sta game_mode
    rts
:
    cmp #'1'
    bcc @done
    cmp #'5'
    bcs @done
    sec
    sbc #'1'
    tax
    jsr full_purchase
    rts
@overlay:
    cmp #MODE_INVENTORY
    beq @close
    cmp #MODE_READ
    bne @replay
    lda raw_key
    cmp #$FF
    beq @done
    inc reading_page
    jsr full_next_clue
    bcs @done
    lda #0
    sta game_mode
    rts
@close:
    lda raw_key
    cmp #32
    beq @resume
    cmp #13
    beq @resume
    cmp #27
    bne @done
@resume:
    lda #0
    sta game_mode
    rts
@replay:
    lda raw_key
    cmp #'O'
    beq @new
    cmp #13
    bne @done
@new:
    jmp game_reset
@done:
    rts

full_next_clue:
    ldx reading_page
@find:
    cpx #4
    bcs @none
    cpx #3
    beq @book
    lda scrolls
    and objective_bits,x
    bne @found
    jmp @next
@book:
    lda objectives
    and #1
    beq @found
@next:
    inx
    bne @find
@found:
    stx reading_page
    lda #MODE_READ
    sta game_mode
    sec
    rts
@none:
    clc
    rts

full_select_item:
    tax
    lda item_codes,x
    beq @select
    cpx #1
    bne @iron
    ldy torches
    beq @deny
    bne @select
@iron:
    cpx #2
    bne @gold
    ldy possessions
    tya
    and #1
    beq @deny
    bne @reload
@gold:
    cpx #3
    bne @vial
    lda possessions
    and #2
    beq @deny
    bne @reload
@vial:
    cpx #4
    bne @bar
    lda vials
    beq @deny
    bne @reload
@bar:
    lda crowbars
    beq @deny
@reload:
    lda item_codes,x
@select:
    sta held_item
    lda #0
    sta message_id
    rts
@deny:
    jmp full_denied

; B2 13000-13510: atomic funds/quantity update, first-item lifetime only.
full_purchase:
    stx game_tmp
    lda gold+1
    cmp price_hi,x
    bcc @deny
    bne @buy
    lda gold
    cmp price_lo,x
    bcc @deny
@buy:
    lda gold
    sec
    sbc price_lo,x
    sta gold
    lda gold+1
    sbc price_hi,x
    sta gold+1
    lda stock_offsets,x
    tax
    inc GAME_STATE,x
    lda GAME_STATE,x
    cmp #1
    bne @ready
    ldx game_tmp
    cpx #1
    bne @bar
    jsr reset_torch_life
    jmp @ready
@bar:
    cpx #3
    bne @ready
    jsr reset_bar_life
@ready:
    lda #2
    sta message_id
    lda #EVENT_ITEM
    jmp log_event
@deny:
    jmp full_denied

; B2 4701-4710: three stored links, direction zero is current room.
full_transition:
    lda current_room
    cmp #12
    bne @link
    lda facing
    cmp #3
    bne @link
    lda #MODE_EXTERIOR
    sta game_mode
    lda objectives
    bne @stop
    lda #MODE_WIN
    sta game_mode
@stop:
    lda #0
    sta walking
    sta enemy_kind
    sta hazard_active
    sta gate_side
    sta action_kind
    sta object_status
    rts
@link:
    lda current_room
    asl a
    asl a
    clc
    adc #4
    sec
    sbc facing
    tax
    lda facing
    beq @self
    lda WORLD+$100,x
    jmp @destination
@self:
    lda current_room
@destination:
    pha
    and #63
    sta current_room
    pla
    lsr a
    lsr a
    lsr a
    lsr a
    lsr a
    lsr a
    sta arrival_saved
    jsr world_decode
    lda passage
    beq @ordinary
    lda #0
    sta facing
    lda #4
    sta pose
    lda #19
    sta actor_x
    lda #140
    sta actor_y
    jmp @entered
@ordinary:
    ldx arrival_saved
    cpx #3
    beq @keep
    txa
    sta facing
    sta pose
    lda entry_x,x
    sta actor_x
    lda #180
    cpx #0
    bne :+
    ldx room_geometry
    lda geometry_far,x
:
    sta actor_y
    jmp @entered
@keep:
    lda #0
    sta facing
    sta pose
@entered:
    lda #0
    sta message_id
    sta passage
    sta in_pit
    sta pit_wait
    sta enemy_kind
    sta enemy_contact
    sta hazard_active
    sta gate_jump
    sta walking
    sta walk_phase
    lda #1
    sta room_dirty
    lda #EVENT_ROOM
    jmp log_event

; B2 10900-10990. Door locks are fields 9-facing. Chest pickup is separate.
full_open:
    jsr collision_probe
    lda door_status
    cmp #1
    jeq @door
    cmp #2
    jeq @door
    jsr full_secret_reach
    bcc @chest
    lda passage
    jne @deny
    lda #1
    sta passage
    sta room_dirty
    lda #3
    sta message_id
    rts
@chest:
    lda room_furnishing
    cmp #7
    jne @deny
    jsr full_fixture_reach
    jcc @deny
    lda held_item
    cmp #6
    beq @open_chest
    cmp #0
    bne @deny
    lda room_variation
    cmp #101
    bcs @deny
@open_chest:
    lda current_room
    asl a
    asl a
    tax
    lda WORLD+3,x
    ora #$30
    sta WORLD+3,x
    lda #3
    sta room_fields+11     ; explicit original transient/persistent discrepancy
    lda #1
    sta chest_open
    sta room_dirty
    lda held_item
    cmp #6
    bne @opened
    jsr wear_bar
@opened:
    lda #4
    sta message_id
    rts
@door:
    lda #9
    sec
    sbc facing
    tax
    lda room_fields,x
    beq @pass
    cmp #1
    bne @bar
    lda held_item
    cmp #9
    beq @pass
@bar:
    lda room_fields,x
    sta game_tmp
    lda held_item
    cmp #6
    bne @deny
    jsr wear_bar
    bcs @deny
    lda game_tmp
    cmp #3
    beq @deny
    jsr game_random
    ; RND*ST < .3. ST 1: r<76.8; ST 2: r<38.4, quantized r/256.
    ldx door_status
    cpx #2
    beq @reinforced
    cmp #77
    bcc @pass
    bcs @deny
@reinforced:
    cmp #39
    bcs @deny
@pass:
    jmp full_transition
@deny:
    jmp full_denied

wear_bar:
    dec bar_life
    lda bar_life
    bpl @usable
    dec crowbars
    lda crowbars
    beq :+
    jsr reset_bar_life
:
    lda #0
    sta held_item
    sec
    rts
@usable:
    clc
    rts

full_pickup:
    lda facing
    cmp #3
    jeq full_denied
    jsr full_fixture_reach
    jcc @ordinary
    lda facing
    cmp #1
    jne @ordinary
    lda chest_open
    bne @chest
    lda pose
    cmp #4
    bcs @ordinary
    lda held_item
    bne @ordinary
    ldx #0
    lda current_room
    cmp #1
    beq @quest
    inx
    cmp #62
    beq @quest
    inx
    cmp #63
    bne @ordinary
@quest:
    lda objectives
    and objective_bits,x
    jeq full_denied
    cpx #0
    beq @take_quest
    lda #1
    sta hazard_active
    lda #6
    sta hazard_x
    cpx #2
    bne @take_quest
    lda possessions
    and #8
    jeq full_denied
    lda possessions
    and #$F7
    sta possessions
@take_quest:
    lda objectives
    eor objective_bits,x
    sta objectives
    lda objective_points_lo,x
    sta word_arg
    lda objective_points_hi,x
    sta word_arg+1
    jsr add_points
    lda objective_gold_lo,x
    sta word_arg
    lda objective_gold_hi,x
    sta word_arg+1
    jsr add_gold
    jmp @taken
@chest:
    lda chest_open
    beq @ordinary
    ; B2 10775 skips normal held-item/pose guards, for actual initial TR 0/2/5.
    jmp @reward
@ordinary:
    lda held_item
    jne full_denied
    lda pose
    cmp #4
    jcc full_denied
    cmp #8
    jcs full_denied
    jsr full_pickup_probe
    cmp #160
    jne full_denied
@reward:
    ldx room_treasure
    jeq full_denied
    cpx #1
    bne @bag
    lda current_room
    cmp #62
    bne :+
    lda scrolls
    ora #1
    sta scrolls
:
    lda current_room
    cmp #35
    bne :+
    lda scrolls
    ora #2
    sta scrolls
:
    lda current_room
    cmp #1
    jne @clear_treasure
    lda scrolls
    ora #4
    sta scrolls
    jmp @clear_treasure
@bag:
    cpx #2
    bne @iron
    lda #<300
    sta word_arg
    lda #>300
    sta word_arg+1
    jsr random_word
    jsr add_gold
    lda #10
    jmp @score
@iron:
    cpx #3
    bne @gold_key
    lda possessions
    ora #1
    sta possessions
    lda #15
    jmp @score
@gold_key:
    cpx #4
    bne @vial
    lda possessions
    ora #2
    sta possessions
    lda #30
    jmp @score
@vial:
    cpx #5
    bne @ring
    inc vials
    lda current_room
    cmp #14
    beq :+
    cmp #38
    bne @vial_score
:
    inc poison
@vial_score:
    lda #7
    jmp @score
@ring:
    cpx #6
    bne @lead
    lda possessions
    ora #4
    sta possessions
    lda #200
    sta word_arg
    lda #0
    sta word_arg+1
    jsr add_gold
    jmp @clear_treasure
@lead:
    lda possessions
    ora #8
    sta possessions
    lda #50
    sta word_arg
    lda #0
    sta word_arg+1
    jsr add_gold
    lda #10
@score:
    sta word_arg
    lda #0
    sta word_arg+1
    jsr add_points
@clear_treasure:
    lda current_room
    asl a
    asl a
    tax
    lda WORLD+$100,x
    and #$C7
    sta WORLD+$100,x
    lda #0
    sta room_treasure
@taken:
    lda #1
    sta room_dirty
    lda #5
    sta message_id
    lda #EVENT_ITEM
    jmp log_event

full_start_jump:
    lda facing
    cmp #1
    beq @right
    cmp #2
    jne full_denied
    lda actor_x
    cmp #15
    jcc full_denied
    bcs @ready
@right:
    lda actor_x
    cmp #24
    jcs full_denied
@ready:
    lda held_item
    sta saved_item
    lda #0
    sta held_item
    sta walking
    sta action_phase
    lda #3
    sta action_kind
    rts

full_start_climb:
    lda held_item
    jne full_denied
    lda ropes
    jeq full_denied
    lda in_pit
    bne @ready
    lda current_room
    cmp #62
    jne full_denied
    lda actor_x
    cmp #19
    jne full_denied
    lda actor_y
    cmp #160
    jne full_denied
@ready:
    lda #4
    sta action_kind
    lda #0
    sta action_phase
    sta walking
    rts

full_action_tick:
    lda action_kind
    cmp #1
    beq @drink
    cmp #2
    jeq @vertical
    cmp #3
    jeq @jump
    jmp @climb
@drink:
    inc action_phase
    lda action_phase
    cmp #3
    jcc @done
    jsr game_random       ; consumed even for PN=0, source 12127
    lda poison
    beq @restore
    dec poison
    lda drain
    clc
    adc #100
    sta drain
    bcc :+
    inc drain+1
:
    jmp @drank
@restore:
    lda #$10
    sta energy
    lda #$27
    sta energy+1
    lda #1
    sta drain
    lda #0
    sta drain+1
@drank:
    dec vials
    jmp @finish
@vertical:
    inc action_phase
    lda action_phase
    cmp #1
    bne :+
    lda facing
    clc
    adc #4
    sta pose
    rts
:
    cmp #2
    bne :+
    lda facing
    sta pose
    rts
:
    cmp #6
    beq @light
    cmp #3
    jcc @done
    cmp #6
    bcs @down
    lda actor_y
    sec
    sbc #13
    sta actor_y
    rts
@light:
    jmp full_light
@down:
    cmp #10
    bcs @end_vertical
    lda actor_y
    clc
    adc #13
    sta actor_y
    rts
@end_vertical:
    cmp #11
    jcs @finish
    lda facing
    clc
    adc #4
    sta pose
    rts
@jump:
    ldx action_phase
    lda jump_dy,x
    clc
    adc actor_y
    sta actor_y
    cpx #0
    beq :+
    lda facing
    cmp #1
    bne @left_jump
    inc actor_x
    inc actor_x
    jmp :+
@left_jump:
    dec actor_x
    dec actor_x
:
    lda gate_side
    beq :+
    cmp actor_x
    bne :+
    lda #1
    sta gate_jump
:
    inc action_phase
    lda action_phase
    cmp #5
    jcc @done
    lda saved_item
    sta held_item
    jmp @finish
@climb:
    lda action_phase
    bne @ascending
    lda raw_key
    cmp #32
    jeq @finish
    dec ropes
    lda #3
    sta facing
    sta pose
@ascending:
    inc action_phase
    lda action_phase
    cmp #3
    bcc @done
    cmp #7
    bcs @arrive
    cmp #3
    bne :+
    inc actor_x
    inc actor_x
:
    lda actor_y
    sec
    sbc #20
    sta actor_y
    rts
@arrive:
    lda in_pit
    beq @top_room
    lda pit_room
    sta current_room
    lda pit_x
    sta actor_x
    jmp @top
@top_room:
    lda #63
    sta current_room
    lda #19
    sta actor_x
@top:
    lda #180
    sta actor_y
    lda #0
    sta in_pit
    sta pit_wait
    sta facing
    sta pose
    lda #1
    sta room_dirty
@finish:
    lda #0
    sta action_kind
    sta action_phase
    sta walking
@done:
    rts

full_action_frame:
    lda in_pit
    beq @action
    lda pit_wait
    beq @action
    lda #27
    sta frame_id
    sec
    rts
@action:
    lda action_kind
    cmp #3
    bne @climb
    lda action_phase
    beq :+
    sec
    sbc #1
:
    clc
    adc #16
    ldx facing
    cpx #1
    beq :+
    clc
    adc #5
:
    sta frame_id
    sec
    rts
@climb:
    cmp #4
    bne @ordinary
    lda action_phase
    cmp #3
    bcc @ordinary
    lda #26
    sta frame_id
    sec
    rts
@ordinary:
    clc
    rts

full_light:
    lda actor_y
    cmp #141
    bne @done
    lda held_item
    cmp #1
    bne @done
    lda room_light
    beq @done
    lda actor_x
    cmp #7
    bne @right
    lda facing
    cmp #2
    bne @done
    lda #1
    bne @lit
@right:
    cmp #31
    bne @done
    lda facing
    cmp #1
    bne @done
    lda #2
@lit:
    ldx current_room
    ora lamp_history,x
    sta lamp_history,x
    cmp #3
    bne @transient
    txa
    asl a
    asl a
    tax
    lda WORLD,x
    ora #2
    sta WORLD,x
@transient:
    lda #3
    sta room_light
    lda #6
    sta message_id
@done:
    rts

full_clock:
    jsr clock_sample
    lda ui_skip_clock
    beq :+
    lda #0
    sta ui_skip_clock
    jmp clock_reset
:
    lda game_mode
    jne @done
    lda clock_vbls
    cmp #18
    bcc @environment
    sbc #18
    sta clock_vbls
    lda held_item
    cmp #1
    bne @loss
    lda torch_life
    bne :+
    dec torch_life+1
:
    dec torch_life
    lda torch_life+1
    bpl @loss
    dec torches
    lda torches
    beq :+
    jsr reset_torch_life
:
    lda #0
    sta held_item
@loss:
    lda energy
    sec
    sbc drain
    sta energy
    lda energy+1
    sbc drain+1
    sta energy+1
    bmi @dead
@environment:
    lda gate_side
    beq @pit
    cmp actor_x
    bne @pit
    lda action_kind
    cmp #3
    beq @pit
    lda current_room
    asl a
    asl a
    tax
    lda WORLD+$100,x
    ora #$80
    sta WORLD+$100,x
    lda #1
    sta room_dirty
    lda gate_jump
    beq @dead
    lda #0
    sta gate_side
@pit:
    lda in_pit
    bne @services
    lda object_status
    cmp #1
    bne @services
    lda walking
    beq @services
    jsr full_fall
@services:
    jsr full_hazard
    jsr full_enemy
    lda energy+1
    bmi @dead
@done:
    rts
@dead:
    lda #MODE_DEAD
    sta game_mode
    lda #0
    sta walking
    sta enemy_kind
    sta hazard_active
    sta action_kind
    lda #EVENT_END
    jmp log_event

full_fall:
    lda current_room
    sta pit_room
    asl a
    asl a
    tax
    lda WORLD+$100,x
    ora #$40
    sta WORLD+$100,x
    lda actor_x
    clc
    adc #4
    sta pit_x
    lda #1
    sta in_pit
    sta pit_wait
    sta room_dirty
    lda #22
    sta actor_x
    lda #180
    sta actor_y
    lda #3
    sta facing
    sta pose
    lda #0
    sta held_item
    sta walking
    sta enemy_kind
    sta hazard_active
    sta gate_side
    sta action_kind
    sta object_status
    lda #<6000
    sta word_arg
    lda #>6000
    sta word_arg+1
    jsr random_word
    jsr subtract_energy
    lda drain
    sta word_arg
    lda drain+1
    sta word_arg+1
    ; Multiply before rounding: floor(5*drain*random_byte/256).
    lda word_arg
    sta word_tmp
    lda word_arg+1
    sta word_tmp+1
    ldx #4
@times5:
    lda word_arg
    clc
    adc word_tmp
    sta word_arg
    lda word_arg+1
    adc word_tmp+1
    sta word_arg+1
    dex
    bne @times5
    jsr random_word
    lda drain
    clc
    adc word_arg
    sta drain
    lda drain+1
    adc word_arg+1
    sta drain+1
    lda #EVENT_DAMAGE
    jsr log_event
    jmp update_frame

; Original $4CDD: x starts 6 and advances 3, contact at y160 standing.
full_hazard:
    lda hazard_active
    beq @done
    lda actor_y
    cmp #160
    bne @advance
    lda pose
    cmp #4
    bcs @advance
    lda actor_x
    sec
    sbc hazard_x
    bpl :+
    eor #$FF
    clc
    adc #1
:
    cmp #2
    bcs @advance
    lda #<5000
    sta word_arg
    lda #>5000
    sta word_arg+1
    jsr random_word
    lda word_arg
    clc
    adc #<3000
    sta word_arg
    lda word_arg+1
    adc #>3000
    sta word_arg+1
    jsr subtract_energy
    lda drain
    clc
    adc #10
    sta drain
    bcc :+
    inc drain+1
:
    lda #0
    sta hazard_active
    rts
@advance:
    lda hazard_x
    clc
    adc #3
    sta hazard_x
    cmp #37
    bcc @done
    lda #0
    sta hazard_active
@done:
    rts

; Source B2 6400/8000 and workers $4976/$4A50/$4ACE, timer replaced by tick/RNG.
full_enemy:
    lda in_pit
    ora hazard_active
    jne @done
    lda enemy_kind
    jne @active
    lda room_fields+5
    jeq @done
    cmp #1
    beq @spawn
    sta game_tmp
    jsr game_random
    ldx game_tmp
    cpx #2
    bne :+
    cmp #26
    jcs @done
    bcc @spawn
:
    cmp #39
    jcs @done
@spawn:
    lda room_fields+4
    cmp #3
    jeq @done
    cmp #2
    beq @ground
    lda room_light
    cmp #3
    beq :+
    lda held_item
    cmp #1
    jne @done
:
    lda #2
    sta enemy_kind
    lda #7
    sta enemy_x
    lda #80
    sta enemy_y
    jsr game_random
    and #7
    cmp #6
    bcc :+
    lda #5
:
    sta enemy_life
    jmp @spawned
@ground:
    lda #1
    sta enemy_kind
    sta enemy_contact_cue
    sta enemy_life
    lda #35
    sta enemy_x
    lda #120
    sta enemy_y
@spawned:
    lda #1
    sta enemy_direction
    lda #0
    sta enemy_contact
@active:
    lda enemy_phase
    eor #1
    sta enemy_phase
    lda enemy_kind
    cmp #1
    jeq @ground_update
    lda enemy_contact
    beq @fly
    lda pose
    cmp #4
    bcs :+
    lda #<2000
    sta word_arg
    lda #>2000
    sta word_arg+1
    jsr random_word
    jsr subtract_energy
    jsr drain_plus5
:
    lda actor_y
    sec
    sbc #74
    sta enemy_y
    jsr enemy_step2
    lda held_item
    cmp #1
    bne :+
    lda pose
    cmp #4
    bcs :+
    dec enemy_life
:
    lda #0
    sta enemy_contact
    rts
@fly:
    lda enemy_life
    bpl :+
    lda #0
    sta enemy_kind
    rts
:
    lda actor_y
    sec
    sbc #95
    sta enemy_y
    jsr enemy_step2
    lda enemy_x
    cmp #31
    bcs @reverse
    cmp #9
    bcs @look
@reverse:
    lda enemy_direction
    eor #$FE
    sta enemy_direction
@look:
    jsr enemy_step2
    jsr enemy_distance
    cmp #2
    bcs @look_back
    lda #1
    sta enemy_contact
    lda held_item
    cmp #1
    bne @look_back
    lda tick_lo
    and #1
    sta enemy_contact
@look_back:
    lda enemy_x
    sec
    sbc enemy_direction
    sec
    sbc enemy_direction
    sta enemy_x
    rts
@ground_update:
    lda enemy_contact
    bne @charge
    jsr game_random
    cmp #231
    bcs @charge
    jsr game_random
    and #3
    asl a
    asl a
    asl a
    clc
    adc enemy_y
    sec
    sbc #4
    cmp #110
    bcs :+
    lda #110
:
    cmp #131
    bcc :+
    lda #130
:
    sta enemy_y
    rts
@charge:
    lda enemy_contact
    bne @rush
    lda #1
    sta enemy_direction
    lda enemy_x
    cmp actor_x
    bcc :+
    lda #$FF
    sta enemy_direction
:
    lda #1
    sta enemy_contact
@rush:
    lda enemy_x
    clc
    adc enemy_direction
    clc
    adc enemy_direction
    clc
    adc enemy_direction
    sta enemy_x
    lda pose
    cmp #4
    bcs @boundary
    jsr enemy_distance
    cmp #3
    bcs @boundary
    lda #<1000
    sta word_arg
    lda #>1000
    sta word_arg+1
    jsr random_word
    jsr subtract_energy
    lda drain
    clc
    adc #50
    sta drain
    bcc :+
    inc drain+1
:
    lda #0
    sta enemy_kind
    sta enemy_contact
    rts
@boundary:
    lda enemy_x
    cmp #35
    bcs @stop_charge
    cmp #6
    bcs @done
@stop_charge:
    lda #0
    sta enemy_contact
@done:
    rts
enemy_step2:
    lda enemy_x
    clc
    adc enemy_direction
    clc
    adc enemy_direction
    sta enemy_x
    rts
enemy_distance:
    lda enemy_x
    sec
    sbc actor_x
    bpl :+
    eor #$FF
    clc
    adc #1
:
    rts
drain_plus5:
    lda drain
    clc
    adc #5
    sta drain
    bcc :+
    inc drain+1
:
    rts

; Eight-bit output of a 16-bit Galois LFSR, deterministic target policy.
game_random:
    lsr rng_state+1
    ror rng_state
    bcc :+
    lda rng_state+1
    eor #$B4
    sta rng_state+1
:
    lda rng_state
    rts
reset_torch_life:
    lda #100
    sta word_arg
    lda #0
    sta word_arg+1
    jsr random_word
    lda word_arg
    clc
    adc #200
    sta torch_life
    lda word_arg+1
    adc #0
    sta torch_life+1
    rts
reset_bar_life:
    lda #20
    sta word_arg
    lda #0
    sta word_arg+1
    jsr random_word
    lda word_arg
    clc
    adc #20
    sta bar_life
    rts
; word_arg := floor(word_arg * random_byte / 256), no undocumented opcodes.
random_word:
    jsr game_random
    sta game_tmp2
    lda word_arg
    sta math_factor
    lda word_arg+1
    sta math_factor+1
    lda #0
    sta math_factor+2
    sta math_product
    sta math_product+1
    sta math_product+2
    lda #8
    sta math_count
@multiply:
    lsr game_tmp2
    bcc @shift
    lda math_product
    clc
    adc math_factor
    sta math_product
    lda math_product+1
    adc math_factor+1
    sta math_product+1
    lda math_product+2
    adc math_factor+2
    sta math_product+2
@shift:
    asl math_factor
    rol math_factor+1
    rol math_factor+2
    dec math_count
    bne @multiply
    lda math_product+1
    sta word_arg
    lda math_product+2
    sta word_arg+1
    rts
add_gold:
    lda gold
    clc
    adc word_arg
    sta gold
    lda gold+1
    adc word_arg+1
    sta gold+1
    rts
add_points:
    lda points
    clc
    adc word_arg
    sta points
    lda points+1
    adc word_arg+1
    sta points+1
    rts
subtract_energy:
    lda energy
    sec
    sbc word_arg
    sta energy
    lda energy+1
    sbc word_arg+1
    sta energy+1
    lda #EVENT_DAMAGE
    jmp log_event

objective_bits: .byte 1,2,4
objective_points_lo: .byte <1000,<500,<1000
objective_points_hi: .byte >1000,>500,>1000
objective_gold_lo: .byte 0,<200,<5000
objective_gold_hi: .byte 0,>200,>5000
item_codes: .byte 0,1,9,8,10,6
stock_offsets: .byte vials-GAME_STATE,torches-GAME_STATE,ropes-GAME_STATE,crowbars-GAME_STATE
price_lo: .byte <360,<190,<110,<230
price_hi: .byte >360,>190,>110,>230
entry_x: .byte 19,2,34
jump_dy: .byte 0,$F6,$FB,5,10
; Main RAM math/session data are private, not BASIC heap or ROM workspaces.
math_factor = $1370
math_product = $1373
name_count = $1376
attempt_names = $1380

arrival_saved = $1377

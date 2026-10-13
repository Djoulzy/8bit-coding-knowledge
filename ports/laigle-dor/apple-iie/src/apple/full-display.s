; Apple display adapter; rules remain in game/full-core.s.
.segment "LOWCODE"
full_draw_equipment:
    lda #0
    sta static_draw
    sta scene_additive
    lda in_pit
    beq @ordinary
    lda pit_wait
    beq @ordinary
    lda #25
    bne @index
@ordinary:
    lda action_kind
    cmp #3
    bne :+
    lda #18
    bne @index
:
    cmp #4
    bne :+
    lda #23
    ldx action_phase
    cpx #2
    bcc @index
    lda #24
    cpx #3
    bcc @index
    lda #18
    bne @index
:
    lda held_item
    ldx #0
    cmp #1
    bne :+
    ldx #4
:
    cmp #9
    beq @key
    cmp #8
    bne :+
@key:
    ldx #8
:
    cmp #10
    bne :+
    ldx #12
    lda action_kind
    cmp #1
    bne :+
    lda action_phase
    and #1
    beq :+
    ldx #15
:
    lda held_item
    cmp #6
    bne :+
    ldx #19
:
    txa
    clc
    adc facing
@index:
    tax
    lda equipment_lo,x
    sta frame_ptr
    lda equipment_hi,x
    sta frame_ptr+1
    ldy #0
    lda (frame_ptr),y
    beq @done
    sta layer_count
    lda #1
    sta layer_cursor
@layer:
    ldy layer_cursor
    lda (frame_ptr),y
    sta sprite_index
    iny
    lda (frame_ptr),y
    sta dx
    iny
    lda (frame_ptr),y
    sta dy
    lda pose
    cmp #4
    bcc :+
    cmp #8
    bcs :+
    lda dy
    clc
    adc #10
    sta dy
:
    iny
    sty layer_cursor
    jsr draw_sprite
    dec layer_count
    bne @layer
@done:
    jmp full_draw_hand_flame

full_draw_entities:
    lda actor_x
    pha
    lda actor_y
    sta entity_actor_y
    pha
    lda enemy_kind
    beq @hazard
    lda enemy_x
    sta actor_x
    lda enemy_y
    sta actor_y
    lda #0
    sta dx
    sta dy
    ldx #0
    lda enemy_kind
    cmp #1
    bne @flyer
    lda enemy_contact
    beq @phase
    ldx #2
    bne @phase
@flyer:
    ldx #4
    lda enemy_direction
    bpl :+
    ldx #6
:
    lda enemy_y
    clc
    adc #74
    cmp entity_actor_y
    bne @phase
    ldx #8
@phase:
    txa
    clc
    adc enemy_phase
    tax
    lda enemy_sprite_indices,x
    sta sprite_index
    jsr draw_sprite
@hazard:
    lda hazard_active
    beq @restore
    ; Target beam: six native red cells at original source scanline 110.
    ldx #110
    lda y_map,x
    tax
    lda row_lo,x
    sta dst_ptr
    lda row_hi,x
    and #$1F
    ora draw_page_hi
    sta dst_ptr+1
    lda hazard_x
    asl a
    clc
    adc hazard_x
    clc
    adc #10
    sta cell_x
    lda #6
    sta scene_count
@beam:
    lda #8                ; serial pattern for palette red
    sta cell_color
    jsr draw_cell
    inc cell_x
    dec scene_count
    bne @beam
    ; Extend this page's restoration rectangle to cover the beam.
    ldx render_page_index
    lda #0
    sta dirty_left,x
    sta dirty_top,x
    lda #80
    sta dirty_right,x
    lda #VIEW_HEIGHT
    sta dirty_bottom,x
    lda #1
    sta dirty_valid,x
@restore:
    pla
    sta actor_y
    pla
    sta actor_x
    jmp full_draw_rope

; B2 7400/7410: the shared rope atlas follows the actor during climbing.
full_draw_rope:
    lda action_kind
    cmp #4
    bne @done
    lda action_phase
    cmp #3
    bcc @done
    lda actor_x
    sta rope_actor_x
    asl a
    clc
    adc rope_actor_x
    asl a
    clc
    adc #17
    sta scene_x
    lda actor_y
    sta rope_actor_y
    sec
    sbc #74
    sta scene_y
@segment:
    lda #90
    sta scene_id
    lda #1
    sta scene_additive
    jsr scene_stamp
    lda scene_y
    sec
    sbc #14
    sta scene_y
    cmp #20
    bcs @segment
    lda rope_actor_x
    sta actor_x
    lda rope_actor_y
    sta actor_y
    lda #0
    sta static_draw
    sta scene_additive
    ldx render_page_index
    sta dirty_left,x
    sta dirty_top,x
    lda #80
    sta dirty_right,x
    lda #VIEW_HEIGHT
    sta dirty_bottom,x
    lda #1
    sta dirty_valid,x
@done:
    rts

full_visibility:
    lda #0
    sta $C00D
    bit $C053
    lda game_mode
    beq @play
    cmp #MODE_TITLE
    beq @title
@text:
    sta $C00C
    bit $C052
    bit $C051
    rts
@title:
    bit $C052
    rts
@play:
    jsr full_is_dark
    bcs @text
@done:
    rts

; Carry set for the intentional source darkness panel (B2 6000-6003).
; Kept separate from game_mode: gameplay/input still operates in this state.
full_is_dark:
    lda room_light
    cmp #3
    beq @visible
    lda held_item
    cmp #1
    beq @visible
    lda in_pit
    bne @visible
    lda action_kind
    cmp #3
    beq @visible
    sec
    rts
@visible:
    clc
    rts

full_hud_draw:
    ldx game_mode
    lda full_menu_lo,x
    sta menu_ptr
    lda full_menu_hi,x
    sta menu_ptr+1
    cpx #MODE_PLAY
    bne :+
    lda in_pit
    beq :+
    lda #<pit_hud
    sta menu_ptr
    lda #>pit_hud
    sta menu_ptr+1
:
    cpx #MODE_READ
    bne :+
    ldx reading_page
    lda full_clue_lo,x
    sta menu_ptr
    lda full_clue_hi,x
    sta menu_ptr+1
:
    lda #0
    sta hud_row
@row:
    jsr full_hud_address
    ldy #0
@char:
    lda (menu_ptr),y
    ora #$80
    sta (dst_ptr),y
    iny
    cpy #40
    bne @char
    lda menu_ptr
    clc
    adc #40
    sta menu_ptr
    bcc :+
    inc menu_ptr+1
:
    inc hud_row
    lda hud_row
    cmp #4
    bne @row
    lda game_mode
    beq @play
    cmp #MODE_NAME
    bne @inventory
    lda #1
    sta hud_row
    jsr full_hud_address
    ldy #5
    ldx #0
@name:
    lda player_name,x
    ora #$80
    sta (dst_ptr),y
    iny
    inx
    cpx #6
    bne @name
    jmp dhgr_hud_finish
@inventory:
    cmp #MODE_INVENTORY
    jne @done
    lda #0
    sta hud_row
    jsr full_hud_address
    ldy #7
    lda vials
    jsr hud_decimal2
    ldy #18
    lda torches
    jsr hud_decimal2
    ldy #28
    lda ropes
    jsr hud_decimal2
    jmp @done
@play:
    lda #0
    sta hud_row
    jsr full_hud_address
    lda energy
    sta word_tmp
    lda energy+1
    sta word_tmp+1
    ldx #0
@percent:
    lda word_tmp+1
    bmi @percent_ready
    bne @subtract
    lda word_tmp
    cmp #100
    bcc @percent_ready
@subtract:
    lda word_tmp
    sec
    sbc #100
    sta word_tmp
    lda word_tmp+1
    sbc #0
    sta word_tmp+1
    inx
    bne @percent
@percent_ready:
    txa
    ldy #7
    jsr hud_decimal3
    lda points
    sta word_tmp
    lda points+1
    sta word_tmp+1
    ldy #19
    jsr full_decimal5
    lda gold
    sta word_tmp
    lda gold+1
    sta word_tmp+1
    ldy #28
    jsr full_decimal5
    lda #1
    sta hud_row
    jsr full_hud_address
    lda current_room
    ldy #6
    jsr hud_decimal2
    lda actor_x
    ldy #11
    jsr hud_decimal2
    lda actor_y
    ldy #16
    jsr hud_decimal3
    lda held_item
    ldy #25
    jsr hud_decimal2
@done:
    jmp dhgr_hud_finish
full_hud_address:
    ldx hud_row
    lda hud_row_lo,x
    sta dst_ptr
    lda hud_row_hi,x
    ldx render_page_index
    beq :+
    clc
    adc #4
:
    sta dst_ptr+1
    rts
full_decimal5:
    ldx #0
@digit:
    lda #$B0
    sta (dst_ptr),y
@subtract:
    lda word_tmp+1
    cmp decimal_hi,x
    bcc @next
    bne @take
    lda word_tmp
    cmp decimal_lo,x
    bcc @next
@take:
    lda word_tmp
    sec
    sbc decimal_lo,x
    sta word_tmp
    lda word_tmp+1
    sbc decimal_hi,x
    sta word_tmp+1
    lda (dst_ptr),y
    clc
    adc #1
    sta (dst_ptr),y
    jmp @subtract
@next:
    iny
    inx
    cpx #5
    bne @digit
    rts
decimal_lo: .byte <10000,<1000,<100,<10,1
decimal_hi: .byte >10000,>1000,>100,>10,0
.segment "CODE"
.include "full-menus.inc"
pit_hud:
    .byte "FORCES:100% POINTS:00000 OR:00500       "
    .byte "SALLE:12 X:22 Y:180 MAIN:00             "
    .byte "OUBLIETTE - A POUR SE RELEVER           "
    .byte "ESPACE:DEBOUT G:REMONTER AVEC CORDE     "
entity_actor_y = $0F26
rope_actor_x = $0F2A
rope_actor_y = $0F2B

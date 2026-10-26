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
.if HGR_MONO
    asl a
.else
    clc
    adc #10
.endif
    sta cell_x
    lda #(6*(HGR_MONO+1))
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
    lda #RENDER_COLUMNS
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
    lda #RENDER_COLUMNS
    sta dirty_right,x
    lda #VIEW_HEIGHT
    sta dirty_bottom,x
    lda #1
    sta dirty_valid,x
@done:
    rts

full_visibility:
    lda game_mode
    cmp #MODE_CODE_SAVE
    bcs @text
    cmp #MODE_MAP_GROUND
    bcs @map
    lda #0
.if HGR_MONO
    sta $C00C
.else
    sta $C00D
    bit $C05E              ; restore DHGR after the full-screen HGR map
.endif
    bit $C053
    lda game_mode
    beq @play
    cmp #MODE_TITLE
    beq @title
    cmp #MODE_DEAD
    beq @title
    cmp #MODE_WIN
    beq @title
@text:
    sta $C00C
    bit $C052
    bit $C051
    rts
@title:
    bit $C052
    rts
@map:
    sta $C00C              ; ordinary HGR, full 280x192 MAIN frame
    bit $C05F
    bit $C052
    rts
@play:
    jsr full_is_dark
    bcc @done
    bit $C052
    bit $C051              ; retain the same 40/80 columns as the mixed HUD
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
    cmp #ACTION_GATE
    beq @visible
    sec
    rts
@visible:
    clc
    rts

full_hud_draw:
    jsr full_hud_template
    lda game_mode
    beq @play
    jmp @done
@play:
    jsr full_compact_feedback
    jsr full_room_description
    jsr clock_sample
    lda #2
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
    jsr clock_sample
    txa
    ldy #7
    jsr hud_decimal3
    ldy #7
    ldx #3
    jsr full_hud_trim
    lda points
    sta word_tmp
    lda points+1
    sta word_tmp+1
    ldy #23
    jsr full_decimal5
    ldy #23
    ldx #5
    jsr full_hud_trim
    lda #3
    sta hud_row
    jsr full_hud_address
    lda gold
    sta word_tmp
    lda gold+1
    sta word_tmp+1
    ldy #13
    jsr full_decimal5
    ldy #13
    ldx #5
    jsr full_hud_trim
    ldx held_item
    lda hud_hand_lo,x
    sta menu_ptr
    lda hud_hand_hi,x
    sta menu_ptr+1
    ldy #26
    jsr full_hud_string
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
.segment "CODE"
.export full_hud_clue_row, menu_ptr
; The first two gameplay rows are blank, not stored copies of 80 spaces.
; Reading copies three clue rows and the shared fourth-row instruction.
full_hud_template:
    lda #<full_menu_stats
    sta menu_ptr
    lda #>full_menu_stats
    sta menu_ptr+1
    ldx game_mode
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
    jsr clock_sample
    jsr full_hud_address
    ldy #0
    lda game_mode
    cmp #MODE_READ
    bne @ordinary
    lda hud_row
    cmp #3
    bne @clue
    lda #<full_clue_footer
    sta menu_ptr
    lda #>full_clue_footer
    sta menu_ptr+1
@clue:
    jsr full_hud_clue_row
    jmp @next
@ordinary:
    lda hud_row
    cmp #2
    bcs @char
    lda #$A0
@blank:
    sta (dst_ptr),y
    iny
    cpy #40
    bne @blank
    beq @next
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
    bcc @next
    inc menu_ptr+1
@next:
    inc hud_row
    lda hud_row
    cmp #4
    bne @row
    rts

; One NUL-terminated clue row, then blank padding to column 40. Advance by
; consumed bytes, not the padded display width (including a completely blank row).
full_hud_clue_row:
    lda (menu_ptr),y
    beq @pad
    ora #$80
    sta (dst_ptr),y
    iny
    bne full_hud_clue_row
@pad:
    tya
    sec
    adc menu_ptr
    sta menu_ptr
    bcc :+
    inc menu_ptr+1
:
    lda #$A0
@blank:
    cpy #40
    beq @done
    sta (dst_ptr),y
    iny
    bne @blank
@done:
    rts

full_decimal5:
    jsr clock_sample
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
.segment "RODATA"
; Fixed ten-column fields: normal leading spaces, inverse word, ALTCHAR on.
; Uppercase uses ASCII & $3F; lowercase stays $60-$7F (no MouseText/flash).
hud_feedback:
    .byte $09,"mpossible"
    .byte $A0,$A0,$A0,$A0,$A0,$A0,$16,"ide"
    .byte $A0,$A0,$A0,$A0,$A0,$05,"chec"
    .byte $A0,$04,"eja fait"
    .byte $A0,$A0,$A0,$A0,$A0,$03,"asse"
    .byte $16,"errouille"
    .byte $A0,$A0,$A0,$A0,$A0,$06,"erme"
    .byte $A0,$10,"archemin"
    .byte $A0,$0F,"r trouve"
    .byte $A0,$A0,$03,"lef fer"
    .byte $A0,$A0,$A0,$03,"lef or"
    .byte $A0,$A0,$A0,$A0,$A0,$06,"iole"
    .byte $A0,$A0,$A0,$A0,$A0,$02,"ague"
    .byte $A0,$A0,$A0,$A0,$A0,$10,"lomb"
.assert *-hud_feedback = (MSG_FOUND_LEAD-MSG_EMPTY+2)*10, error, "Each feedback field must be ten bytes"
decimal_lo: .byte <10000,<1000,<100,<10,1
decimal_hi: .byte >10000,>1000,>100,>10,0
.segment "CODE"
.include "full-menus.inc"
.include "full-description.inc"
entity_actor_y = $0F26
rope_actor_x = $0F2A
rope_actor_y = $0F2B

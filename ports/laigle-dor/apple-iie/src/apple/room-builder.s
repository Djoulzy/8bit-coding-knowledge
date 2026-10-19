scene_program = $F0
scene_opcode = $F2
scene_tmp = $F3
scene_grid_index = $F4

; Native parameterized constructor. B2 BASIC 100-1110; no per-room raster.
; Four shared wall programs, then upper/left/right openings and furnishings.
.export world_load_scene, scene_program_run, scene_stamp, scene_line
.macro stamp sid, xpos, ypos, add
    lda #sid
    ldx #xpos
    ldy #ypos
    jsr scene_place
    lda #add
    sta scene_additive
    jsr scene_stamp
.endmacro
.macro grid3 index, value
    ldx #index
    lda #value
    jsr scene_cells3
.endmacro
world_load_scene:
    ; Construct the new immutable baseline while the previous frame stays visible.
    lda #$FF
    sta line_pattern
    lda #15
    sta scene_ink
    lda in_pit
    beq @room_decode
    lda #0
    ldx #17
@pit_fields:
    sta room_geometry,x
    dex
    bpl @pit_fields
    lda #3
    sta room_geometry
    sta room_light
    jmp @decoded
@room_decode:
    jsr world_decode
@decoded:
    lda actor_x
    sta actor_saved
    lda actor_y
    sta actor_saved+1
    lda #0
    sta static_draw
    sta scene_additive
    ldx #119
@grid:
    sta GRID,x
    dex
    bpl @grid
    ; Clear main and auxiliary immutable baselines. Instruction reads stay main.
    sta dst_ptr
    lda #$A0
    sta dst_ptr+1
    ldx #32
    ldy #0
@clear:
    lda #0
    sta (dst_ptr),y
.if !HGR_MONO
    sta $C005
    sta (dst_ptr),y
    sta $C004
.endif
    iny
    bne @clear
    inc dst_ptr+1
    dex
    bne @clear
    lda #$A0
    sta draw_page_hi
    lda in_pit
    beq :+
    jsr scene_pit
    jmp scene_finished
:
    ldx room_geometry
    lda geometry_lo,x
    sta scene_program
    lda geometry_hi,x
    sta scene_program+1
    jsr scene_program_run
    jsr scene_upper
    jsr scene_left
    jsr scene_right
    lda room_geometry
    cmp #3
    bne :+
    lda #<geometry_left_border
    sta scene_program
    lda #>geometry_left_border
    sta scene_program+1
    jsr scene_program_run
:
    grid3 42,128
    grid3 77,128
    grid3 86,128
    grid3 113,128
    lda room_fields+1
    clc
    adc #128
    sta GRID+3
    lda room_fields+2
    clc
    adc #128
    sta GRID+37
    jsr scene_furnishing
    lda room_light
    beq :+
    stamp 14,18,80,0
    stamp 15,214,80,0
:
    jsr scene_floor
    jsr scene_gate
    jsr scene_objects
scene_finished:
    lda actor_saved
    sta actor_x
    lda actor_saved+1
    sta actor_y
    lda #0
    sta static_draw
    sta scene_additive
    sta room_dirty
    sta dirty_valid
    sta dirty_valid+1
    lda #3
    sta terrain_pending
    rts

; Called after draw_scene selects the hidden pair. Initialize only that pair,
; then compose actor/effects/HUD before the existing vertical-blank flip.
; The previous visible pair is initialized on the following iteration.
.export full_prepare_page
full_prepare_page:
    lda game_mode
    bne @repair
    jsr full_is_dark
    bcs @repair
    ldx render_page_index
    lda title_page_bits,x
    and terrain_pending
    beq @repair
    lda #0
    sta render_bank
    lda draw_page_hi
    jsr init_page
.if !HGR_MONO
    lda #1
    sta render_bank
    sta $C005
    lda draw_page_hi
    jsr init_page
    sta $C004
.endif
    ldx render_page_index
    lda title_page_bits,x
    eor #$FF
    and terrain_pending
    sta terrain_pending
    lda #0
    sta render_bank
    sta dirty_valid,x
    rts
@repair:
    jmp repair_page

scene_upper:
    lda room_geometry
    cmp #3
    beq @done
    lda #49
    ldx room_geometry
    bne :+
    lda #69
:
    sta scene_y
    lda room_fields
    beq @special
    lda #5
    sta scene_id
    lda #99
    sta scene_x
    lda #0
    sta scene_additive
    jsr scene_stamp
    lda room_fields
    cmp #3
    beq @special
    clc
    adc #7
    sta scene_id
    lda #105
    sta scene_x
    lda scene_y
    clc
    adc #10
    sta scene_y
    lda #1
    sta scene_additive
    jsr scene_stamp
@special:
    lda room_geometry
    beq @done
    lda room_furnishing
    cmp #1
    beq @stairs
    lda current_room
    cmp #63
    bne @done
@stairs:
    stamp 20,99,76,0
    lda room_fields+3
    and #1
    beq @done
.if HGR_MONO
    ; Original B2 398 point, without the enlarged DHGR marker.
    lda #107
    sta line_x
    lda #108
    sta line_y
    jsr scene_point
.else
    ; B2 398/10907 cue, enlarged on the right pillar for native DHGR.
    stamp 200,126,103,0
.endif
    jsr scene_secret_open
@done:
    rts
scene_left:
    lda room_fields+1
    beq @done
    stamp 6,6,105,0
    lda room_fields+1
    cmp #3
    beq @done
    clc
    adc #9
    ldx #12
    ldy #114
    jsr scene_place
    lda room_fields+1
    cmp #2
    bne :+
    lda #118
    sta scene_y
:
    lda #1
    sta scene_additive
    jmp scene_stamp
@done:
    rts
scene_right:
    lda room_fields+2
    beq @done
    stamp 7,204,105,0
    lda room_fields+2
    cmp #3
    beq @done
    clc
    adc #11
    ldx #210
    ldy #115
    jsr scene_place
    lda room_fields+2
    cmp #2
    bne :+
    lda #119
    sta scene_y
:
    lda #1
    sta scene_additive
    jmp scene_stamp
@done:
    rts

scene_furnishing:
    lda room_furnishing
    cmp #2
    bne @painting3
    lda room_variation
    cmp #129
    bcc :+
    stamp 21,80,36,0
    rts
:
    stamp 21,147,45,0
    rts
@painting3:
    cmp #3
    bne @chair
    stamp 22,80,45,0      ; B2 730 literal V (room number), not ROM variation M
    rts
@chair:
    cmp #4
    bne @table
    lda room_geometry
    beq :+
    cmp #3
    beq :+
    stamp 23,165,97,0
    grid3 108,151
    rts
:
    stamp 23,165,120,0
    grid3 69,151
    rts
@table:
    cmp #5
    bne @pedestal
    lda room_geometry
    beq :+
    stamp 25,159,107,0
    grid3 109,153
    grid3 112,153
    rts
:
    stamp 25,165,130,0
    grid3 69,153
    grid3 72,153
    rts
@pedestal:
    cmp #6
    bne @chest
    lda room_geometry
    beq @done
    cmp #3
    beq @done
    stamp 24,189,122,0
    grid3 73,152
    rts
@chest:
    cmp #7
    bne @done
    lda chest_open
    beq :+
    stamp 27,177,126,0
    jmp @chest_grid
:
    stamp 26,177,136,0
@chest_grid:
    grid3 73,154
@done:
    rts

scene_floor:
    lda scene_x
    sta floor_cursor
    lda scene_y
    sta floor_cursor+1
    lda room_features
    and #1
    jeq @done
    lda room_variation
    and #31
    asl a
    asl a
    ldx #0
@div31:
    cmp #31
    bcc :+
    sec
    sbc #31
    inx
    bne @div31
:
    txa
    asl a
    asl a
    clc
    adc #11
    sta scene_grid_index
    tax
    lda #1
    jsr scene_cells3
    lda scene_grid_index
    sec
    sbc #2
    jsr scene_times6
    sta scene_x
    lda room_floor
    beq @mark
    lda #16
    sta scene_id
    lda #172
    sta scene_y
    lda #0
    sta scene_additive
    jmp scene_stamp
@mark:
    lda possessions
    and #4
    bne @done
    lda room_variation
    and #63
    sta scene_tmp
    asl a
    asl a
    clc
    adc scene_tmp
    sta word_tmp
    lda #0
    adc #0
    sta word_tmp+1
    ldx #0
@div63:
    lda word_tmp+1
    bne @subtract
    lda word_tmp
    cmp #63
    bcc @glyph
@subtract:
    lda word_tmp
    sec
    sbc #63
    sta word_tmp
    lda word_tmp+1
    sbc #0
    sta word_tmp+1
    inx
    bne @div63
@glyph:
    txa
    clc
    adc #161
    sta scene_id
    cpx #1
    bcc @implicit
    cpx #5
    bcs @implicit
    lda scene_x
    clc
    adc floor_dx,x
    sta scene_x
    lda floor_y,x
    sta scene_y
@implicit:
    cpx #1
    bcc @restore_cursor
    cpx #5
    bcc :+
@restore_cursor:
    lda floor_cursor
    sta scene_x
    lda floor_cursor+1
    sta scene_y
:
    jmp scene_glyph
@done:
    rts

scene_gate:
    lda room_features
    and #2
    jeq @other
    lda room_gate
    jeq @wire
    lda #17
    ldx #68
    ldy #10
    jsr scene_place
    lda room_variation
    cmp #201
    bcc :+
    lda #18
    ldx #158
    ldy #10
    jsr scene_place
:
    lda #7
    sta scene_count
@bars:
    lda #1
    sta scene_additive
    jsr scene_stamp
    lda scene_y
    clc
    adc #19
    sta scene_y
    dec scene_count
    bne @bars
    lda #8
    sta scene_count
    lda #0
    sta scene_y
    lda room_variation
    cmp #201
    bcc :+
    lda scene_x
    clc
    adc #6
    jmp :++
:
    lda scene_x
    sec
    sbc #6
:
    sta scene_x
@bars2:
    jsr scene_stamp
    lda scene_y
    clc
    adc #20
    sta scene_y
    dec scene_count
    bne @bars2
    lda room_variation
    cmp #201
    bcc :+
    grid3 28,128
    grid3 68,128
    jmp @other
:
    grid3 12,128
    grid3 52,128
    jmp @other
@wire:
    lda room_fields+3
    cmp #2
    bcs @other
    lda possessions
    and #4
    bne @other
    lda room_variation
    cmp #201
    bcc @left_wire
    lda #<wire_right
    sta scene_program
    lda #>wire_right
    bne @wire_program
@left_wire:
    lda #<wire_left
    sta scene_program
    lda #>wire_left
@wire_program:
    sta scene_program+1
    jsr scene_program_run
@other:
    lda room_features
    and #4
    beq @done
    lda room_fields+3
    cmp #2
    bcs @done
    lda room_geometry
    cmp #3
    beq @done
    lda possessions
    and #4
    bne @done
    lda #167
    ldx #42
    ldy #100
    jsr scene_place
    jmp scene_glyph
@done:
    rts

scene_objects:
    lda room_geometry
    cmp #3
    beq @pile
    lda room_furnishing
    cmp #7
    beq @pile
    ldx room_treasure
    beq @pile
    lda treasure_ids,x
    sta scene_id
    lda treasure_x,x
    sta scene_x
    lda treasure_y,x
    sta scene_y
    lda #0
    sta scene_additive
    jsr scene_stamp
    grid3 48,160
    lda room_treasure
    cmp #7
    bne @pile
    grid3 51,160
@pile:
    lda room_fields+3
    cmp #2
    bcc @quests
    lda room_variation
    lsr a
    lsr a
    lsr a
    lsr a
    lsr a
    lsr a
    asl a
    asl a
    clc
    adc #12
    sta scene_grid_index
    tax
    lda #156
    jsr scene_cells3
    lda scene_grid_index
    clc
    adc #4
    tax
    lda #156
    jsr scene_cells3
    lda scene_grid_index
    sec
    sbc #2
    jsr scene_times6
    tax
    lda #28
    ldy #169
    jsr scene_place
    lda #0
    sta scene_additive
    jsr scene_stamp
@quests:
    lda current_room
    cmp #1
    bne @diamond
    lda objectives
    and #1
    beq @done
    stamp 93,183,120,0
    rts
@diamond:
    cmp #62
    bne @eagle
    lda objectives
    and #2
    beq :+
    stamp 31,183,104,0
:
    lda #168
    ldx #122
    ldy #154
    jsr scene_place
    jmp scene_glyph
@eagle:
    cmp #63
    bne @room36
    lda objectives
    and #4
    beq :+
    stamp 30,183,107,0
:
    stamp 16,78,172,0
    rts
@room36:
    cmp #36
    bne @done
    lda #169
    ldx #220
    ldy #110
    jsr scene_place
    jmp scene_glyph
@done:
    rts

scene_place:
    sta scene_id
    stx scene_x
    sty scene_y
    rts
scene_times6:
    sta scene_tmp
    asl a
    clc
    adc scene_tmp
    asl a
    rts
scene_cells3:
    sta GRID,x
    sta GRID+1,x
    sta GRID+2,x
    rts
scene_glyph:
    lda #2
    sta static_draw
    lda #1
    sta scene_additive
    bne scene_draw_atlas
scene_stamp:
    lda #1
    sta static_draw
scene_draw_atlas:
    lda scene_x
    ldx #0
@divide:
    cmp #6
    bcc :+
    sec
    sbc #6
    inx
    bne @divide
:
    stx actor_x
    lda scene_y
    sta actor_y
    lda #0
    sta dx
    sta dy
    ldx scene_id
    lda atlas_lo,x
    sta src_ptr
    lda atlas_hi,x
    sta src_ptr+1
    jmp draw_sprite_pointer

.segment "LOWCODE"
scene_program_run:
    ldy #0
    lda (scene_program),y
    beq @done
    sta scene_opcode
    iny
    lda (scene_program),y
    sta line_x
    sta scene_id
    iny
    lda (scene_program),y
    sta line_y
    sta scene_x
    iny
    lda (scene_program),y
    sta line_end_x
    sta scene_y
    iny
    lda (scene_program),y
    sta line_end_y
    sta scene_additive
    lda scene_program
    clc
    adc #5
    sta scene_program
    bcc :+
    inc scene_program+1
:
    lda scene_opcode
    cmp #1
    bne @sprite
    jsr scene_line
    lda line_end_x
    sta scene_x
    lda line_end_y
    sta scene_y
    jmp scene_program_run
@sprite:
    jsr scene_stamp
    jmp scene_program_run
@done:
    rts

; Signed 16-bit Bresenham error, source coordinates kept independent of DHGR.
scene_line:
    lda #1
    sta line_sx
    sta line_sy
    lda line_end_x
    sec
    sbc line_x
    bcs :+
    eor #$FF
    clc
    adc #1
    dec line_sx
    dec line_sx
:
    sta line_dx
    lda line_end_y
    sec
    sbc line_y
    bcs :+
    eor #$FF
    clc
    adc #1
    dec line_sy
    dec line_sy
:
    sta line_dy
    lda line_dx
    sec
    sbc line_dy
    sta line_err
    lda #0
    sbc #0
    sta line_err+1
@pixel:
    jsr scene_point
    lda line_x
    cmp line_end_x
    bne @advance
    lda line_y
    cmp line_end_y
    beq @done
@advance:
    lda line_err
    asl a
    sta line_twice
    lda line_err+1
    rol a
    sta line_twice+1
    ; e2 >= -dy iff e2+dy is nonnegative.
    lda line_twice
    clc
    adc line_dy
    lda line_twice+1
    adc #0
    bmi @vertical
    lda line_err
    sec
    sbc line_dy
    sta line_err
    lda line_err+1
    sbc #0
    sta line_err+1
    lda line_x
    clc
    adc line_sx
    sta line_x
@vertical:
    ; e2 <= dx iff dx-e2 is nonnegative.
    lda line_dx
    sec
    sbc line_twice
    lda #0
    sbc line_twice+1
    bmi @pixel
    lda line_err
    clc
    adc line_dx
    sta line_err
    lda line_err+1
    adc #0
    sta line_err+1
    lda line_y
    clc
    adc line_sy
    sta line_y
    jmp @pixel
@done:
    rts
scene_point:
    lda line_pattern
    lsr a
    bcc @pattern_skip
    ora #$80
    sta line_pattern
    ldx line_y
    cpx #200
    bcs @done
    lda y_map,x
    cmp #$FF
    beq @done
    cmp y_map+1,x
    beq @done
    tax
    lda row_lo,x
    sta dst_ptr
    lda row_hi,x
    and #$1F
    ora #$A0
    sta dst_ptr+1
    lda line_x
    cmp #240
    bcs @done
.if !HGR_MONO
    lsr a
    clc
    adc #10
.endif
    sta cell_x
    lda scene_ink
    sta cell_color
    jmp draw_cell
@done:
    rts
@pattern_skip:
    sta line_pattern
    rts
.segment "RODATA"
floor_dx: .byte 0,0,18,36,18
floor_y: .byte 0,176,170,176,184
treasure_ids: .byte 0,35,32,33,33,34,38,30
treasure_x: .byte 0,36,42,30,30,36,36,42
treasure_y: .byte 0,153,153,153,153,143,153,140
.segment "CODE"
wire_right: .byte 1,164,40,164,110,1,162,80,162,130,0
wire_left: .byte 1,95,133,88,148,1,88,148,81,163,1,81,163,74,178,1,74,178,67,193,0

floor_cursor = $0F24

; B2 7030-7048/6910: dedicated oubliette, not a numbered room template.
scene_pit:
    lda #<pit_outline
    sta scene_program
    lda #>pit_outline
    sta scene_program+1
    jsr scene_program_run
    grid3 11,128
    grid3 29,128
    lda #255
    ldx #41
@back_wall:
    sta GRID,x
    inx
    cpx #72
    bne @back_wall
    ; Source FILL mask $2A becomes stable gray material in the Apple palette.
    lda #0
    sta scene_y
@panel_row:
    ldx scene_y
    lda row_lo,x
    sta dst_ptr
    lda row_hi,x
    and #$1F
    ora #$A0
    sta dst_ptr+1
.if HGR_MONO
    lda #12
.else
    lda #16
.endif
    sta cell_x
    jsr pit_panel_row
.if HGR_MONO
    lda #168
.else
    lda #94
.endif
    sta cell_x
    jsr pit_panel_row
    inc scene_y
    lda scene_y
    cmp #VIEW_HEIGHT
    bne @panel_row
    ; Patterned perspective floor, B2 6910, original line endpoints.
    lda #90
    sta scene_x
@floor:
    lda scene_x
    sta line_x
    sec
    sbc #9
    sta line_end_x
    lda #165
    sta line_y
    lda #189
    sta line_end_y
    lda #15
    sta line_pattern
    jsr scene_line
    inc scene_x
    lda scene_x
    cmp #119
    bne @floor
    lda #$FF
    sta line_pattern
    lda room_variation
    and #63
    cmp #32
    bcs @done
    stamp 28,90,182,0
@done:
    rts
pit_panel_row:
.if HGR_MONO
    lda #60
.else
    lda #30
.endif
    sta scene_count
@cell:
.if HGR_MONO
    ; Source FILL $2A: alternating foreground dots, not a gray color cell.
    lda cell_x
    eor #1
    and #1
.else
    lda #5                ; gray DHGR serial pattern, palette $05
.endif
    sta cell_color
    jsr draw_cell
    inc cell_x
    dec scene_count
    bne @cell
    rts
pit_outline:
    .byte 1,72,0,72,199,1,72,199,81,179,1,81,179,104,159
    .byte 1,104,159,134,159,1,134,159,157,179
    .byte 1,157,179,166,199,1,166,199,166,0,0

; Mixed DHGR, two MAIN+AUX frame pairs; immutable terrain in both $A000 banks.
; No firmware calls or mirrored application code. RAMRD aux reads run in ZP.
.export video_init, draw_scene, draw_sprite, present_frame, present_flip
.export display_page_hi, draw_page_hi, dirty_left, dirty_right, dirty_top, dirty_bottom, dirty_valid
.exportzp sprite_index, dx, dy, render_page_index
.exportzp cell_x, cell_color, cell_mask, dst_ptr
.export draw_masked_cell
.import __AUXREAD_LOAD__, __AUXREAD_RUN__, __AUXREAD_SIZE__
video_init:
    lda #0
    sta $C000              ; 80STORE off: PAGE2 selects a real frame pair
    sta $C002
    sta $C004
    sta $C008              ; main ZP and stack, including safe bank workers
.if HGR_MONO
    sta $C00C              ; ordinary HGR, 40-column mixed text
.else
    sta $C00D              ; 80-column mixed text / DHGR hardware
.endif
.if FULL_GAME
    sta $C00F              ; alternate charset: inverse lowercase, no flashing
.else
    sta $C00E
.endif
    bit $C051
    bit $C054
    bit $C057
.if HGR_MONO
    bit $C05F              ; AN3 on: disable double HGR
.else
    bit $C05E              ; AN3 off = DHGR enable on configured Rev-B IIe
.endif
    bit $C053
    ldx #<(__AUXREAD_SIZE__-1)
@install:
    lda __AUXREAD_LOAD__,x
    sta __AUXREAD_RUN__,x
    dex
    bpl @install
    lda #$20
    sta display_page_hi
    lda #0
    sta dirty_valid
    sta dirty_valid+1
    jsr hud_init
.if FULL_GAME
    rts                   ; world display initializes each frame pair while hidden
.else
    lda #<room12_rle
    sta src_ptr
    lda #>room12_rle
    sta src_ptr+1
    jsr expand_baseline
    lda #<room12_aux_rle
    sta src_ptr
    lda #>room12_aux_rle
    sta src_ptr+1
    sta $C005              ; write only aux; instruction/resource reads remain main
    jsr expand_baseline
    sta $C004
    lda #0
    sta render_bank
@bank:
    lda render_bank
    beq :+
    sta $C005
:
    lda #$20
    jsr init_page
    lda #$40
    jsr init_page
    sta $C004
    inc render_bank
    lda render_bank
    cmp #2
    bne @bank
    rts
.endif

.if !FULL_GAME
expand_baseline:
    lda #0
    sta dst_ptr
    lda #BASELINE_HI
    sta dst_ptr+1
@packet:
    jsr read_src
    cmp #0
    beq @ready
    sta run_count
    jsr read_src
    ldy #0
@repeat:
    sta (dst_ptr),y
    inc dst_ptr
    bne :+
    inc dst_ptr+1
:
    dec run_count
    bne @repeat
    jmp @packet
@ready:
    rts
read_src:
    ldy #0
    lda (src_ptr),y
    inc src_ptr
    bne :+
    inc src_ptr+1
:
    rts
.endif
init_page:
    sta dst_ptr+1
    lda #BASELINE_HI
    sta src_ptr+1
    lda #0
    sta src_ptr
    sta dst_ptr
    ldx #32
    ldy #0
@copy:
    lda render_bank
    beq @main
    jsr aux_read_src
    jmp @write
@main:
    lda (src_ptr),y
@write:
    sta (dst_ptr),y
    dey
    bne @copy
    inc src_ptr+1
    inc dst_ptr+1
    dex
    bne @copy
    rts

draw_scene:
    lda display_page_hi
    eor #$60
    sta draw_page_hi
    ldx #0
    cmp #$20
    beq :+
    inx
:
    stx render_page_index
.if FULL_GAME
    lda game_mode
    cmp #MODE_CODE_SAVE
    jcs full_text_draw
    cmp #MODE_MAP_GROUND
    jcs full_map_draw
    jsr actor_cache
    bcc :+
    jsr full_draw_torches
    jmp hud_draw
:
    jsr full_prepare_page
.else
    jsr repair_page
.endif
    ldx render_page_index
    lda #RENDER_COLUMNS
    sta dirty_left,x
    lda #0
    sta dirty_right,x
    sta dirty_bottom,x
    sta dirty_valid,x
.if FULL_GAME
    lda game_mode
    cmp #MODE_TITLE
    bne :+
    jmp title_draw
:
    lda game_mode
    beq :+
    jmp full_text_draw
:
    jsr full_is_dark
    bcc :+
    jmp full_dark_text_draw
:
.endif
    lda #VIEW_HEIGHT
    sta dirty_top,x
.if FULL_GAME
    jsr full_draw_torches
.endif
    ldx frame_id
    lda frame_lo,x
    sta frame_ptr
    lda frame_hi,x
    sta frame_ptr+1
    ldy #0
    lda (frame_ptr),y
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
    iny
    sty layer_cursor
    jsr draw_sprite
    dec layer_count
    bne @layer
.if FULL_GAME
    jsr full_draw_equipment
    jsr full_draw_entities
.endif
    jmp hud_draw

repair_page:
    ldx render_page_index
    lda dirty_valid,x
    bne :+
    rts
:
    lda dirty_left,x
    sta repair_left
    lda dirty_right,x
    sta repair_right
    lda dirty_top,x
    sta repair_y
    lda dirty_bottom,x
    sta repair_bottom
repair_rectangle:
.if FULL_GAME
    jsr clock_sample
.endif
    ldx repair_y
    lda row_lo,x
    sta src_ptr
    sta dst_ptr
    lda row_hi,x
    and #$1F
    ora #BASELINE_HI
    sta src_ptr+1
    lda row_hi,x
    and #$1F
    ora draw_page_hi
    sta dst_ptr+1
.if FULL_GAME
    lda repair_right
.if !HGR_MONO
    lsr a
.endif
    sta repair_limit
    lda repair_left
.if !HGR_MONO
    lsr a
.endif
    tay
    cpy repair_limit
    beq @aux_span
@main_span:
    lda (src_ptr),y
    sta (dst_ptr),y
    iny
    cpy repair_limit
    bne @main_span
@aux_span:
.if !HGR_MONO
    lda repair_right
    lsr a
    adc #0                 ; ceil(serial right / 2): AUX bytes have even index
    sta repair_limit
    lda repair_left
    lsr a
    adc #0
    tay
    cpy repair_limit
    beq :+
    jsr aux_copy_span
:
.endif
.else
    lda repair_left
    sta serial_col
@byte:
.if HGR_MONO
    ldy serial_col
    lda (src_ptr),y
    sta (dst_ptr),y
    jmp @next
.else
    lda serial_col
    lsr a                   ; carry clear: AUX byte, carry set: MAIN byte
    tay
    bcs @main
    jsr aux_read_src
    sta $C005
    sta (dst_ptr),y
    sta $C004
    jmp @next
@main:
    lda (src_ptr),y
    sta (dst_ptr),y
.endif
@next:
    inc serial_col
    lda serial_col
    cmp repair_right
    bne @byte
.endif
    inc repair_y
    lda repair_y
    cmp repair_bottom
    bne repair_rectangle
    rts

present_frame:
@leave_blank:
.if FULL_GAME
    jsr clock_sample
.endif
    bit $C019
    bpl @leave_blank
@enter_blank:
.if FULL_GAME
    jsr clock_sample
.endif
    bit $C019
    bmi @enter_blank
present_flip:
    lda draw_page_hi
    cmp #$20
    bne @page2
    bit $C054
    jmp @selected
@page2:
    bit $C055
@selected:
    sta display_page_hi
    bit $C050
.if FULL_GAME
    jsr full_visibility
    jmp clock_sample        ; include the blank edge that triggered this flip
.endif
    rts

; 16-byte header: cell width, source height, row stride, seven byte extents.
; Each row: raw foreground pattern, then two 4-bit pair statuses/byte.
; Fine art keeps opacity/foreground per source dot. Both $A and $F use the
; row material. Adapted hair/legs use $0/$5/$F for empty/black/full-color cells.
draw_sprite:
    ldx sprite_index
    lda sprite_lo,x
    sta src_ptr
    lda sprite_hi,x
    sta src_ptr+1
draw_sprite_pointer:
    lda actor_x
    clc
    adc dx
    tax
    cpx #40
    bcc :+
    rts
:
    lda actor_cell_x,x
    sta origin_cell
    lda x_byte,x
    sta x_column
    lda x_phase,x
    sta phase
    lda actor_y
    clc
    adc dy
    sta row_y
    cmp #200
    bcc :+
    rts
:
    ldy #0
 .if FULL_GAME
    jsr aux_read_src
 .else
    lda (src_ptr),y
 .endif
    sta sprite_w
    iny
 .if FULL_GAME
    jsr aux_read_src
 .else
    lda (src_ptr),y
 .endif
    sta sprite_h
    iny
 .if FULL_GAME
    jsr aux_read_src
 .else
    lda (src_ptr),y
 .endif
    sta row_stride
    lda phase
    clc
    adc #3
    tay
 .if FULL_GAME
    jsr aux_read_src
 .else
    lda (src_ptr),y
 .endif
    sta out_w
.if FULL_GAME
    ldy #10
    jsr aux_read_src
    sta tile_format
    iny
    jsr aux_read_src
    sta tile_accent
    ldy #13
    jsr aux_read_src
    sta native_width
    ldy #12
    jsr aux_read_src
    beq :+
    lda #0
    sta scene_additive       ; grille holes clear the underlying arch
:
    lda static_draw
    cmp #2
    bne :+
    lda scene_x
.if !HGR_MONO
    lsr a
    clc
    adc #10
.endif
    sta origin_cell
:
    lda static_draw
    bne :+
.endif
    jsr include_bounds
.if FULL_GAME
:
.endif
    lda src_ptr
    clc
    adc #16
    sta src_ptr
    bcc :+
    inc src_ptr+1
:
.if FULL_GAME
    lda tile_format
    cmp #2
    jeq draw_native_sprite
.endif
@row:
.if FULL_GAME
    jsr clock_sample
.endif
    ldx row_y
    cpx #200
    bcc :+
    jmp @done              ; clip before unsigned source-y could wrap
:
    lda y_map,x
    cmp #$FF
    bne :+
    jmp @advance
:
.if FULL_GAME
    lda static_draw
    beq :+
    lda y_map,x
    cmp y_map+1,x
    jeq @advance
:
    lda y_map,x
.endif
    tax
    lda row_lo,x
    sta dst_ptr
    lda row_hi,x
    and #$1F
    ora draw_page_hi
    sta dst_ptr+1
    ldy #0
 .if FULL_GAME
    jsr aux_read_src
 .else
    lda (src_ptr),y
 .endif
    sta row_color
    lda #1
    sta data_cursor
    lda #0
    sta code_count
    lda origin_cell
    sta cell_x
    lda sprite_w
    sta cells_left
@cell:
    lda code_count
    bne @loaded
    ldy data_cursor
 .if FULL_GAME
    jsr aux_read_src
 .else
    lda (src_ptr),y
 .endif
    sta dhgr_codes
    inc data_cursor
.if FULL_GAME
    lda tile_format
    beq :+
    lda #4
    bne :++
:
.endif
    lda #2
.if FULL_GAME
:
.endif
    sta code_count
@loaded:
    lda dhgr_codes
.if FULL_GAME
    ldx tile_format
    beq @actor_status
    and #3
    beq @next_cell
    cmp #1
    bne @static_ink
    lda scene_additive
    bne @next_cell
    lda #5
    bne @status_ready
@static_ink:
    cmp #3
    bne :+
    lda #15
    sta cell_mask
    lda tile_accent
    sta cell_color
    jmp @put_color
:
    lda #15
    bne @status_ready
@actor_status:
.endif
    and #$0F
.if FULL_GAME
@status_ready:
.endif
    tax
    lda sprite_status_mask,x
    beq @next_cell
    sta cell_mask
    cpx #15
    beq @material
    cpx #10               ; full foreground pair at a source detail boundary
    bne @detail
@material:
    lda row_color
    jmp @color
@detail:
    lda sprite_status_pattern,x
    beq @color            ; source black remains black
    and row_color
    bne @color
    lda sprite_status_pattern,x ; retain a fine dot if hue phase would erase it
@color:
    sta cell_color
.if FULL_GAME
@put_color:
.endif
    lda cell_x
    cmp #CELL_LIMIT
    bcs @next_cell
    jsr draw_masked_cell
@next_cell:
    lsr dhgr_codes
    lsr dhgr_codes
.if FULL_GAME
    lda tile_format
    bne :+
.endif
    lsr dhgr_codes
    lsr dhgr_codes
.if FULL_GAME
:
.endif
    dec code_count
.if HGR_MONO
    lda cell_x
    cmp #239
    bcs @advance           ; clip before 8-bit source x could wrap to the left
.endif
    inc cell_x
    dec cells_left
.if FULL_GAME
    jne @cell
.else
    bne @cell
.endif
@advance:
    lda row_stride
    clc
    adc src_ptr
    sta src_ptr
    bcc :+
    inc src_ptr+1
:
    inc row_y
    dec sprite_h
    beq @done
    jmp @row
@done:
    rts

; A cell may span two serial bytes and either bank. Update all four bits;
; nibble masks preserve neighboring colors and holes even at bank boundaries.
draw_cell:
    lda #15
    sta cell_mask
draw_masked_cell:
.if HGR_MONO
    ; One Oric source dot per HGR bit, at x+20. Bit 7 stays zero.
    ; AUX is resource storage only, never a graphics framebuffer.
    ldx cell_x
    cpx #240
    bcs @done
    lda cell_phase,x
    sta mask
    lda cell_byte,x
    tay
    lda cell_color
    beq @black
    lda (dst_ptr),y
    ora mask
    sta (dst_ptr),y
    rts
@black:
    lda mask
    eor #$7F
    and (dst_ptr),y
    sta (dst_ptr),y
@done:
    rts
.else
    ldx cell_x
    lda cell_byte,x
    sta serial_col
    lda cell_phase,x
    ora cell_color
    tax
    lda cell_color_lo,x
    sta pixel
    lda cell_color_hi,x
    sta spill
    ldx cell_x
    lda cell_phase,x
    ora cell_mask
    tax
    lda cell_color_lo,x
    sta mask
    lda cell_color_hi,x
    sta mask_spill
    jsr write_fragment
    inc serial_col
    lda mask_spill
    beq @done
    sta mask
    lda spill
    sta pixel
    jsr write_fragment
@done:
    rts
write_fragment:
    lda serial_col
    lsr a
    tay
    bcs @main
    jsr aux_read_dst
    jmp @compose
@main:
    lda (dst_ptr),y
@compose:
    sta tmp
    lda mask
    eor #$FF
    and tmp
    ora pixel
    sta tmp
    lda serial_col
    and #1
    bne @main_write
    lda tmp
    sta $C005
    sta (dst_ptr),y
    sta $C004
    rts
@main_write:
    lda tmp
    sta (dst_ptr),y
    rts
.endif

include_bounds:
    lda row_y
    cmp #200
    bcs @empty
    cmp #VIEW_TOP
    bcs @top
    lda #VIEW_TOP
@top:
    tax
    lda y_map,x
    sta bounds_top
    lda row_y
    clc
    adc sprite_h
    bcs @bottom_clip
    cmp #201
    bcc :+
@bottom_clip:
    lda #200
:
    sec
    sbc #1
    cmp #VIEW_TOP
    bcc @empty
    tax
    lda y_map,x
    clc
    adc #1
    sta bounds_bottom
    ldx render_page_index
    lda bounds_top
    cmp dirty_top,x
    bcs :+
    sta dirty_top,x
:
    lda bounds_bottom
    cmp dirty_bottom,x
    bcc :+
    sta dirty_bottom,x
:
    lda x_column
    cmp dirty_left,x
    bcs :+
    sta dirty_left,x
:
    lda x_column
    clc
    adc out_w
    cmp #(RENDER_COLUMNS+1)
    bcc :+
    lda #RENDER_COLUMNS
:
    cmp dirty_right,x
    bcc :+
    sta dirty_right,x
:
    lda #1
    sta dirty_valid,x
@empty:
    rts

; Linker run address $0040. Install once after BOOT0 is finished using ZP.
; ALTZP remains off: these instruction bytes and the stack never bank out.
.segment "AUXREAD"
.export aux_read_src, aux_read_dst
aux_read_src:
    sta $C003
    lda (src_ptr),y
    sta $C002
    rts
aux_read_dst:
    sta $C003
    lda (dst_ptr),y
    sta $C002
    rts
.if FULL_GAME
aux_read_row:
    sta $C003
@copy:
    lda (src_ptr),y
    sta NATIVE_ROW,y
    dey
    bpl @copy
    sta $C002
    rts
aux_copy_span:
    sta $C003
    sta $C005
@copy:
    lda (src_ptr),y
    sta (dst_ptr),y
    iny
    cpy repair_limit
    bne @copy
    sta $C004
    sta $C002
    rts
.endif
.segment "CODE"

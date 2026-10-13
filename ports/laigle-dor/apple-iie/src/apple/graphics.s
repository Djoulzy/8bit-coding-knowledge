; Mixed HGR: two frame pages, immutable terrain baseline at $A000.
; Only the hidden page is repaired/drawn. Each page owns its prior dirty bounds.
.export video_init, draw_scene, draw_sprite, present_frame, present_flip
.export display_page_hi, draw_page_hi, dirty_left, dirty_right, dirty_top, dirty_bottom, dirty_valid
.exportzp sprite_index, dx, dy, render_page_index
video_init:
    lda #0
    sta $C000              ; 80STORE off: PAGE2 selects main-RAM display pages
    sta $C002
    sta $C004
    sta $C008
    sta $C00C              ; 40-column text
    sta $C00E              ; normal charset
    bit $C051              ; text until first completed frame
    bit $C054
    bit $C057
    bit $C053              ; HGR 160 rows + four text rows
    lda #$20
    sta display_page_hi
    lda #0
    sta dirty_valid
    sta dirty_valid+1
    jsr hud_init
    lda #<room12_rle
    sta src_ptr
    lda #>room12_rle
    sta src_ptr+1
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
    lda #$20
    jsr init_page
    lda #$40
    jmp init_page
read_src:
    ldy #0
    lda (src_ptr),y
    inc src_ptr
    bne :+
    inc src_ptr+1
:
    rts
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
    lda (src_ptr),y
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
    eor #$60               ; $20 <-> $40
    sta draw_page_hi
    ldx #0
    cmp #$20
    beq :+
    inx
:
    stx render_page_index
    jsr repair_page
    ldx render_page_index
    lda #40
    sta dirty_left,x
    lda #0
    sta dirty_right,x
    sta dirty_bottom,x
    sta dirty_valid,x
    lda #VIEW_HEIGHT
    sta dirty_top,x
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
@row:
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
    ldy repair_left
@byte:
    lda (src_ptr),y
    sta (dst_ptr),y
    iny
    cpy repair_right
    bne @byte
    inc repair_y
    lda repair_y
    cmp repair_bottom
    bne @row
    rts

present_frame:
    ; IIe RDVBLBAR: high during active display, low in vertical blank.
@leave_blank:
    bit $C019
    bpl @leave_blank
@enter_blank:
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
    rts

; Header: byte width, source height, seven output widths, legacy extent masks;
; then interleaved pixel/mask bytes. Source ink/paper is not retained.
draw_sprite:
    ldx sprite_index
.if HGR_COLOR
    lda sprite_color_phase,x
    sta color_phase
.endif
    lda sprite_lo,x
    sta src_ptr
    lda sprite_hi,x
    sta src_ptr+1
    lda actor_x
    clc
    adc dx
    tax
    cpx #40
    bcc :+
    rts
:
    lda x_byte,x
    sta x_column
    lda x_phase,x
    sta phase
    clc
    adc #>shift_table
    sta shift_ptr+1
    lda #<shift_table
    sta shift_ptr
    lda actor_y
    clc
    adc dy
    sta row_y
    cmp #200
    bcc :+
    rts                    ; invalid unsigned source-y must not wrap into viewport
:
    ldy #0
    lda (src_ptr),y
    sta sprite_w
    iny
    lda (src_ptr),y
    sta sprite_h
    lda phase
    clc
    adc #2
    tay
    lda (src_ptr),y
    sta out_w
    jsr include_bounds
    lda src_ptr
    clc
    adc #16
    sta src_ptr
    bcc @row
    inc src_ptr+1
@row:
    ldx row_y
    cpx #200
    bcc :+
    jmp @advance
:
    lda y_map,x
    cmp #$FF
    bne :+
    jmp @advance
:
    tax
    lda row_lo,x
    clc
    adc x_column
    sta dst_ptr
    lda row_hi,x
    and #$1F
    ora draw_page_hi
    adc #0
    sta dst_ptr+1
    lda #0
    sta spill
    sta mask_spill
    sta col
@column:
    lda col
    cmp sprite_w
    bcs @zero
    asl a
    tay
    lda (src_ptr),y
    sta raw_pixel
    iny
    lda (src_ptr),y
    jmp @mask_ready
@zero:
    lda #0
    sta raw_pixel
@mask_ready:
    sta raw_mask
    ldy raw_pixel
    lda (shift_ptr),y
    ora spill
    sta pixel
    tya
    ora #$80
    tay
    lda (shift_ptr),y
    sta spill
    ldy raw_mask
    lda (shift_ptr),y
    ora mask_spill
    sta mask
    tya
    ora #$80
    tay
    lda (shift_ptr),y
    sta mask_spill
    lda x_column
    clc
    adc col
    cmp #40
    bcs @next_column
    ldy col
.if HGR_COLOR
    lda mask
    beq @next_column      ; transparent bytes cannot change terrain's phase
.endif
    lda mask
    eor #$7F
    and (dst_ptr),y
    sta tmp
    lda pixel
    and mask
    ora tmp
.if HGR_COLOR
    and #$7F              ; bit 7 is byte-wide HGR phase, never a pixel mask
    ora color_phase
.endif
    sta (dst_ptr),y
@next_column:
    inc col
    lda col
    cmp out_w
    bne @column
@advance:
    lda sprite_w
    asl a
    clc
    adc src_ptr
    sta src_ptr
    bcc :+
    inc src_ptr+1
:
    inc row_y
    dec sprite_h
    beq @empty
    jmp @row
@empty:
    rts

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
    cmp #41
    bcc :+
    lda #40
:
    cmp dirty_right,x
    bcc :+
    sta dirty_right,x
:
    lda #1
    sta dirty_valid,x
@empty:
    rts

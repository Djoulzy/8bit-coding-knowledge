; B1 title bitmap and source-controlled lightning, adapted DHGR frame cadence.
.segment "LOWCODE"
.export title_begin, title_draw, title_tick_update
title_begin:
    lda #0
    sta title_tick
    sta title_stage
    sta title_pages_ready
    sta room_dirty
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
.if HGR_MONO
    cmp #1
.else
    cmp #2
.endif
    bne @bank
    lda #$20
    sta draw_page_hi
    jsr title_cover_bottom
    lda #$40
    sta draw_page_hi
    jsr title_cover_bottom
    lda #MODE_TITLE
    sta game_mode
    rts
title_tick_update:
    lda raw_key
    cmp #13
    beq @start
    cmp #32
    beq @start
    inc title_tick
    lda title_tick
    cmp #72
    bcc @done
    lda #1
    sta title_stage
@done:
    rts
@start:
    lda #MODE_INTRO
    sta game_mode
    rts
title_draw:
    lda title_stage
    beq @patch
    ldx render_page_index
    lda title_page_bits,x
    and title_pages_ready
    bne @patch
    lda title_page_bits,x
    ora title_pages_ready
    sta title_pages_ready
    jsr title_restore_bottom
@patch:
    lda #<title_flash_data
    sta src_ptr
    lda #>title_flash_data
    sta src_ptr+1
@record:
    ldy #0
    lda (src_ptr),y
    sta dst_ptr
    iny
    lda (src_ptr),y
    cmp #$FF
    beq @done
    sta title_patch_bank
    and #$1F
    ora draw_page_hi
    sta dst_ptr+1
    ldy #3                ; off-state byte
    lda title_stage
    bne :+
    lda title_tick
    and #4
    beq :+
    dey                   ; yellow flash-state byte
:
    lda (src_ptr),y
    ldy title_patch_bank
    bpl :+
    sta $C005
:
    ldy #0
    sta (dst_ptr),y
    sta $C004
    lda src_ptr
    clc
    adc #4
    sta src_ptr
    bcc @record
    inc src_ptr+1
    jmp @record
@done:
    rts
title_cover_bottom:
    lda #0
    beq title_bottom
title_restore_bottom:
    lda #1
title_bottom:
    sta title_copy
    lda #110              ; source graphic title begins at row 131 -> target 110
    sta title_row
@row:
    ldx title_row
    lda row_lo,x
    sta dst_ptr
    sta src_ptr
    lda row_hi,x
    and #$1F
    ora draw_page_hi
    sta dst_ptr+1
    lda row_hi,x
    and #$1F
    ora #$A0
    sta src_ptr+1
    ldy #39
@byte:
    lda #0
    ldx title_copy
    beq :+
    lda (src_ptr),y
:
    sta (dst_ptr),y
    lda #0
    ldx title_copy
.if !HGR_MONO
    beq :+
    jsr aux_read_src
:
    sta $C005
    sta (dst_ptr),y
    sta $C004
.endif
    dey
    bpl @byte
    inc title_row
    lda title_row
    cmp #192
    bne @row
    rts
.segment "CODE"
title_page_bits: .byte 1,2
title_patch_bank = $0F27
title_row = $0F28
title_copy = $0F29

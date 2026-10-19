; All editions show the same full-screen MAIN HGR map. Each page is loaded
; while hidden; no AUX graphics, terrain baseline or Apple TEXT is modified.
.segment "LOWCODE"
.export full_map_draw, full_map_mark, map_cached
full_map_draw:
    ldx render_page_index
    lda map_cached,x
    cmp game_mode
    beq @done
    lda game_mode
    sta map_cached,x
    sec
    sbc #MODE_MAP_GROUND
    asl a
    clc
    adc #15                 ; physical sector 240; 32 sectors per HGR page
    sta disk_wanted_track
    lda #0
    sta disk_wanted_sector
    sta asset_aux
    lda draw_page_hi
    sta asset_page
    lda #32
    sta asset_pages
    jsr asset_load_range
    jmp full_map_mark
@done:
    rts

full_map_mark:
    lda #MODE_MAP_OTHER
    ldx current_room
    cpx #9
    bcc @page
    cpx #58
    bcs @page
    lda #MODE_MAP_GROUND
@page:
    cmp game_mode
    bne @status
    lda map_room_row,x
    sta map_y
    lda map_room_column,x   ; pin occupies a reserved byte-aligned 7x9 area
    sta map_columns
    lda #0
    sta panel_column
@pin:
    jsr full_map_address
    ldx panel_column
    lda map_pin,x
    ora (dst_ptr),y
    sta (dst_ptr),y
    inc map_y
    inc panel_column
    lda panel_column
    cmp #9
    bne @pin
@status:
    lda #14
    sta map_columns
    lda current_room
    ldx #0
@tens:
    cmp #10
    bcc @digits
    sec
    sbc #10
    inx
    bne @tens
@digits:
    sta map_rows            ; units survive the first glyph call
    txa
    jsr full_map_glyph
    inc map_columns
    lda map_rows
    jsr full_map_glyph
    lda #35
    sta map_columns
    lda #10                 ; '-' normally, 'X' when in an oubliette
    ldx in_pit
    beq :+
    lda #11
:
    jmp full_map_glyph

; A = glyph index, map_columns = HGR byte column. Seven rows at y=164.
; Glyph index * 7 fits a byte for all 12 resident glyphs.
full_map_glyph:
    sta tmp
    asl a
    asl a
    asl a
    sec
    sbc tmp
    sta panel_column
    lda #164
    sta map_y
@row:
    jsr full_map_address
    ldx panel_column
    lda map_glyphs,x
    sta (dst_ptr),y         ; reserved blank byte: replace stale digits entirely
    inc panel_column
    inc map_y
    lda map_y
    cmp #171
    bne @row
    rts

.segment "CODE"
full_map_address:
    ldx map_y
    lda row_lo,x
    sta dst_ptr
    lda row_hi,x
    and #$1F
    ora draw_page_hi
    sta dst_ptr+1
    ldy map_columns
    rts
.segment "CODE"

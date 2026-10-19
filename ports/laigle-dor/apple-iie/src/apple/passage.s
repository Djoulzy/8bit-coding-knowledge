; Visible final opening inspired by B2 10980. The target fills the whole slit
; instead of the source's animated alternate scanlines. Render into baseline;
; room_dirty/terrain_pending propagates it to each hidden frame, without trails.
.segment "EXTRACODE"
scene_secret_open:
    lda passage
    beq @done
    lda #98
    sta line_end_y
@row:
    lda line_end_y
    sta line_y
    lda #114
    sta line_x
    lda #130
    sta line_end_x
    jsr scene_line
    lda #0
    sta scene_ink
    inc line_end_y
    lda line_end_y
    cmp #121
    bcc @row
    lda #15
    sta scene_ink
@done:
    rts
.segment "CODE"

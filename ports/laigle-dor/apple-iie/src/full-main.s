.setcpu "6502"
.macpack longbranch
.include "memory.inc"
.import __LOWCODE_LOAD__, __LOWCODE_RUN__, __LOWCODE_SIZE__
.segment "CODE"
.export entry, main_loop, frame_complete
entry:
    sei
    cld
    lda #0
    sta $C000
    sta $C002
    sta $C004
    sta $C008
    ldx #$FF
    txs
    lda #<__LOWCODE_LOAD__
    sta src_ptr
    lda #>__LOWCODE_LOAD__
    sta src_ptr+1
    lda #<__LOWCODE_RUN__
    sta dst_ptr
    lda #>__LOWCODE_RUN__
    sta dst_ptr+1
    lda #<__LOWCODE_SIZE__
    sta word_tmp
    lda #>__LOWCODE_SIZE__
    sta word_tmp+1
    ldy #0
@install:
    lda (src_ptr),y
    sta (dst_ptr),y
    inc src_ptr
    bne :+
    inc src_ptr+1
:
    inc dst_ptr
    bne :+
    inc dst_ptr+1
:
    lda word_tmp
    bne :+
    dec word_tmp+1
:
    dec word_tmp
    lda word_tmp
    ora word_tmp+1
    bne @install
    lda #0
    sta disk_cache_valid
    sta disk_drive2_ready
    sta disk_tracks+1
    sta disk_phases+1
    sta session_attempt
    jsr game_reset
    jsr video_init
    jsr title_load
    jsr title_begin
    jsr draw_scene
    jsr present_frame
    jsr asset_load          ; castle stays visible while shared sprites load
main_loop:
    jsr keyboard_poll
    jsr game_tick
    jsr full_clock
    lda room_dirty
    beq :+
    jsr world_load_scene
:
    jsr draw_scene
    jsr present_frame
frame_complete:
    jmp main_loop
.include "game/core.s"
.include "game/full-core.s"
.include "game/proximity.s"
.include "apple/input.s"
.include "apple/audio.s"
.include "apple/dhgr.s"
.include "apple/hud.s"
.include "apple/dhgr-hud.s"
.include "apple/full-display.s"
.include "apple/torches.s"
.include "apple/full-text.s"
.include "apple/title.s"
.include "apple/asset-loader.s"
.include "apple/room-builder.s"
.export code_end
code_end:
.segment "RODATA"
.export room12_grid, sprite_lo, sprite_hi, frame_lo, frame_hi, row_lo, row_hi
.include "generated.inc"
.export resident_end
resident_end:
.assert resident_end <= $A000, lderror, "Resident code/resources overlap terrain baseline"
.assert __AUXREAD_LOAD__+__AUXREAD_SIZE__ <= $A000, lderror, "Bank worker template overlaps baseline"

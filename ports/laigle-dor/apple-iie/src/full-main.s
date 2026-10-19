.setcpu "6502"
.macpack longbranch
.include "memory.inc"
.import __LOWCODE_LOAD__, __LOWCODE_RUN__, __LOWCODE_SIZE__
.import __EXTRACODE_LOAD__, __EXTRACODE_RUN__, __EXTRACODE_SIZE__
.import __PASSCODE_LOAD__, __PASSCODE_RUN__, __PASSCODE_SIZE__
.import __PASSUI_LOAD__, __PASSUI_RUN__, __PASSUI_SIZE__
.import __PASSTAIL_LOAD__, __PASSTAIL_RUN__, __PASSTAIL_SIZE__
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
    ; Free MAIN gap after the 40-byte HUD buffer and before disk state at $0F00.
    ldx #0
@extra:
    lda __EXTRACODE_LOAD__,x
    sta __EXTRACODE_RUN__,x
    inx
    cpx #<__EXTRACODE_SIZE__
    bne @extra
    ldx #0
@pass:
    lda __PASSCODE_LOAD__,x
    sta __PASSCODE_RUN__,x
    inx
    cpx #<__PASSCODE_SIZE__
    bne @pass
    ldx #0
@passui:
    lda __PASSUI_LOAD__,x
    sta __PASSUI_RUN__,x
    inx
    cpx #<__PASSUI_SIZE__
    bne @passui
    ldx #0
@passtail:
    lda __PASSTAIL_LOAD__,x
    sta __PASSTAIL_RUN__,x
    inx
    cpx #<__PASSTAIL_SIZE__
    bne @passtail
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
    jsr clock_reset         ; room construction is not charged as active play
:
    jsr draw_scene
    jsr present_frame
frame_complete:
    jmp main_loop
.include "game/core.s"
.include "game/full-core.s"
.include "game/ui.s"
.include "game/debug.s"
.include "game/proximity.s"
.include "game/passage.s"
.include "game/checkpoint.s"
.include "apple/input.s"
.include "apple/audio.s"
.include "apple/dhgr.s"
.include "apple/native-sprites.s"
.include "apple/actor-cache.s"
.include "apple/service-clock.s"
.include "apple/hud.s"
.include "apple/dhgr-hud.s"
.include "apple/full-display.s"
.include "apple/torches.s"
.include "apple/full-text.s"
.include "apple/map.s"
.include "apple/title.s"
.include "apple/asset-loader.s"
.include "apple/room-builder.s"
.include "apple/passage.s"
.include "apple/feedback.s"
.include "apple/checkpoint.s"
.export code_end
code_end:
.segment "RODATA"
.export room12_grid, sprite_lo, sprite_hi, frame_lo, frame_hi, row_lo, row_hi
.include "generated.inc"
.export resident_end
resident_end:
.assert resident_end <= $A000, lderror, "Resident code/resources overlap terrain baseline"
.assert __AUXREAD_LOAD__+__AUXREAD_SIZE__ <= $A000, lderror, "Bank worker template overlaps baseline"
.assert __EXTRACODE_RUN__ >= HUD_BUFFER+40, lderror, "Extra code overlaps HUD scratch"
.assert __EXTRACODE_RUN__+__EXTRACODE_SIZE__ <= $0F00, lderror, "Extra code overlaps disk state"
.assert __PASSCODE_RUN__ >= STATE+29, lderror, "Checkpoint codec overlaps game state"
.assert __PASSCODE_RUN__+__PASSCODE_SIZE__ <= EVENT_LOG, lderror, "Checkpoint codec overlaps event log"
.assert __PASSUI_RUN__ >= DISK_BUFFER+$100, lderror, "Checkpoint UI overlaps disk buffer"
.assert __PASSUI_RUN__+__PASSUI_SIZE__ <= $2000, lderror, "Checkpoint UI overlaps graphics page 1"
.assert __PASSTAIL_RUN__ > code_crc_hi, lderror, "Checkpoint code overlaps scratch"
.assert __PASSTAIL_RUN__+__PASSTAIL_SIZE__ <= WORLD, lderror, "Checkpoint code overlaps WORLD"

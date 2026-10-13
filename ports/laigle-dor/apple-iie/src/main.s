.setcpu "6502"
.include "memory.inc"
.segment "CODE"
.export entry, main_loop, frame_complete
entry:
    sei
    cld
    lda #0
    sta $C000              ; 80STORE off before taking ownership of RAM
    sta $C002              ; main reads
    sta $C004              ; main writes before game_reset touches state
    sta $C008              ; main zero page/stack before installing our stack
    ldx #$FF
    txs
    jsr game_reset
    jsr video_init
    jsr draw_scene
    jsr present_frame
main_loop:
    jsr keyboard_poll
    jsr game_tick
    jsr draw_scene
    jsr present_frame
frame_complete:
    jmp main_loop
.include "game/core.s"
.include "apple/input.s"
.include "apple/audio.s"
.if DHGR
.include "apple/dhgr.s"
.else
.include "apple/graphics.s"
.endif
.include "apple/hud.s"
.if DHGR
.include "apple/dhgr-hud.s"
.endif
.export code_end
code_end:
.segment "RODATA"
.export room12_grid, sprite_lo, sprite_hi, frame_lo, frame_hi, row_lo, row_hi
.include "generated.inc"

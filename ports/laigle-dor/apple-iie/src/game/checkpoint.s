; Resident checkpoint adapter. Disk track 34 supplies a temporary MAIN $A000
; module while TEXT is shown. Never rebuild the baseline with an overlay
; return address still on the stack: close/apply tail-jump to resident code.
.segment "CODE"
.export full_code_key, full_code_encode, full_code_decode, full_code_crc
.export full_code_draw, full_code_close, checkpoint_load
.export code_fields,code_packet,code_ascii,checkpoint_count,code_error,code_return_mode
.export full_text_address, full_hud_string, debug_teleport, reset_torch_life, reset_bar_life
full_code_key:
    lda game_mode
    cmp #MODE_CODE_SAVE
    beq @save
    cmp #MODE_CODE_LOAD
    beq @load
    cmp #MODE_PLAY
    bne @exterior
    lda raw_key
    cmp #'C'
    bne @ordinary
    lda #MODE_CODE_SAVE
    jsr @open
    jsr full_code_encode
    bcs @range
    lda #24
    sta checkpoint_count
    bne @consume
@range:
    lda #5
    sta code_error
    bne @consume
@exterior:
    cmp #MODE_EXTERIOR
    bne @ordinary
    lda raw_key
    cmp #'4'
    bne @ordinary
    lda #MODE_CODE_LOAD
    jsr @open
    sec
    rts
@open:
    ldx game_mode
    stx code_return_mode
    sta game_mode
    lda #0
    sta code_error
    sta checkpoint_count
    jmp checkpoint_load
@save:
    lda raw_key
    cmp #32
    beq full_code_close
    cmp #13
    beq full_code_close
@load:
    lda raw_key
    cmp #27
    beq full_code_close
    cmp #'H'
    beq @ordinary
    cmp #'?'
    beq @ordinary
    lda game_mode
    cmp #MODE_CODE_LOAD
    bne @consume
    jmp $A000               ; key module returns straight to full_ui_key
@consume:
    sec
    rts
@ordinary:
    clc
    rts

full_code_close:
    lda code_return_mode
    sta game_mode
    bne @done
    ; Recreate the discarded baseline before the next hidden-page draw.
    ; A falling grille's latched side is controller state, not fresh geometry.
    lda gate_side
    pha
    jsr world_load_scene
    pla
    sta gate_side
@done:
    lda #1
    sta ui_skip_clock
    sec
    rts

checkpoint_load:
    lda #34                 ; physical sectors 544..559, final disk track
    sta disk_wanted_track
    lda #0
    sta disk_wanted_sector
    sta asset_aux
    sta dirty_valid
    sta dirty_valid+1
    lda #$A0
    sta asset_page
    lda #16
    sta asset_pages
    jmp asset_load_range

; Stable entry vectors shared with the independently linked module.
full_code_draw:   jmp $A003
full_code_encode: jmp $A006
full_code_decode: jmp $A009
full_code_crc:    jmp $A00C

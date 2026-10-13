; One startup preload of the shared atlas. No disk access on room changes.
; Exact private 16-sector slot-6 BOOT0 ABI; same pinned firmware as boot.s.
.import __ASSETS_SIZE__
.export asset_load
asset_load:
    lda game_mode
    cmp #MODE_TITLE
    beq :+
    bit $C051
:
    lda #$60
    sta asset_page
    lda #<((__ASSETS_SIZE__+$FF)/$100)
    sta asset_pages
    lda #6
    sta disk_wanted_track
    lda #0
    sta disk_wanted_sector
    lda #1
    sta asset_aux
    jmp asset_load_range
title_load:
    bit $C051
    lda #$A0
    sta asset_page
    lda #32
    sta asset_pages
    lda #10
    sta disk_wanted_track
    lda #0
    sta disk_wanted_sector
    sta asset_aux
    jsr asset_load_range
    lda #$A0
    sta asset_page
    lda #32
    sta asset_pages
    lda #1
    sta asset_aux
    jmp asset_load_range
asset_load_range:
    lda $C0EA
    lda $C0E9
asset_next_page:
    jsr asset_seek
    ldx #3
@save:
    lda $0800,x
    sta disk_return_saved,x
    dex
    bpl @save
    lda #$4C
    sta $0801
    lda #<asset_return
    sta $0802
    lda #>asset_return
    sta $0803
    lda #<DISK_BUFFER
    sta $26
    lda #>DISK_BUFFER
    sta $27
    lda disk_wanted_track
    sta $41
    lda disk_wanted_sector
    sta $3D
    clc
    adc #1
    sta $0800
    ldx #$60
    clc
    jmp $C65C
asset_return:
    ldx #3
@restore:
    lda disk_return_saved,x
    sta $0800,x
    dex
    bpl @restore
    ; BOOT0 owns $40/$41; reinstall the safe auxiliary-read workers.
    ldx #<(__AUXREAD_SIZE__-1)
@workers:
    lda __AUXREAD_LOAD__,x
    sta __AUXREAD_RUN__,x
    dex
    bpl @workers
    lda #0
    sta copy_ptr
    lda asset_page
    sta copy_ptr+1
    ldy #0
    lda asset_aux
    beq :+
    sta $C005
:
@copy:
    lda DISK_BUFFER,y
    sta (copy_ptr),y
    iny
    bne @copy
    sta $C004
    inc asset_page
    inc disk_wanted_sector
    lda disk_wanted_sector
    cmp #16
    bne :+
    lda #0
    sta disk_wanted_sector
    inc disk_wanted_track
:
    dec asset_pages
    jne asset_next_page
    lda $C0E8
    rts

asset_seek:
    lda disk_tracks
    cmp disk_wanted_track
    beq @done
    lda #2
    sta disk_step
    lda disk_tracks
    cmp disk_wanted_track
    bcc @half
    lda #$FE
    sta disk_step
@half:
    jsr asset_step_half
    jsr asset_step_half
    lda disk_step
    bmi @inward
    inc disk_tracks
    jmp asset_seek
@inward:
    dec disk_tracks
    jmp asset_seek
@done:
    rts
asset_step_half:
    lda disk_phases
    clc
    adc disk_step
    and #6
    tax
    lda $C0E1,x
    ldx disk_phases
    lda $C0E0,x
    lda disk_phases
    clc
    adc disk_step
    and #6
    sta disk_phases
    ldx #24
@wait:
    ldy #0
@inner:
    dey
    bne @inner
    dex
    bne @wait
    rts
asset_page = $0F20
asset_pages = $0F21
disk_step = $0F22
asset_aux = $0F23

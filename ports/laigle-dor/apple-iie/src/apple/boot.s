; Original project boot sector, ca65/NMOS. Disk II 16-sector controller, slot 6.
; BOOT0 reads sector 0 to $0800, then JMP $0801. We call its private reader
; at $C65C with $26/27=destination, $3D=sector, $41=track, X=$60, C clear.
; Reader increments destination and sector, then returns via JMP $0801.
; Assumes exact 16-sector BOOT0 contract pinned in tools/dependencies.json.
.setcpu "6502"
.segment "BOOT"
    .byte 1
.export boot_entry
boot_entry:
    sei
    cld
    lda started
    bne next_track
    inc started
    lda #0
    sta $26
    sta $41
    lda #$60
    sta $27
    lda #1
    sta $3D                 ; T0/S0 holds this loader, payload starts T0/S1
    jmp read_track
next_track:
    lda $27
    cmp #APP_END_PAGE
    bcs loaded
    inc $41
    jsr step_half
    jsr step_half
    lda #0
    sta $3D
read_track:
    ; Number of sectors BOOT0 should read on this track, exclusive upper bound.
    lda #APP_END_PAGE
    sec
    sbc $27
    clc
    adc $3D
    cmp #16
    bcc :+
    lda #16
:
    sta $0800
    ldx #$60
    clc
    jmp $C65C
loaded:
    lda $C0E8               ; stop drive motor; application never needs disk IRQ
    jmp $6000
step_half:
    lda phase
    clc
    adc #2
    and #6
    tax
    lda $C0E1,x             ; energize next adjacent coil
    ldx phase
    lda $C0E0,x             ; release previous coil
    lda phase
    clc
    adc #2
    and #6
    sta phase
    ldx #24                 ; conservative software settle; not measured hardware
@wait:
    ldy #0
@inner:
    dey
    bne @inner
    dex
    bne @wait
    rts
started: .byte 0
phase: .byte 0
    .res $100-(*-boot_entry+1),0

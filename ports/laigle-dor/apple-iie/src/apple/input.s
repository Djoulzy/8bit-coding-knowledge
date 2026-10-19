; Apple IIe KBD=$C000, KBDSTRB=$C010. One pending character consumed per tick.
.export keyboard_poll
keyboard_poll:
    lda #$FF
    sta key_action
.if FULL_GAME
    sta raw_key
.endif
    lda $C000
    bpl @done
    and #$7F
    bit $C010
.if FULL_GAME
    ldx game_mode
    cpx #MODE_NAME
    bne :+
    sta raw_key            ; preserve typed case in names, normalize commands only
    rts
:
.endif
    cmp #$61
    bcc :+
    cmp #$7B
    bcs :+
    and #$DF
:
.if FULL_GAME
    sta raw_key
    ldx game_mode
    cpx #MODE_HELP
    beq @done
    cpx #MODE_INTRO
    beq @done
    cpx #MODE_DEBUG
    bcs @done                ; hidden menu and its two map pages
.endif
    ldx #0
@find:
    cmp key_codes,x
    beq @matched
    inx
    cpx #12
    bne @find
    cmp #'R'
    bne @done
    jmp game_reset          ; prototype-only reset
@matched:
    lda key_actions,x
    sta key_action
@done:
    rts
key_codes: .byte $08,$15,$0A,$0B,'J','K','N','U',' ', 'A', $0D, $1B
key_actions: .byte 2,1,0,3,2,1,0,3,4,5,4,4

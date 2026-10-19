; Modal help consumes its opening/closing key and freezes controller time.
; No Apple hardware access; all underlying game/action state is retained.
.segment "LOWCODE"
; Explicit T reports failure. The automatic attempt at the top of a vertical
; jump still calls full_light directly and may harmlessly find no fixture.
full_request_light:
    jsr full_light
    lda message_id
    cmp #6
    beq @done
    jmp full_denied
@done:
    rts

full_ui_key:
    jsr full_code_key
    bcs @consume
    jsr full_debug_key
    bcc :+
    rts
:
    lda game_mode
    cmp #MODE_HELP
    bne @request
    lda raw_key
    cmp #$FF
    beq @consume
    lda help_return_mode
    sta game_mode
    lda #1
    sta ui_skip_clock
    bne @consume
@request:
    lda raw_key
    cmp #'?'
    beq @open
    cmp #'H'
    bne @intro
    lda game_mode
    cmp #MODE_NAME          ; H remains a name character; ? opens help here
    beq @ordinary
@open:
    lda game_mode
    sta help_return_mode
    lda #MODE_HELP
    sta game_mode
@consume:
    sec
    rts
@intro:
    lda game_mode
    cmp #MODE_INTRO
    bne @ordinary
    lda raw_key
    cmp #$FF
    beq @consume
    lda #MODE_NAME
    sta game_mode
    sec
    rts
@ordinary:
    clc
    rts
.segment "CODE"

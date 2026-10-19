; New port interface: compact room/inventory checkpoint, not a savestate.
; Payload: 54 meaningful bits + two zero padding bits, then CRC-16.
.segment "CODE"
.export full_code_key, full_code_encode, full_code_decode, full_code_crc
.export code_fields,code_packet,code_ascii,checkpoint_count,code_error,code_return_mode
full_code_key:
    lda game_mode
    cmp #MODE_CODE_SAVE
    beq @save_keys
    cmp #MODE_CODE_LOAD
    beq @load_keys
    cmp #MODE_PLAY
    bne @exterior
    lda raw_key
    cmp #'C'
    bne @ordinary
    lda #MODE_CODE_SAVE
    jsr @open
    jsr full_code_encode
    lda #18
    sta checkpoint_count
    sec
    rts
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
    rts
@save_keys:
    lda raw_key
    cmp #32
    beq @close
    cmp #13
    beq @close
    cmp #27
    beq @close
@load_keys:
    lda raw_key
    cmp #'H'
    beq @ordinary
    cmp #'?'
    beq @ordinary
    lda game_mode
    cmp #MODE_CODE_LOAD
    bne @consume
    jsr full_code_edit
@consume:
    sec
    rts
@ordinary:
    clc
    rts
@close:
    jmp full_code_close
.segment "PASSTAIL"
full_code_close:
    lda code_return_mode
    sta game_mode
    lda #1
    sta ui_skip_clock
    sec
    rts

full_code_encode:
    lda #1
    sta code_fields
    lda current_room
    sta code_fields+1
    lda held_item
    ldx action_kind
    cpx #3
    bne :+
    lda saved_item           ; jump animation temporarily hides its held item
:
    ldx #5
@slot:
    cmp item_codes,x
    beq @found
    dex
    bne @slot
@found:
    stx code_fields+2
    ldx #6
@inventory:
    lda vials,x
    sta code_fields+3,x
    dex
    bpl @inventory
    lda #0
    sta code_fields+10
    jsr full_code_pack
    jsr full_code_crc
    lda code_crc_hi
    sta code_packet+7
    lda code_crc_lo
    sta code_packet+8
    ldx #0
    ldy #0
@hex:
    lda code_packet,x
    lsr a
    lsr a
    lsr a
    lsr a
    jsr full_code_hex_digit
    lda code_packet,x
    and #15
    jsr full_code_hex_digit
    inx
    cpx #9
    bne @hex
    rts
.segment "PASSUI"
full_code_hex_digit:
    cmp #10
    bcc :+
    adc #6                  ; carry set: add 7, then ASCII '0'
:
    clc
    adc #'0'
    sta code_ascii,y
    iny
    rts

; CRC-16/CCITT-FALSE: init $FFFF, polynomial $1021, no reflection/xorout.
.segment "PASSCODE"
full_code_crc:
    lda #$FF
    sta code_crc_lo
    sta code_crc_hi
    ldx #0
@byte:
    lda code_packet,x
    eor code_crc_hi
    sta code_crc_hi
    ldy #8
@bit:
    asl code_crc_lo
    rol code_crc_hi
    bcc :+
    lda code_crc_hi
    eor #$10
    sta code_crc_hi
    lda code_crc_lo
    eor #$21
    sta code_crc_lo
:
    dey
    bne @bit
    inx
    cpx #7
    bne @byte
    rts

; Decode into scratch first: callers commit only after every check passes.
.segment "CODE"
full_code_decode:
    ldx #0
    ldy #0
@byte:
    jsr full_code_nibble
    bcs @invalid
    asl a
    asl a
    asl a
    asl a
    sta code_value
    jsr full_code_nibble
    bcs @invalid
    ora code_value
    sta code_packet,x
    inx
    cpx #9
    bne @byte
    jsr full_code_crc
    lda code_crc_hi
    cmp code_packet+7
    bne @invalid
    lda code_crc_lo
    cmp code_packet+8
    bne @invalid
    jsr full_code_unpack
    lda code_fields
    cmp #1
    bne @invalid
    lda code_fields+10
    bne @invalid
    ldy code_fields+2
    cpy #6
    bcs @invalid
    tya
    beq @valid
    ldx code_owner_field,y
    lda code_fields,x
    and code_owner_mask,y
    beq @invalid
@valid:
    clc
    rts
@invalid:
    sec
    rts
full_code_nibble:
    lda code_ascii,y
    iny
    cmp #'0'
    bcc @invalid
    cmp #'9'+1
    bcc @digit
    cmp #'A'
    bcc @invalid
    cmp #'F'+1
    bcs @invalid
    sbc #6                  ; carry clear from CMP 'F'+1: subtract 7
@digit:
    sec
    sbc #'0'
    clc
    rts
@invalid:
    sec
    rts
.segment "PASSTAIL"
code_owner_field: .byte 0,4,7,7,3,6
code_owner_mask: .byte $FF,$FF,1,2,$FF,$FF

.segment "CODE"
full_code_apply:
    ; Keep the newly typed name; all excluded state starts as a fresh game.
    ldx #5
@name:
    lda player_name,x
    sta code_name,x
    dex
    bpl @name
    lda name_count
    sta code_name_count
    dec session_attempt     ; reset initializes this same attempt, not a new one
    jsr game_reset
    ldx #6
@inventory:
    lda code_fields+3,x
    sta vials,x
    dex
    bpl @inventory
    ldx code_fields+2
    lda item_codes,x
    sta held_item
    lda torches
    beq :+
    jsr reset_torch_life
:
    lda crowbars
    beq :+
    jsr reset_bar_life
:
    ldx #5
@restore:
    lda code_name,x
    sta player_name,x
    dex
    bpl @restore
    lda code_name_count
    sta name_count
    lda code_fields+1
    jmp debug_teleport      ; shared safe-floor spawn and hidden-page preparation

.segment "PASSCODE"
full_code_pack:
    lda #0
    sta code_byte
    sta code_bits
    ldx #8
@clear:
    sta code_packet,x
    dex
    bpl @clear
    ldy #0
@field:
    lda code_fields,y
    sta code_value
    lda code_width,y
    sta code_remaining
    lda #8
    sec
    sbc code_remaining
    tax
    beq @bit
@align:
    asl code_value
    dex
    bne @align
@bit:
    asl code_value
    ldx code_byte
    rol code_packet,x
    inc code_bits
    lda code_bits
    and #7
    bne :+
    inc code_byte
:
    dec code_remaining
    bne @bit
    iny
    cpy #11
    bne @field
    rts
full_code_unpack:
    lda #0
    sta code_byte
    sta code_bits
    ldy #0
@field:
    lda #0
    sta code_fields,y
    lda code_width,y
    sta code_remaining
@bit:
    ldx code_byte
    asl code_packet,x
    lda code_fields,y
    rol a
    sta code_fields,y
    inc code_bits
    lda code_bits
    and #7
    bne :+
    inc code_byte
:
    dec code_remaining
    bne @bit
    iny
    cpy #11
    bne @field
    rts
code_width: .byte 3,6,3,8,8,8,8,4,3,3,2
.segment "CODE"

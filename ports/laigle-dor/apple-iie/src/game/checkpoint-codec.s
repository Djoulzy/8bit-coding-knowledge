; V2: 64 bits of inventory/room/economy/strength + 16 pickup flags + CRC-16.
; Fields use a byte-wise MSB-first codec. Wide integers are split high first.
.segment "CHECKPOINT"
full_code_encode:
    ldx #3
@stocks:
    lda vials,x
    cmp #8
    jcs @invalid             ; never silently truncate a real stock
    sta code_fields,x
    dex
    bpl @stocks
    lda possessions
    cmp #16
    jcs @invalid
    sta code_fields+4
    lda objectives
    cmp #8
    jcs @invalid
    sta code_fields+5
    lda scrolls
    cmp #8
    jcs @invalid
    sta code_fields+6
    lda current_room
    cmp #64
    jcs @invalid
    sta code_fields+7
    lda gold+1
    sta code_fields+8
    lda gold
    sta code_fields+9
    lda points+1
    cmp #16
    jcs @invalid
    sta code_fields+10
    lda points
    sta code_fields+11
    lda energy
    sta word_tmp
    lda energy+1
    sta word_tmp+1
    cmp #$27
    bcc @percent
    jne @invalid
    lda energy
    cmp #$11
    jcs @invalid             ; valid strength is 0..10000 hundredths
@percent:
    lda #0
    sta code_fields+12
@divide:
    lda word_tmp
    sec
    sbc #100
    tax
    lda word_tmp+1
    sbc #0
    bcc @tag
    sta word_tmp+1
    stx word_tmp
    inc code_fields+12
    bne @divide
@tag:
    lda code_fields+12
    ora #$80                 ; high bit is the v2 format marker
    sta code_fields+12
    lda #0
    sta code_fields+13
    sta code_fields+14
    ldy #15
@pickup:
    lda checkpoint_rooms,y
    asl a
    asl a
    tax
    lda WORLD+$100,x
    and #$38
    beq @picked
    clc
    bcc @roll
@picked:
    sec
@roll:
    rol code_fields+14
    rol code_fields+13
    dey
    bpl @pickup
    jsr full_code_pack
    jsr full_code_crc
    lda code_crc_hi
    sta code_packet+10
    lda code_crc_lo
    sta code_packet+11
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
    cpx #12
    bne @hex
    clc
    rts
@invalid:
    sec
    rts
full_code_hex_digit:
    cmp #10
    bcc :+
    adc #6
:
    clc
    adc #'0'
    sta code_ascii,y
    iny
    rts

; Decode only into scratch. No game/world writes until every check succeeds.
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
    cpx #12
    bne @byte
    jsr full_code_crc
    lda code_crc_hi
    cmp code_packet+10
    bne @invalid
    lda code_crc_lo
    cmp code_packet+11
    bne @invalid
    jsr full_code_unpack
    lda code_fields+12
    bpl @invalid             ; marker must be set
    and #$7F
    cmp #101
    bcs @invalid
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
    sbc #6
@digit:
    sec
    sbc #'0'
    clc
    rts
@invalid:
    sec
    rts

full_code_apply:
    ; Keep the newly typed name, never the old session's name or held item.
    ldx #5
@name:
    lda player_name,x
    sta code_name,x
    dex
    bpl @name
    lda name_count
    sta code_name_count
    dec session_attempt
    jsr game_reset           ; resets WORLD and excluded controller state
    ldx #3
@stocks:
    lda code_fields,x
    sta vials,x
    dex
    bpl @stocks
    lda code_fields+4
    sta possessions
    lda code_fields+5
    sta objectives
    lda code_fields+6
    sta scrolls
    lda code_fields+8
    sta gold+1
    lda code_fields+9
    sta gold
    lda code_fields+10
    sta points+1
    lda code_fields+11
    sta points
    lda #0
    sta energy
    sta energy+1
    lda code_fields+12
    and #$7F
    tax
    beq @pickups
@strength:
    lda energy
    clc
    adc #100
    sta energy
    lda energy+1
    adc #0
    sta energy+1
    dex
    bne @strength
@pickups:
    ldy #0
@removed:
    lsr code_fields+13
    ror code_fields+14
    bcc @next
    lda checkpoint_rooms,y
    asl a
    asl a
    tax
    lda WORLD+$100,x
    and #$C7                 ; remove treasure only; furniture/hazards survive
    sta WORLD+$100,x
@next:
    iny
    cpy #16
    bne @removed
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
    lda code_fields+7
    ; This MUST be a tail jump: debug_teleport replaces our executing $A000
    ; module with the new room baseline, then returns to the resident UI.
    jmp debug_teleport

; CRC-16/CCITT-FALSE: init $FFFF, polynomial $1021, unreflected, xorout zero.
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
    cpx #10
    bne @byte
    rts

full_code_pack:
    lda #0
    sta code_byte
    sta code_bits
    ldx #11
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
    cpy #15
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
    cpy #15
    bne @field
    rts
code_width: .byte 3,3,3,3,4,3,3,6,8,8,4,8,8,8,8
checkpoint_rooms: .incbin "checkpoint-rooms.bin"

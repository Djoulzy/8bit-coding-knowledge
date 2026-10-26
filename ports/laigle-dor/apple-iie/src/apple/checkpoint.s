; Hidden-page Apple TEXT adapter, part of the temporary checkpoint module.
.segment "CHECKPOINT"
full_code_edit:
    lda raw_key
    cmp #$FF
    beq @done
    cmp #13
    beq @enter
    cmp #8
    beq @erase
    cmp #' '
    beq @done
    cmp #'-'
    beq @done
    cmp #'0'
    bcc @bad
    cmp #'9'+1
    bcc @accept
    cmp #'A'
    bcc @bad
    cmp #'F'+1
    bcs @bad
@accept:
    ldx code_error
    cpx #3
    bcs @done
    ldx checkpoint_count
    cpx #24
    beq @long
    sta code_ascii,x
    inc checkpoint_count
    lda #0
    sta code_error
@done:
    sec                     ; consume the key, including an idle frame
    rts
@bad:
    lda #3
    bne @error
@long:
    lda #4
    bne @error
@erase:
    ldx checkpoint_count
    beq :+
    dec checkpoint_count
:
    lda #0
    sta code_error
    rts
@enter:
    lda code_error
    cmp #3
    bcc :+
    cmp #5
    bcc @done              ; invalid/overflow input must be edited first
:
    lda checkpoint_count
    cmp #24
    bne @short
    jsr full_code_decode
    bcs @invalid
    jmp full_code_apply
@short:
    cmp #18
    bne :+
    lda #6                  ; distinguish the replaced v1 protocol
    bne @error
:
    lda #1
    bne @error
@invalid:
    lda #2
@error:
    sta code_error
    sec
    rts

full_code_draw:
    lda #9
    jsr full_text_address
    ldx #0
    ldy #6
@char:
    cpx checkpoint_count
    beq @status
    lda code_ascii,x
    ora #$80
    sta (dst_ptr),y
    iny
    inx
    cpx #6
    beq @gap
    cpx #12
    beq @gap
    cpx #18
    bne @char
@gap:
    iny
    bne @char
@status:
    lda code_error
    beq @done
    lda #13
    jsr full_text_address
    ldx code_error
    dex
    lda code_error_lo,x
    sta menu_ptr
    lda code_error_hi,x
    sta menu_ptr+1
    ldy #3
    jmp full_hud_string
@done:
    rts
code_invalid: .asciiz "Code invalide. Corrigez la saisie."
code_range: .asciiz "Stock >7 / score >4095 / force >100."
code_legacy: .asciiz "Code a 18 caracteres incompatible."
code_error_lo: .lobytes code_invalid,code_invalid,code_invalid,code_invalid,code_range,code_legacy
code_error_hi: .hibytes code_invalid,code_invalid,code_invalid,code_invalid,code_range,code_legacy

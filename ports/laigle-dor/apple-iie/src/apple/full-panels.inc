; AUX script: row, column, zero-terminated text; $FF ends the page.
; MAIN code/stack and the established ZP AUX-read worker remain resident.
full_panel_draw:
@row:
    jsr full_panel_get
    cmp #$FF
    beq full_panel_dynamic
    jsr full_text_address
    jsr full_panel_get
    sta panel_column
@char:
    jsr full_panel_get
    beq @row
    ora #$80
    ldy panel_column
    sta (dst_ptr),y
    inc panel_column
    jmp @char
full_panel_get:
    ldy #0
    jsr aux_read_src
    inc src_ptr
    bne :+
    inc src_ptr+1
:
    cmp #0                 ; callers test the byte, not the pointer INC flags
    rts

full_panel_dynamic:
    lda game_mode
    cmp #MODE_DEAD
    bcc :+
    cmp #MODE_NAME
    bcs :+
    lda #4
    jsr full_text_address
    lda gold
    sta word_tmp
    lda gold+1
    sta word_tmp+1
    ldy #28
    jmp full_decimal5
:
    cmp #MODE_CODE_SAVE
    jcs full_code_draw
    cmp #MODE_DEBUG
    jeq full_debug_panel
    cmp #MODE_INVENTORY
    jeq full_inventory_panel
    cmp #MODE_EXTERIOR
    bne @merchant
    lda #4
    jsr full_text_address
    ldx #0
    ldy #2
@name:
    lda player_name,x
    ora #$80
    sta (dst_ptr),y
    iny
    inx
    cpx #6
    bne @name
    dex
@trim:
    lda player_name,x
    cmp #' '
    bne @suffix
    dex
    bpl @trim
@suffix:
    txa
    clc
    adc #3
    tay
    lda #<exterior_suffix
    sta menu_ptr
    lda #>exterior_suffix
    sta menu_ptr+1
    jmp full_hud_string
@merchant:
    cmp #MODE_MERCHANT
    bne @entry
    lda #18
    jsr full_text_address
    lda gold
    sta word_tmp
    lda gold+1
    sta word_tmp+1
    ldy #16
    jsr full_decimal5
    ldy #16
    ldx #5
    jsr full_hud_trim
    lda message_id
    cmp #1
    beq @denied
    cmp #2
    bne @done
    lda #<purchase_ready
    ldx #>purchase_ready
    bne @message
@denied:
    lda #<purchase_denied
    ldx #>purchase_denied
@message:
    sta menu_ptr
    stx menu_ptr+1
    lda #21
    jsr full_text_address
    ldy #3
    jmp full_hud_string
@entry:
    cmp #MODE_NAME
    bne @done
    lda #10
    jsr full_text_address
    ldx #0
    ldy #12
@letter:
    cpx name_count
    bcs @done
    lda player_name,x
    ora #$80
    sta (dst_ptr),y
    iny
    inx
    bne @letter
@done:
    rts
exterior_suffix: .asciiz ", tu peux :"
purchase_ready: .asciiz "D'accord."
purchase_denied: .asciiz "Impossible: pas assez d'or !"
panel_column = $0F2C

; A dedicated 40-column inventory. Static labels live in the AUX script;
; quantities and possession flags are read afresh on each hidden-page draw.
; panel_column is free after the script and serves as the loop index here.
full_inventory_panel:
    lda #3
    jsr full_text_address
    ldx held_item
    beq @stocks             ; the static page says Vide for an empty hand
    lda hud_hand_lo,x
    sta menu_ptr
    lda hud_hand_hi,x
    sta menu_ptr+1
    ldy #12
    jsr full_hud_string
@stocks:
    lda #0
    sta panel_column
@stock:
    lda panel_column
    asl a
    clc
    adc #7
    jsr full_text_address
    ldx panel_column
    lda vials,x             ; contiguous vials, torches, ropes, crowbars
    ldy #17
    jsr hud_decimal3
    ldy #17
    ldx #3
    jsr full_hud_trim
    inc panel_column
    lda panel_column
    cmp #4
    bne @stock
    lda #0
    sta panel_column
@flag:
    ldx panel_column
    lda inventory_rows,x
    jsr full_text_address
    ldx panel_column
    ldy inventory_columns,x
    lda possessions
    cpx #4
    bcc @mask
    lda objectives
    eor #7                  ; objective bits are cleared when acquired
@mask:
    and inventory_masks,x
    beq @absent
    ldx #3
    bne @status
@absent:
    ldx #0                  ; three characters: non or oui
@status:
    lda inventory_status,x
    ora #$80
    sta (dst_ptr),y
    lda inventory_status+1,x
    ora #$80
    iny
    sta (dst_ptr),y
    lda inventory_status+2,x
    ora #$80
    iny
    sta (dst_ptr),y
    inc panel_column
    lda panel_column
    cmp #7
    bne @flag
    lda #19
    jsr full_text_address
    lda scrolls
    ldx #3
    ldy #0
@scroll:
    lsr a
    bcc :+
    iny
:
    dex
    bne @scroll
    tya
    ora #$B0
    ldy #36
    sta (dst_ptr),y
    rts
inventory_rows: .byte 7,9,11,13,17,17,19
inventory_columns: .byte 36,36,36,36,17,36,17
inventory_masks: .byte 1,2,4,8,1,2,4
inventory_status: .byte "nonoui"

full_debug_panel:
    lda #9
    jsr full_text_address
    ldy #19
    lda current_room
    jsr hud_decimal2
    lda #12
    jsr full_text_address
    ldx #0
    ldy #16
@digit:
    cpx debug_count
    beq @status
    lda debug_digits,x
    ora #$80
    sta (dst_ptr),y
    inx
    iny
    bne @digit
@status:
    lda debug_status
    beq @done
    cmp #1
    beq @granted
    lda #<debug_invalid
    ldx #>debug_invalid
    bne @message
@granted:
    lda #<debug_granted
    ldx #>debug_granted
@message:
    sta menu_ptr
    stx menu_ptr+1
    lda #19
    jsr full_text_address
    ldy #3
    jmp full_hud_string
@done:
    rts
; Keep constants out of CODE so its page-aligned RODATA successor leaves room
; below the $A000 terrain baseline. Both segments remain resident in MAIN.
.segment "RODATA"
debug_invalid: .asciiz "Salle invalide: 0 a 63. Corriger."
debug_granted: .asciiz "Tous les objets ajoutes."
.segment "CODE"

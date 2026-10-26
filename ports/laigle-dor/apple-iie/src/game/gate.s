; B2 5015-5018, 6300-6320. Persist the trap, show its fall, then resolve HT.
; Nine displayed stages; the last two contain the complete shared gate art.
; This is a native controller cadence, not original Oric timing emulation.
.segment "CODE"
.export full_gate_start, full_gate_tick, full_gate_crossing
full_gate_start:
    lda current_room
    asl a
    asl a
    tax
    lda WORLD+$100,x
    ora #$80
    sta WORLD+$100,x
    lda #0
    sta walking
    lda facing
    sta pose
    lda #1
    sta action_phase
    lda #ACTION_GATE
    sta action_kind
    lda #EVENT_ACTION
    jmp log_event

full_gate_tick:
    inc action_phase
    lda action_phase
    cmp #10
    bcc @done
    lda #1
    sta room_dirty
    lda #0
    sta action_kind
    sta action_phase
    sta gate_side
    lda gate_jump
    beq full_death
    lda #0
    sta gate_jump
@done:
    rts

; A jump advances by two source bytes. Even walking positions can straddle
; the odd trigger x=11/27. Latch either landing cell at/beyond the crossed plane;
; full_clock resolves that latch after the jump, even if its endpoint is farther.
full_gate_crossing:
    lda gate_side
    beq @done
    sec
    sbc actor_x
    ldx facing
    cpx #1
    bne @distance
    eor #$FF
    clc
    adc #1
@distance:
    cmp #2
    bcs @done
    lda #1
    sta gate_jump
@done:
    rts

full_death:
    lda #MODE_DEAD
    sta game_mode
    lda #0
    sta walking
    sta enemy_kind
    sta hazard_active
    sta action_kind
    lda #EVENT_END
    jmp log_event

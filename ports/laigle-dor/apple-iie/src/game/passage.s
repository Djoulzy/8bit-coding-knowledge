; B2 10907/10970 and 10405. Target approach windows retain source anchors.
; Rules only: no display or Apple I/O. Passage is transient, not a world edit.
.segment "EXTRACODE"
full_secret_reach:
    lda held_item
    cmp #8
    bne @no
    lda facing
    cmp #3
    bne @no
    lda room_fields+3
    and #1
    beq @no
    lda actor_x
    cmp #14
    bcc @no
    cmp #21
    bcs @no
    jmp full_passage_depth
@no:
    clc
    rts

full_secret_enter:
    lda key_action
    cmp #3
    bne @no
    cmp facing
    bne @no
    lda passage
    beq @no
    lda pose
    cmp #4
    bcc @no
    cmp #8
    bcs @no
    lda actor_x
    cmp #18
    bcc @no
    cmp #21
    bcs @no
    jsr full_passage_depth
    bcc @no
    jsr full_transition
    sec
    rts
@no:
    clc
    rts

full_passage_depth:
    lda actor_y
    cmp #125
    bcc @done
    cmp #146
    bcs @no
    sec
@done:
    rts
@no:
    clc
    rts
.segment "CODE"

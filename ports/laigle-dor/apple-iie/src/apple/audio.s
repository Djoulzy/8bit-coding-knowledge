; Silent event sink. Catalog in resources/audio-events.json; never touches $C030.
.export log_event
log_event:
    sta event_kind
    sta last_event
    lda event_head
    asl a
    asl a
    tax
    lda event_kind
    sta EVENT_LOG,x
    lda tick_lo
    sta EVENT_LOG+1,x
    lda tick_hi
    sta EVENT_LOG+2,x
    lda #0
    sta EVENT_LOG+3,x
    inc event_head
    lda event_head
    and #63
    sta event_head
    lda event_count
    cmp #64
    beq @overflow
    inc event_count
    rts
@overflow:
    inc event_overflow       ; modulo-256 count of overwritten records
    rts

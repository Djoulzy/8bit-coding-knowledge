; One fixed 8 KiB disk slot per ending scene. Never replace executing resident
; code: the overlay owns only the disposable MAIN $A000-$BFFF baseline.
.segment "ENDCODE"
.export full_end_draw
full_end_draw:
    ldx render_page_index
    lda map_cached,x
    cmp game_mode
    beq @done
    lda game_mode
    sta map_cached,x
    lda #22                 ; physical sector 352: victory
    ldy game_mode
    cpy #MODE_WIN
    beq @load
    lda session_attempt
    asl a
    clc
    adc #22                 ; death attempts: tracks 24,26,28,30,32
@load:
    sta disk_wanted_track
    lda #0
    sta disk_wanted_sector
    sta asset_aux
    lda #$A0
    sta asset_page
    lda #32
    sta asset_pages
    jsr asset_load_range
    jmp $A000
@done:
    rts
.segment "CODE"

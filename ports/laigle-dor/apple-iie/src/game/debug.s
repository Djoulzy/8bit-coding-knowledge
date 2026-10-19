; Apple port development aid, not part of the historical Oric rules.
; No Apple I/O: input, TEXT panel and room construction use target interfaces.
; Ctrl+D is deliberately absent from the ordinary player help page.
.export full_debug_key, debug_input, debug_count, debug_digits, debug_status
.export saved_item
full_debug_key:
    lda game_mode
    cmp #MODE_CODE_SAVE
    bcs @ordinary
    cmp #MODE_MAP_GROUND
    jcs full_map_key
    cmp #MODE_DEBUG
    beq @menu
    cmp #MODE_PLAY
    bne @ordinary
    lda raw_key
    cmp #4                   ; Ctrl+D, not the D jump command
    bne @ordinary
    lda #0
    sta debug_input
    sta debug_count
    sta debug_status
    lda #MODE_DEBUG
    sta game_mode
    bne @consume
@ordinary:
    clc
    rts
@menu:
    lda raw_key
    cmp #$1B
    beq debug_close
    cmp #4
    beq debug_close
    ldx debug_input
    jne debug_room_key
    cmp #'1'
    beq debug_grant
    cmp #'3'
    bne :+
    jmp full_map_open
:
    cmp #'2'
    bne @consume
    lda #1
    sta debug_input
    lda #0
    sta debug_count
    sta debug_status
@consume:
    sec
    rts

debug_close:
    lda #MODE_PLAY
    sta game_mode
    lda #1
    sta ui_skip_clock        ; closing key cannot advance a fall/action/service
    sec
    rts

debug_grant:
    lda #9
    sta vials
    sta torches
    sta ropes
    sta crowbars
    lda #15
    sta possessions          ; iron/gold keys, ring, lead eagle
    lda #7
    sta scrolls
    lda #0
    sta objectives           ; also own book, diamond and golden eagle
    jsr reset_torch_life
    jsr reset_bar_life
    lda #1
    sta debug_status
    sta room_dirty           ; remove now-owned quest objects from the scenery
    sec
    rts

.segment "LOWCODE"
.export full_map_open
full_map_open:
    lda #0
    sta map_cached
    sta map_cached+1
    sta dirty_valid
    sta dirty_valid+1
    lda #3
    sta terrain_pending     ; restore game baseline after either map buffer
    lda #MODE_MAP_OTHER
    ldx current_room
    cpx #9
    bcc @open
    cpx #58
    bcs @open
    lda #MODE_MAP_GROUND
@open:
    sta game_mode
    sec
    rts

full_map_key:
    lda raw_key
    cmp #4
    jeq debug_close
    cmp #$1B
    beq @menu
    cmp #32
    beq @toggle
    cmp #$0D
    beq @toggle
    cmp #'1'
    bcc @consume
    cmp #'4'
    bcs @consume
    sec
    sbc #'1'-MODE_MAP_GROUND
    bne @select
@toggle:
    lda game_mode
    clc
    adc #1
    cmp #MODE_MAP_LEGEND+1
    bcc @select
    lda #MODE_MAP_GROUND
@select:
    sta game_mode
    bne @consume
@menu:
    lda #MODE_DEBUG
    sta game_mode
@consume:
    sec
    rts

debug_room_key:
    cmp #$0D
    beq @enter
    cmp #$08
    beq @erase
    cmp #'0'
    bcc @consume
    cmp #'9'+1
    bcs @consume
    ldx debug_count
    cpx #2
    beq @invalid             ; never silently accept a truncated 3-digit room
    sta debug_digits,x
    inc debug_count
@clear:
    lda #0
    sta debug_status
@consume:
    sec
    rts
@erase:
    lda debug_count
    beq @clear
    dec debug_count
    jmp @clear
@enter:
    lda debug_status
    cmp #2
    beq @consume
    ldx debug_count
    beq @invalid
    lda debug_digits
    sec
    sbc #'0'
    dex
    beq @range
    asl a
    sta game_tmp
    asl a
    asl a
    clc
    adc game_tmp
    adc debug_digits+1
    sec
    sbc #'0'
@range:
    cmp #64
    jcc debug_teleport
@invalid:
    lda #2
    sta debug_status
    sec
    rts

.segment "CODE"
debug_teleport:
    sta current_room          ; validated before WORLD is indexed
    lda action_kind
    cmp #3
    bne :+
    lda saved_item            ; a cancelled jump must not discard the held item
    sta held_item
:
    lda #0
    ldx #16
@transient:
    sta pit_room,x            ; pit, passage, actions, chest/message, gate, enemy
    dex
    bpl @transient
    ldx #4
@contact:
    sta enemy_direction,x     ; direction/contact/life/cue/hazard_x
    dex
    bpl @contact
    sta walking
    sta walk_phase
    sta facing
    sta pose
    sta blocked
    sta object_status
    lda #19
    sta actor_x
    lda #180
    sta actor_y
    jsr world_load_scene      ; shared constructor, retaining persistent WORLD
    ldx #21                   ; semantic feet = actor_x+2 on the near floor band
@spawn:
    lda GRID,x
    beq @found
    inx
    cpx #35
    bcc @spawn
    ldx #21                   ; defensive fallback; all 64 source rooms fit
@found:
    dex
    dex
    stx actor_x
    jsr update_frame
    jmp debug_close           ; next hidden frame is prepared before flipping

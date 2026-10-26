; Temporary checkpoint module; MAIN $A000-$AFFF, loaded only for its TEXT UI.
; Resident addresses are generated after linking each edition. No ROM calls.
.setcpu "6502"
.macpack longbranch
.include "memory.inc"
.include "checkpoint-symbols.inc"
.segment "CHECKPOINT"
    jmp full_code_edit       ; $A000: consumed key (tail call)
    jmp full_code_draw       ; $A003: draw on hidden TEXT page
    jmp full_code_encode     ; $A006: capture -> 24 hex digits, C=error
    jmp full_code_decode     ; $A009: validate into scratch, C=error
    jmp full_code_crc        ; $A00C: CRC of the ten payload bytes
.include "game/checkpoint-codec.s"
.include "apple/checkpoint.s"

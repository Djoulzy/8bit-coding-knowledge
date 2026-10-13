; Standalone takeover ABI. No OS, BASIC or monitor calls after entry.
.ifndef FULL_GAME
FULL_GAME = 0
.endif
STATE = $0C00              ; outside both text pages ($0400/$0800)
actor_x = STATE
actor_y = STATE+1
facing = STATE+2
pose = STATE+3
walking = STATE+4
walk_phase = STATE+5
tick_lo = STATE+6
tick_hi = STATE+7
last_event = STATE+8
event_head = STATE+9
event_count = STATE+10
event_overflow = STATE+11
blocked = STATE+12
door_status = STATE+13
object_status = STATE+14
key_action = STATE+15
frame_id = STATE+16
display_page_hi = STATE+17
draw_page_hi = STATE+18
dirty_left = STATE+19      ; two per-page rectangles, byte-x / target pixel-y
dirty_right = STATE+21     ; exclusive right/bottom
dirty_top = STATE+23
dirty_bottom = STATE+25
dirty_valid = STATE+27
EVENT_LOG = $0D00  ; 64 four-byte records: kind, tick lo, tick hi, argument
BASELINE_HI = $A0
VIEW_TOP = 35
VIEW_HEIGHT = 160
; Private main-bank ZP $80–$AA; DHGR extends it through $B6.
; All workers may clobber A/X/Y/P.
src_ptr = $80
dst_ptr = $82
frame_ptr = $84
shift_ptr = $86
tmp = $88
run_count = $89
grid_base = $8A
col = $8B
row_y = $8C
sprite_w = $8D
sprite_h = $8E
out_w = $8F
last_mask = $90
color_phase = $90        ; reserved monochrome scratch reused by color build
first_mask = $91
spill = $92
pixel = $93
mask = $94
x_column = $95
phase = $96
layer_count = $97
layer_cursor = $98
sprite_index = $99
dx = $9A
dy = $9B
delay_count = $9C
event_kind = $9D
render_page_index = $9E
mask_spill = $9F
raw_mask = $A0
raw_pixel = $A1
repair_left = $A2
repair_right = $A3
repair_y = $A4
repair_bottom = $A5
bounds_top = $A6
bounds_bottom = $A7
hud_row = $A8
hud_ptr = $A9             ; $A9/$AA
.if DHGR
; DHGR-only scratch; game state, stack and all these pointers stay in main RAM.
dhgr_codes = $AB
cell_x = $AC
cells_left = $AD
code_count = $AE
row_stride = $AF
cell_color = $B0
serial_col = $B1
render_bank = $B2
data_cursor = $B3
origin_cell = $B4
row_color = $B5
cell_mask = $B6
HUD_BUFFER = $0E00        ; 40 bytes: compact HUD to interleaved 80-column text
.endif
EVENT_WALK = 1
EVENT_STOP = 2
EVENT_EXIT = 3
EVENT_BLOCKED = 4
.if FULL_GAME
.include "game/full-memory.inc"
.endif

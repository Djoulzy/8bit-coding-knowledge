# Compatibility ledger for W06

Source references below are original B2 BASIC line numbers or loaded addresses
in [the pinned analysis](../../../../research/analyses/laigle-dor/overview.md).
All scene reproduction is statically analyzed unless the verification report
explicitly names an executed target test.

| Source behavior / evidence | Target choice | Reason / limitation |
| --- | --- | --- |
| 607 reads M from ROM `$D000+room`; 720–725 positions furnishing 2 | M=0 until a ROM is supplied; room-12 picture at source CURSET(147,45) | Provisional data; correct source ROM and position remain unknown |
| 100/300/390 and 600–699 build room 12 using vectors and atlas images | Translate this checked room's exact field-selected branches to a cached monochrome scene | Bresenham line rasterization is proposed, not a proof of Oric ROM rasterization; compare a runtime image |
| 690 uses color attributes and a colored paper band | Discard serial ink/paper state and crop the cleared header; native bitmap pixels/masks | Requested Apple adaptation: no Oric color-clash simulation, color-dependent geometry or opaque attribute-cell erasure |
| Oric graphic data have `(byte AND $60) != 0`; bits `$20` through `$01` left to right | Repack bitmap shape including `$22` in sprite 48; make attribute cells transparent; row-span silhouette masks | Target opacity comes from pixels, not attribute-color cells; black interior pixels can still occlude terrain |
| `$3EBD` takes a ROM byte cursor; `$3E52` copies offsets width..1 | First room atlas column is `(CURSET_x div 6 + 1)*6` | Source-byte anchor; vector endpoint rasterization still unverified |
| `$3EF8/$3E21/$3E52` actor draw | First pixel x is `(actor_x + signed_dx + 1)*6` | Retain actor-byte coordinates; add 20 target pixels as horizontal margin |
| Room 12 has 200 graphics rows; B2 690 clears rows 0–34 | Map source 35–199 to target 0–159, last row wins; native text rows 20–23 below | Crop only the known cleared header, preserve the floor/feet; general rooms/intro may need a different viewport |
| Historical restore slots F3/F4/F5 and descriptor mutation | Alternate HGR pages and paired text pages; repair the hidden page's previous actor rectangle from `$A000` | Both pages carry their own old bounds; completed graphics/HUD are selected at fresh vertical blank; third baseline costs 8 KiB |
| 5030 continues AC=1 when KEY$ is empty | Keep walking until stop, collision or portal | Release alone does not stop; compare actual keyboard repeat later |
| 5020 runs a second `$16`-linked motion phase through 4910, bypassing the 4900 collision precheck | One translated motion phase and one bounded precheck per target iteration; input polled each phase | Explicit cadence/input-boundary difference; timing and hazard interleaving need the original runtime trace |
| Each of the two walking phases has its own `$00,dx,dy` | Move 2 source bytes horizontally or 10 source rows vertically on **both** phases | Extracted deltas verified; half-step timing is not assumed to equal one source BASIC loop |
| `$4CB6` maps y=140 to row 2, y=160 to row 1, otherwise row 0; down probe subtracts 40 | Out-of-grid probe cells are virtual empty cells inside independently bounded actor coordinates | If called at y=150/170, the source pointer can address `$03xx` instead of grid RAM; normal second phase bypasses precheck. ROM/IO trace needed before interpreting this as normal gameplay |
| Bounds/data-dependent flags in `$4B82/$4B75` | Named blocked/door/object results; guard x/y range and never read Oric I/O | W06 room has no treasure marker; `$A0`/full-game and other geometries require W07 comparison |
| 4920/4700 transition through status 3 | Log EXIT_REQUEST and retain room 12 at right portal | Deliberate first-milestone boundary; room-12 right link decodes destination 11, arrival 1 |
| Oric right arrow `$09` | Apple right `$15`; other arrow directions `$08/$0A/$0B` | Machine keyboard encoding differs; J/K/N/U added for accessibility |
| Mostly uppercase comparisons | Normalize lower case, add R/Return/Escape conveniences | New prototype controls; no claim these are original gameplay bindings |
| `>` points to missing line 21827; ordinary unknown keys default to 21845 | Ignore unsupported bindings safely | The anomaly is not implemented as a new mechanic; retain source evidence |
| MUSIC/SOUND/PLAY and RNG calls occur during controller/effects | Record walk/stop cue parameters, no speaker; tick stamps in RAM | Actual source event counts, effect RNG consumption, pitch and latency unverified |
| Oric BASIC uses floating-point numbers and ROM RND | Host `Fraction` plus explicitly supplied `RandomTape` values; lock predicate evaluates its random operand eagerly | Exact rational predicate oracle, not Oric floating-point or PRNG emulation; evaluator/effect call order needs a source trace; not used by the small Apple controller yet |

The host rule oracle covers ordinary treasure, merchant boundaries, ordinary
locks/crowbar wear, finished-vial effects, pit loss, quest prerequisites,
per-game reset and victory predicate. Chest direct-handler quirks, staged drink,
ropes, traps/enemies, lighting, complete replay history and controller RNG order
remain outside its current scope. Do not treat passing isolated predicates as
a completed W03 source-runtime comparison.

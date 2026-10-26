"""Separate native-world checks; do not mix their evidence with W06 graphics."""
import sys
import argparse
import time
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT,write_json,digest


FEEDBACK_TESTS = (
    'test_chest_feedback_distinguishes_range_closed_empty_and_already_open',
    'test_crowbar_feedback_distinguishes_lock_random_failure_and_breakage',
    'test_pickup_names_real_chest_contents_and_retains_single_award',
    'test_outcome_words_are_inverse_right_aligned_on_both_pages_and_in_darkness',
    'test_impossible_actions_persist_until_next_command',
    'test_impossible_feedback_in_special_rooms_and_darkness',
    'test_light_feedback_distinguishes_request_from_automatic_attempt',
    'test_gameplay_hud_original_room_descriptions',
    'test_gameplay_hud_stats_and_hand_names',
    'test_name_exterior_merchant_and_resume',
    'test_help_pauses_walking_and_staged_actions',
    'test_room_change_keeps_graphics_until_hidden_pair_is_complete',
    'test_lighting_does_not_leave_an_unanimated_fixture',
    'test_clues_display_original_content_and_advance',
)
INTERACTION_TESTS = (
    'test_boot_preloads_shared_atlas_and_keeps_program_main',
    'test_secret_passages_open_and_traverse_all_source_links',
    'test_secret_passage_guards_and_original_anchor',
) + FEEDBACK_TESTS + (
    'test_all_64_rooms_use_the_same_constructor_and_grid',
    'test_transition_uses_original_link_and_arrival_bits',
)
HAZARD_TESTS = (
    'test_compact_clue_rows_blank_fullwidth_and_page_carry',
    'test_room36_grille_falls_on_both_pages_before_death_and_pauses_with_help',
    'test_jumps_latch_both_grille_sides_and_parities_until_the_fall_finishes',
    'test_dark_rooms_keep_lit_hud_rows_and_center_only_the_darkness_message',
    'test_darkness_panel_replaces_merchant_and_defers_graphics_preparation',
    'test_help_in_darkness_and_during_oubliette_recovery',
) + FEEDBACK_TESTS
PIT_TESTS = (
    'test_boot_preloads_shared_atlas_and_keeps_program_main',
    'test_alternate_hint_glyphs_render_captured_bytes_on_both_pages',
    'test_floor_hints_keep_source_anchors_and_ring_hides_only_unopened_hints',
    'test_room55_and_implicit_variants_show_floor_hints_on_both_buffers',
    'test_pit_walk_probes_fit_the_drawn_floor_and_never_use_room_portals',
    'test_pit_horizontal_jumps_require_a_landing_inside_the_floor',
    'test_room36_marker_and_pit_walk_routes_are_visible_without_wall_escape',
    'test_room23_trap_recovery_rope_and_return',
    'test_help_in_darkness_and_during_oubliette_recovery',
    'test_half_steps_and_continuous_depth_bands',
    'test_portals_require_approaching_the_visible_door',
    'test_room36_grille_falls_on_both_pages_before_death_and_pauses_with_help',
    'test_chest_and_quest_remain_reachable_with_reduced_clearance',
    'test_pickup_names_real_chest_contents_and_retains_single_award',
)
PRESENTATION_TESTS = (
    'test_boot_preloads_shared_atlas_and_keeps_program_main',
    'test_inventory_spaced_layout_live_values_and_modal_return',
    'test_lowercase_name_text_codes_and_preview_inverse',
    'test_name_exterior_merchant_and_resume',
    'test_gameplay_hud_original_room_descriptions',
    'test_gameplay_hud_stats_and_hand_names',
    'test_impossible_actions_persist_until_next_command',
    'test_impossible_feedback_in_special_rooms_and_darkness',
    'test_help_pauses_walking_and_staged_actions',
    'test_help_returns_to_each_modal_page_and_name_input',
    'test_clues_display_original_content_and_advance',
    'test_title_lightning_reveal_and_text_transition',
    'test_debug_menu_is_hidden_modal_and_freezes_gameplay',
    'test_debug_map_navigation_pauses_and_returns_to_menu_or_game',
)
MAP_TESTS = (
    'test_boot_preloads_shared_atlas_and_keeps_program_main',
    'test_map_artwork_ignores_locks_and_merges_doors_with_grilles',
    'test_map_artwork_hides_furniture_and_floor_obstacles_but_keeps_fireplaces',
    'test_map_artwork_marks_secret_fireplaces_with_a_solid_right_pillar',
    'test_debug_map_all_rooms_initial_content_and_live_position',
    'test_debug_map_ignores_pit_state_on_all_pages_and_buffers',
    'test_debug_map_navigation_pauses_and_returns_to_menu_or_game',
    'test_inventory_spaced_layout_live_values_and_modal_return',
    'test_help_returns_to_each_modal_page_and_name_input',
)
ENDING_TESTS = (
    'test_ending_source_canvas_matches_executed_original_6502_blitter',
    'test_graphical_victory_requires_all_three_objectives_on_exit_and_caches_both_pages',
    'test_graphical_death_retains_five_names_then_wraps_and_replays',
    'test_ending_disk_slots_and_overlay_leave_resident_code_and_aux_assets_intact',
    'test_partial_departure_keeps_compact_text_layout_and_live_gold',
    'test_room36_grille_falls_on_both_pages_before_death_and_pauses_with_help',
    'test_title_lightning_reveal_and_text_transition',
    'test_debug_map_navigation_pauses_and_returns_to_menu_or_game',
)
CHECKPOINT_TESTS = (
    'test_boot_preloads_shared_atlas_and_keeps_program_main',
    'test_checkpoint_codec_native_vectors_and_corruption',
    'test_checkpoint_save_pauses_help_and_consumes_close_keys',
    'test_checkpoint_entry_errors_editing_cancel_and_help',
    'test_checkpoint_cold_cross_profile_resume_preserves_new_name',
    'test_checkpoint_rejects_unrepresentable_stocks_without_changing_game_limits',
    'test_checkpoint_removed_treasures_cannot_award_twice',
    'test_checkpoint_close_rebuilds_room_and_retains_gate_and_pit_state',
    'test_debug_map_navigation_pauses_and_returns_to_menu_or_game',
    'test_name_exterior_merchant_and_resume',
)
GEOMETRY_TESTS = (
    'test_boot_preloads_shared_atlas_and_keeps_program_main',
    'test_carried_flame_tracks_torch_head_in_every_direction_and_pose',
    'test_source_torch_flames_animate_on_both_pages_without_trails',
    'test_chair_footprint_blocks_surface_but_allows_front_and_sides',
    'test_tables_block_rear_route_and_keep_front_approach',
    'test_half_steps_and_continuous_depth_bands',
    'test_portals_require_approaching_the_visible_door',
    'test_room18_25_arch_round_trip_at_visible_center',
    'test_room25_grille_to26_rejects_keys_and_accepts_crowbar',
    'test_chest_and_quest_remain_reachable_with_reduced_clearance',
    'test_room26_chest_opens_from_front_with_crowbar',
    'test_all_chests_block_rear_and_top_and_keep_opening_and_rewards_reachable',
    'test_debug_map_all_rooms_initial_content_and_live_position',
    'test_debug_map_navigation_pauses_and_returns_to_menu_or_game',
)


def main(mode='dhgr', selection='full'):
    directory=ROOT/('build/game-mono' if mode=='mono' else 'build/game')
    selected={'feedback':FEEDBACK_TESTS,'interactions':INTERACTION_TESTS,
              'presentation':PRESENTATION_TESTS,'map':MAP_TESTS,'checkpoint':CHECKPOINT_TESTS,
              'geometry':GEOMETRY_TESTS,'hazards':HAZARD_TESTS,'pits':PIT_TESTS,
              'endings':ENDING_TESTS}.get(selection)
    report={'feedback':'action-feedback-test-results.json','interactions':'interactions-test-results.json',
            'presentation':'presentation-test-results.json','map':'map-test-results.json',
            'checkpoint':'checkpoint-test-results.json',
            'geometry':'geometry-test-results.json','hazards':'hazard-test-results.json',
            'pits':'pit-test-results.json','endings':'ending-test-results.json'}.get(selection,'game-test-results.json')
    for name in [report] + (['room-verification.json'] if selection=='full' else []):
        (directory/name).unlink(missing_ok=True)
    if selected:
        from tests.world_port import NativeWorldTests
        from tests.mono_world import MonoWorldTests
        case=MonoWorldTests if mode=='mono' else NativeWorldTests
        suite=unittest.TestSuite(case(name) for name in selected)
    else:
        suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='mono_world.py' if mode=='mono' else 'world_port.py')
    started=time.monotonic()
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    write_json(directory/report,{'success':result.wasSuccessful(),'video_profile':mode,'suite':selection,
        'selected_tests':list(selected) if selected else 'all',
        'elapsed_seconds':round(time.monotonic()-started,3),
        'tests_run':result.testsRun,'failures':[c.id() for c,_ in result.failures],
        'errors':[c.id() for c,_ in result.errors],
        'program_sha256':digest((directory/'game.bin').read_bytes()),
        'disk_sha256':digest((directory/'laigle-dor.do').read_bytes()),
        'execution':'py65 functional 6502 / real Disk II BOOT0; no ROM cold-start',
        'original_oric_runtime':'not tested','virtual_ii':'not tested','real_hardware':'not tested'})
    return 0 if result.wasSuccessful() else 1


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--video',choices=['mono','dhgr'],default='dhgr')
    parser.add_argument('--suite',choices=['full','feedback','interactions','presentation','map','checkpoint','geometry','hazards','pits','endings'],default='full')
    args=parser.parse_args()
    sys.exit(main(args.video,args.suite))

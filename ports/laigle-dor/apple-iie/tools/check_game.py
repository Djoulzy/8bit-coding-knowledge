"""Separate native-world checks; do not mix their evidence with W06 graphics."""
import sys
import argparse
import time
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.common import ROOT,write_json,digest


FEEDBACK_TESTS = (
    'test_impossible_actions_persist_until_next_command',
    'test_impossible_feedback_in_special_rooms_and_darkness',
    'test_light_feedback_distinguishes_request_from_automatic_attempt',
    'test_gameplay_hud_original_room_descriptions',
    'test_gameplay_hud_stats_and_hand_names',
    'test_name_exterior_merchant_and_resume',
    'test_help_pauses_walking_and_staged_actions',
    'test_room_change_keeps_graphics_until_hidden_pair_is_complete',
    'test_lighting_does_not_leave_an_unanimated_fixture',
)
INTERACTION_TESTS = (
    'test_boot_preloads_shared_atlas_and_keeps_program_main',
    'test_secret_passages_open_and_traverse_all_source_links',
    'test_secret_passage_guards_and_original_anchor',
) + FEEDBACK_TESTS + (
    'test_all_64_rooms_use_the_same_constructor_and_grid',
    'test_transition_uses_original_link_and_arrival_bits',
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
    'test_debug_map_all_rooms_initial_content_and_live_position',
    'test_debug_map_navigation_pauses_and_returns_to_menu_or_game',
    'test_inventory_spaced_layout_live_values_and_modal_return',
    'test_help_returns_to_each_modal_page_and_name_input',
)
CHECKPOINT_TESTS = (
    'test_boot_preloads_shared_atlas_and_keeps_program_main',
    'test_checkpoint_codec_native_vectors_and_corruption',
    'test_checkpoint_save_pauses_help_and_consumes_close_keys',
    'test_checkpoint_entry_errors_editing_cancel_and_help',
    'test_checkpoint_cold_cross_profile_resume_preserves_new_name',
    'test_debug_map_navigation_pauses_and_returns_to_menu_or_game',
    'test_name_exterior_merchant_and_resume',
)


def main(mode='dhgr', selection='full'):
    directory=ROOT/('build/game-mono' if mode=='mono' else 'build/game')
    selected={'feedback':FEEDBACK_TESTS,'interactions':INTERACTION_TESTS,
              'presentation':PRESENTATION_TESTS,'map':MAP_TESTS,'checkpoint':CHECKPOINT_TESTS}.get(selection)
    report={'feedback':'action-feedback-test-results.json','interactions':'interactions-test-results.json',
            'presentation':'presentation-test-results.json','map':'map-test-results.json',
            'checkpoint':'checkpoint-test-results.json'}.get(selection,'game-test-results.json')
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
    parser.add_argument('--suite',choices=['full','feedback','interactions','presentation','map','checkpoint'],default='full')
    args=parser.parse_args()
    sys.exit(main(args.video,args.suite))

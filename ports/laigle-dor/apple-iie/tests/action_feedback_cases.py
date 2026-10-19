"""Execute outcome distinctions and their rendering in the native 6502 game."""


OUTCOME_WORDS = {
    1: 'Impossible', 7: 'Vide', 8: 'Echec', 9: 'Deja fait', 10: 'Casse',
    11: 'Verrouille', 12: 'Ferme', 13: 'Parchemin', 14: 'Or trouve',
    15: 'Clef fer', 16: 'Clef or', 17: 'Fiole', 18: 'Bague', 19: 'Plomb',
}


class ActionFeedbackTests:
    def feedback_room(self, number, x=28, y=170, facing=3, item=6):
        for name, value in [('game_mode', 0), ('current_room', number), ('in_pit', 0),
                ('actor_x', x), ('actor_y', y), ('facing', facing), ('pose', facing),
                ('walking', 0), ('action_kind', 0), ('held_item', item),
                ('crowbars', 1), ('bar_life', 30), ('message_id', 0)]:
            self.set(name, value)
        self.call('world_load_scene')

    def message(self):
        return self.m.bus.ram[self.m.symbols['message_id']]

    def outcome_rows(self):
        rows = self.m.text_rows(all_rows=True)
        start = 8 if self.m.bus.switches['TEXT'] else 20
        return rows[start:start + 4]

    def test_chest_feedback_distinguishes_range_closed_empty_and_already_open(self):
        self.feedback_room(26)
        self.call('full_pickup')
        self.assertEqual(self.message(), 12, 'a reachable closed chest is not empty')
        self.set('actor_x', 19)
        self.call('full_pickup')
        self.assertEqual(self.message(), 1, 'distance still makes the action impossible')
        self.set('actor_x', 28)
        self.call('full_open')
        self.assertEqual(self.message(), 4)
        self.assertEqual(self.m.bus.ram[self.m.symbols['chest_open']], 1)
        self.assertEqual(self.m.bus.ram[self.m.symbols['bar_life']], 29)
        self.call('world_load_scene')
        world = bytes(self.m.bus.ram[0x1000:0x1200])
        self.call('full_open')
        self.assertEqual(self.message(), 9)
        self.assertEqual(self.m.state()['room_dirty'], 0)
        self.assertEqual(self.m.bus.ram[self.m.symbols['bar_life']], 29)
        self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]), world)
        before = self.m.state()
        self.m.frame(ord('P'))
        self.assertEqual(self.message(), 7)
        self.assertEqual(self.m.state()['last_event'], 7)
        for _ in range(3):
            self.assertEqual(self.message(), 7)
            self.assertEqual(self.decode_text(self.outcome_rows()[0])[-4:], 'Vide')
            self.m.frame()
        self.assertEqual((self.m.state()['gold'], self.m.state()['points']),
                         (before['gold'], before['points']))
        (self.directory/'action-empty-chest.png').write_bytes(self.m.screen_png())
        self.m.frame(ord('H')); self.m.frame(32)
        self.assertEqual(self.message(), 7, 'help pauses the outcome too')
        self.m.frame(32)
        self.assertEqual(self.message(), 0)
        self.feedback_room(11, x=19, y=140, item=8)
        self.call('full_open')
        self.assertEqual(self.message(), 3)
        self.call('world_load_scene')
        self.call('full_open')
        self.assertEqual(self.message(), 9)
        self.assertEqual(self.m.bus.ram[self.m.symbols['passage']], 1)
        self.assertEqual(self.m.state()['room_dirty'], 0)
        self.assertFalse(self.m.bus.visible_text_write_violations)

    def test_crowbar_feedback_distinguishes_lock_random_failure_and_breakage(self):
        self.feedback_room(25, x=19, y=145)
        world = bytes(self.m.bus.ram[0x1000:0x1200])
        for item in (0, 8, 9):
            self.set('held_item', item)
            self.call('full_open')
            self.assertEqual(self.message(), 11)
            self.assertEqual(self.m.bus.ram[self.m.symbols['bar_life']], 30)
        self.set('held_item', 6)
        self.word('rng_state', 0xACE1)
        for life in (29, 28):
            self.m.frame(ord('O'))
            self.assertEqual(self.message(), 8)
            self.assertEqual(self.m.state()['last_event'], 7)
            self.assertEqual(self.m.state()['current_room'], 25)
            self.assertEqual(self.m.bus.ram[self.m.symbols['bar_life']], life)
            self.assertEqual(bytes(self.m.bus.ram[0x1000:0x1200]), world)
        (self.directory/'action-crowbar-failed.png').write_bytes(self.m.screen_png())
        for attempt in range(3, 21):
            self.m.frame(ord('O'))
            if self.m.state()['current_room'] == 26:
                break
            self.assertEqual(self.message(), 8)
            self.assertEqual(self.m.bus.ram[self.m.symbols['bar_life']], 30-attempt)
        self.assertEqual(self.m.state()['current_room'], 26)
        self.assertEqual(self.message(), 0, 'successful transition clears the attempt')
        self.feedback_room(25, x=19, y=145)
        self.set('bar_life', 0)
        self.call('full_open')
        self.assertEqual(self.message(), 10)
        self.assertEqual(self.m.state()['held_item'], 0)
        self.assertEqual(self.m.state()['crowbars'], 0)
        self.assertEqual(self.m.state()['current_room'], 25)
        # Controlled lock-class fixture: class 3 cannot be forced and does not
        # draw a random value. Preserve its existing wear-before-refusal rule.
        self.feedback_room(25, x=19, y=145)
        self.m.bus.ram[self.m.symbols['room_fields'] + 6] = 3
        rng = self.m.state()['rng_state']
        self.call('full_open')
        self.assertEqual(self.message(), 11)
        self.assertEqual(self.m.state()['rng_state'], rng)
        self.assertEqual(self.m.bus.ram[self.m.symbols['bar_life']], 29)

    def test_pickup_names_real_chest_contents_and_retains_single_award(self):
        for number, treasure in [(4, 5), (13, 5), (26, 0), (52, 2), (58, 2), (60, 5)]:
            with self.subTest(room=number):
                self.feedback_room(number)
                self.assertEqual(self.m.state()['room_treasure'], treasure)
                self.call('full_open'); before = self.m.state()
                self.m.frame(ord('P'))
                self.assertEqual(self.message(), {0: 7, 2: 14, 5: 17}[treasure])
                self.assertEqual(self.m.state()['vials'] - before['vials'], int(treasure == 5))
                self.assertEqual(self.m.state()['points'] - before['points'], {0: 0, 2: 10, 5: 7}[treasure])
                if treasure == 2:
                    self.assertGreater(self.m.state()['gold'], before['gold'])
                self.assertEqual(self.m.state()['room_treasure'], 0)
                self.assertEqual(self.m.bus.ram[0x1100 + 4*number] & 0x38, 0)
                after = self.m.state()
                self.assertEqual(self.decode_text(self.outcome_rows()[0]).strip()[-len(OUTCOME_WORDS[self.message()]):],
                                 OUTCOME_WORDS[self.message()])
                if number in (4, 52):
                    (self.directory/('action-found-vial.png' if number == 4 else 'action-found-gold.png')).write_bytes(self.m.screen_png())
                self.m.frame(ord('P'))
                self.assertEqual(self.message(), 7)
                self.assertEqual((self.m.state()['gold'], self.m.state()['points'], self.m.state()['vials']),
                                 (after['gold'], after['points'], after['vials']))
        # Exercise the other ordinary treasure types with controlled chest
        # contents; these are not claimed to be original chest placements.
        for treasure, bit in [(1, None), (3, 1), (4, 2), (6, 4), (7, 8)]:
            with self.subTest(treasure=treasure):
                self.feedback_room(26)
                self.set('chest_open', 1); self.set('room_treasure', treasure)
                self.set('possessions', 0)
                address = 0x1100 + 4*26
                self.m.bus.ram[address] = (self.m.bus.ram[address] & 0xC7) | (treasure << 3)
                self.call('full_pickup')
                self.assertEqual(self.message(), 12 + treasure)
                self.assertEqual(self.m.state()['room_treasure'], 0)
                self.assertEqual(self.m.bus.ram[address] & 0x38, 0)
                if bit is not None:
                    self.assertEqual(self.m.state()['possessions'] & bit, bit)
                self.assertEqual(self.m.state()['last_event'], 6)  # EVENT_ITEM, not a refusal

    def test_outcome_words_are_inverse_right_aligned_on_both_pages_and_in_darkness(self):
        for number, pit in [(12, 0), (63, 0), (23, 1), (9, 0)]:
            self.feedback_room(number, x=19, y=180, item=0)
            self.set('in_pit', pit)
            self.call('draw_scene'); self.call('present_frame')
            original = [self.decode_text(row[:40]) for row in self.outcome_rows()]
            for message, word in OUTCOME_WORDS.items():
                with self.subTest(room=number, message=message):
                    self.set('message_id', message)
                    pages = set()
                    for _ in range(2):
                        self.call('draw_scene'); self.call('present_frame')
                        pages.add(self.m.state()['display_page_hi'])
                        raw = self.outcome_rows()
                        encoded = bytes(ord(c) & 0x3F if 'A' <= c <= 'Z' else ord(c) for c in word)
                        self.assertEqual(raw[0][-10:], b'\xA0'*(10-len(word)) + encoded)
                        self.assertEqual([self.decode_text(row[:40]) for row in raw[2:]], original[2:])
                        text = [self.decode_text(row[:40]) for row in raw[:2]]
                        if self.m.bus.switches['80COL']:
                            self.assertEqual(text, original[:2])
                        elif original[1].strip():
                            self.assertEqual(text, [original[0][:30] + word.rjust(10), original[1]])
                        else:
                            self.assertEqual(text, [original[0][:10].ljust(30) + word.rjust(10),
                                                    original[0][10:].strip().ljust(40)])
                    self.assertEqual(pages, {0x20, 0x40})
            for marker in (0, 2, 3, 4, 5, 6):
                self.set('message_id', marker)
                self.call('draw_scene'); self.call('present_frame')
                self.assertEqual([self.decode_text(row[:40]) for row in self.outcome_rows()], original)
        # Exercise the compact reading fallback as well as the AUX script
        # pages in the pre-existing clue test. Its footer is stored only once.
        import textwrap
        from tools.video_layout import text_address
        self.set('game_mode', 4)
        for index, name in enumerate(('scroll1.bin', 'scroll2.bin', 'scroll3.bin', 'book.bin')):
            text = (self.directory/'resources'/name).read_bytes().rstrip(b'\\').decode('ascii')
            lines = textwrap.wrap(' '.join(text.split()), width=40)
            expected = [s.ljust(40) for s in lines + ['']*(3-len(lines)) + ['Une touche: indice suivant']]
            self.set('reading_page', index)
            for page in (0x20, 0x40):
                self.set('draw_page_hi', page); self.set('render_page_index', int(page == 0x40))
                # Rendering into an explicitly hidden page, without flipping
                # into the modal 40-column view before inspecting the bytes.
                self.m.bus.switches['PAGE2'] = int(page == 0x20)
                self.call('full_hud_draw')
                actual = []
                for row in range(20, 24):
                    address = text_address(row, int(page == 0x40))
                    main = self.m.bus.ram[address:address + 40]
                    aux = self.m.bus.aux[address:address + 40]
                    raw = bytes(v for pair in zip(aux, main) for v in pair)[:40] if self.video == 'dhgr' else main
                    actual.append(self.decode_text(raw))
                self.assertEqual(actual, expected, (index, page))
        self.assertFalse(self.m.bus.visible_write_violations)
        self.assertFalse(self.m.bus.visible_text_write_violations)

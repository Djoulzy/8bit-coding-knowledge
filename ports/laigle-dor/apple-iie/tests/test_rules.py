from fractions import Fraction
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import Source
from model.rules import Rules, RandomTape


class RulesTests(unittest.TestCase):
    def new(self, values=()):
        return Rules(Source().read(0x5600, 512), RandomTape(values))

    def test_energy_zero_is_not_death_and_replay_resets(self):
        g = self.new(); g.energy = Fraction(1, 100)
        self.assertFalse(g.controller_loss()); self.assertEqual(g.energy, 0)
        self.assertTrue(g.controller_loss())
        g.world[0] ^= 0xFF; g.stock['rope'] = 3; g.objectives['book'] = 0
        fresh = g.replay()
        self.assertEqual(fresh.world, fresh.snapshot)
        self.assertEqual((fresh.energy, fresh.money, fresh.stock['rope'], fresh.objectives['book']), (100, 500, 0, 1))

    def test_merchant_boundaries_and_first_wear_rng(self):
        for item, price in [('vial', 360), ('torch', 190), ('rope', 110), ('crowbar', 230)]:
            g = self.new(['1/2'])
            g.money = price - 1
            self.assertFalse(g.purchase(item)); self.assertEqual(g.stock[item], 0)
            g.money = price
            self.assertTrue(g.purchase(item)); self.assertEqual(g.money, 0)
            self.assertEqual(g.stock[item], 1)
            g.money = price
            self.assertTrue(g.purchase(item))
            self.assertEqual(len(g.rng.calls), 1 if item in ['torch', 'crowbar'] else 0)

    def test_door_keys_wear_and_strict_threshold(self):
        g = self.new(['1/10', '1/10']); g.held = 9
        self.assertTrue(g.door(1, 1)); self.assertFalse(g.door(2, 2))
        g.held = 6; g.stock['crowbar'] = 1; g.crowbar_wear = 1
        self.assertTrue(g.door(2, 2)); self.assertEqual(g.crowbar_wear, 0)
        self.assertFalse(g.door(2, 2)); self.assertEqual(g.stock['crowbar'], 0)
        g = self.new(); g.held = 6; g.crowbar_wear = 2
        self.assertFalse(g.door(3, 1)); self.assertEqual(g.crowbar_wear, 1)
        self.assertEqual(len(g.rng.calls), 0)

    def test_all_ordinary_rewards_single_transaction(self):
        for tr, points, money in [(1, 0, 500), (2, 10, 650), (3, 15, 500),
                                  (4, 30, 500), (5, 7, 500), (6, 0, 700), (7, 10, 550)]:
            g = self.new(['1/2']); room = 35
            a = 256 + room * 4; g.world[a] = (g.world[a] & 0xC7) | (tr << 3)
            self.assertFalse(g.pickup(room, tr, 0, 0, 160))
            self.assertTrue(g.pickup(room, tr, 0, 4, 160))
            self.assertEqual((g.points, g.money), (points, money))
            self.assertFalse(g.pickup(room, tr, 0, 4, 160))
            self.assertEqual(g.world[a] & 0x38, 0)

    def test_poison_consumes_rng_even_when_zero(self):
        for poison in [0, 1, 2]:
            g = self.new(['999/1000']); g.stock['vial'] = 1; g.held = 10; g.poison = poison
            g.energy = 15
            self.assertTrue(g.finish_drink())
            self.assertEqual(len(g.rng.calls), 1)
            self.assertEqual(g.poison, max(0, poison - 1))
            self.assertEqual(g.drain, Fraction(101, 100) if poison else Fraction(1, 100))
            self.assertEqual(g.energy, 15 if poison else 100)
            self.assertEqual(g.stock['vial'], 0)

    def test_pit_mutation_and_source_fractional_formula(self):
        g = self.new(['1/2', '1/2']); g.fall(12, 19)
        self.assertEqual(g.energy, 70)
        self.assertEqual(g.drain, Fraction(7, 200))
        self.assertEqual(g.pit_origin, (12, 19))
        self.assertTrue(g.world[256 + 48] & 64)

    def test_quest_hazard_precedes_eagle_prerequisite(self):
        g = self.new()
        self.assertFalse(g.objective_pickup(63, 27, 160, 1, 1))
        self.assertTrue(g.quest_hazard); self.assertFalse(g.victory())
        g.possessions.add('lead')
        self.assertTrue(g.objective_pickup(63, 27, 160, 1, 1))
        self.assertNotIn('lead', g.possessions)
        self.assertTrue(g.objective_pickup(62, 27, 160, 1, 1))
        self.assertTrue(g.objective_pickup(1, 27, 160, 1, 1))
        self.assertTrue(g.victory()); self.assertEqual(g.points, 2500)
        self.assertEqual(g.money, 5700)
        self.assertFalse(g.objective_pickup(1, 27, 160, 1, 1))

    def test_random_input_contract(self):
        for value in ['-1/10', 1]:
            with self.assertRaises(ValueError):
                RandomTape([value]).next('invalid')

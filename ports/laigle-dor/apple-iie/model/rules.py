"""W03 source-expression oracle for independent rule tests, not a full game.

Fraction gives exact model arithmetic, not Oric floating-point emulation. RNG
values are supplied explicitly with tags; the Oric ROM RNG is not reproduced.
Source references are original B2 BASIC line numbers in the pinned analysis.
"""
from dataclasses import dataclass, field
from fractions import Fraction


class RandomTape:
    def __init__(self, values=()):
        self.values = iter(Fraction(v) for v in values)
        self.calls = []

    def next(self, tag):
        value = next(self.values)
        if not 0 <= value < 1:
            raise ValueError('Oric RND(1) contract is [0,1)')
        self.calls.append((tag, str(value)))
        return value


@dataclass
class Rules:
    snapshot: bytes
    rng: RandomTape = field(default_factory=RandomTape)
    energy: Fraction = Fraction(100)
    drain: Fraction = Fraction(1, 100)
    money: int = 500
    points: int = 0
    held: int = 0
    stock: dict = field(default_factory=lambda: {'vial': 0, 'torch': 0, 'rope': 0, 'crowbar': 0})
    objectives: dict = field(default_factory=lambda: {'book': 1, 'diamond': 1, 'eagle': 1})
    possessions: set = field(default_factory=set)
    poison: int = 0
    crowbar_wear: Fraction = Fraction(0)
    torch_wear: Fraction = Fraction(0)
    pit_origin: tuple = None
    quest_hazard: bool = False

    def __post_init__(self):
        if len(self.snapshot) != 512:
            raise ValueError('World snapshot must contain 512 bytes')
        self.world = bytearray(self.snapshot)

    def controller_loss(self):
        self.energy -= self.drain  # B2 5200; death at 5800 if EO<0
        return self.energy < 0

    def purchase(self, item):
        prices = {'vial': 360, 'torch': 190, 'rope': 110, 'crowbar': 230}
        price = prices[item]
        if self.money < price:
            return False
        self.money -= price
        first = self.stock[item] == 0
        self.stock[item] += 1
        if first and item == 'torch':
            self.torch_wear = 200 + 100 * self.rng.next('torch lifetime')
        if first and item == 'crowbar':
            self.crowbar_wear = 20 + 20 * self.rng.next('crowbar lifetime')
        return True

    def door(self, lock, status):
        # B2 4600–4640. True means accepted, not an executed room transition.
        if lock == 0 or (lock == 1 and self.held == 9):
            return True
        if self.held == 6:
            self.crowbar_wear -= 1
            if self.crowbar_wear < 0:
                self.stock['crowbar'] -= 1
                if self.stock['crowbar'] > 0:
                    self.crowbar_wear = 20 + 20 * self.rng.next('replacement crowbar lifetime')
                self.held = 0
                return False  # exhaustion enters B2 2300 instead of continuing
        if lock == 3:
            return False
        # Explicit eager-operand oracle policy; confirm actual BASIC evaluator
        # and intervening effect RNG calls in W00 before sequence comparison.
        r = self.rng.next('lock predicate (eager oracle)')
        return self.held == 6 and r * status < Fraction(3, 10)

    def pickup(self, room, treasure, facing, pose, marker):
        # B2 10700–10752: ordinary map pickup only, not chest/direct handlers.
        if facing == 3 or marker != 160 or not treasure or self.held != 0:
            return False
        if not 4 <= pose <= 7:
            return False
        actual = (self.world[256 + room * 4] >> 3) & 7
        if actual != treasure:
            return False
        if treasure == 1:
            scroll = {62: 'scroll1', 35: 'scroll2', 1: 'scroll3'}.get(room)
            if scroll:
                self.possessions.add(scroll)
        elif treasure == 2:
            self.money += int(self.rng.next('gold bag') * 300)
            self.points += 10
        elif treasure == 3:
            self.possessions.add('iron_key'); self.points += 15
        elif treasure == 4:
            self.possessions.add('gold_key'); self.points += 30
        elif treasure == 5:
            self.stock['vial'] += 1; self.points += 7
            if room in [14, 38]:
                self.poison += 1
        elif treasure == 6:
            self.possessions.add('ring'); self.money += 200
        elif treasure == 7:
            self.possessions.add('lead'); self.money += 50; self.points += 10
        else:
            raise ValueError('Unknown treasure')
        self.world[256 + room * 4] &= 0xC7
        return True

    def objective_pickup(self, room, x, y, facing, pose):
        # B2 10785–10797. Position/standing/empty hand precede hazard activation.
        if (x, y, facing) != (27, 160, 1) or pose > 3 or self.held != 0:
            return False
        if room == 62 and self.objectives['diamond'] == 1:
            self.quest_hazard = True
            self.objectives['diamond'] = 0
            self.points += 500; self.money += 200
            return True
        if room == 63 and self.objectives['eagle'] == 1:
            self.quest_hazard = True
            if 'lead' not in self.possessions:
                return False
            self.objectives['eagle'] = 0
            self.possessions.remove('lead')
            self.points += 1000; self.money += 5000
            return True
        if room == 1 and self.objectives['book'] == 1:
            self.objectives['book'] = 0
            self.points += 1000
            return True
        return False

    def finish_drink(self):
        # B2 12127–12130 after FG stages completed. Includes RNG call for PN=0.
        if self.stock['vial'] == 0 or self.held != 10:
            return False
        r = self.rng.next('vial poison')
        if r * self.poison < self.poison:
            self.poison -= 1
            self.drain += 1
        else:
            self.energy, self.drain = Fraction(100), Fraction(1, 100)
        self.stock['vial'] -= 1
        return True

    def fall(self, room, x):
        # B2 7000/7047/7048: mutation and EO/BL formulas, not rope animation.
        self.world[256 + room * 4] |= 0x40
        self.pit_origin = (room, x)
        self.energy -= 60 * self.rng.next('pit energy')
        self.drain += self.drain * 5 * self.rng.next('pit drain')
        self.held = 0

    def victory(self):
        return all(v == 0 for v in self.objectives.values())  # B2 3000 at exterior

    def replay(self):
        return Rules(self.snapshot, self.rng)  # per-game reset, session history external

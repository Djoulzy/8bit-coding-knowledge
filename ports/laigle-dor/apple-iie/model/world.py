"""Source room fields; no display or Apple hardware dependency."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Room:
    number: int
    geometry: int
    light: int
    features: tuple
    fields: tuple
    furnishing: int
    treasure: int
    gate: int
    floor: int
    links: tuple

    @classmethod
    def decode(cls, snapshot, number):
        if len(snapshot) != 512 or not 0 <= number < 64:
            raise ValueError('Expected 64 two-page room records')
        a = snapshot[4 * number:4 * number + 4]
        b = snapshot[256 + 4 * number:260 + 4 * number]
        fields = tuple((v >> shift) & 3 for v in a[1:] for shift in [0, 2, 4, 6])
        return cls(number, a[0] >> 6, a[0] & 3,
                   tuple((a[0] >> bit) & 1 for bit in [2, 3, 4, 5]),
                   fields, b[0] & 7, (b[0] >> 3) & 7,
                   b[0] >> 7, (b[0] >> 6) & 1, tuple(b[1:]))

    def transition(self, facing):
        if facing not in range(4):
            raise ValueError('Invalid facing')
        v = self.number if facing == 0 else self.links[3 - facing]
        return v & 63, v >> 6

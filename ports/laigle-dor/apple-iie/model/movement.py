"""Translated W06 controller: source turn/stop/continue and two-phase motion."""
from dataclasses import dataclass


def room12_grid(room):
    grid = bytearray(120)
    for first in [42, 77, 86, 113]:
        grid[first:first + 3] = bytes([128]) * 3
    grid[3] = 128 + room.fields[1]  # $0483: left
    grid[37] = 128 + room.fields[2]  # $0484: right
    return grid


def probe(grid, room, x, y, facing):
    """Return blocked, door status, object; source $4B75/$4B82/$4C73."""
    if len(grid) != 120 or not 0 <= x < 40 or y not in [140, 150, 160, 170, 180]:
        return True, 4, 0
    base = x + (80 if y == 140 else 40 if y == 160 else 0)
    status, blocked, obj = 4, False, 0
    if facing == 0:
        blocked = y == 180
        indices = range(base - 40, base - 37)
    elif facing == 1:
        if x == 31 and base < 40:
            status = room.fields[2]
            return status < 3, status, 0
        indices = range(base + 3, base + 8)
    elif facing == 2:
        if x == 7 and base < 40:
            status = room.fields[1]
            return status < 3, status, 0
        indices = range(base - 4, base)
    elif facing == 3:
        limit = [160, 140, 140, 180][room.geometry]
        if y == limit:
            if x == 19:
                status = room.fields[0]
                return status < 3, status, 0
            return True, status, 0
        indices = range(base + 40, base + 44)
    else:
        raise ValueError('Invalid facing')
    for index in indices:
        # Transitional y=150/170 can make the source read mirrored Oric VIA.
        # W06 virtual probes are empty, inside the independently bounded room.
        v = grid[index] if 0 <= index < 120 else 0
        blocked |= bool(v & 128) and not (v == 160 and room.treasure == 0)
        if v == 1:
            obj = 1
    return blocked or status < 3, status, obj


@dataclass
class Actor:
    x: int = 19
    y: int = 140
    facing: int = 0
    pose: int = 0
    walking: int = 0
    phase: int = 0

    @property
    def frame(self):
        if self.walking:
            return 8 + 2 * self.facing + self.phase
        return self.facing + (4 if self.pose >= 4 else 0)

    def tick(self, key, grid, room):
        events = []
        if key is not None:
            if key in range(4):
                if self.walking:
                    self.walking = self.phase = 0
                    self.pose = self.facing
                    events.append(2)  # source line 97 stop cue
                elif self.pose >= 4:
                    self.facing = key
                    self.pose = 4 + key
                elif self.facing != key:
                    self.facing = self.pose = key
                else:
                    self.walking, self.phase = 1, 1  # next step becomes phase 0
            elif key == 4:  # space
                if self.walking:
                    events.append(2)
                self.walking = self.phase = 0
                self.pose = self.facing
            elif key == 5:  # crouch
                if not 4 < self.pose < 8:
                    self.pose = 4 + self.facing
                    self.walking = self.phase = 0
            # Unimplemented keys explicitly ignored, rather than unsafe dispatch.
        if self.walking:
            blocked, status, _ = probe(grid, room, self.x, self.y, self.facing)
            if blocked:
                self.walking = self.phase = 0
                self.pose = self.facing
                events.append(4)
            elif status == 3:
                # W06 retains room 12 at its exit; W07 will consume the request.
                self.walking = self.phase = 0
                self.pose = self.facing
                events.append(3)
            else:
                self.phase ^= 1
                self.x += [0, 2, -2, 0][self.facing]
                self.y += [10, 0, 0, -10][self.facing]
                events.append(1)
        return events

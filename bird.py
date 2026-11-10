"""Fourteen right-facing frames from the original 918 x 506 sprite sheet."""
from pathlib import Path
from pico2d import load_image
import game_framework

CANVAS_WIDTH, CANVAS_HEIGHT = 1600, 600
DRAW_WIDTH, DRAW_HEIGHT = 110, 102
FLIGHT_SPEED = 200.0  # pixels per second
FRAMES_PER_SECOND = 14.0  # one complete wingbeat per second

# Measured transparent gutters; second-row wing pixels extend to y=339.
COLUMN_EDGES = (0, 182, 364, 546, 728, 918)
ROW_EDGES = (0, 170, 340, 506)
FRAME_RECTS = tuple(
    (COLUMN_EDGES[col], 506 - ROW_EDGES[row + 1],
     COLUMN_EDGES[col + 1] - COLUMN_EDGES[col],
     ROW_EDGES[row + 1] - ROW_EDGES[row])
    for row, count in enumerate((5, 5, 4))
    for col in range(count)
)


class Bird:
    image = None

    def __init__(self, index):
        if Bird.image is None:
            Bird.image = load_image(str(Path(__file__).resolve().with_name('bird_animation.png')))
        self.left = DRAW_WIDTH / 2
        self.right = CANVAS_WIDTH - DRAW_WIDTH / 2
        self.x = self.left + (self.right - self.left) * (index + 0.5) / 10
        self.y = 70 + index * 50
        self.direction = 1 if index % 2 == 0 else -1
        self.frame = index % len(FRAME_RECTS)

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_SECOND * dt) % len(FRAME_RECTS)
        # Unfold a round trip, then reflect it. Preserve any number of overshoots.
        span = self.right - self.left
        offset = self.x - self.left
        phase = offset if self.direction == 1 else 2 * span - offset
        phase = (phase + FLIGHT_SPEED * dt) % (2 * span)
        if phase < span:
            self.x, self.direction = self.left + phase, 1
        else:
            self.x, self.direction = self.right - (phase - span), -1

    def draw(self):
        self.image.clip_composite_draw(
            *FRAME_RECTS[int(self.frame)], 0,
            '' if self.direction == 1 else 'h',
            self.x, self.y, DRAW_WIDTH, DRAW_HEIGHT,
        )

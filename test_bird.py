import unittest
from unittest.mock import Mock, patch

import bird
import game_framework
import game_world
import play_mode


class FlightTests(unittest.TestCase):
    def setUp(self):
        self.image = Mock()
        self.image_patch = patch.object(bird.Bird, 'image', self.image)
        self.image_patch.start()
        self.addCleanup(self.image_patch.stop)
        self.addCleanup(play_mode.finish)
        self.addCleanup(setattr, game_framework, 'frame_time', 0.0)

    def advance(self, obj, dt):
        game_framework.frame_time = dt
        obj.update()

    def test_partitioned_time_matches_one_large_step(self):
        for direction in (-1, 1):
            a, b = bird.Bird(0), bird.Bird(0)
            a.direction = b.direction = direction
            self.advance(a, 123.456)
            for _ in range(1000):
                self.advance(b, 0.123456)
            self.assertAlmostEqual(a.x, b.x, places=7)
            self.assertAlmostEqual(a.frame, b.frame, places=7)
            self.assertEqual(a.direction, b.direction)

    def test_speed_and_both_edge_reflections(self):
        obj = bird.Bird(0)
        obj.x = 500
        self.advance(obj, 0.5)
        self.assertEqual(obj.x, 600)
        obj.x = obj.right - 10
        self.advance(obj, 0.1)
        self.assertEqual((obj.x, obj.direction), (obj.right - 10, -1))
        obj.x = obj.left + 10
        self.advance(obj, 0.1)
        self.assertEqual((obj.x, obj.direction), (obj.left + 10, 1))
        self.advance(obj, 10000)
        self.assertTrue(obj.left <= obj.x <= obj.right)

    def test_animation_order_and_horizontal_flip(self):
        obj = bird.Bird(0)
        self.assertEqual(len(bird.FRAME_RECTS), 14)
        for index in range(14):
            obj.frame = index
            for direction, flip in ((1, ''), (-1, 'h')):
                obj.direction = direction
                obj.draw()
                args = self.image.clip_composite_draw.call_args.args
                self.assertEqual(args[:4], bird.FRAME_RECTS[index])
                self.assertEqual(args[5], flip)
        obj.frame = 0
        self.advance(obj, 0.5)
        self.assertEqual(obj.frame, 7)
        self.advance(obj, 0.5)
        self.assertEqual(obj.frame, 0)
        for x, y, w, h in bird.FRAME_RECTS:
            self.assertTrue(0 <= x < x + w <= 918)
            self.assertTrue(0 <= y < y + h <= 506)

    def test_exactly_ten_birds_and_lifecycle(self):
        for _ in range(2):
            play_mode.init()
            objects = [obj for layer in game_world.world for obj in layer]
            self.assertEqual(len(objects), 10)
            self.assertEqual(len({id(obj) for obj in objects}), 10)
            self.assertTrue(all(isinstance(obj, bird.Bird) for obj in objects))
            self.assertEqual(objects, play_mode.birds)
            game_framework.frame_time = 0.25
            game_world.update()
            game_world.render()
            play_mode.finish()
            self.assertFalse(play_mode.birds)
            self.assertFalse(any(game_world.world))


if __name__ == '__main__':
    unittest.main()

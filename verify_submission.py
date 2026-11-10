"""Run the real SDL flight scene briefly and verify submission resources."""
import hashlib
from pathlib import Path
import subprocess

import pico2d
import bird
import game_framework
import game_world
import play_mode

ROOT = Path(__file__).resolve().parent


def verify_resources():
    tracked = set(subprocess.check_output(
        ['git', 'ls-files'], cwd=ROOT, text=True).splitlines())
    required = {'main.py', 'bird.py', 'play_mode.py', 'game_framework.py',
                'game_world.py', 'bird_animation.png', 'requirements.txt'}
    assert required <= tracked, f'Untracked required files: {required - tracked}'
    data = (ROOT / 'bird_animation.png').read_bytes()
    blob = b'blob ' + str(len(data)).encode('ascii') + b'\0' + data
    assert hashlib.sha1(blob).hexdigest() == '8c19f4108af91c6497c332d408a756e83b52d5ef', 'Original sprite differs'
    print('PASS: required files tracked; original professor sprite blob verified')


def verify_scene():
    frames = 0
    seen_directions = set()
    seen_frames = set()
    real_render = play_mode.render

    def render():
        nonlocal frames
        real_render()
        frames += 1
        objects = [obj for layer in game_world.world for obj in layer]
        assert len(objects) == 10 and objects == play_mode.birds
        assert len({id(obj) for obj in objects}) == 10
        for obj in objects:
            assert isinstance(obj, bird.Bird)
            assert obj.left <= obj.x <= obj.right
            seen_directions.add(obj.direction)
            seen_frames.add(int(obj.frame))
        if frames == 60:
            game_framework.quit()

    pico2d.open_canvas(bird.CANVAS_WIDTH, bird.CANVAS_HEIGHT)
    try:
        play_mode.render = render
        game_framework.run(play_mode)
        assert frames == 60, 'Scene closed before validation finished'
        assert (bird.Bird.image.w, bird.Bird.image.h) == (918, 506)
        assert seen_directions == {-1, 1}
        assert seen_frames == set(range(14))
        assert game_framework.frame_time > 0
        assert not any(game_world.world) and not play_mode.birds
        print('PASS: 60 real SDL frames, ten birds, 14 animation frames, both directions, cleanup')
    finally:
        play_mode.render = real_render
        # Discard the texture before closing its owning renderer.
        bird.Bird.image = None
        pico2d.close_canvas()


if __name__ == '__main__':
    verify_resources()
    verify_scene()

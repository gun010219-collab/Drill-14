from pico2d import open_canvas, close_canvas
import game_framework
import play_mode
from bird import CANVAS_WIDTH, CANVAS_HEIGHT


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        game_framework.run(play_mode)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()

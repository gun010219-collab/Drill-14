from pico2d import clear_canvas, update_canvas, get_events, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE
import game_framework
import game_world
from bird import Bird

BIRD_COUNT = 10
birds = []


def init():
    game_world.clear()
    birds[:] = [Bird(index) for index in range(BIRD_COUNT)]
    for bird in birds:
        game_world.add_object(bird, 1)


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            game_framework.quit()


def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    birds.clear()


def pause():
    pass


def resume():
    pass

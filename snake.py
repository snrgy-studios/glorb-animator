"""
Visualize a snake game on a 2v icosahedron with triangular pixels. the snake is able to
move to an unoccupied neighboring pixel of the head of the snake, and the tail follows.
"""

import random
from typing import Optional

from vedo import BaseActor, Triangle, color_map

from animation_player_cached import AnimationPlayerCached

from .geometry import Glorb


class Snake:
    """Defining the game mechanics for a snake"""

    def __init__(self, g: Glorb, occupied: set[int]):
        candidates = {i for i in range(glorb.no_faces - 1)} - occupied
        self.body = [random.choice(list(candidates))]
        self.max_length = 4
        self.g = g
        self.color = color_map(random.uniform(0, 1), name="rainbow", vmin=0, vmax=1)

    def step(self, occupied: set[int], food: set[int]):
        """move snake one step"""
        # Move head one step
        next_head = self._next_head(occupied)
        if next_head is None:
            return None
        self.body.append(next_head)

        if next_head in food:
            # don't delete tail if eating something
            food.remove(next_head)
            self.max_length += 1

        # Delete tail one step
        if len(self.body) > self.max_length:
            self.body.pop(0)

        return self

    def _next_head(self, occupied: set[int]) -> Optional[int]:
        """Get a random random unoccupied neighboring pixel to move to"""
        candidates = set(self.g.neighbors[self.body[-1]]) - occupied
        if len(candidates) == 0:
            return None
        return random.choice(list(candidates))


glorb = Glorb()

snakes: list[Snake] = []
food: set[int] = set()


def simulation_func(sim_step: int) -> tuple:
    """Returns current state of simulation"""
    occupied: set[int] = set()
    for s in snakes:
        occupied |= set(s.body)

    # move all snakes one step
    for idx, s in enumerate(snakes):
        if not s.step(occupied, food):
            snakes.pop(idx)  # snakes die when they cannot move
        occupied |= set(s.body)

    # sometimes, spawn new snakes
    while random.uniform(0, 1) > 0.8:
        s = Snake(glorb, occupied)
        snakes.append(s)
        occupied |= set(s.body)

    # sometimes, spawn new food
    food_candidates = {i for i in range(glorb.no_faces - 1)} - occupied
    while random.uniform(0, 1) > 0.7:
        food.add(random.choice(list(food_candidates)))

    return tuple((tuple(s.body), s.color) for s in snakes), tuple(food)


# All visual elements in the view
actors: dict[str, BaseActor] = {}

# Populate with the triangular pixels
for i, f in enumerate(glorb.faces):
    actors[f"{i} triangle"] = Triangle(
        glorb.vertices[f[0]], glorb.vertices[f[1]], glorb.vertices[f[2]]
    ).linewidth(1)


def show_func(state: tuple) -> None:
    """Shows current state of simulation"""
    # turn off all pixels
    for a in actors.values():
        assert isinstance(a, Triangle)
        a.color("grey5")

    snake_pixels, food_pixels = state

    for idx in food_pixels:
        a = actors[f"{idx} triangle"]
        assert isinstance(a, Triangle)
        a.color("yellow")

    # turn on snake pixels
    for body, color in snake_pixels:
        for idx in body:
            a = actors[f"{idx} triangle"]
            assert isinstance(a, Triangle)
            a.color(color)


visualizer = AnimationPlayerCached(
    simulation_func,
    show_func,
    actors,
    irange=(0, 500),
    dt=300,
    loop=True,
    show_kwargs={"axes": 0, "viewup": "z"},
)

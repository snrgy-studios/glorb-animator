from typing import Callable

from vedo import BaseActor
from vedo.applications import AnimationPlayer


# pylint: disable=too-few-public-methods
class AnimationPlayerCached(AnimationPlayer):
    """A wrapper for AnimationPlayer which handles all history caching.

    simulation_func is guaranteed to only be called once per increment, without skips,
    always increasing idx. This is useful for simulations which can not go backwards.
    simulation_func shall return a tuple with all states needed for show_func, and
    show_func is called with that same tuple when it is time to render a certain idx.
    """

    def __init__(
        self,
        simulation_func: Callable[[int], tuple],
        show_func: Callable[[tuple], None],
        actors: dict[str, BaseActor],
        irange: tuple,
        **kwargs,
    ):
        show_kwargs = kwargs.pop("show_kwargs", {})
        super().__init__(func=self._simulate_and_show, irange=irange, **kwargs)
        self.simulation_func = simulation_func
        self.show_func = show_func
        self.history: dict[int, tuple] = {}
        self.simulated_step = self.min_value - 1
        self += list(actors.values())
        self.show(interactive=False, **show_kwargs)
        self.set_frame(self.min_value)
        self.interactive()  # execution stops here until window is closed
        self.close()

    def _simulate_and_show(self, i: int) -> None:
        while i > self.simulated_step:
            self.simulated_step = self.simulated_step + 1
            self.history[self.simulated_step] = self.simulation_func(
                self.simulated_step
            )
        self.show_func(self.history[i])
        self.render()

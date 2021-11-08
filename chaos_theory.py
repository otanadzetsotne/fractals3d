import random
import itertools
from typing import Generator
import numpy as np
import plotly.graph_objects as go


DIMENSIONS = 3
MAX_SIZE = 128

POINTS_QUANTITY = 4
ITERATIONS = 10_000
CREATE = False


class FractalChaos:
    """
    FractalChaos class implements base logic for fractal generation with chaos theory
    by points generation

    Example:
    fractal = FractalPyramid(iterations=100_000)
    fractal = fractal.create()
    fractal.render(marker={'size': 1})
    """

    point_start = None
    points_main = None
    points_generated = None

    def __init__(
            self,
            points_quantity: int = POINTS_QUANTITY,
            iterations: int = ITERATIONS,
            create: bool = CREATE,
    ):
        self.__points_quantity = points_quantity
        self.__iterations = iterations

        if create:
            self.create()

    def render(self, *args, **kwargs):
        """
        Render plotly figure
        :param args: args for plotly Scatter3d object
        :param kwargs: kwargs for plotly Scatter3d object
        :return FractalChaos
        """

        points_by_axis = self.get().T

        fig = go.Figure(go.Scatter3d(
            *args,
            **kwargs,
            x=points_by_axis[0],
            y=points_by_axis[1],
            z=points_by_axis[2],
            mode='markers',
        ))

        fig.show()

        return self

    def get(self) -> np.array:
        """
        Get fractal points
        :return np.array of shape (self.points_quantity + self.iterations, 3)
        """

        return np.array([*self.get_generator()])

    def get_generator(self) -> itertools.chain[np.array]:
        """
        Get fractal points generator
        :return Generator[np.array]
        """

        if not self._is_created():
            self.create()

        return itertools.chain(self.points_main, self.points_generated)

    def create(self):
        """
        Create all fractal points
        :return FractalChaos
        """

        self.point_start = self._generate_point_random()
        self.points_main = self._generate_points_main()
        self.points_generated = self._generate_points_fractal()

        return self

    def _is_created(self) -> bool:
        """
        Check if all fractal points are generated
        :return bool
        """

        return self.points_main is not None and self.points_generated is not None

    def _generate_points_fractal(self) -> Generator:
        """
        Generate fractal points
        :return Generator[np.array]
        """

        point_last = self.point_start
        points_quantity = len(self.points_main)

        for _ in range(self.__iterations):
            # Choose random point from main
            point_target = self.points_main[random.randrange(0, points_quantity)]

            # Calculate middle point between last one and chosen target
            point_middle = self._point_middle(point_last, point_target)

            # Last point is calculated middle
            point_last = point_middle

            yield point_last

    def _generate_points_main(self) -> np.array:
        return np.array([
            self._generate_point_random() for _ in range(self.__points_quantity)
        ])

    @staticmethod
    def _generate_point_random() -> np.array:
        return np.array([
            random.randrange(0, MAX_SIZE) for _ in range(DIMENSIONS)
        ])

    @staticmethod
    def _point_middle(
            point_a: np.array,
            point_b: np.array,
    ) -> np.array:
        return (point_a + point_b) * .5


class FractalPyramid(FractalChaos):
    """
    FractalChaos Child for equilateral pyramid
    """

    def _generate_points_main(self, *args, **kwargs):
        height = ((MAX_SIZE ** 2) * 2) ** .5 * .5

        return np.array([
            [0, 0, 0],
            [0, MAX_SIZE, 0],
            [MAX_SIZE, 0, 0],
            [MAX_SIZE, MAX_SIZE, 0],
            [MAX_SIZE * .5, MAX_SIZE * .5, height],
        ])

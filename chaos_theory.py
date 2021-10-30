import random
import itertools
import numpy as np
import plotly.graph_objects as go


DIMENSIONS = 3
POINTS_QUANTITY = 4
MAX_SIZE = 100
ITERATIONS = 10_000


class Fractal:
    dimensions = None

    point_start = None
    points_main = None
    points_all = None

    def __init__(
            self,
            points_quantity: int = POINTS_QUANTITY,
            dimensions: int = DIMENSIONS,
    ):
        if points_quantity <= dimensions:
            raise ValueError(
                'points_quantity value needs to be more than dimensions value'
            )

        self.point_start = self.point_random(dimensions)
        self.points_main = self.generate_points_main(points_quantity, dimensions)

    def calculate(self, iterations: int = ITERATIONS):
        return itertools.chain(self.points_main, self.generate_fractal(iterations))

    def visualize(self, iterations: int = ITERATIONS):
        points = self.calculate(iterations)
        points = np.array([*points]).T

        fig = go.Figure(go.Scatter3d(
            x=points[0],
            y=points[1],
            z=points[2],
            mode='markers',
            marker={'size': 1, 'color': 'black'}
        ))
        fig.show()

    def generate_fractal(self, iterations: int):
        point_last = self.point_start
        points_quantity = len(self.points_main)

        for _ in range(iterations):
            # Choose random point from main
            point_target = self.points_main[random.randrange(0, points_quantity)]

            # Calculate middle point between last one and chosen target
            point_middle = self.point_middle(point_last, point_target)

            # Last point is calculated middle
            point_last = point_middle

            yield point_last

    def generate_points_main(self, points_quantity: int, *args, **kwargs):
        return np.array([
            self.point_random(*args, **kwargs) for _ in range(points_quantity)
        ])

    @staticmethod
    def point_middle(point_a, point_b):
        return (point_a + point_b) * .5

    @staticmethod
    def point_random(dimensions: int):
        return np.array([
            random.randrange(0, MAX_SIZE) for _ in range(dimensions)
        ])


class FractalPyramid(Fractal):
    def generate_points_main(self, points_quantity: int, *args, **kwargs):
        height = ((MAX_SIZE ** 2) * 2) ** .5 * .5

        return np.array([
            [0, 0, 0],
            [0, MAX_SIZE, 0],
            [MAX_SIZE, 0, 0],
            [MAX_SIZE, MAX_SIZE, 0],
            [MAX_SIZE * .5, MAX_SIZE * .5, height],
        ])


if __name__ == '__main__':
    frac = FractalPyramid()
    all_points = frac.calculate(100_000)

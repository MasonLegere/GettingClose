import argparse
import math

import matplotlib.pyplot as plt
import numpy as np
import yaml
from adjustText import adjust_text

parser = argparse.ArgumentParser(description='Algorithm to find the distance between a convex polygon and a '
                                             'non-intersecting line in logarithmic time')
parser.add_argument('-f', action='store', dest='file',
                    help='relative path for runtime information to be provided', required=True)
parser.add_argument('--plot', dest='plot', action='store_true',
                    help='Boolean flag to denote if the result should be plotted')
parser.set_defaults(feature=False)


class PolygonLine:

    def __init__(self, polygon, line):
        self.line = line
        self.polygon = polygon
        self.point_history = []

    # Returns the minimum distance between the line and a vertex of the polygon.
    # Selects a random point and performs binary search with respect to the distance to the line.
    # The distance from the line is done using the projection operator.
    def get_min_distance(self):

        n = int(len(self.polygon))
        skip_size = math.ceil(n / 2)
        index = 0
        self.point_history.append(self.polygon[index])

        while skip_size > 0:

            right_dist = PolygonLine.distance(self.polygon[(index + 1) % n], self.line)
            left_dist = PolygonLine.distance(self.polygon[(index - 1) % n], self.line)

            if left_dist < right_dist:
                index = (index - skip_size) % n
                # Used only for logging purposes
                self.point_history.append(self.polygon[index])
            else:
                index = (index + skip_size) % n
                # Used only for logging purposes
                self.point_history.append(self.polygon[index])
            skip_size = int(skip_size / 2)

        search_lst = self.polygon[index - 3:index + 2]
        self.point_history = self.point_history + search_lst
        return PolygonLine.brute_force_min_distance(search_lst, self.line)

    # Prints the minimum distance formatted to the output stream
    def print_minimum_distance(self):
        min_distance = self.get_min_distance()
        print("The minimum Euclidean distance between the convex polygon and the line is: {}".format(
            round(min_distance, 2)))

    # Brute force solution that iterates over all points provided, computes each distance and then returns the minimum
    @staticmethod
    def brute_force_min_distance(polygon, line):

        min_distance = math.inf
        for vertex in polygon:
            min_distance = min(PolygonLine.distance(vertex, line), min_distance)
        return min_distance

    # Plots the polygon, line and the order of the selection of points found in the binary search
    def plot(self):
        self._plot_polygon()
        self._plot_line()
        self._plot_history()
        plt.show()

    # Method to compute the distance from a point (x0, y0) in R^2 onto a line given in the form ax + by = c
    @staticmethod
    def distance(point, line):
        a, b, c = line
        x0, y0 = point
        return abs(a * x0 + b * y0 - c) / math.sqrt(a ** 2 + b ** 2)

    # Plots the original polygon with blue for the edges and green nodes for the vertices
    def _plot_polygon(self):

        polygon_coords = self.polygon.copy()
        polygon_coords.append(polygon_coords[0])

        xs, ys = zip(*polygon_coords)

        plt.figure()
        plt.plot(xs, ys)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.scatter(xs, ys, color='g')

    # Plots the vertices visited during the algorithm running
    def _plot_history(self):

        xs, ys = zip(*self.point_history)
        plt.plot(xs, ys)
        plt.scatter(xs, ys, color='r')
        texts = []

        for i in range(len(xs)):
            texts.append(plt.text(xs[i], ys[i], i + 1))

        adjust_text(texts, only_move={'points': 'y', 'texts': 'y'}, arrowprops=dict(arrowstyle="->", color='r', lw=0.5))

    # Plots the linear function that is given in the form of the tuple (a,b,c) representing
    # the points satisfying ax + by = c
    def _plot_line(self):

        a, b, c = self.line

        if b != 0:
            x = np.linspace(-100, 100, 100)
            y = -a / b * x + c / b
            plt.plot(x, y, '-r')

        elif a != 0:
            y = np.linspace(-100, 100, 100)
            x = [c / a] * len(y)
            plt.plot(x, y, '-r')

        else:
            raise ValueError


if __name__ == '__main__':
    args = parser.parse_args()

    parameters = yaml.load(open(args.file),
                           Loader=yaml.FullLoader)
    pl = PolygonLine(parameters['polygon'], parameters['line'])
    pl.print_minimum_distance()

    if args.plot:
        pl.plot()

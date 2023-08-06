"""This module contains different self-implemented statistical tools. It isn't documented good, because I am lazy ;)"""

from typing import Iterable, Tuple, Sequence, Dict, List

from collections import defaultdict
from random import sample
from functools import partial
from math import fsum, sqrt
from pprint import pprint

Point = Tuple[int, ...]
Centroid = Point


def transpose(data: Iterable[Iterable]):
    """Swap the rows and columns in a 2-D array of data"""
    return list(zip(*data))


def mean(data: Iterable[float]) -> float:
    """Accurate arithemetic mean"""
    data = list(data)
    return fsum(data) / len(data)


def dist(p: Point, q: Point, fsum=fsum, sqrt=sqrt, zip=zip) -> float:
    """Euclidian distance for multidemensional data"""
    return sqrt(fsum([(x - y) ** 2 for x, y in zip(p, q)]))


def assign_data(centroids: Sequence[Centroid], data: Iterable[Point]) -> Dict:
    """Group the data points to the closest centroid"""
    assigned = defaultdict(list)
    for point in data:
        closest_centroid = min(centroids, key=partial(dist, point))
        assigned[closest_centroid].append(point)
    return dict(assigned)


def compute_centroids(groups: Iterable[Sequence[Point]]) -> List[Centroid]:
    """Compute the centroid for each group"""
    return [tuple(map(mean, transpose(group))) for group in groups]


def k_means(
        data: Iterable[Point],
        k: int = 2, iterations: int = 50) -> List[Centroid]:
    data = list(data)
    centroids = sample(data, k)
    for i in range(iterations):
        labeled = assign_data(centroids, data)
        centroids = compute_centroids(labeled.values())
    return centroids


if __name__ == "main":
    points = [
        (1, 2, 3),
        (1, 2, 4),
        (2, 4, 3),
        (10, 12, 13),
        (11, 12, 13),
        (11, 13, 12)
        ]

    centroids = k_means(points, k=2)
    d = assign_data(centroids, points)
    pprint(d)

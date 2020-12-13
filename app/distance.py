import numpy as np


def select_closest(candidates, origin):
    """Возвращаем индекс ближайшего пункта к данной точке"""
    return euclidean_distance(candidates, origin).argmin()


def euclidean_distance(a, b):
    """Возвращаем массив расстояний двух массивов точек"""
    return np.linalg.norm(a - b, axis=1)


def route_distance(cities):
    """Возвращаем сумму пути прохождения маршрута городов в определенном порядке"""
    points = cities[['x', 'y']]
    distances = euclidean_distance(points, np.roll(points, 1, axis=0))
    return np.sum(distances)

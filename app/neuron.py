import numpy as np

from app.distance import select_closest


def generate_network(size):
    """
    Создаем нейронную сеть заданного размера.

    Возвращаем вектор двумерных точек в интервале [0,1].
    """
    return np.random.rand(size, 2)


def get_neighborhood(center, radix, domain):
    """Получаем Гауссовский диапазон заданной системы счисления вокруг индекса центра."""

    # Накладываем верхнюю границу на основание системы счисления, чтобы предотвратить NaN и блоки
    if radix < 1:
        radix = 1

    # Вычисляем расстояние круговой сети до центра
    deltas = np.absolute(center - np.arange(domain))
    distances = np.minimum(deltas, domain - deltas)

    # Вычисляем Гауссовое распределение вокруг данного центра
    return np.exp(-(distances * distances) / (2 * (radix * radix)))


def get_route(cities, network):
    """Возвращаем маршрут, рассчитанный сетью."""
    cities['winner'] = cities[['x', 'y']].apply(
        lambda c: select_closest(network, c),
        axis=1, raw=True)

    return cities.sort_values('winner').index

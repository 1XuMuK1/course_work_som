from sys import argv

import numpy as np

from app.io_helper import read_tsp, normalize
from app.neuron import generate_network, get_neighborhood, get_route
from app.distance import select_closest, route_distance
from app.plot import plot_network, plot_route


def main():
    if len(argv) != 2:
        print("Необходимо указать путь к файлу .tsp\nПример: python app/main.py <filename>.tsp")
        return -1

    problem = read_tsp(argv[1])
    route = som(problem, 100000)
    problem = problem.reindex(route)
    distance = route_distance(problem)
    print('Маршрут найденой длины {}'.format(distance))


def som(problem, iterations, learning_rate=0.8):
    """Решение TSP с помощью самоорганизующейся карты"""
    # Получаем нормализованный набор городов (с координатами в [0,1])
    cities = problem.copy()
    cities[['x', 'y']] = normalize(cities[['x', 'y']])
    # Население в 8 раз превышает количество городов.
    n = cities.shape[0] * 8
    # Создаем сеть нейронов:
    network = generate_network(n)
    print('Создана сеть из {} нейронов. Запуск итераций:'.format(n))

    for i in range(iterations):
        if not i % 100:
            print('\t> Итерация {}/{}'.format(i, iterations), end="\r")
        # Выбераем случайный город
        city = cities.sample(1)[['x', 'y']].values
        winner_idx = select_closest(network, city)
        # Создаем фильтр, который применяет изменения к Гауссову победителя
        gaussian = get_neighborhood(winner_idx, n // 10, network.shape[0])
        # Обновляем веса сети (ближе к городу)
        network += gaussian[:, np.newaxis] * learning_rate * (city - network)
        # Распад переменных
        learning_rate = learning_rate * 0.99997
        n = n * 0.9997
        # Проверяем интервал построения
        if not i % 1000:
            plot_network(cities, network, name='results/{:05d}.png'.format(i))
        # Проверяем, полностью ли испортился какой-либо параметр.
        if n < 1:
            print('Радиус полностью разрушился, выполнение завершено на {} итерациях.'.format(i))
            break
        if learning_rate < 0.001:
            print('Скорость обучения полностью снизилась, выполнение завершается на {} итерациях'.format(i))
            break
    else:
        print('Выполнено {} итераций.'.format(iterations))
    plot_network(cities, network, name='results/final.png')

    route = get_route(cities, network)
    plot_route(cities, route, 'results/route.png')
    return route


if __name__ == '__main__':
    main()

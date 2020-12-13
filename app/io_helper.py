import pandas as pd
import numpy as np


def read_tsp(filename):
    """
    Читаем файл в формате .tsp с использованием pandas DataFrame
    Файлы .tsp можно найти в проекте TSPLIB.
    """
    with open(filename) as f:
        node_coord_start = None
        count = None
        lines = f.readlines()

        # Получить информацию о .tsp
        i = 0
        while not count or not node_coord_start:
            line = lines[i]
            if line.startswith('DIMENSION :'):
                count = int(line.split()[-1])
            if line.startswith('NODE_COORD_SECTION'):
                node_coord_start = i
            i = i + 1

        print('Проблема с {} городами прочитана.'.format(count))

        f.seek(0)

        # Читаем структуру данных из файлового дескриптора
        cities = pd.read_csv(
            f,
            skiprows=node_coord_start + 1,
            sep=' ',
            names=['city', 'y', 'x'],
            dtype={'city': str, 'x': np.float64, 'y': np.float64},
            header=None,
            nrows=count
        )
        return cities


def normalize(points):
    """
    Возвращаем нормализованную версию заданного вектора точек.

    Для данного массива из n измерений нормализуем каждое измерение,
    удалив начальное смещение и нормализуя точки в пропорциональном интервале:
    [0,1] по y, сохраняя исходное соотношение по x.
    """
    ratio = (points.x.max() - points.x.min()) / (points.y.max() - points.y.min()), 1
    ratio = np.array(ratio) / max(ratio)
    norm = points.apply(lambda c: (c - c.min()) / (c.max() - c.min()))
    return norm.apply(lambda p: ratio * p, axis=1)

# course_work_som
# Реализация самоорганизующихся карт для решения задачи TSP
Данную реализацию можно использовать для поиска неоптимальных решений для задачи TSP (Travelling salesman problem). 
Примерами проблем, которые поддерживает программа, являются .tsp файлы, 
что является широко распространенным форматом в этой проблеме.
TSP файлы можно взять тут > http://www.math.uwaterloo.ca/tsp/world/countries.html или в другой библиотеке TSPLIB.

## How to use:
Python 3.6

создаем  виртуальное окружение
> python3 -m venv env

аткивируем env
> source env/bin/activate

устанавливаем зависимости
> pip install -r requirements.txt

run
> python main.py tsp/fi10639.tsp

## Result
После анализа tsp файла будут созданы изображения с кратчайшем путем.
Созданные изображения будут сохранены в results папке.
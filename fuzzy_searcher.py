from fuzzywuzzy import process
from typing import List, Tuple, Callable


class FuzzySearcher:
    def filter_found(method: Callable):
        def decorator(self, *args, **kwargs) -> List[Tuple[str, int]]:
            return list(filter(lambda t: t[1] >= self.__min_ratio, method(self, *args, **kwargs)))

        return decorator

    def tuple_to_list(method: Callable):
        def decorator(self, *args, **kwargs) -> List[str]:
            return list(map(lambda t: t[0], method(self, *args, **kwargs)))

        return decorator

    def __init__(self, min_ratio: int):
        self.__min_ratio = min_ratio

    @tuple_to_list
    @filter_found
    def find_in_list(self, query: str, choices: List[str], limit: int = 5) -> List[Tuple[str, int]]:
        return process.extract(query, choices, limit=limit)

    @tuple_to_list
    @filter_found
    def find_one_in_list(self, query: str, choices: List[str]) -> List[Tuple[str, int]]:
        return [process.extractOne(query, choices)]

    @property
    def min_ratio(self) -> int:
        return self.__min_ratio

    @min_ratio.setter
    def min_ratio(self, ratio: int):
        self.__min_ratio = ratio


names = [
    'Есенин Сергей Александрович',
    'Достоевский Фёдор Михайлович',
    'Замятин Евгений Иванович',
    'Чехов Антон Павлович',
    'Александр Сергеевич Пушкин',
    'Крылов Иван Андреевич',
    'Рога Сергей Николаевич',
    'Самуил Яковлевич Маршак',
    'Михаил Афанасьевич Булгаков',
    'Михаил Юрьевич Лермонтов',
]

search = 'Миил ич'

s = FuzzySearcher(50)

match_one = s.find_one_in_list(search, names)
match_many = s.find_in_list(search, names)

print(match_one)
print('*' * 50)
print(match_many)

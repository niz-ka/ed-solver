#!/usr/bin/env python3

from typing import Dict, List

# BEGIN: EDIT HERE

# Values must be Integer, no support for categorical values :(
table = {
    'A': [-2, -2, 0, 0, 2, 2],
    'B': [1, -2, 2, -2, 2, 1],
    'AD': [1, 1, 0, 1, 0, 0],
}

# END: EDIT HERE


def calculate(attr: str, point: int, labels: List[int]) -> None:
    print(f'## Split {attr} <= {point} ##')

    less: Dict[int, int] = {k: 0 for k in labels}
    greater: Dict[int, int] = {k: 0 for k in labels}

    for i in range(len(table[attr])):
        value = table[attr][i]
        label = table[list(table.keys())[-1]][i]
        if value <= point:
            less[label] += 1
        if value > point:
            greater[label] += 1

    print(f'{attr} <= {point}: {greater}')
    print(f'{attr} > {point}: {less}')

    sum_less = sum(less.values())
    sum_greater = sum(greater.values())
    sum_all = sum_less + sum_greater

    gini_less = round(1 - (sum([(i / sum_less)**2 for i in less.values()])), 7)
    gini_greater = round(1 - (sum([(i / sum_greater)**2 for i in greater.values()])), 7)
    gini_split = round((sum_less / sum_all * gini_less) + (sum_greater / sum_all * gini_greater), 7)

    print(f'gini({attr} <= {point}) = {gini_less}')
    print(f'gini({attr} > {point}) = {gini_greater}')
    print(f'gini_split({attr} <= {point}) = {gini_split}')

    print()


def run() -> None:
    points: Dict[str, List[int]] = {k: sorted(set(v))[:-1] for k, v in table.items()}
    points.popitem()

    labels: List[int] = sorted(set(table[list(table.keys())[-1]]))

    for attr, values in points.items():
        for value in values:
            calculate(attr, value, labels)


if __name__ == '__main__':
    run()

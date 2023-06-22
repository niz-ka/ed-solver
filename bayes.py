#!/usr/bin/env python3

from typing import Dict, List
from collections import Counter
from functools import reduce

# BEGIN: EDIT HERE

instance = {
    'A': 1,
    'B': 2,
    'C': 1,
}

# Doesn't solve zero-frequency problem ...
table = {
    'A': [0, 1, 1, 2, 1, 2, 0, 0, 2, 1],
    'B': [2, 2, 1, 0, 1, 2, 1, 0, 1, 0],
    'C': [1, 2, 0, 2, 1, 2, 0, 2, 0, 0],
    'AD': [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
}

# END: EDIT HERE


def count_labels() -> Dict[int, int]:
    name = list(table.keys())[-1]
    labels = sorted(table[name])
    counter = Counter(labels)
    all = sum(counter.values())
    result: Dict[int, int] = {}

    for label, count in counter.items():
        result[label] = count
        print(f'P({name} = {label}) = {count} / {all} = {count / all}')
    print()

    return result


def count_conditional_probs(labels_count: Dict[int, int]) -> Dict[int, List[float]]:
    result: Dict[int, List[float]] = {}

    table_cp = {k: table[k] for k in list(table.keys())[:-1]}
    name = list(table.keys())[-1]
    ad_list = table[list(table.keys())[-1]]

    for right_val, label_count in labels_count.items():
        result[right_val] = []
        for attr, value in table_cp.items():
            left_val = instance[attr]
            counter = 0
            for i, val in enumerate(value):
                if val == left_val and ad_list[i] == right_val:
                    counter += 1
            print(f'P({attr}={left_val}|{name}={right_val}) = {counter} / {label_count} = {counter / label_count}')
            result[right_val].append(counter / label_count)
    print()

    return result


def count_probs(probs: Dict[int, List[float]], labels_count: Dict[int, int]) -> None:
    name = list(table.keys())[-1]
    all = sum(labels_count.values())
    results: Dict[int, float] = {}
    for label, p in probs.items():
        p_str = " * ".join([str(i) for i in p])
        px = labels_count[label] / all
        result = round(reduce(lambda x, y: x * y, p) * px, 7)
        results[label] = result
        print(f'P({instance}|{name}={label}) * P({name}={label}) = {p_str} * {px} = {result}')
    print()

    print(f'Naive Bayes Classifer result {name} =', max(results, key=results.get))


def run() -> None:
    labels_count = count_labels()
    probs = count_conditional_probs(labels_count)
    count_probs(probs, labels_count)


if __name__ == '__main__':
    run()

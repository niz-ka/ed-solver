#!/usr/bin/env python3

import numpy as np

# BEGIN: EDIT HERE

rows = ['a', '~a']
cols = ['b', '~b']

table = np.array([
    [890, 10],
    [10, 90],
])

# END: EDIT HERE


def calculate(row: int, col: int) -> None:
    print(f"### Rule {rows[row]} -> {cols[col]} ###")

    support = table[row][col] / np.sum(table)
    confidence = table[row][col] / np.sum(table[row])
    interest = support / ((np.sum(table[row]) / np.sum(table)) * (np.sum(table[:, col]) / np.sum(table)))
    lift = confidence / (np.sum(table[:, col]) / np.sum(table))

    print(f'sup: {round(support, 7)}')
    print(f'conf: {round(confidence, 7)}')
    print(f'interest: {round(interest, 7)}')
    print(f'lift: {round(lift, 7)}')
    print()


def run() -> None:
    # row, col
    pairs = ((0, 0), (0, 1), (1, 0), (1, 1))

    for pair in pairs:
        calculate(pair[0], pair[1])


if __name__ == '__main__':
    run()

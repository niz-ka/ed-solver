#!/usr/bin/env python3

import pandas as pd
from typing import Dict, Tuple, List

# BEGIN: EDIT HERE

market_basket = {
    'A1': ['C', 'B', 'A', 'C', 'B', 'B'],
    'A2': ['B', 'F', 'F', 'B', 'F', 'C'],
    'A3': ['H', 'S', 'F', 'F', 'G', 'K'],
}

# END: EDIT HERE


def run() -> None:
    table: Dict[Tuple[str, str], List[str]] = {}
    for attr, values in market_basket.items():
        unique_values = sorted(set(values))
        for value in unique_values:
            table[(attr, value)] = ['1' if value == v else '0' for v in values]

    df = pd.DataFrame([i for i in table.values()], [f'{i[0]}.{i[1]}' for i in table.keys()]).T
    print(df)

    print("\nWpakuj to do rules.py jako zmienną market_basket:\n")

    result: Dict[str, List[str]] = {}
    for i, values in df.iterrows():
        result[str(i + 1)] = []
        for j, val in enumerate(values):
            if val == '1':
                result[str(i + 1)].append(str(j + 1))

    print(result)

    print('\nA tu masz do przepisania:\n')

    for key, value in result.items():
        print(f'{key}: {",".join(value)}')


if __name__ == '__main__':
    run()

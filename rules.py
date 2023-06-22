#!/usr/bin/env python3

import itertools
import math
from typing import Dict, List, Tuple

# BEGIN: EDIT HERE

# Always use string as keys and values (string can be numeric Integer, e.g. '2')
market_basket = {
    '1': ['a', 'b', 'd', 'e'],
    '2': ['b', 'c', 'd'],
    '3': ['a', 'b', 'd', 'e'],
    '4': ['a', 'c', 'd', 'e'],
    '5': ['b', 'c', 'd', 'e'],
    '6': ['b', 'd', 'e'],
    '7': ['c', 'd'],
    '8': ['a', 'b', 'c'],
    '9': ['a', 'd', 'e'],
    '10': ['b', 'd'],
}

min_support: float = 0.4
min_confidence: float = 0.7

# END: EDIT HERE


def gte(first: float, second: float) -> bool:
    if math.isclose(first, second) or first > second:
        return True
    return False


def calculate_support(products: Tuple[str]) -> float:
    return sum([1 if set(products).issubset(basket) else 0 for basket in market_basket.values()]) / len(
        market_basket.values())


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))


def create_l_table(c_table: Dict[Tuple[str], float]) -> Dict[Tuple[str], float]:
    l_table: Dict[Tuple[str], float] = {}
    for products, support in c_table.items():
        if gte(support, min_support):
            l_table[products] = support

    return l_table


def create_c_table(l_table: Dict[Tuple[str], float]) -> Dict[Tuple[str], float]:
    size = len(next(iter(l_table))) - 1
    c_table: Dict[Tuple[str], float] = {}

    for pair in itertools.combinations(l_table.keys(), 2):
        if pair[0][:size] == pair[1][:size]:
            new_key = pair[0] + (pair[1][size],)
            c_table[new_key] = calculate_support(new_key)

    return c_table


def pretty_print(header: str, table: Dict[Tuple[str], float]) -> None:
    print('========================================================')
    print(header)
    for prodcuts, support in table.items():
        print(f'{",".join(prodcuts)}: {support}')
    if not table:
        print('∅')


def calculate_confidence(products: Tuple[str], left: Tuple[str]) -> float:
    return sum([1 if set(products).issubset(basket) else 0 for basket in market_basket.values()]) / sum(
        [1 if set(left).issubset(basket) else 0 for basket in market_basket.values()])


def generate_rules(frequent_itemsets: List[Dict[Tuple[str], float]]) -> None:
    rules = []

    for itemset in frequent_itemsets[1:]:
        for products in itemset.keys():
            all_sets = list(powerset(products))
            for subset in all_sets:
                if len(subset) != 0 and len(subset) != len(products):
                    left = subset
                    right = tuple(set(products).difference(subset))
                    support = itemset[products]
                    confidence = calculate_confidence(products, left)
                    is_strong = (gte(confidence, min_confidence) and gte(support, min_support))
                    rules.append((left, right, support, confidence, is_strong))

    print('### Strong rules: ###')
    for rule in rules:
        left, right, support, confidence, is_strong = rule
        if is_strong:
            print(f'{",".join(left)} -> {",".join(right)} | sup: {support} | conf: {confidence} | {is_strong}')

    print('\n### NOT Strong rules: ###')
    for rule in rules:
        left, right, support, confidence, is_strong = rule
        if not is_strong:
            print(f'{",".join(left)} -> {",".join(right)} | sup: {support} | conf: {confidence} | {is_strong}')


def generate_closed_frequent_itemsets(frequent_itemsets: List[Dict[Tuple[str], float]]) -> None:
    print("======================================")
    print("## FREQUENT CLOSED ITEMSETS ##")

    for i in range(len(frequent_itemsets) - 1):
        for first in frequent_itemsets[i]:
            for second in frequent_itemsets[i + 1]:
                support1 = frequent_itemsets[i][first]
                support2 = frequent_itemsets[i + 1][second]
                if set(first).issubset(set(second)) and math.isclose(support1, support2):
                    break
            else:
                print(f"{','.join(first)} | sup: {frequent_itemsets[i][first]}")

    for last, support in frequent_itemsets[len(frequent_itemsets) - 1].items():
        print(f"{','.join(last)} | sup: {support}")

    print("======================================\n")


def generate_maximal_frequent_itemsets(frequent_itemsets: List[Dict[Tuple[str], float]]) -> None:
    print("======================================")
    print("## FREQUENT MAXIMAL ITEMSETS ##")

    joined_itemsets: Dict[Tuple[str], float] = {}
    for itemset in frequent_itemsets:
        joined_itemsets.update(itemset)

    products = list(joined_itemsets.keys())

    for i in range(len(products)):
        for j in range(i + 1, len(products)):
            first = products[i]
            second = products[j]
            if len(second) > len(first) and set(second).issuperset(first):
                break
        else:
            print(f"{','.join(products[i])} | sup: {joined_itemsets[products[i]]}")

    print("======================================\n")


def run():
    # Create first c_table
    all_products: List[str] = weird_sort(list(set(itertools.chain.from_iterable(market_basket.values()))))
    c_table: Dict[Tuple[str], float] = {}
    for product in all_products:
        c_table[(product,)] = calculate_support((product,))

    pretty_print('C1', c_table)

    i = 1
    frequent_itemsets: List[Dict[Tuple[str], float]] = []
    while True:
        l_table = create_l_table(c_table)
        pretty_print(f'L{i}', l_table)
        if len(l_table.keys()) == 0:
            break
        frequent_itemsets.append(l_table)

        i += 1

        c_table = create_c_table(l_table)
        pretty_print(f'C{i}', c_table)

    generate_closed_frequent_itemsets(frequent_itemsets)
    generate_maximal_frequent_itemsets(frequent_itemsets)
    generate_rules(frequent_itemsets)


def weird_sort(array: List[str]) -> List[str]:
    all_int = all([element.isdigit() for element in array])
    none_int = all([not element.isdigit() for element in array])
    if none_int:
        return sorted(array)
    elif all_int:
        return sorted(array, key=lambda x: int(x))
    else:
        raise ValueError('Invalid array to sort!')


if __name__ == '__main__':
    # Sort products in market basket
    for id in market_basket:
        market_basket[id] = weird_sort(market_basket[id])

    run()

"""
Author: Avo-Catto
Page: algorythms.py
Note: containing the algorythms
"""
from itertools import combinations
import json, os

# functions
def get_weight_worth(item):
    item_list =  json.load(open("./items.json", "r")) # "Key":[weight, worth]
    weight = 0.0
    worth = 0.0
    
    try:
        _ = item_list["zero"]
    except:
        item_list.update({"zero":[0.0, 0.0]})

    for i in item:
        weight += item_list[i][0]
        worth += item_list[i][1]
    
    return weight, worth

# algorythms
def recursion(items:tuple, max_weight:float, best_comb:list=[0.0, 0.0, None], count:int=1) -> tuple:
    overflow = True
    combs = tuple(combinations(items, count))

    for item in combs:
        foo = get_weight_worth(item)

        if all((
                foo[0] <= best_comb[0], # best_comb = [weight, worth, items]
                foo[1] > best_comb[1]
            )) or all((
                foo[1] > best_comb[1], 
                foo[0] <= max_weight
            )):

            best_comb[0] = foo[0]
            best_comb[1] = foo[1]
            best_comb[2] = item
        
        if foo[0] < max_weight:
            overflow = False
    
    if not overflow:
        return recursion(items=items, max_weight=max_weight, best_comb=best_comb, count=count + 1)
    else:
        return best_comb


def recursively_algorythm(weight_limit):
    item_list =  json.load(open("./items.json", "r")) # "Key":[weight, worth]

    try: del item_list['zero']
    except: ...

    backpack = recursion(items=item_list, max_weight=weight_limit)

    return backpack


def greedy_algorythm(weight_limit):
    item_list =  json.load(open("./items.json", "r")) # "Key":[weight, worth]

    try:
        _ = item_list["zero"]
    except:
        item_list.update({"zero":[0.0, 0.0]})

    backpack = []
    overflow = False
    weight = 0.0
    worth = 0.0

    while not overflow:
        best_item = "zero"

        for item in item_list:
            if item_list[item][1] > item_list[best_item][1] and item_list[item][0] <= (weight_limit - weight) and item not in backpack:
                best_item = item

        if best_item == "zero":
            overflow = True

        else:
            backpack.append(best_item)
            weight += item_list[best_item][0]
            worth += item_list[best_item][1]
    
    return (backpack, worth, weight)


def smart_greedy_algorithm(weight_limit):
    item_list =  json.load(open("./items.json", "r")) # "Key":[weight, worth]

    try:
        _ = item_list["zero"]
    except:
        item_list.update({"zero":[0.0, 0.0]})

    backpack = []
    overflow = False
    weight = 0.0
    worth = 0.0

    while not overflow:
        best_item = ["zero", 0, False] # [key, distance between weight and worth, True if worth > weight else False]
        overflow = True

        for item in item_list:
            if item_list[item][0] < item_list[item][1] and (item_list[item][1] - item_list[item][0]) > best_item[1] and item_list[item][0] <= (weight_limit - weight) and item not in backpack:
                best_item = [item, item_list[item][1] - item_list[item][0], True]
                overflow = False
            
            elif item_list[item][0] > item_list[item][1] and not best_item[2] and (item_list[item][0] - item_list[item][1]) < best_item[1] and item_list[item][0] <= (weight_limit - weight) and item not in backpack:
                best_item = [item, item_list[item][1] - item_list[item][0], False]
                overflow = False
            
            else:
                pass

        if not overflow:
            weight += item_list[best_item[0]][0]
            worth += item_list[best_item[0]][1]
            backpack.append(best_item[0])
    
    return (backpack, worth, weight)


# file check
def check_file():
    if not os.path.exists("./items.json"):
        with open("./items.json", "w+") as file:
            file.write('{"zero":[0.0, 0.0]}')

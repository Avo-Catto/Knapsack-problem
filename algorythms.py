"""
> Contains algorythms.
"""

from itertools import combinations
import json, os

# functions
def get_weight_worth(item:list) -> tuple:
    """Returning weight and worth of parsed item list."""
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
def recursively_algorythm(weight_limit:float) -> tuple:
    """Calculating weight and worth for every combination."""
    item_list =  json.load(open("./items.json", "r")) # "Key":[weight, worth]

    try:
        _ = item_list["zero"]
    except:
        item_list.update({"zero":[0.0, 0.0]})

    backpack = [0.0, 0.0, None]
    weight = 0.0
    worth = 0.0
    amount = 0
    overflow = False
    selection = []
    
    while not overflow:
        overflow = True

        amount += 1
        combis = combinations(item_list, amount)

        for item in combis:
            weight, worth = get_weight_worth(item)
            selection.append([weight, worth, item])

            if weight <= weight_limit:
                overflow = False

    for items in selection:
        if items[0] <= weight_limit and items[1] > backpack[1]:
            backpack = items
        
    return backpack

def greedy_algorythm(weight_limit:float) -> tuple:
    """Searching for item with highest worth."""
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
            if all((
                    item_list[item][1] > item_list[best_item][1], 
                    item_list[item][0] <= (weight_limit - weight), 
                    item not in backpack
            )):

                best_item = item

        if best_item == "zero":
            overflow = True

        else:
            backpack.append(best_item)
            weight += item_list[best_item][0]
            worth += item_list[best_item][1]
    
    return (backpack, worth, weight)


def smart_greedy_algorithm(weight_limit:float) -> tuple:
    """Calculating distance between weight and worth of items."""
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
            if all((
                    item_list[item][0] < item_list[item][1],
                    (item_list[item][1] - item_list[item][0]) > best_item[1], 
                    item_list[item][0] <= (weight_limit - weight), 
                    item not in backpack
            )):
                
                best_item = [item, item_list[item][1] - item_list[item][0], True]
                overflow = False
            
            elif all((
                    item_list[item][0] > item_list[item][1], 
                    not best_item[2], 
                    (item_list[item][0] - item_list[item][1]) < best_item[1], 
                    item_list[item][0] <= (weight_limit - weight), 
                    item not in backpack
            )):

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
def check_file() -> None:
    """Creates file if not exist."""
    if not os.path.exists("./items.json"):
        with open("./items.json", "w+") as file:
            file.write('{"zero":[0.0, 0.0]}')

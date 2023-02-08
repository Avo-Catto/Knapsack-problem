"""
> Used to create random items.
"""

import json, random

rounds = int(input("How much items you like to have?\n\nUser:"))
items = {}

for i in range(0, rounds):
    items.update({f"item{i}": [round(float(random.randint(10, 100)*0.1), 2), round(float(random.randint(10, 100)*0.1), 2)]})


with open(f"items.json", "w") as file:
    json.dump(items, file)

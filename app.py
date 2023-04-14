from random import choices, randint, choice

from fastapi import FastAPI
from fastapi.responses import JSONResponse

BURGAPI_VERSION = 0.3

# out of 100
CHEESE_CHANCE = 90
MUSTARD_CHANCE = 65

TOPPINGS_MIN = 1
TOPPINGS_MAX = 3
SAUCES_MIN = 1
SAUCES_MAX = 3
SLOP_EM_UP = 11


app = FastAPI(redoc_url="/docs", docs_url=None)

ingredienttypes = ("meat", "prep", "cheeses", "toppings", "sauces", "mustard", "bun")

# load ingredients files
burgerdata = {}
for i in ingredienttypes:
    burgerdata[i] = [
        j for j in open(f"./ingredients/{i}.txt", "r").read().split("\n") if len(j) > 1
    ]


def generate_burger():
    burger = {}

    # required ingredients
    for i in ("bun", "meat", "prep"):
        burger[i] = [choice(burgerdata[i])]

    # good chance of cheese
    if randint(0, 100) < CHEESE_CHANCE:
        burger["cheeses"] = [choice(burgerdata["cheeses"])]
    else:
        burger["cheeses"] = None

    # 1 or 2 toppings
    burger["toppings"] = list(
        set([choice(burgerdata["toppings"]) for i in range(TOPPINGS_MIN, TOPPINGS_MAX)])
    )

    # a 90% chance for the max sauces to be 2, a 10% chance for the max sauces to be 10
    sauce_max_roulette = choices([SAUCES_MAX, (SLOP_EM_UP)], [0.90, 0.10])
    burger["sauces"] = list(
        set([choice(burgerdata["sauces"]) for i in range(SAUCES_MIN, sauce_max_roulette)])
    )

    # pretty good chance of mustard
    if randint(0, 100) < MUSTARD_CHANCE:
        burger["mustard"] = [choice(burgerdata["mustard"])]
    else:
        burger["mustard"] = None

    return burger


def humanize_burger(burger):
    """turn our burger into a nice string to read"""
    flattened_burger = []
    for i in ingredienttypes:
        if burger[i]:
            flattened_burger.extend(burger[i])
    return_string = f"{flattened_burger[0]} ({flattened_burger[1]}) with "
    return_string += ", ".join(flattened_burger[2:-2])
    return_string += " and " + flattened_burger[-2]
    return_string += " on " + flattened_burger[-1]
    return return_string


@app.get("/")
def getburger():
    b = generate_burger()
    rt = {"burger": b, "humanized": humanize_burger(b)}
    return JSONResponse(rt)

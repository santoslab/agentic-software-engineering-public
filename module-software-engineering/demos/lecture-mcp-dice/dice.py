"""Stage A: bounded ordinary functions, also usable through a JSON CLI."""
import argparse
import json
import random

ALLOWED_SIDES = (4, 6, 8, 10, 12, 20)


def bounded_count(count: int, limit: int) -> None:
    if type(count) is not int or not 1 <= count <= limit:
        raise ValueError(f"count must be an integer between 1 and {limit}")


def roll(count: int = 1, sides: int = 6) -> dict:
    bounded_count(count, 20)
    if type(sides) is not int or sides not in ALLOWED_SIDES:
        raise ValueError(f"sides must be one of {ALLOWED_SIDES}")
    rolls = [random.randint(1, sides) for _ in range(count)]
    return {"rolls": rolls, "total": sum(rolls), "sides": sides}


def flip_coins(count: int = 1) -> dict:
    bounded_count(count, 100)
    flips = "".join(random.choice("HT") for _ in range(count))
    return {"flips": flips, "heads": flips.count("H"), "tails": flips.count("T")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool", choices=["roll", "flip_coins"])
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--sides", type=int, default=6)
    args = parser.parse_args()
    try:
        print(json.dumps(roll(args.count, args.sides) if args.tool == "roll"
                         else flip_coins(args.count)))
    except ValueError as exc:
        parser.error(str(exc))

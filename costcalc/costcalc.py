import argparse
import csv
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]

RECIPES_PATH = ROOT_PATH / "data" / "recipes.csv"
PRICES_PATH = ROOT_PATH / "data" / "vendor_prices.csv"

def normalize_price(purchase_unit: str, cost: float):
    conversions = {
        "50lb_case": 50,
        "25lb_case": 25,
        "lb": 1,
        "gallon": 1,
        "#10_can": 1,
    }

    if purchase_unit not in conversions:
        return cost

    divisor = conversions[purchase_unit]

    return cost / divisor

def load_vendor_prices():
    prices = {}

    with PRICES_PATH.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            raw_cost = float(row["cost"])

            normalized_cost = normalize_price(
                row["purchase_unit"],
                raw_cost
            )

            prices[row["ingredient"]] = {
                "purchase_unit": row["purchase_unit"],
                "cost": normalized_cost,
            }

    return prices


def cost_recipe(recipe_name: str):
    prices = load_vendor_prices()

    with RECIPES_PATH.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        recipe_rows = [
            row for row in reader
            if row["recipe"] == recipe_name
        ]

    if not recipe_rows:
        print(f"Recipe not found: {recipe_name}")
        return

    base_portions = float(recipe_rows[0]["base_portions"])
    total_cost = 0

    print("\n===================================")
    print(" TenzoToolkit Recipe Cost Calculator")
    print("===================================\n")

    print(f"Recipe: {recipe_name}")
    print(f"Base Portions: {base_portions:g}\n")

    print("Ingredient Costs")
    print("-----------------------------------")

    for row in recipe_rows:
        ingredient = row["ingredient"]
        quantity = float(row["quantity"])
        unit = row["unit"]

        if ingredient not in prices:
            print(f"{ingredient:<20} price missing")
            continue

        ingredient_cost = prices[ingredient]["cost"] * quantity
        unit_cost = prices[ingredient]["cost"]
        total_cost += ingredient_cost

        print(
            f"{ingredient:<20}"
            f"{quantity:>8.2f} {unit:<8}"
            f"@ ${unit_cost:>6.2f} "
            f"= ${ingredient_cost:>7.2f}"
        )

    cost_per_portion = total_cost / base_portions

    print("-----------------------------------")
    print(f"Total Batch Cost:     ${total_cost:.2f}")
    print(f"Cost Per Portion:     ${cost_per_portion:.2f}")

def main():
    parser = argparse.ArgumentParser(
        description="TenzoToolkit Recipe Cost Calculator"
    )

    parser.add_argument(
        "recipe",
        help="Recipe name to cost"
    )

    args = parser.parse_args()

    cost_recipe(args.recipe)


if __name__ == "__main__":
    main()

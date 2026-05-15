import argparse
import csv
from pathlib import Path

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "recipes.csv"
)


def scale_recipe(recipe_name: str, target_portions: float):
    with DATA_PATH.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        rows = [
            row for row in reader
            if row["recipe"] == recipe_name
        ]

    if not rows:
        print(f"Recipe not found: {recipe_name}")
        return

    base_portions = float(rows[0]["base_portions"])

    scale_factor = target_portions / base_portions

    print("\n===================================")
    print(" TenzoToolkit Prep Calculator")
    print("===================================\n")

    print(f"Recipe: {recipe_name}")
    print(f"Base Portions: {base_portions:g}")
    print(f"Target Portions: {target_portions:g}")
    print(f"Scale Factor: {scale_factor:.2f}\n")

    print("Scaled Ingredients")
    print("-----------------------------------")

    for row in rows:
        quantity = float(row["quantity"])

        scaled_quantity = quantity * scale_factor

        print(
            f"{row['ingredient']:<20}"
            f"{scaled_quantity:>8.2f} "
            f"{row['unit']}"
        )

def calculate_yield(raw_weight: float, yield_percent: float):
    usable_yield = raw_weight * (yield_percent / 100)

    waste_loss = raw_weight - usable_yield

    print("\n===================================")
    print(" TenzoToolkit Yield Calculator")
    print("===================================\n")

    print(f"Raw Weight:      {raw_weight:.2f} lb")
    print(f"Yield %:         {yield_percent:.2f}%")
    print(f"Usable Yield:    {usable_yield:.2f} lb")
    print(f"Trim/Waste Loss: {waste_loss:.2f} lb")

def estimate_portions(total_amount: float, portion_size: float, unit: str):
    portions = total_amount / portion_size

    print("\n===================================")
    print(" TenzoToolkit Portion Estimator")
    print("===================================\n")

    print(f"Total Amount: {total_amount:.2f} {unit}")
    print(f"Portion Size: {portion_size:.2f} {unit}")
    print(f"Estimated Portions: {portions:.2f}")

def convert_units(amount: float, from_unit: str, to_unit: str):
    conversions = {
        ("lb", "oz"): 16,
        ("oz", "lb"): 1 / 16,
        ("gal", "qt"): 4,
        ("qt", "gal"): 1 / 4,
        ("qt", "cup"): 4,
        ("cup", "qt"): 1 / 4,
        ("cup", "floz"): 8,
        ("floz", "cup"): 1 / 8,
        ("tbsp", "tsp"): 3,
        ("tsp", "tbsp"): 1 / 3,
    }

    key = (from_unit, to_unit)

    if key not in conversions:
        print(f"Conversion not available: {from_unit} to {to_unit}")
        return

    converted = amount * conversions[key]

    print("\n===================================")
    print(" TenzoToolkit Unit Converter")
    print("===================================\n")

    print(f"{amount:.2f} {from_unit} = {converted:.2f} {to_unit}")

def main():
    parser = argparse.ArgumentParser(
        description="TenzoToolkit Kitchen Prep Calculator"
    )

    subparsers = parser.add_subparsers(dest="command")

    scale_parser = subparsers.add_parser(
        "scale",
        help="Scale a recipe"
    )

    scale_parser.add_argument(
        "recipe",
        help="Recipe name"
    )

    scale_parser.add_argument(
        "portions",
        type=float,
        help="Target portions"
    )

    yield_parser = subparsers.add_parser(
        "yield",
        help="Calculate edible yield"
    )

    yield_parser.add_argument(
        "raw_weight",
        type=float,
        help="Raw starting weight"
    )

    yield_parser.add_argument(
        "yield_percent",
        type=float,
        help="Yield percentage"
    )

    portions_parser = subparsers.add_parser(
        "portions",
        help="Estimate number of portions from total amount"
    )

    portions_parser.add_argument(
        "total_amount",
        type=float,
        help="Total prepared amount"
    )

    portions_parser.add_argument(
        "portion_size",
        type=float,
        help="Single portion size"
    )

    portions_parser.add_argument(
        "unit",
        help="Unit of measurement"
    )

    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert between common kitchen units"
    )

    convert_parser.add_argument(
        "amount",
        type=float,
        help="Amount to convert"
    )

    convert_parser.add_argument(
        "from_unit",
        help="Starting unit"
    )

    convert_parser.add_argument(
        "to_unit",
        help="Target unit"
    )

    args = parser.parse_args()

    if args.command == "scale":
        scale_recipe(
            args.recipe,
            args.portions
        )
    elif args.command == "yield":
        calculate_yield(
            args.raw_weight,
            args.yield_percent
        )
    elif args.command == "portions":
        estimate_portions(
            args.total_amount,
            args.portion_size,
            args.unit
        )
    elif args.command == "convert":
        convert_units(
            args.amount,
            args.from_unit,
            args.to_unit
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

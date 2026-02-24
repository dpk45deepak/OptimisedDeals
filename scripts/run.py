import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from smart_grocery_optimizer.data_loader import load_data
from smart_grocery_optimizer.recommender import recommend


def main():
    families, shops, inventory = load_data()

    family_id = input("Family ID: ")
    item_name = input("Item Name: ")
    quantity = float(input("Quantity: "))

    result = recommend(
        family_id,
        item_name,
        quantity,
        families,
        shops,
        inventory,
    )

    print("\n===== RESULT =====")

    if "error" in result:
        print(result["error"])
    else:
        for k, v in result.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
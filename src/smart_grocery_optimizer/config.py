from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

FAMILIES_FILE = DATA_DIR / "families.csv"
SHOPS_FILE = DATA_DIR / "shops.csv"
INVENTORY_FILE = DATA_DIR / "inventory.csv"

DISTANCE_WEIGHT = 0.3
PRICE_WEIGHT = 0.5
RATING_WEIGHT = 0.2
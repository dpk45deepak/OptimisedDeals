import pandas as pd
from .config import FAMILIES_FILE, SHOPS_FILE, INVENTORY_FILE


def load_data():
    families = pd.read_csv(FAMILIES_FILE)
    shops = pd.read_csv(SHOPS_FILE)
    inventory = pd.read_csv(INVENTORY_FILE)
    return families, shops, inventory
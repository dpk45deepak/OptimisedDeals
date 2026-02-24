class Family:
    def __init__(self, row):
        self.id = row["family_id"]
        self.lat = row["latitude"]
        self.lon = row["longitude"]
        self.budget = row["monthly_grocery_budget"]


class Shop:
    def __init__(self, row):
        self.id = row["shop_id"]
        self.name = row["shop_name"]
        self.lat = row["latitude"]
        self.lon = row["longitude"]
        self.rating = row["rating"]
import pandas as pd
from .models import Family, Shop
from .graph import build_graph
from .dijkstra import dijkstra
from .optimizer import optimize_shops


def recommend(family_id, item_name, quantity, families_df, shops_df, inventory_df):

    family_row = families_df[families_df["family_id"] == family_id]
    if family_row.empty:
        return {"error": "Family not found"}

    family = Family(family_row.iloc[0])

    shops = [Shop(row) for _, row in shops_df.iterrows()]

    graph = build_graph(family, shops)
    distances = dijkstra(graph)

    item_rows = inventory_df[
        inventory_df["item_name"].str.lower().str.contains(item_name.lower())
    ]

    if item_rows.empty:
        return {"error": "Item not available"}

    results = []

    for _, inv in item_rows.iterrows():
        if inv["stock_quantity"] < quantity:
            continue

        total_cost = inv["price_per_unit"] * (
            1 - inv["discount_percent"] / 100
        ) * quantity

        if total_cost > family.budget:
            continue

        shop_row = shops_df[shops_df["shop_id"] == inv["shop_id"]].iloc[0]

        results.append({
            "shop_id": shop_row["shop_id"],
            "shop_name": shop_row["shop_name"],
            "total_cost": total_cost,
            "distance": distances[shop_row["shop_id"]],
            "rating": shop_row["rating"]
        })

    if not results:
        return {"error": "No valid shop found"}

    df = pd.DataFrame(results)
    ranked = optimize_shops(df)

    return ranked.iloc[0].to_dict()
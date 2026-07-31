import pandas as pd
from .models import Family, Shop
from .graph import build_graph
from .dijkstra import dijkstra
from .optimizer import optimize_shops


def recommend_many(family_id, item_name, quantity, families_df, shops_df, inventory_df, top_n=5):
    family_row = families_df[families_df["family_id"] == family_id]
    if family_row.empty:
        return []

    family = Family(family_row.iloc[0])

    shops = [Shop(row) for _, row in shops_df.iterrows()]

    graph = build_graph(family, shops)
    distances = dijkstra(graph)

    item_rows = inventory_df[
        inventory_df["item_name"].str.lower().str.contains(item_name.lower(), na=False)
    ]

    if item_rows.empty:
        return []

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
            "total_cost": round(total_cost, 2),
            "distance": round(distances[shop_row["shop_id"]], 2),
            "rating": round(shop_row["rating"], 2),
        })

    if not results:
        return []

    df = pd.DataFrame(results)
    ranked = optimize_shops(df)

    return ranked.head(top_n).to_dict(orient="records")


def recommend(family_id, item_name, quantity, families_df, shops_df, inventory_df):
    ranked_results = recommend_many(
        family_id,
        item_name,
        quantity,
        families_df,
        shops_df,
        inventory_df,
        top_n=1,
    )

    if not ranked_results:
        return {"error": "No valid shop found"}

    return ranked_results[0]
import pandas as pd
from .distance import haversine
from .config import DISTANCE_WEIGHT, PRICE_WEIGHT, RATING_WEIGHT


def normalize_column(series):
    if series.max() == 0:
        return 1
    return series / series.max()


def recommend_shop_for_item(
    family_id,
    item_name,
    quantity,
    families_df,
    shops_df,
    inventory_df,
):

    # Check family exists
    family_data = families_df[families_df["family_id"] == family_id]
    if family_data.empty:
        return {"error": "Family ID not found."}

    family = family_data.iloc[0]

    # Filter inventory for item
    item_data = inventory_df[
        inventory_df["item_name"].str.lower() == item_name.lower()
    ]

    if item_data.empty:
        return {"error": f"{item_name} not available in any shop."}

    results = []

    for _, inv_row in item_data.iterrows():

        # Skip if stock insufficient
        if inv_row["stock_quantity"] < quantity:
            continue

        shop_data = shops_df[shops_df["shop_id"] == inv_row["shop_id"]]
        if shop_data.empty:
            continue

        shop = shop_data.iloc[0]

        # Calculate final price with discount
        unit_price = inv_row["price_per_unit"]
        discount = inv_row["discount_percent"]
        final_unit_price = unit_price * (1 - discount / 100)

        total_cost = final_unit_price * quantity

        # Check budget
        if total_cost > family["monthly_grocery_budget"]:
            continue

        # Calculate distance
        distance = haversine(
            family["latitude"],
            family["longitude"],
            shop["latitude"],
            shop["longitude"],
        )

        results.append({
            "shop_id": shop["shop_id"],
            "shop_name": shop["shop_name"],
            "unit_price": round(final_unit_price, 2),
            "total_cost": round(total_cost, 2),
            "distance": round(distance, 2),
            "rating": shop["rating"]
        })

    if not results:
        return {"error": "No shop satisfies stock and budget constraints."}

    result_df = pd.DataFrame(results)

    # Normalization (safe)
    result_df["price_score"] = 1 - normalize_column(result_df["total_cost"])
    result_df["distance_score"] = 1 - normalize_column(result_df["distance"])
    result_df["rating_score"] = result_df["rating"] / 5

    result_df["final_score"] = (
        PRICE_WEIGHT * result_df["price_score"]
        + DISTANCE_WEIGHT * result_df["distance_score"]
        + RATING_WEIGHT * result_df["rating_score"]
    )

    best = result_df.sort_values(by="final_score", ascending=False).iloc[0]

    return {
        "recommended_shop": best["shop_name"],
        "shop_id": best["shop_id"],
        "unit_price": best["unit_price"],
        "total_cost": best["total_cost"],
        "distance_km": best["distance"],
        "rating": best["rating"],
        "score": round(best["final_score"], 3),
    }
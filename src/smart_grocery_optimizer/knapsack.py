def knapsack(items, budget):
    n = len(items)
    dp = [[0 for _ in range(int(budget) + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        price, value = items[i - 1]
        for w in range(int(budget) + 1):
            if price <= w:
                dp[i][w] = max(value + dp[i - 1][int(w - price)], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][int(budget)]
# 🛒 Smart Grocery Optimization Engine

> 🚀 A Python-based, constraint-aware grocery recommendation system  
> that helps families choose the best grocery shop based on budget, distance, price, stock availability, and ratings.

---

## 📌 Problem Statement

Urban families often struggle to:

- 🏷 Compare grocery prices across shops  
- 💰 Stay within budget  
- 📍 Minimize travel distance  
- 📦 Ensure stock availability  
- ⭐ Choose high-rated stores  

This project simulates a real-world grocery optimization engine using algorithmic decision-making and optimization techniques.

---

## 🧠 Key Features

- ✅ Family-specific recommendations  
- 💰 Budget constraint enforcement  
- 📦 Stock availability validation  
- 📍 Geo-distance calculation (Haversine Formula)  
- 🗺 Graph-based shop modeling  
- 🛣 Dijkstra-based shortest path mapping  
- 🎯 Multi-factor scoring (Price + Distance + Rating)  
- 🧩 Modular, clean, and scalable architecture  

---

## 🏗 Project Architecture

```
CSV Data
   │
   ▼
Data Loader → Models → Graph → Dijkstra
                               │
                               ▼
                    Optimizer (Multi-Factor Scoring)
                               │
                               ▼
                        Recommender
                               │
                               ▼
                           CLI Output
```

---

## 📂 Project Structure

```
smart-grocery-optimizer/
│
├── data/
│   └── raw/                      # CSV datasets
│
├── src/smart_grocery_optimizer/
│   ├── config.py
│   ├── data_loader.py
│   ├── models.py
│   ├── distance.py
│   ├── graph.py
│   ├── dijkstra.py
│   ├── knapsack.py
│   ├── optimizer.py
│   └── recommender.py
│
└── scripts/
    └── run.py                    # CLI entry point
```

---

## 🧮 Algorithms Used

### 📍 Haversine Formula
Calculates real-world geographical distance (in kilometers) between families and grocery shops.

### 🗺 Graph Modeling
Models Family → Shops relationships as a weighted graph.

### 🛣 Dijkstra Algorithm
Computes shortest distance efficiently between nodes.

### 🎯 Multi-Objective Optimization
Weighted scoring system combining:

- 💰 Price  
- 📍 Distance  
- ⭐ Rating  

---

## ⚙️ Requirements

- Python 3.10+
- pandas
- uv (recommended for dependency management)

---

## ▶️ How To Run

### 1️⃣ Install Dependencies

```bash
uv add pandas
```

_or using pip:_

```bash
pip install pandas
```

---

### 2️⃣ Run the Project

```bash
uv run python scripts/run.py
```

_or_

```bash
python scripts/run.py
```

---

### 3️⃣ Provide Input

```
Family ID: F001
Item Name: Rice
Quantity: 5
```

---

## 🧪 Sample Output

```
===== RESULT =====
shop_id: S002
shop_name: Big Bazaar Hyper
total_cost: 215.0
distance: 6.4 km
rating: 4.5
final_score: 0.812
```

---

## 📊 Dataset Overview

The system uses realistic Delhi NCR simulated data:

- 👨‍👩‍👧 50 Families  
- 🏬 20 Grocery Shops  
- 📦 Inventory dataset with price, stock, and discounts  

---

## 🚀 Future Improvements

- 🛒 Multi-item cart optimization (Knapsack Algorithm)
- 🚚 Delivery cost modeling
- 📦 Bulk discount optimization
- 🔎 Fuzzy item name matching
- 🌐 FastAPI REST API service
- 📊 Interactive Dashboard (Streamlit)
- 🤖 ML-based price prediction
- 🧪 Automated unit testing

---

## 🧩 Design Philosophy

- Clean modular architecture
- Separation of concerns
- Scalable optimization logic
- Real-world inspired constraints
- Easy extensibility for API or dashboard layer

---

## 🤝 Contributing

Contributions are welcome! 🎉

### Ways to Contribute

- Improve multi-item optimization
- Enhance scoring logic
- Implement advanced knapsack strategies
- Add test coverage
- Improve performance
- Add REST API layer
- Build UI dashboard

### Steps

1. Fork the repository  
2. Create a new branch  
3. Make your changes  
4. Submit a Pull Request 🚀  

Let’s build something amazing together.

---

## 👨‍💻 Author

**Deepak Kumar**  
Full Stack Developer & Aspiring Data Engineer  

---

## 📜 License

This project is open-source and available under the MIT License.
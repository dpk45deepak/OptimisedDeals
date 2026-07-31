import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from smart_grocery_optimizer.data_loader import load_data
from smart_grocery_optimizer.recommender import recommend_many


class RecommendManyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.families, cls.shops, cls.inventory = load_data()

    def test_recommend_many_returns_ranked_shops(self):
        results = recommend_many(
            "F001",
            "rice",
            5,
            self.families,
            self.shops,
            self.inventory,
            top_n=3,
        )

        self.assertTrue(results)
        self.assertLessEqual(len(results), 3)
        self.assertIn("shop_name", results[0])
        self.assertIn("final_score", results[0])


if __name__ == "__main__":
    unittest.main()

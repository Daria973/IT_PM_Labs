import unittest
from code import ClothingRecommendation  # type: ignore

class TestWeatherApp(unittest.TestCase):

    def test_recommend_outfit(self):
        recommendation = ClothingRecommendation()
        outfit = recommendation.recommend_outfit('Сонячно', 30)
        self.assertEqual(outfit, "Легкий одяг, капелюх та сонцезахисні окуляри") 

if __name__ == '__main__':
    unittest.main()

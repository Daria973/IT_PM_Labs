import unittest
import tkinter as tk
from main import WeatherForecast

class TestWeatherApp(unittest.TestCase):

    def test_get_date_list(self):
        app = WeatherForecast(tk.Tk())
        date_list = app.get_date_list()
        self.assertEqual(len(date_list), 5) 
 
if __name__ == '__main__':
    unittest.main()

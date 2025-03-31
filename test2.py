import unittest
import tkinter as tk
from code import WeatherForecast  # type: ignore

class TestWeatherApp(unittest.TestCase):

    def test_build_url(self):
        app = WeatherForecast(tk.Tk())
        url = app.build_url('Kyiv', 'Tomorrow')
        expected_url = 'https://www.google.com/search?q=Kyiv+weather+Tomorrow'
        self.assertEqual(url, expected_url) 

if __name__ == '__main__':
    unittest.main()

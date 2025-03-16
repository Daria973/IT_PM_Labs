import tkinter as tk
from tkinter import ttk
import requests
import bs4
from datetime import datetime, timedelta
from googletrans import Translator
import calendar
import locale

class WeatherForecast:
    def __init__(self, root): #Ініціалізує клас WeatherForecast.
        
        self.root = root
        self.clothing_recommendation = ClothingRecommendation()  # Створення об'єкту ClothingRecommendation
        self.create_widgets()

    def create_widgets(self): #Створює віджети GUI для відображення погоди.
        
        self.canvas = tk.Canvas(self.root, height=600, width=1200)
        self.canvas.pack()

        # self.img = tk.PhotoImage(file='new1.png')
        # self.label = tk.Label(self.root, image=self.img)
        # self.label.place(relwidth=1, relheight=1)

        self.frame = tk.Frame(self.root, bg='#373552', bd=3)
        self.frame.place(relx=0.5, rely=0.1, relwidth=0.92, relheight=0.1, anchor='n')

        self.frame1 = tk.Frame(self.root, bg='#373552', bd=3)
        self.frame1.place(relx=0.5, rely=0.22, relwidth=0.92, relheight=0.1, anchor='n')

        self.label1 = tk.Label(self.frame1, text="Оберіть дату для прогнозу >>>>", font=('calibre', 16, 'italic'), bg='white')
        self.label1.place(relwidth=0.696, relheight=1)

        days = self.get_date_list()
        self.spinbox = ttk.Combobox(self.frame1, values=days, font=('calibre', 16, 'italic'), justify=tk.CENTER)
        self.spinbox.place(relx=0.7, relheight=1, relwidth=0.3)
        self.spinbox.set(days[0])  # Значення по замовчуванню - сьогодні

        self.entry = tk.Entry(self.frame, font=('calibre', 16, 'italic'), justify=tk.CENTER)
        self.entry.place(relwidth=0.696, relheight=1)
        self.entry.insert(0, "Введіть назву міста")

        self.frame2 = tk.Frame(self.root, bg='#373552', bd=3)
        self.frame2.place(relx=0.5, rely=0.34, relwidth=0.92, relheight=0.6, anchor='n')

        self.label2 = tk.Label(self.frame2, text="", font=('calibre', 15, 'bold'), bg='white', justify=tk.LEFT, anchor='c')
        self.label2.place(relwidth=0.55, relheight=1)

        self.label_weather = tk.Label(self.frame2, text="", bg='white', anchor='c')
        self.label_weather.place(relx=0.5, relwidth=0.5, relheight=1)

        self.button = tk.Button(self.frame, text="Отримати прогноз", font=('calibre', 16, 'italic'), command=self.weather)
        self.button.place(relx=0.7, relheight=1, relwidth=0.3)

    def weather(self): #Метод, який отримує погодні дані за введеним містом та обраною датою.
        
        city_name = self.entry.get()
        if not city_name:
            print("Enter city name")
            return

        translator = Translator()
        translated_city_name = translator.translate(city_name, src='uk', dest='en').text

        selected_day = self.spinbox.get()
        date = datetime.strptime(selected_day, "%d/%m")

        days = (date - datetime.now()).days
        if days == 0:
            days = "Now"
        elif days == 1:
            days = "Tomorrow"
        else:
            days = f"{date.strftime('%A')}"

        url = self.build_url(translated_city_name, days)
        request = self.make_request(url)
        soup = self.parse_html(request)

        try:
            location_text, time_date_text, weather_text, temperature_text = self.extract_data(soup)

            # Додавання погодніх умов до виводу
            output_text = self.format_output(location_text, time_date_text, weather_text, temperature_text)

            # Отримання рекомендацій щодо одягу
            clothing_recommendation = self.clothing_recommendation.recommend_outfit(weather_text, float(temperature_text))

            # Додавання рекомендацій щодо одягу до виводу
            output_text += f"\n\nРекомендований одяг:\n{clothing_recommendation}"

            self.label2.config(text=output_text)

            weather_img = self.get_weather_image(weather_text)
            self.label_weather.config(image=weather_img)
            self.label_weather.image = weather_img
        except Exception as e:
            print("Error:", e)
            print("Failed to extract data from HTML.")

    def build_url(self, city_name, days): #Метод, що будує URL для запиту погодних даних.
        
        return 'https://www.google.com/search?q=%s+weather+%s' % (city_name, days)

    def make_request(self, url): #Метод, що відправляє HTTP-запит на вказаний URL.
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
        return requests.get(url, headers=headers)

    def parse_html(self, request): #Метод, що розбирає HTML-відповідь та повертає розібраний об'єкт BS4.
        
        request.raise_for_status()
        return bs4.BeautifulSoup(request.text, "html.parser")

    def extract_data(self, soup): #Метод, що видобуває необхідні дані з розібраного HTML.
        
        temperature = soup.select('#wob_t')
        timedate = soup.select('#wob_dts')
        location = soup.select('#wob_loc')
        weathercondition = soup.select('#wob_dc')

        if not temperature or not timedate or not location or not weathercondition:
            raise ValueError("Failed to find necessary elements in HTML.")

        location_text = location[0].text
        time_date_text = timedate[0].text
        weather_text = weathercondition[0].text
        temperature_text = temperature[0].text
        return location_text, time_date_text, weather_text, temperature_text

    def format_output(self, location_text, time_date_text, weather_text, temperature_text):
        #Метод, що форматує виведення погодних даних.
        formatted_date = self.spinbox.get()
        day, month = map(int, formatted_date.split('/'))

        # Українські назви днів тижня
        ukrainian_days = ["понеділок", "вівторок", "середа", "четвер", "п'ятниця", "субота", "неділя"]

        # Визначення дня тижня за допомогою datetime
        day_of_week = datetime(datetime.now().year, month, day).weekday()

        # Вибір української назви дня тижня
        ukrainian_day_of_week = ukrainian_days[day_of_week]

        return f"День: {formatted_date} ({ukrainian_day_of_week})\n\nПогода: {weather_text}\n\nТемпература: {temperature_text} градусів Цельсія\n\n"
    
    def get_weather_image(self, weather_text): #Метод, що повертає зображення погоди для відображення.
        
        if weather_text in ('Сонячно', 'Ясно'):
            return tk.PhotoImage(file="sunny.png")
        elif weather_text in ('Переважно сонячно','Переважно хмарно', 'Хмарно', 'Мінлива хмарність', 'Частково сонячно'):
            return tk.PhotoImage(file="mostlysunny.png")
        elif weather_text in ('Гроза', 'Ізольовані грози', 'Розсіяні грози'):
            return tk.PhotoImage(file="thunderstorms.png")
        elif weather_text == 'Туман':
            return tk.PhotoImage(file="fog.png")
        elif weather_text in ('Зливи','Дощ', 'Місцями зливи'):
            return tk.PhotoImage(file="download.png")
        else:
            return tk.PhotoImage(file="def.png")

    def get_date_list(self): #Метод, що повертає список дат на кілька днів вперед.
        
        today = datetime.now()
        dates = [today + timedelta(days=i) for i in range(5)]
        date_str = [date.strftime("%d/%m") for date in dates]
        return date_str

class ClothingRecommendation:
    def __init__(self):
        pass

    def recommend_outfit(self, weather_text, temperature): #Метод, що рекомендує вибір одягу залежно від погодних умов та температури.
        
        if weather_text in ('Сонячно', 'Ясно'):
            if temperature >= 25:
                return "Легкий одяг, капелюх та сонцезахисні окуляри"
            elif temperature >= 20:
                return "Футболка, шорти, капелюх та сонцезахисні окуляри"
            elif temperature >= 15:
                return "Футболка, штани та легка куртка"
            elif temperature >= 10:
                return "Кофта, штани та легка куртка"
            elif temperature <= 0:
                return "Кофта, штани, тепла куртка, шапка, рукавиці"
            else:
                return "Штани, светр та куртка"

        elif weather_text in ('Переважно сонячно', 'Переважно хмарно', 'Хмарно', 'Мінлива хмарність', 'Частково сонячно', 'Туман'):
            if temperature >= 25:
                return "Легкий одяг та сонцезахисні окуляри"
            elif temperature >= 20:
                return "Футболка та шорти"
            elif temperature >= 15:
                return "Кофта, штани та легка куртка"
            elif temperature >= 10:
                return "Кофта, штани та легка куртка"
            elif temperature <= 0:
                return "Кофта, штани, тепла куртка, шапка, рукавиці"
            else:
                return "Штани, светр та куртка"
            
        elif weather_text in ('Гроза', 'Ізольовані грози', 'Розсіяні грози', 'Зливи','Дощ', 'Місцями зливи'):
            if temperature >= 25:
                return "Легкий одяг та парасолька"
            elif temperature >= 20:
                return "Футболка, шорти та парасолька"
            elif temperature >= 15:
                return "Кофта, штани, легка куртка та парасолька"
            elif temperature >= 10:
                return "Кофта, штани, легка куртка та парасолька"
            elif temperature <= 0:
                return "Кофта, штани, тепла куртка, шапка, рукавиці"
            else:
                return "Штани, светр, куртка та парасолька"

        else:
            return "Погодні умови не знайдено"

class App:
    def __init__(self, root): #Ініціалізує клас App та створює екземпляр WeatherForecast.
        
        self.weather_forecast = WeatherForecast(root)
        self.clothing_recommendation = ClothingRecommendation()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Прогноз погоди")
    app = App(root)
    root.mainloop()
    print("Hello everyone!")
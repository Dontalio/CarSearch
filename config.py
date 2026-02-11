from selenium.webdriver import ChromeOptions
from decouple import config


class BrowserSet:
    BASE_URL = config('BASE_URL')
    END_URL =  config('END_URL')
    @staticmethod
    def chrome_setup():
        options = ChromeOptions()
        options.add_argument('--headless=new')  # скрытый режим, чтоб не "открывать" браузер визуально.
        options.add_argument('--window-size=1920,1080')

        options.add_argument('--disable-blink-features=AutomationControlled')  # Скрываем автоматизацию
        options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Скрываем автоматизацию
        options.add_experimental_option('useAutomationExtension', False)  # Скрываем автоматизацию

        # Скрываем автоматизацию. Имитация реального пользователя
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")

        # Дополнительные опции для стабильности
        options.add_argument('--no-sandbox')  # Для Linux/docker
        options.add_argument('--disable-dev-shm-usage')  # Для ограниченной памяти
        options.add_argument('--disable-gpu')  # Если есть проблемы с GP

        prefs = {"profile.managed_default_content_settings.images": 2}  # экономия ресурсов отключаем изображения.
        options.add_experimental_option("prefs", prefs)

        return options

    @classmethod
    def create_url(cls, car_number : str) -> str:
        car_number = car_number.upper()
        url = cls.BASE_URL + car_number + cls.END_URL
        return url


class BotSet:
    BOT_TOKEN = config("TOKEN")
    ADMINS = config("ADMINS")
    FUNC_LIST = {
        'start': 'Первый и повторный запуск бота, регистрация',
        'search_car': 'search_car AA999A',
    }


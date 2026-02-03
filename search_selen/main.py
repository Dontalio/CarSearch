from selenium import webdriver
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from get_cars.config import BrowserSet as BS


def search_car(plate : str) -> str:
    options = BS.chrome_setup()
    browser = webdriver.Chrome(options=options)
    url = BS.create_url(plate)
    try:
        browser.get(url=url)
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "report-short-page"))
        )
        print(f'{browser.title} : открыта страница')
    except Exception as e:
        print(f'Error {e}')
        browser.quit() # закроем и всё.


    try:
        element = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "report-header__car-title"))
            )
        return element.text
    except Exception as e:
        print(f'Error in search {e}')
        browser.quit()  # закроем и всё.


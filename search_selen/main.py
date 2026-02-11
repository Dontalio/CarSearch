from selenium import webdriver
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from get_cars.config import BrowserSet as BS


async def search_car(plate : str) -> None | list[[str, str],]:
    options = BS.chrome_setup()
    browser = webdriver.Chrome(options=options)
    url = BS.create_url(plate)
    title = 'пустая информация'
    try:
        browser.get(url=url)
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.ID, "report-short-page"))
        )
        print(f'{browser.title} : открыта страница')
        title = str(browser.title)

    except Exception as e:
        print(f'Error in first step search : {e}')
        browser.quit() # закроем и всё.
        return


    try:
        # info_car = browser.find_element(By.XPATH, "//*[contains(text(), 'кг')]")
        info_car =  browser.find_element(By.ID, 'identifiers')
        print(info_car)
        #find_el_name = browser.find_elements(By.XPATH, ".//span[contains(@class, 'lcn-list__cell lcn-list__cell_left')]")
        find_el_value = browser.find_elements(By.XPATH, ".//span[contains(@class, 'sn-list__result')]")
        find_el_name = [elemento.find_element(By.XPATH, "ancestor::li") for elemento in find_el_value]
        print(f'найдено названий {len(find_el_name)} и значений {len(find_el_value)}')

        # допрасить последовательно структуру. Учти, что тут много одноимённых классов
        res_set = []
        for elemento in find_el_name:
            new_elemento = elemento.text.split('\n')
            if len(new_elemento) == 2:
                res_set.append(new_elemento)
        browser.quit()
        return res_set

    except Exception as e:
        print(f'Error in search {e}')
        browser.quit()  # закроем и всё.
        return



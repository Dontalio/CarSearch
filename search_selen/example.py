from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Настройка драйвера
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')  # Скрываем автоматизацию
browser = webdriver.Chrome(options=options)

try:
    # 1. Открываем страницу
    url = "https://selectel.ru/blog/"  # URL из HTML
    browser.get(url)
    print(f"Открыта страница: {browser.current_url}")

    # 2. Ждем полной загрузки страницы
    time.sleep(3)  # Базовая задержка для начальной загрузки

    # 3. Проверяем, что страница загружена
    if "selectel" in browser.title.lower():
        print(f"Заголовок страницы: {browser.title}")
    else:
        print("Страница не загрузилась корректно")

    # 4. Ищем элемент с разными стратегиями
    wait = WebDriverWait(browser, 15)  # Увеличиваем время ожидания

    # Способ 1: Поиск по CSS селектору (надежнее, чем по классу)
    try:
        open_search = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".header__btn-search"))
        )
        print("✓ Элемент найден по CSS селектору")
    except Exception as e:
        print(f"✗ Не удалось найти по CSS: {e}")

        # Способ 2: Поиск по XPath (более гибкий)
        try:
            open_search = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'header__btn-search')]"))
            )
            print("✓ Элемент найден по XPath")
        except Exception as e:
            print(f"✗ Не удалось найти по XPath: {e}")

            # Способ 3: Ищем все кнопки с похожими классами
            buttons = browser.find_elements(By.TAG_NAME, "button")
            print(f"Найдено кнопок на странице: {len(buttons)}")

            for i, btn in enumerate(buttons):
                class_attr = btn.get_attribute('class')
                if class_attr and 'search' in class_attr.lower():
                    print(f"Найдена кнопка поиска #{i}: класс='{class_attr}'")
                    open_search = btn
                    break
            else:
                print("Кнопка поиска не найдена среди всех кнопок")
                raise Exception("Элемент не найден")

    # 5. Выводим информацию о найденном элементе
    print(f"Текст элемента: {open_search.text}")
    print(f"Класс элемента: {open_search.get_attribute('class')}")
    print(f"Тип элемента: {open_search.tag_name}")

    # 6. Проверяем видимость элемента
    if open_search.is_displayed():
        print("✓ Элемент видим на странице")
    else:
        print("⚠ Элемент есть в DOM, но скрыт")
        # Прокручиваем к элементу
        browser.execute_script("arguments[0].scrollIntoView(true);", open_search)
        time.sleep(1)

    # 7. Пробуем кликнуть
    try:
        open_search.click()
        print("✓ Клик выполнен успешно")

        # Ждем появления модального окна поиска
        time.sleep(5)

        # Проверяем, появилось ли модальное окно поиска
        search_modals = browser.find_elements(By.CLASS_NAME, "search-modal")
        if search_modals:
            print("✓ Модальное окно поиска открылось")
        else:
            print("✗ Модальное окно поиска не открылось")

    except Exception as e:
        print(f"✗ Не удалось кликнуть: {e}")

        # Альтернативный способ клика через JavaScript
        print("Пробуем клик через JavaScript...")
        browser.execute_script("arguments[0].click();", open_search)
        time.sleep(2)

    # 8. Делаем скриншот для проверки
    browser.save_screenshot("search_button_found.png")
    print("Скриншот сохранен как 'search_button_found.png'")

    # 9. Ждем немного для визуальной проверки
    time.sleep(3)

except Exception as e:
    print(f"Произошла ошибка: {type(e).__name__}: {e}")

    # Сохраняем HTML для отладки
    with open("debug_page.html", "w", encoding="utf-8") as f:
        f.write(browser.page_source)
    print("HTML страницы сохранен в 'debug_page.html'")

finally:
    # Закрываем браузер
    input("Нажмите Enter для закрытия браузер...")
    browser.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Функция для перехода на страницу и извлечения параграфов
def navigate_to_page(browser, url):
    browser.get(url)
    time.sleep(3)
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    return paragraphs


# Функция для вывода параграфов статьи
def read_paragraphs(paragraphs):
    for i, paragraph in enumerate(paragraphs):
        print(paragraph.text)
        next_action = input(
            "\nНажмите Enter для перехода к следующему параграфу или введите 'q' для выхода: ").strip().lower()
        if next_action == 'q':
            break


# Основная функция для работы с программой
def wikipedia_browser():
    browser = webdriver.Chrome()
    try:
        # 1. Получаем первоначальный запрос от пользователя
        initial_query = input("Введите поисковый запрос на Википедии: ").strip()
        search_url = f"https://ru.wikipedia.org/wiki/{initial_query}"

        paragraphs = navigate_to_page(browser, search_url)

        while True:
            # 3. Предлагаем пользователю выбор действий
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")
            choice = input("Ваш выбор: ").strip()

            if choice == '1':
                read_paragraphs(paragraphs)
            elif choice == '2':
                # Находим связанные страницы (внутренние ссылки)
                links = browser.find_elements(By.XPATH,
                                              "//div[@id='bodyContent']//a[@href and not(contains(@href, ':'))]")
                if not links:
                    print("Не удалось найти связанных страниц.")
                    continue

                # Выводим список доступных ссылок
                print("\nСвязанные страницы:")
                for idx, link in enumerate(links[:10], 1):
                    print(f"{idx}. {link.text}")

                link_choice = input("Выберите номер страницы для перехода или введите 'q' для отмены: ").strip()
                if link_choice == 'q':
                    continue

                try:
                    selected_link = links[int(link_choice) - 1]
                    new_url = selected_link.get_attribute("href")
                    paragraphs = navigate_to_page(browser, new_url)
                except (IndexError, ValueError):
                    print("Некорректный выбор. Попробуйте снова.")
            elif choice == '3':
                print("Выход из программы.")
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")
    finally:
        browser.quit()


# Запуск программы
wikipedia_browser()

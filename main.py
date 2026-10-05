import time
import csv
from selenium.webdriver.common.by import By
from web_driver_manager import WebDriverManager


def main():
    manager = WebDriverManager()
    driver = manager.setup_driver()

    try:
        # Open hotel service website
        driver.get('https://ostrovok.ru/')
        time.sleep(15)

        # Search for hotels by city
        city_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="destination-input"]')
        city_input.clear()
        city_input.send_keys('Москва')
        time.sleep(15)

        search_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="search-button"]')
        search_button.click()
        time.sleep(10)

        # Select the hotel category filter
        select_category_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div[1]/div/div[2]/div[1]/button[2]')
        select_category_button.click()
        time.sleep(10)

        # Extract hotel links from search results
        hotel_cards = driver.find_elements(By.CSS_SELECTOR, '.HotelListDatefull_card__Z82uV')

        def get_reviews(driver):
            reviews_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[1]/div[1]/div[3]/div[1]/div/div[3]/span/button/div')
            reviews_button.click()
            time.sleep(10)

        def open_review_details(driver):
            review_details_button = driver.find_element(By.CLASS_NAME, 'Review_detailesLink__UQAEU')
            review_details_button.click()
            time.sleep(10)

        def expand_review(driver):
            expand_review_button = driver.find_element(By.XPATH, "//button[contains(normalize-space(.), 'Развернуть отзыв')]")
            expand_review_button.click()
            time.sleep(10)

        def get_ratings(driver):
            labels = driver.find_elements(By.CSS_SELECTOR, '.Review_detailedWrapper__DyLCF p:first-child')
            values = driver.find_elements(By.CSS_SELECTOR, 'p.Review_detailedValue__hym1s')
            return {label.text.strip(): value.text.strip() for label, value in zip(labels, values)}

        def get_review_text(driver):
            review = driver.find_element(By.CLASS_NAME, 'Review_inner__Fy5av')
            return review.text.strip()

        hotel_links = []

        for hotel_card in hotel_cards:
            hotel_link = hotel_card.find_element(By.CSS_SELECTOR, '[data-testid="hotel-card-name"]')
            hotel_links.append(hotel_link.get_attribute('href'))

        print(f'Найдено ссылок: {len(hotel_links)}')

        # Save scraped review data to CSV
        def save_reviews_to_csv():
            filename = 'hotel_reviews.csv'
            with open(filename, 'w', newline='', encoding='utf-8') as file:

                writer = csv.writer(file, delimiter=',')

                writer.writerow([
                    'Cleanliness',
                    'Location',
                    'Price/Quality',
                    'Service',
                    'Room',
                    'Food',
                    'Text',
                ])

                for hotel_link in hotel_links:

                    try:
                        print(f'\nОбрабатываем: {hotel_link}')

                        driver.get(hotel_link)
                        time.sleep(10)
                        get_reviews(driver)
                        open_review_details(driver)
                        expand_review(driver)
                        ratings = get_ratings(driver)
                        review_text = get_review_text(driver)

                        row = [
                            ratings.get('Чистота', ''),
                            ratings.get('Расположение', ''),
                            ratings.get('Цена/Качество', ''),
                            ratings.get('Обслуживание', ''),
                            ratings.get('Номер', ''),
                            ratings.get('Питание', ''),
                            review_text
                        ]

                        writer.writerow(row)
                        file.flush()

                        print(f'Получены оценки: {row}')

                    except Exception as ex:
                        print(f'Ошибка при обработке отеля {hotel_link}: {ex}')
                        continue

            print(f'\nГотово! Результат сохранён в файл: {filename}')

        save_reviews_to_csv()

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()

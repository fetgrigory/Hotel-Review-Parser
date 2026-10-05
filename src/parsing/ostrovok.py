import time
import csv
from selenium.webdriver.common.by import By


class OstrovokParser:
    def __init__(self, driver):
        self.driver = driver

    # Open hotel service website
    def open_site(self):
        self.driver.get('https://ostrovok.ru/')
        time.sleep(15)

    # Search for hotels by city
    def search_city(self, city):
        city_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="destination-input"]')
        city_input.clear()
        city_input.send_keys(city)
        time.sleep(15)

        search_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="search-button"]')
        search_button.click()
        time.sleep(10)

    # Select the hotel category filter
    def select_category(self):
        select_category_button = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div[1]/div/div[2]/div[1]/button[2]')
        select_category_button.click()
        time.sleep(10)

    def get_reviews(self):
        reviews_button = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[1]/div[1]/div[3]/div[1]/div/div[3]/span/button/div')
        reviews_button.click()
        time.sleep(10)

    def expand_review(self):
        expand_review_button = self.driver.find_elements(By.XPATH, "//button[contains(normalize-space(.), 'Развернуть отзыв')]")
        for button in expand_review_button:
            button.click()
            time.sleep(10)

    def get_ratings(self):
        labels = self.driver.find_elements(By.CSS_SELECTOR, '.Rating_detailedWrapper__D78k3 p:first-child')
        values = self.driver.find_elements(By.CSS_SELECTOR, '.Rating_detailedWrapper__D78k3 p:last-child')
        return {label.text.strip(): value.text.strip() for label, value in zip(labels, values)}

    def get_review_text(self):
        reviews = self.driver.find_elements(By.CLASS_NAME, 'Review_inner__Fy5av')
        texts = []
        for review in reviews:
            texts.append(review.text.strip())
        return texts

    # Extract hotel links from search results
    def get_hotel_links(self):
        hotel_cards = self.driver.find_elements(By.CSS_SELECTOR, '.HotelListDatefull_card__Z82uV')

        hotel_links = []

        for hotel_card in hotel_cards:
            hotel_link = hotel_card.find_element(By.CSS_SELECTOR, '[data-testid="hotel-card-name"]')
            hotel_links.append(hotel_link.get_attribute('href'))

        return hotel_links

    # Save scraped review data to CSV
    def save_reviews_to_csv(self, hotel_links):
        filename = 'hotel_reviews.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as file:

            writer = csv.writer(file, delimiter=',')

            writer.writerow([
                'review_id',
                'cleanliness',
                'hygiene',
                'location',
                'price',
                'service',
                'room',
                'food',
                'wifi',
                'text',
            ])
            empty_ratings = [''] * 8
            review_id = 1

            for hotel_link in hotel_links:
                try:
                    print(f'\nОбрабатываем: {hotel_link}')

                    self.driver.get(hotel_link)
                    time.sleep(10)
                    self.get_reviews()
                    self.expand_review()
                    ratings = self.get_ratings()
                    review_texts = self.get_review_text()

                    rating_row = [
                        ratings.get('Чистота', ''),
                        ratings.get('Средства гигиены', ''),
                        ratings.get('Расположение', ''),
                        ratings.get('Цена/Качество', ''),
                        ratings.get('Обслуживание', ''),
                        ratings.get('Номер', ''),
                        ratings.get('Питание', ''),
                        ratings.get('Качество Wi-Fi', ''),
                    ]

                    rows = [[''] + rating_row] + [
                        [review_id + i] + empty_ratings + [text]
                        for i, text in enumerate(review_texts)
                    ]
                    review_id += len(review_texts)

                    for row in rows:
                        writer.writerow(row)
                        file.flush()

                        print(f'Получены оценки: {row}')

                except Exception as ex:
                    print(f'Ошибка при обработке отеля {hotel_link}: {ex}')
                    continue

        print(f'\nГотово! Результат сохранён в файл: {filename}')

    def run(self, city):
        self.open_site()
        self.search_city(city)
        self.select_category()

        hotel_links = self.get_hotel_links()
        print(f'Найдено ссылок: {len(hotel_links)}')

        self.save_reviews_to_csv(hotel_links)

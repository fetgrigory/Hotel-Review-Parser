import time
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
        сity_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="destination-input"]')
        сity_input.clear()
        сity_input.send_keys('Москва')
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

        hotel_links = []

        for hotel_card in hotel_cards:
            hotel_link = hotel_card.find_element(By.CSS_SELECTOR, '[data-testid="hotel-card-name"]')
            hotel_links.append(hotel_link.get_attribute('href'))

        print(f'Найдено ссылок: {len(hotel_links)}')

        for hotel_link in hotel_links:
            print(hotel_link)

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()

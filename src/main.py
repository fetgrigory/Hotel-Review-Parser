import traceback
from src.browser_manager import WebDriverManager
from src.parsing.ostrovok import OstrovokParser


def main():
    manager = WebDriverManager()
    driver = manager.setup_driver()

    try:
        OstrovokParser(driver).run(city='Москва')
    except Exception:
        traceback.print_exc()
    finally:
        driver.quit()


if __name__ == '__main__':
    main()

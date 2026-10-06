import logging
import os
import traceback

from src.browser_manager import WebDriverManager
from src.parsing.ostrovok import OstrovokParser

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/parser.log',
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
    encoding='utf-8'
)

logger = logging.getLogger(__name__)


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

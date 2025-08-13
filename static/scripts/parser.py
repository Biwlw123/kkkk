from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time, re
from bs4 import BeautifulSoup


def parse(vin, wait_time=15):
    driver = None  # Инициализируем заранее
    
    try:
        # Инициализация драйвера (без перезаписи None!)
        driver = uc.Chrome(headless=True)
        
        # Открытие страницы
        url = f"https://statenumber.ru/gosnomer/{vin}"
        print(f"Открываю страницу: {url}")
        driver.get(url)
        
        # Ожидание
        print(f"Жду {wait_time} секунд...")
        time.sleep(wait_time)
        
        # Получение HTML
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        number = soup.find(id="dataGosnomer")
        color = soup.find(id="dataColor")
        brand_and_year = soup.find(class_="resultAutoH1")
        img = soup.find('div', class_='resultAutoCardPhotoImg').attrs['style']

        result = {
            'number': number.text if number else '',
            'color': color.text if color else '',
            'release_year': brand_and_year.text.split(', ', maxsplit=1)[1] if brand_and_year else '',
            'brand': brand_and_year.text.split(', ', maxsplit=1)[0] if brand_and_year else '',
            'image': re.search(r'url\(["\']?(.*?)["\']?\)', img)[1] if img else ''
        }

        print(result)
        return result
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {'number': '', 'color': '', 'release_year': '', 'brand': '', 'image': ''}
    finally:
        if driver is not None:  # Закрываем driver, если он был создан
            driver.quit()

# Пример использования
if __name__ == "__main__":
    vin = "WVGZZZCAZJC558510"
    parse(vin)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import time
from bs4 import BeautifulSoup
import os
import json

def scrape_dynamic_content(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless') 
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Inisialisasi webdriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=chrome_options
    )
    
    try:
        driver.get(url)
        # time.sleep(30)
        '''Close Policy Overlay'''
        exit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mt-cb-policy-close"))
        )
        exit_button.click()

        '''Change Component To Counter Page'''
        # Menunggu Counter tab dapat diklik
        counters_tab = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'mt-list-item') and span[text()='COUNTERS']]"))
        )
        counters_tab.click() # Klik page counter
        
        # Menunggu data muncul
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mt-2684369'))  # Counter score class name 
        )
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mt-2684562'))  # Compatibility score class name
        )
        
        '''Scraping the data on the first component page'''
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        
        first_counter_score = soup.find_all('div', class_='mt-2684369')  
        first_compatibility_score = soup.find_all('div', class_='mt-2684562')
        print("First Component Score")
        for score in first_counter_score:
            print(score.text)
        for score in first_compatibility_score:
            print(score.text)

        # time.sleep(30)
        '''Scraping the data on the second component page'''
        second_counter_component = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'mt-list-item') and span[text()='Most Countered by']]"))
        )
        second_counter_component.click()

        # Menunggu page kedua counter score untuk load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mt-2684514'))
        )

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        second_counter_score = soup.find_all('div', class_='mt-2684514')
        print("Second Component Score")
        for score in second_counter_score:
            print(score.text)


        # Menunggu page kedua compatibility score untuk load
        second_compatibility_component = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'mt-list-item') and span[text()='Not Compatible']]"))
        )
        second_compatibility_component.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mt-2690829'))
        )

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        second_compatibility_score = soup.find_all('div', class_='mt-2690829')
        for score in second_compatibility_score:
            print(score.text)
        
    finally:
        driver.quit()
        return first_counter_score, second_counter_score, first_compatibility_score, second_counter_score 
    
def main():
    base_url = "https://m.mobilelegends.com/hero/detail?channelid=2819992&heroid=" 
    base_dir = "hero_data"
    os.makedirs(base_dir, exist_ok=True)

    for hero_id in range(1, 128):  # 127 total hero
        url = base_url + str(hero_id)
        print(url)
        print(f"Scraping data for Hero ID: {hero_id}")
        hero_dir = os.path.join(base_dir, f"hero_{hero_id}")
        os.makedirs(hero_dir, exist_ok=True)

        try:
            first_counter_score, second_counter_score, first_compatibility_score, second_compatibility_score = scrape_dynamic_content(url)
            
            data = {
                "counter": [score.text for score in first_counter_score],
                "countered": [score.text for score in second_counter_score],
                "compatible": [score.text for score in first_compatibility_score],
                "incompatible": [score.text for score in second_compatibility_score],
            }

            file_path = os.path.join(hero_dir, "weight.json")
            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
        except Exception as e:
            print(f"Error scraping Hero ID {hero_id}: {e}")

if __name__ == "__main__":
    main()

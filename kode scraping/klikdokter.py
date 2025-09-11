import pandas as pd
import time 
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

# Fungsi buat scrape isi konten artikelnya
def scrape_contents(link):
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    driver.get(link)

    content_text = ""
    try:
        # ambil isi artikel
        content_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'index_wrap-article-detail__dxkF0')) 
        )
        content_text = content_element.text

    except Exception as e:
        print(f"Error scraping content from {link}: {e}")

    driver.close()
    driver.switch_to.window(original_window)
    return content_text    

service = ChromeService('../chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = "https://www.klikdokter.com/info-sehat/berita-kesehatan" 

driver.get(url)
driver.maximize_window()

all_articles_data = []
max_articles = 100  # Batas maksimal artikel yang ingin diambil

click_count = 0
max_clicks = 10  # batas maksimal klik "Muat lebih banyak"

while click_count < max_clicks:
    try:
        muat_lebih_banyak = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'zULNOA3F'))
        )

        # klik pakai JavaScript biar gak ketahan iklan
        driver.execute_script("arguments[0].click();", muat_lebih_banyak)
        click_count += 1
        print(f"'Muat lebih banyak' diklik ke-{click_count}")
        time.sleep(3)  # kasih jeda biar artikel sempet load

    except Exception as e:
        print("Tombol 'Muat lebih banyak' tidak ditemukan atau tidak bisa diklik lagi:", e)
        break


# Jalanin proses scraping
while True:
    if len(all_articles_data) >= max_articles:  # stop kalau sudah 100 artikel
        print("Reached maximum article limit.")
        break

    try:
        # Sesuain dengan elemen yang nyimpan artikel di halaman hasil pencarian
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'container')) 
        )
        print("Articles section loaded.")
    except Exception as e:
        print(f"Articles section did not load: {e}")
        driver.quit()
        exit()
    
    container = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'MDQEq_jB'))
    )
    articles = container.find_elements(By.CLASS_NAME, 'column-article')
    print(f"Found {len(articles)} articles")

    for article in articles:
        try:
            # Sesuain dengan elemen yang ada pada website yang akan di scrape dan masukin ke dalam ()
            title_element = article.find_element(By.XPATH, './/h2')
            tag_element = article.find_element(By.XPATH, '//div[@class="ant-col"]//p[@class="a9mSBAS1"]/a')
            link_element = article.find_element(By.XPATH, './/a')
            date_element = article.find_element(By.CLASS_NAME, 'a9mSBAS1')
            match = re.search(r'(\d{1,2}\s\w+\s\d{4})', date_element.text)

            if match:
                date = match.group(1)

            description_element = article.find_element(By.XPATH, './/p[@class="__6bizoCJ2"]')
            content_element = scrape_contents(link_element.get_attribute('href'))
            
            all_articles_data.append({
                "title": title_element.text,
                "tag": tag_element.text,
                "link": link_element.get_attribute('href'),
                "date": date,
                "description": description_element.text, 
                "content": content_element
            })

            print(f"Scraped article: {title_element.text}")
            print(f"Tag: {tag_element.text}")
            print(f"Link: {link_element.get_attribute('href')}")
            print(f"Date: {date}")
            print(f"Description: {description_element.text}") 
            print(f"Content length: {len(content_element)} characters")
            print("-" * 80)

        except Exception as e:
            print(f"Error extracting article details: {e}")
            continue

print(f"Total articles scraped: {len(all_articles_data)}")
driver.quit()

df = pd.DataFrame(all_articles_data)
nama_web = 'klikdokter' # Isi nama webnya
df.to_csv(f"../artikel/{nama_web}.csv", index=False)
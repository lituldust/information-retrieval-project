import pandas as pd
import time 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

service = ChromeService('chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = "https://www.biofarma.co.id/id/artikel-kesehatan" 

driver.get(url)
driver.maximize_window()

all_articles_data = []
page = 1
max_articles = 100  # Batas maksimal artikel yang ingin diambil

# Fungsi buat scrape isi konten artikelnya
def scrape_contents(link):
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    driver.get(link)

    content_text = ""
    try:
        # ambil isi artikel
        content_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'content__description')) 
        )
        content_text = content_element.text

    except Exception as e:
        print(f"Error scraping content from {link}: {e}")

    driver.close()
    driver.switch_to.window(original_window)
    return content_text

def scrape_date(link):
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    driver.get(link)

    date = ""
    try:
        # ambil isi artikel
        date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'date-heading')) 
        )
        date = date_element.text

    except Exception as e:
        print(f"Error scraping content from {link}: {e}")

    driver.close()
    driver.switch_to.window(original_window)
    return date
    

# Jalanin proses scraping
while True:
    if len(all_articles_data) >= max_articles:  # stop kalau sudah 100 artikel
        print("Reached maximum article limit.")
        break

    print("Scraping page:", page)
    try:
        # Sesuain dengan elemen yang nyimpan artikel di halaman hasil pencarian
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="main-sct pt-9"]')) 
        )
        print("Articles section loaded.")
    except Exception as e:
        print(f"Articles section did not load: {e}")
        driver.quit()
        exit()
    
    container = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="main-sct__cnt"]/div[@class="row row--space"]'))
    )
    articles = container.find_elements(By.CLASS_NAME, 'col-md-4')
    print(f"Found {len(articles)} articles on page {page}")

    for article in articles:
        try:
            # Sesuain dengan elemen yang ada pada website yang akan di scrape dan masukin ke dalam ()
            title_element = article.find_element(By.CLASS_NAME, 'title')
            link_element = article.find_element(By.TAG_NAME, 'a')
            date_element = scrape_date(link_element.get_attribute('href'))
            description_element = article.find_element(By.CLASS_NAME, 'card--cap__cnt') 
            content_element = scrape_contents(link_element.get_attribute('href'))
            
            all_articles_data.append({
                "title": title_element.text,
                "link": link_element.get_attribute('href'),
                "date": date_element,
                "description": description_element.text, 
                "content": content_element
            })

            print(f"Scraped article: {title_element.text}")
            print(f"Link: {link_element.get_attribute('href')}")
            print(f"Date: {date_element}")
            print(f"Description: {description_element.text}") 
            print(f"Content length: {len(content_element)} characters")
            print("-" * 80)

        except Exception as e:
            print(f"Error extracting article details: {e}")
            continue
    
    try:
        # Buat ganti halaman, sesuain sama elemen html yg nyimpen tombol next page
        next_page = page + 1
        next_button = driver.find_elements(By.XPATH, f'//div[@class="pagination"]//a[@aria-label="pagination {next_page}"]') 
        next_page = next_button[0].get_attribute("href")
        driver.get(next_page)
        page += 1

    except Exception as e:
        print("No more pages or error navigating to next page:", e)
        break

print(f"Total articles scraped: {len(all_articles_data)}")
driver.quit()

df = pd.DataFrame(all_articles_data)
df.head()
# %%
nama_web = 'biofarma' # Isi nama webnya
df.to_csv(f"artikel/{nama_web}.csv", index=False)
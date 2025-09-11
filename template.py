import pandas as pd
import time 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

service = ChromeService('../chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Scraping menggunakan kata kunci (opsional)
# query = input("Masukkan kata kunci berita: ")
# query = query.replace(" ", "+")

# Isi URL pake link website yang mau di scrape, yang ada page"nya
url = f"" # Contoh dari kompas -> https://indeks.kompas.com/?site=news

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
        # Ini buat misal isi artikelnya ada banyak trus ada tulisan kaya "read more" atau "show all"
        try:
            # Ini nanti sesuain sama elemen di htmlnya yang buat nampilin semua isi artikel, biasanya kaya tombol "show all" gitu
            show_all = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(()) # Taruh di dalam kurung ini nanti
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", show_all)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", show_all)
            print("Clicked 'Show All News' button")
            time.sleep(2)
        except Exception:
            print("No 'Show All News' button found or not clickable")

        # ambil isi artikel
        content_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(()) # Kasih elemen yang mencakup semua isi artikelnya
        )
        content_text = content_element.text

    except Exception as e:
        print(f"Error scraping content from {link}: {e}")

    driver.close()
    driver.switch_to.window(original_window)
    return content_text

# Jalanin proses scraping
while True:
    print("Scraping page:", page)
    try:
        # Sesuain dengan elemen yang nyimpan artikel di halaman hasil pencarian
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(({})) # Ganti {} dengan By.CLASS_NAME atau By.ID atau By.XPATH sesuai kebutuhan 
        )
        print("Articles section loaded.")
    except Exception as e:
        print(f"Articles section did not load: {e}")
        driver.quit()
        exit()
    
    articles = driver.find_elements(By.XPATH, '//div[@class="articleList -list "]/div[@class="articleItem"]')
    print(f"Found {len(articles)} articles on page {page}")

    for article in articles:
        try:
            # Sesuain dengan elemen yang ada pada website yang akan di scrape dan masukin ke dalam ()
            title_element = article.find_element()
            link_element = article.find_element()
            date_element = article.find_element()
            description_element = article.find_element()
            content_element = scrape_contents(link_element.get_attribute('href'))
            
            if len(all_articles_data) <= max_articles:
                all_articles_data.append({
                    "title": title_element.text,
                    "link": link_element.get_attribute('href'),
                    "date": date_element.text,
                    "description": description_element.text,
                    "content": content_element
                })

                print(f"Scraped article: {title_element.text}")
                print(f"Link: {link_element.get_attribute('href')}")
                print(f"Date: {date_element.text}")
                print(f"Description: {description_element.text}")
                print(f"Content length: {len(content_element)} characters")
                print("-" * 80)

        except Exception as e:
            print(f"Error extracting article details: {e}")
            continue
    
    try:
        # Buat ganti halaman, sesuain sama elemen html yg nyimpen tombol next page
        next_button = driver.find_elements() # Kasih elemen tombol next page ke dalam kurung
        next_page = next_button[0].get_attribute('href') if next_button else None
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
nama_web = '' # Isi nama webnya
df.to_csv(f"{nama_web}.csv", index=False)
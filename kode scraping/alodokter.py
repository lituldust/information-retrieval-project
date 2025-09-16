import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

# Fungsi buat scrape isi artikel detail
def scrape_contents(link):
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    driver.get(link)

    content_text, date_text = "", ""

    try:
        # ambil tanggal artikel
        date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "date-article"))
        )
        date_text = date_element.text.strip()

        # ambil isi artikel
        content_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "postContent"))
        )
        content_text = content_element.text.strip()

    except Exception as e:
        print(f"Error scraping content from {link}: {e}")

    driver.close()
    driver.switch_to.window(original_window)
    return date_text, content_text


service = ChromeService('../chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = "https://www.alodokter.com/"
driver.get(url)
driver.maximize_window()

all_articles_data = []
max_articles = 100   # batas artikel
page = 1

while len(all_articles_data) < max_articles:
    print(f"Scraping page {page}...")

    try:
        container = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-container"))
        )
        articles = container.find_elements(By.TAG_NAME, "card-post-index")
        print(f"Found {len(articles)} articles on page {page}")
    except Exception as e:
        print(f"Articles not found on page {page}: {e}")
        break

    for idx, article in enumerate(articles):
        if len(all_articles_data) >= max_articles:
            break

        try:
            title = article.get_attribute("title")
            url_path = article.get_attribute("url-path")
            link = f"https://www.alodokter.com{url_path}"
            description = article.get_attribute("short-description")
            category = article.get_attribute("category") or "Kesehatan"

            # Scrape detail isi artikel
            date_text, content = scrape_contents(link)

            all_articles_data.append({
                "title": title,
                "tag": category,
                "link": link,
                "date": date_text,
                "description": description,
                "content": content
            })

            print(f"[{len(all_articles_data)}] {title}")
            print(f"Tag: {category}")
            print(f"Description: {description}")
            print(f"Date: {date_text}")
            print(f"Link: {link}")
            print(f"Content length: {len(content)} chars")
            print("-" * 80)

        except Exception as e:
            print(f"Error extracting article {idx}: {e}")
            continue

    try:
        paginate = driver.find_element(By.TAG_NAME, "paginate-button")
        next_page = paginate.get_attribute("next-page")
        base_url = paginate.get_attribute("base-url")
        page_url = paginate.get_attribute("page-url")

        if next_page and next_page != "0":
            next_link = f"https://www.alodokter.com{base_url}{page_url}{next_page}"
            page += 1
            driver.get(next_link)
            time.sleep(3)
        else:
            print("No more pages.")
            break
    except:
        print("Pagination not found.")
        break

print(f"Total articles scraped: {len(all_articles_data)}")
driver.quit()

# Simpan ke CSV
df = pd.DataFrame(all_articles_data)
nama_web = 'alodokter'
df.to_csv(f"{nama_web}.csv", index=False, encoding="utf-8-sig")
print(f"Saved to {nama_web}.csv")
import pandas as pd
import time
import string
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

# Fungsi bikin slug dari title
def make_slug(title):
    slug = title.lower().strip()
    slug = ''.join(c for c in slug if c not in string.punctuation)
    slug = re.sub(r'\s+', '-', slug)
    return slug

# Fungsi buat scrape isi artikel detail
def scrape_contents(link):
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    driver.get(link)

    content_text = ""
    date_text = ""

    try:
        # ambil tanggal artikel
        date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='article-page__reviewer']/span[last()]"))
        )
        date_text = date_element.text

        # ambil isi artikel
        content_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'article-page__article-content-wrapper')) 
        )
        content_text = content_element.text

    except Exception as e:
        print(f"Error scraping content from {link}: {e}")

    driver.close()
    driver.switch_to.window(original_window)
    return date_text, content_text


service = ChromeService('../chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = "https://www.halodoc.com/artikel"
driver.get(url)
driver.maximize_window()

all_articles_data = []
max_articles = 100   # batas artikel yang mau diambil
click_count = 0
max_clicks = 15 
element = driver.find_element(By.CLASS_NAME, "latest-article__ghost")
driver.execute_script("arguments[0].scrollIntoView();", element)
print("Scrolled to bottom of the page.")

while click_count < max_clicks:
    try:
        muat_lebih_banyak = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'load-more-articles'))
        )
        driver.execute_script("arguments[0].click();", muat_lebih_banyak)
        click_count += 1
        print(f"'Muat lebih banyak' diklik ke-{click_count}")
        time.sleep(10)
    except Exception as e:
        print("Tombol 'Muat lebih banyak' tidak ditemukan atau sudah habis:", e)
        break

try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'latest-article-container'))
    )
    print("Articles section loaded.")
except Exception as e:
    print(f"Articles section did not load: {e}")
    driver.quit()
    exit()

articles = driver.find_elements(By.XPATH, '//div[@class="latest-article"]/hd-base-article-card')
print(f"Found {len(articles)} articles")

for idx, article in enumerate(articles):
    if len(all_articles_data) >= max_articles:
        print("Reached maximum article limit.")
        break

    try:
        # Ambil title
        title_element = article.find_element(
            By.CSS_SELECTOR,
            ".hd-base-vertical-card__title, .hd-base-vertical-card_title, .article-card--horizontal__desc__title"
        )
        title = title_element.text.strip()

        # Ambil tag
        tag_elements = article.find_elements(By.ID, "article-lable")
        tags = [tag.text for tag in tag_elements]
        tags_joined = ", ".join(tags)
        if not tags_joined:
            tags_joined = "Umum"  # default tag kalau kosong

        # Ambil deskripsi
        try:
            desc_element = article.find_element(
                By.CSS_SELECTOR,
                "#article-subtitle, .article-card--horizontal__desc__more-info__subtitle"
            )
            description = desc_element.text.strip()
        except:
            description = ""

        # Generate link dari slug
        slug = make_slug(title)
        link = f"https://www.halodoc.com/artikel/{slug}"

        # Scrape isi konten artikel
        date_text, content = scrape_contents(link)

        all_articles_data.append({
            "title": title,
            "tag": tags_joined,
            "link": link,
            "date": date_text,
            "description": description,
            "content": content
        })

        print(f"[{idx+1}] {title}")
        print(f"Tags: {tags_joined}")
        print(f"Desc: {description}")
        print(f"Date: {date_text}")
        print(f"Link: {link}")
        print(f"Content length: {len(content)} chars")
        print("-" * 80)

    except Exception as e:
        print(f"Error extracting article {idx}: {e}")
        continue

print(f"Total articles scraped: {len(all_articles_data)}")
driver.quit()

# Simpan ke CSV
df = pd.DataFrame(all_articles_data)
nama_web = 'halodoc'
df.to_csv(f"../artikel/{nama_web}.csv", index=False, encoding="utf-8-sig")
print(f"Saved to ../artikel/{nama_web}.csv")

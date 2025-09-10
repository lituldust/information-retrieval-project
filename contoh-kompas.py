#%%
import pandas as pd
import time 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# %%
service = ChromeService('../chromedriver.exe')

driver = webdriver.Chrome(service=service)

query = input("Masukkan kata kunci berita: ")
query = query.replace(" ", "+")

url = f"https://search.kompas.com/search?q={query}"

driver.get(url)
driver.maximize_window()

all_articles_data = []
page = 1
# %%
def scrape_contents(link):
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    driver.get(link)

    content_text = ""
    try:
        # coba klik "Show All News" kalau ada
        try:
            show_all = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'show_all_news'))
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
            EC.presence_of_element_located((By.CLASS_NAME, 'read__content'))
        )
        content_text = content_element.text

    except Exception as e:
        print(f"Error scraping content from {link}: {e}")

    driver.close()
    driver.switch_to.window(original_window)
    return content_text
# %%
while True:
    print("Scraping page:", page)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sectionBox'))
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
            title_element = article.find_element(By.CLASS_NAME, 'articleTitle')
            link_element = article.find_element(By.TAG_NAME, 'a')
            date_element = article.find_element(By.CLASS_NAME, 'articlePost-date')
            description_element = article.find_element(By.CLASS_NAME, 'articleLead')
            content_element = scrape_contents(link_element.get_attribute('href'))

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

        next_button = driver.find_elements(By.XPATH, '//div[@class="text-center mt5 clearfix"]/div[@class="paging clearfix"]/div[@class="paging__wrap clearfix"]/div[@class="paging__item"]/a[@class="paging__link paging__link--next"]')
        next_page = next_button[0].get_attribute('href') if next_button else None
        driver.get(next_page)
        page += 1

    except Exception as e:
        print("No more pages or error navigating to next page:", e)
        break

print(f"Total articles scraped: {len(all_articles_data)}")
driver.quit()
# %%
df = pd.DataFrame(all_articles_data)
df.head()
# %%
df.to_csv(f"kompas_{query.replace('+', '_')}.csv", index=False)
# %%

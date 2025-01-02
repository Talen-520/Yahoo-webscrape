from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time

def scrape_yahoo_finance_article(url):
    # https://googlechromelabs.github.io/chrome-for-testing/#stable
    # download chrome driver and place under same directory with your python file
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "content.yf-18q3fnf"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    news_articles = []

    links = soup.find_all('div', class_='content yf-18q3fnf')
    for link in links[:5]:
        a_tag = link.find('a')
        if a_tag:
            news_url = a_tag['href']
            print(news_url)
            try:
                driver.get(news_url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'h1'))
                )

                article_soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # title
                news_title = article_soup.find('h1', class_='cover-title yf-1o1tx8g')
                title_text = news_title.get_text(strip=True) if news_title else "No Title"
                
                # body
                news_body = article_soup.find_all('p', class_='yf-1pe5jgt')
                news_body_text = [p.get_text(strip=True) for p in news_body]
                
                article = {
                    "link": news_url,
                    "title": title_text,
                    "content": news_body_text
                }
                
                news_articles.append(article)
            except Exception as e:
                print(f"Error fetching news article: {e}")
        else:
            print(f"No anchor tag found in div: {link}")

    driver.quit()
    return news_articles

url = "https://finance.yahoo.com/quote/NVDA/"
body = scrape_yahoo_finance_article(url)

json_output = json.dumps(body, indent=2)

print("News Articles:")
print(json_output)

with open('news_articles.json', 'w', encoding='utf-8') as f:
    json.dump(body, f, ensure_ascii=False, indent=2)

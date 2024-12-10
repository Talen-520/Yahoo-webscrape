import requests
from bs4 import BeautifulSoup
import json

def scrape_yahoo_finance_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    news_articles = []
    links = soup.find_all('div', class_='content yf-18q3fnf')
    for link in links[:5]:
        a_tag = link.find('a')
        if a_tag:
            news_url = a_tag['href']
            print(news_url)
            try:
                response = requests.get(news_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find title
                    news_title = soup.find('h1', class_='cover-title yf-1o1tx8g')
                    title_text = news_title.get_text(strip=True) if news_title else "No Title"
                    
                    # Find body
                    news_body = soup.find_all('p', class_='yf-1pe5jgt')
                    news_body_text = [p.get_text(strip=True) for p in news_body]
                    
                    # Create article dictionary
                    article = {
                        "link": news_url,
                        "title": title_text,
                        "content": news_body_text
                    }
                    
                    news_articles.append(article)
                else:
                    print(f"Failed to fetch news article: {news_url}")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching news article: {e}")
        else:
            print(f"No anchor tag found in div: {link}")

    return news_articles

url = "https://finance.yahoo.com/quote/NVDA/"
body = scrape_yahoo_finance_article(url)

# Convert to JSON
json_output = json.dumps(body, indent=2)

print("News Articles:")
print(json_output)

# Optionally, write to a file
with open('news_articles.json', 'w', encoding='utf-8') as f:
    json.dump(body, f, ensure_ascii=False, indent=2)
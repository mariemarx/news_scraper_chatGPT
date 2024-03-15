from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from collections import defaultdict
import json

def is_recent(article_date, days_ago):
    """
    Check if the article has been written within x days
    Two formats: "x days/weeks/months/years ago" or "MMM DD, YYYY"
    """
    result = True
    if article_date.endswith("ago"):
        period = article_date[2]
        quantity = int(article_date[0])
        if period == "d":
            result = True
        elif period == "w":
            result = 7 * quantity <= days_ago
        elif period == "m":
            result = 30 * quantity <= days_ago
        else:
            result = 365 * quantity <= days_ago
    else:
        date_obj = datetime.strptime(article_date, "%b %d, %Y")
        difference = datetime.now() - date_obj
        result = difference <= timedelta(days_ago)
    return result

def extract_article_info(article):
    """
    Extract information from each article: link, domain, title, destription, date
    """
    result = None
    try:
        article_link = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
        article_info = article.find_elements(By.CSS_SELECTOR, 'a>div>div>div')
        domain = article_info[1].text
        title = article_info[2].text
        description = article_info[3].text
        article_date = article_info[4].text

        result = {
            "Link:": article_link,
            "Domain:": domain,
            "Title:": title,
            "Description:": description,
            "Date:": article_date
        }
    
    except Exception as e:
        print(e)

    return result

def process_link(base_url, driver, days_ago):
    """
    For a page of the news search, extract info for each article
    Make sure the article published within days_ago
    """
    driver.get(base_url)
    WebDriverWait(driver, 10)
    news_page = driver.find_elements(By.CSS_SELECTOR, 'div#rso>div>div>div>div')
    results = []
    for article in news_page:
        article_info = extract_article_info(article)
        if article_info and is_recent(article_info["Date:"], days_ago):
            results.append(article_info)
    return results

def save_to_json(d, filename):
    """
    Save extracted information for each article into JSON
    """
    with open(filename, "w") as out_file:
        json.dump(d, out_file, indent=6)

def retrieve_article_info(base_url, driver, num_pages, days_ago):
    """
    Access the news url and save the article information
    """
    retrieved_info = defaultdict(dict)

    for page_num in range(num_pages):
        url = base_url if page_num == 0 else f'{base_url}&start={page_num * 10}'
        articles_info = process_link(url, driver, days_ago)
        for news_item in articles_info:
            retrieved_info[news_item["Link:"]] = news_item

    driver.quit()
    save_to_json(retrieved_info, "retrieved-info.json")

    for article in retrieved_info.values():
        print(article["Domain:"])
        print(article["Title:"])
        print(article["Description:"])
        print(article["Date:"])
        print()

base_url = 'https://www.google.com/search?q=hottest+korean+movies+2024&tbm=nws'
num_pages = 5
days_ago = 45
retrieve_article_info(base_url, driver=webdriver.Chrome(), num_pages=num_pages, days_ago=days_ago)
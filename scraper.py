from bs4 import BeautifulSoup
from selenium import webdriver

import urllib.parse
import cache
import bot

BASE_URL = "https://www.upwork.com/nx/search/jobs?sort=recency&q="

driver = webdriver.Firefox()

def read_search_terms() -> list[str]:
    with open("./config/search_terms.txt", "r") as f:
        return f.readlines()

def get_html() -> list[str]:
    htmls = []

    for search_term in read_search_terms():
        driver.refresh()
        driver.get(BASE_URL+urllib.parse.quote_plus(search_term))

        html = driver.page_source

        htmls.insert(0, html)

    return htmls

async def parse_jobs():
    htmls = get_html()
    for html in htmls:
        soup = BeautifulSoup(html, 'html.parser')

        articles = soup.find_all("article")

        for article in articles:
            title = article.select("div.job-tile-header > div.job-tile-header-line-height > div > div > h2 > a")
            details = article.select("div[data-test='JobTileDetails'] > div[data-test*='JobDescription'] > div > p")

            if len(title) == 0 or len(details) == 0:
                print("title or description is empty")
                continue

            url = title[0].get("href")
            title_str: str = title[0].encode_contents(encoding='utf-8').decode()
            description_str: str = details[0].encode_contents(encoding='utf-8').decode()

            title_str = title_str.replace('<span class="highlight">', "")
            title_str = title_str.replace('</span>', "")
            description_str = description_str.replace('<span class="highlight">', "")
            description_str = description_str.replace('</span>', "")

            if cache.check_cache(title_str):
                continue

            try:
                await bot.send_alert(title_str, description_str, url)
            except Exception as e:
                print(e)
                continue

            cache.cache_job(title_str, description_str)

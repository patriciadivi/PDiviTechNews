import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url: str, wait: int = 1):
    try:
        response = requests.get(
            url, timeout=wait, headers={"user-agent": "Fake user-agent"}
        )
        response.raise_for_status()
        time.sleep(1)
    except (requests.HTTPError, requests.ReadTimeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content):
    getSelector = Selector(html_content)
    news = list()

    for each_line in getSelector.css(".archive-main > .entry-preview"):
        linkNew = each_line.css(".entry-title > a::attr(href)").get()
        news.append(linkNew)
    return news


# Requisito 3
def scrape_next_page_link(html_content):
    getSelector = Selector(html_content)

    nextPage = getSelector.css(
        ".nav-links > a.next.page-numbers::attr(href)"
    ).get()

    if not nextPage:
        return None
    else:
        return nextPage


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""

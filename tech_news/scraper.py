import time
import requests
from tech_news.database import create_news
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
    getSelector = Selector(html_content)

    resultComments = getSelector.css(".comment-list li").getall()

    return {
        "url": getSelector.css("link[rel=canonical]::attr(href)").get(),
        "title": getSelector.css(".entry-header-inner > h1.entry-title::text")
        .get()
        .strip(),
        "timestamp": getSelector.css(".post-meta li.meta-date::text").get(),
        "writer": getSelector.css("span.author > a::text").get(),
        "comments_count": len(resultComments) if resultComments else 0,
        "summary": "".join(
            getSelector.css(
                ".entry-content > p:first-of-type *::text"
            ).getall()
        ).strip(),
        "tags": getSelector.css("section.post-tags a[rel=tag]::text").getall(),
        "category": getSelector.css(
            ".category-style > span.label::text"
        ).get(),
    }


# Requisito 5
def get_tech_news(amount):
    urlBase = "https://blog.betrybe.com/"
    linksNews = []

    while amount > len(linksNews):
        linksNewNews = scrape_novidades(fetch(urlBase))
        linksNews.extend(linksNewNews)
        urlBase = scrape_next_page_link(fetch(urlBase))

    linksNewsNow = linksNews[:amount]
    news = [
        scrape_noticia(fetch(newsNow)) for newsNow in linksNewsNow
    ]

    create_news(news)
    return news

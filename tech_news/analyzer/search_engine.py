from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    resultNews = list()
    newNews = search_news({
        # "$options": "i" = Procura por maiúsculas e minúsculas
        "title": {"$regex": title, "$options": "i"},
    })
    for each_line in newNews:
        resultNews.append((each_line["title"], each_line["url"]))
    return resultNews


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_tag(tag):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pprint import pprint


main_page = "https://habr.com/ru/articles/top/daily/"

def get_url_html(url: str) -> str:
    res = requests.get(
        url,
        headers={
            "User-Agent": UserAgent().chrome
            }
        )
    return res.text


def get_soup(html_text: str) -> BeautifulSoup:
    return BeautifulSoup(html_text, "lxml")


@dataclass
class ArticleData:
    title: str
    views: str


def get_all_habr_posts(soup: BeautifulSoup) -> list[ArticleData]:
    posts_data = []
    all_articles_soup = soup.find_all("article", class_="tm-articles-list__item")
    for article_soup in all_articles_soup:
        article_title: str = article_soup.find("a", class_="tm-title__link").find("span").text
        article_views = article_soup.find("span", class_="tm-icon-counter__value").text
        posts_data.append(ArticleData(
            title=article_title,
            views=article_views
        ))
    return posts_data



def main():
    html = get_url_html(main_page)
    soup = get_soup(html)
    posts = get_all_habr_posts(soup)
    pprint(posts)


if __name__ == "__main__":
    main()
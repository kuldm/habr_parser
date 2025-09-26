import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pprint import pprint


main_page = "https://habr.com/ru/articles/top/daily/"
habr_page = "https://habr.com"

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
    link: str
    text: str


def get_article_text(article_link: str):
    article_html = get_url_html(article_link)
    article_soup = get_soup(article_html)
    article_body = article_soup.find("div", class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
    return article_body.text



def get_all_habr_posts(soup: BeautifulSoup) -> list[ArticleData]:
    posts_data = []
    all_articles_soup = soup.find_all("article", class_="tm-articles-list__item")
    for article_soup in all_articles_soup:
        article_title: str = article_soup.find("a", class_="tm-title__link").find("span").text
        article_views = article_soup.find("span", class_="tm-icon-counter__value").text
        article_link = article_soup.find("a", class_="tm-title__link").get("href")
        article_text = get_article_text(f"{habr_page}{article_link}")
        posts_data.append(ArticleData(
            title=article_title,
            views=article_views,
            link=f"{habr_page}{article_link}",
            text=article_text
        ))
    return posts_data



def main():
    html = get_url_html(main_page)
    soup = get_soup(html)
    posts = get_all_habr_posts(soup)
    pprint(posts)


if __name__ == "__main__":
    main()
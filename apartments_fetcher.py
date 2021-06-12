import datetime
import locale
import re

import requests
from bs4 import BeautifulSoup


URL = "https://ogloszenia.trojmiasto.pl/nieruchomosci-rynek-wtorny/ai,_600000,dw,3d,e1i,81_33_91_34_32_1_87_76_86_2_7_31_82,ri,3_,ti,_6.html"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

scrapped_apartments = soup.find_all("div", class_="list__item__picture")


def generate_apartments_urls() -> list:
    urls = []
    for apartment in scrapped_apartments:
        link = apartment.find("a")["href"]
        urls.append(link)
    return urls


def generate_single_apartment_data(ap_URL) -> dict:
    single_ap_dict = {}
    single_page = requests.get(ap_URL)
    single_soup = BeautifulSoup(single_page.content, "html.parser")

    # Retrieve ad information
    metrics = single_soup.find("ul", class_="oglStats")
    metrics_dict = dict(info.text.split(": ") for info in metrics.findAll("li"))

    ad_number = metrics_dict["Numer ogłoszenia"]

    created = metrics_dict["Data wprowadzenia"]
    locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
    converted_date = datetime.datetime.strptime(created, "%d %B %Y")

    price = single_soup.find("span", class_="oglDetailsMoney").text
    price = re.sub("[^0-9]", "", price)
    url = ap_URL

    single_ap_dict.update(
        {"ad_number": ad_number, "created": converted_date, "price": price, "url": url}
    )
    return single_ap_dict


def fetch_apartments() -> list:
    apartments_urls = generate_apartments_urls()
    apartments_list = []
    for ap_URL in apartments_urls:
        single_dict = generate_single_apartment_data(ap_URL)
        apartments_list.append(single_dict)
    return apartments_list

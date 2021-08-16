import datetime
import re

import requests
from bs4 import BeautifulSoup

import argparse

parser = argparse.ArgumentParser()

# -mp 600000 -d 3 -mf 6 -s 3
parser.add_argument("-mp", "--max_price", help="Max price", type=int)
parser.add_argument("-d", "--days_recency", help="Ad recency 1 or 3", type=int)
parser.add_argument("-mf", "--max_floor", help="Max desired floor", type=int)
parser.add_argument("-s", "--size", help="Min amount of rooms", type=int)

args = parser.parse_args()

# url to apartments in whole Gdansk
URL_to_fill = (
    f"https://ogloszenia.trojmiasto.pl/nieruchomosci-rynek-wtorny/gdansk/ai,_{args.max_price},"
    f"dw,{args.days_recency}d,"
    f"ri,{args.size}_,"
    f"ti,_{args.max_floor}.html#Modal"
)

page = requests.get(URL_to_fill)
soup = BeautifulSoup(page.content, "html.parser")

scrapped_apartments = soup.find_all("div", class_="list__item__picture")

months = {
    1: "stycznia",
    2: "lutego",
    3: "marca",
    4: "kwietnia",
    5: "maja",
    6: "czerwca",
    7: "lipca",
    8: "sierpnia",
    9: "września",
    10: "października",
    11: "listopada",
    12: "grudnia",
}


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

    created = process_date(metrics_dict["Data wprowadzenia"])

    # print(converted_date)
    price = single_soup.find("span", class_="oglDetailsMoney").text
    price = re.sub("[^0-9]", "", price)
    url = ap_URL
    title = re.sub("\n\\s+", "", single_soup.find("h1", class_="title").text)

    single_ap_dict.update(
        {
            "ad_number": ad_number,
            "created": created,
            "price": price,
            "url": url,
            "title": title,
        }
    )
    return single_ap_dict


def fetch_apartments() -> list:
    apartments_urls = generate_apartments_urls()
    apartments_list = []
    for ap_URL in apartments_urls:
        single_dict = generate_single_apartment_data(ap_URL)
        apartments_list.append(single_dict)
    return apartments_list


def process_date(date) -> datetime:
    created_date_original = date.split(" ")
    for key, value in months.items():
        if created_date_original[1] == value:
            created_date_original[1] = f"{key}"
    created_date_original = " ".join(created_date_original)
    converted_date = datetime.datetime.strptime(created_date_original, "%d %m %Y")
    return converted_date

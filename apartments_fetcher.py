import datetime
import re

import requests
from bs4 import BeautifulSoup

URL = "https://ogloszenia.trojmiasto.pl/nieruchomosci-rynek-wtorny/ai,_600000,dw,3d,e1i,81_33_99_3_32_1_36_87_76_86_2_7_31,ri,3_,o1,1.html"
url_price = 600000
url_days = 3
url_max_floors = 6
url_min_rooms = 3
districts = {
    81: "Aniołki",
    33: "Brzeźno"
}
URL_to_fill = f"https://ogloszenia.trojmiasto.pl/nieruchomosci-rynek-wtorny/ai,_{url_price},dw,{url_days}d,e1i,81_33_91_34_32_1_87_76_86_2_7_31_82,ri,{url_min_rooms}_,ti,_{url_max_floors}.html#Modal"


page = requests.get(URL)
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


# if __name__ == "__main__":
#     # main()
#
#     generate_single_apartment_data(
#         "https://ogloszenia.trojmiasto.pl/nieruchomosci-rynek-wtorny/2-pokoje-z-oddzielna-kuchnia-w-sercu-starowki-ogl64327835.html"
#     )
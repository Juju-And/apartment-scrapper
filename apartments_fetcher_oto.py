import datetime
import locale
import re

import requests
from bs4 import BeautifulSoup


URL = "https://www.otodom.pl/sprzedaz/mieszkanie/?search%5Bfilter_float_price%3Ato%5D=600000&search%5Bfilter_enum_rooms_num%5D%5B0%5D=3&search%5Bfilter_float_building_floors_num%3Ato%5D=6&search%5Bcreated_since%5D=7&locations%5B0%5D%5Bdistrict_id%5D=30&locations%5B1%5D%5Bregion_id%5D=11&locations%5B1%5D%5Bsubregion_id%5D=439&locations%5B1%5D%5Bcity_id%5D=40&locations%5B1%5D%5Bdistrict_id%5D=16&locations%5B2%5D%5Bregion_id%5D=11&locations%5B2%5D%5Bsubregion_id%5D=439&locations%5B2%5D%5Bcity_id%5D=40&locations%5B2%5D%5Bdistrict_id%5D=1688&locations%5B3%5D%5Bregion_id%5D=11&locations%5B3%5D%5Bsubregion_id%5D=439&locations%5B3%5D%5Bcity_id%5D=40&locations%5B3%5D%5Bdistrict_id%5D=136&locations%5B4%5D%5Bregion_id%5D=11&locations%5B4%5D%5Bsubregion_id%5D=439&locations%5B4%5D%5Bcity_id%5D=40&locations%5B4%5D%5Bdistrict_id%5D=140"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

scrapped_apartments = soup.find_all("article", class_="offer-item")

# print(scrapped_apartments)


def generate_apartments_urls() -> list:
    urls = []
    for apartment in scrapped_apartments:
        link = apartment.find("a")["href"]
        urls.append(link)
    return urls


def generate_single_apartment_data(ap_URL):
    single_ap_dict = {}
    single_page = requests.get(ap_URL)
    single_soup = BeautifulSoup(single_page.content, "html.parser")


    price = single_soup.find("strong", class_="css-srd1q3").text
    price = re.sub("[^0-9]", "", price)
    print(price)

    # Retrieve ad information
    # metrics = single_soup.find("ul", class_="oglStats")
    # metrics_dict = dict(info.text.split(": ") for info in metrics.findAll("li"))
    #
    ad_number = single_soup.find("div", class_="css-jjerc6").text
    # print(single_soup)
    print(ad_number)
    #
    # created = metrics_dict["Data wprowadzenia"]
    # locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
    # converted_date = datetime.datetime.strptime(created, "%d %B %Y")
    # price = single_soup.find("span", class_="oglDetailsMoney").text
    # price = re.sub("[^0-9]", "", price)
    # url = ap_URL
    #
    # single_ap_dict.update(
    #     {"ad_number": ad_number, "created": converted_date, "price": price, "url": url}
    # )
    # return single_ap_dict

single_url = "https://www.otodom.pl/pl/oferta/sloneczne-mieszkanie-3-pokoje-z-tarasem-ID4bVJR.html#dc6b647539"
print(generate_single_apartment_data(single_url))


# def fetch_apartments() -> list:
#     apartments_urls = generate_apartments_urls()
#     apartments_list = []
#     for ap_URL in apartments_urls:
#         single_dict = generate_single_apartment_data(ap_URL)
#         apartments_list.append(single_dict)
#     return apartments_list


# if __name__ == "__main__":
#     fetch_apartments()

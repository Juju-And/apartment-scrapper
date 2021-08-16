import json
import re

import requests
from bs4 import BeautifulSoup

general_url = "https://ogloszenia.trojmiasto.pl/nieruchomosci-rynek-wtorny/#Modal"


page = requests.get(general_url)
soup = BeautifulSoup(page.content, "html.parser")

location_box = soup.find_all("div", class_="location_select_box")


def fetch_single_district():
    districts_dict = {}
    # district_list = city_district_list
    # print(district_list)
    print(location_box)
    for city in location_box:
        district_list = city.find("ul").find_all("li")
        for idx, district in enumerate(district_list):
            print(idx, district)
            districts_dict.update(
                {district.find("input")["id"]: re.sub("\n", "", district.text)}
            )
    # for idx, district in enumerate(scrapped_districts):
    #     print(idx, district)
    # print(location_box)
    with open("districts.json", "w", encoding="utf8") as json_file:
        json.dump(districts_dict, json_file, ensure_ascii=False)


if __name__ == "__main__":
    fetch_single_district()

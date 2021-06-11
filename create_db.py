

def add_apartment(apartment):
    SQL = """ CREATE TABLE apartments (
    ad_number VARCHAR (50) UNIQUE NOT NULL,
    created TIMESTAMP NOT NULL,
    price INT NOT NULL,
    url VARCHAR (2048) UNIQUE NOT NULL
);
"""
# ad_number = metrics_dict["Numer ogłoszenia"]
# created = metrics_dict["Data wprowadzenia"]
# price = single_soup.find("span", class_="oglDetailsMoney").text
# url = ap_URL

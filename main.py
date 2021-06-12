import time
import sys

from apartments_fetcher import fetch_apartments
from database import (
    create_db_context,
    apartment_exists,
    add_apartment,
)
from mailer import send_email

# sender = sys.argv[1]
# recipient = sys.argv[2]
# password = sys.argv[3]


def main():
    db = create_db_context()

    while True:
        apartments = fetch_apartments()
        new_apartments = []

        for apartment in apartments:
            if not apartment_exists(db, apartment["ad_number"]):
                add_apartment(db, apartment)
                new_apartments.append(apartment)

        if len(new_apartments) > 0:
            send_email(new_apartments)

        time.sleep(300)


if __name__ == "__main__":
    main()

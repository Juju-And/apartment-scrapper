import datetime
import re
import time

from apartments_fetcher import (
    generate_apartments_urls,
    generate_single_apartment_data,
)
from create_db import setup_database
from database import (
    create_db_context,
    apartment_exists,
    add_apartment,
)
from mailer import send_email

# sender = sys.argv[1]
# recipient = sys.argv[2]
# password = sys.argv[3]

TIME_SLEEP_MIN = 10


def main():
    db = create_db_context()
    setup_database(db)

    while True:
        print(datetime.datetime.now(), "Checking for new apartments...")
        apartment_urls = generate_apartments_urls()
        new_apartments = []
        for apartment_url in apartment_urls:
            ad_number = re.search(r"(-ogl)(\d+)(\.html)", apartment_url)
            if not apartment_exists(db, ad_number.group(2)):
                apartment = generate_single_apartment_data(apartment_url)
                add_apartment(db, apartment)
                new_apartments.append(apartment)

        if len(new_apartments) > 0:
            send_email(new_apartments)
        else:
            print(
                datetime.datetime.now(),
                f"No new apartments. Check in {TIME_SLEEP_MIN} minutes.",
            )

        time.sleep(TIME_SLEEP_MIN*60)


if __name__ == "__main__":
    main()

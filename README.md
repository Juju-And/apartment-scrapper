# Apartment-scrapper

This is a web application intended to scrap a specific website in order to get email notifications about new properties with specific parameters in a specific location.

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Install all required modules running pip with the provided file:

```
pip install -r requirements.txt
```

### Installing

As a first step, you need to create locally PostgreSQL database named 'apartments'.

Secondly,copy the .env.sample as .env and fill with your PostgreSQL credentials, and credentials for your scraper working email, which is going to be used in the process of sending notifications, and declare the recipient of notifications.

```
USERNAME=sample_username
PASSWD=XXXXXX
HOSTNAME=sample_hostname
DB_NAME=apartments
SENDER_MAIL=sender@example.com
MAIL_PASSWORD=XXXXXX
RECIPIENT_MAIL=recipient@example.com
```

With ready empty DB, and filled .env file you're ready to run and receive your first email notifications:
```
$ python main.py
```




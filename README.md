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

As a first step, you need to create locally PostgreSQL database named 'apartments', and provide your PostgreSQL credentials in

Secondly, please edit the config.json file with email account data, which is going to be used in the process of sending notifications.

With ready empty DB you're ready to run:
```
$ python main.py
```




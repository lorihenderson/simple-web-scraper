"""
Simple Web Scraper Extra Credit

TODO:
- get HTML of site to scrap
- read the contents of the HTML
- extract specific data
    - email addresses
    - phone numbers
    - URLs
"""
# Used Daniel's study hall demo on web scraping as a guide
__author__ = "Lori Henderson with some guidance from Chris"

import requests
import argparse
import sys
import re
from bs4 import BeautifulSoup, SoupStrainer


def web_scraper(link):
    """Scrapes phone numbers, email addresses, and urls."""
    response = requests.get(link)

    for link in BeautifulSoup(response.text,
                              "html.parser", parse_only=SoupStrainer("a")):
        if link.has_attr("href"):
            address = link.get("href")
            url = re.search(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                            str(address))
            if url:
                print("URL: " + url.group())

    for email in BeautifulSoup(response.text, "html.parser"):
        emails = re.search("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
                           str(email))
        if emails:
            print("Email Address: " + emails.group())

    for phone_number in BeautifulSoup(response.text, "html.parser"):
        phone_numbers = re.search(r"1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?",
                                  str(phone_number))
        if phone_numbers:
            print("Phone Number: " + phone_numbers.group())


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("link", help="url of page to scrape")
    return parser


def main(args):
    parser = create_parser()
    args = parser.parse_args(args)
    url = args.link
    return web_scraper(url)


if __name__ == '__main__':
    main(sys.argv[1:])

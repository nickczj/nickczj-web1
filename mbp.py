import urllib.request
from bs4 import BeautifulSoup
import time
from time import gmtime, strftime

url = 'http://www.apple.com/sg/shop/product/G0UK4ZP/A/Refurbished-133-inch-MacBook-Pro-23GHz-dual-core-Intel-Core-i5-with-Retina-display-Space-Gray'


def get_availability():
    f = urllib.request.urlopen(url)
    soup = BeautifulSoup(f.read(), "html.parser")
    form = soup.find('form', id="product-details-form")
    s = form.__str__()
    return 'Out of stock' not in s


def mbp():
    availability = get_availability()

    while True:
        print(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + " MBP Availability: " + availability.__str__())
        if availability != get_availability():
            availability = get_availability()
            print(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + " MBP Stock: " + availability.__str__())
        time.sleep(60)


from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches
from collections import defaultdict
import random
import csv

class PriceCompare:

    def __init__(self):
        pass

    def find_price(self, product):
        product_arr = product.split()
        n = 1
        key = ""

        for word in product_arr:
            if n == 1:
                key = key + str(word)
                n += 1
            else:
                key = key + '+' + str(word)

        flipkart_prices = self.price_flipkart(key)
        amazon_prices = self.price_amzn(key)

        return {
            'flipkart_prices': flipkart_prices,
            'amazon_prices': amazon_prices
        }

    def price_flipkart(self, key):
        url_flip = 'https://www.flipkart.com/search?q=' + str(
            key) + '&marketplace=FLIPKART&otracker=start&as-show=on&as=off'
        map = defaultdict(list)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        source_code = requests.get(url_flip, headers=headers)
        soup = BeautifulSoup(source_code.text, "html.parser")

        home = 'https://www.flipkart.com'
        for block in soup.find_all('div', {'class': '_2kHMtA'}):
            title, price, link = None, 'Currently Unavailable', None
            for heading in block.find_all('div', {'class': '_4rR01T'}):
                title = heading.text
            for p in block.find_all('div', {'class': '_30jeq3 _1_WHN1'}):
                price = p.text[1:]
            for l in block.find_all('a', {'class': '_1fQZEK'}):
                link = home + l.get('href')
            for img in block.find_all('img', {'class': '_396cs4'}):
                image_url = img.get('src')
            map[title] = [price, link, image_url]

            with open(f'flipkart_{key}.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Price", "Link"])
                for title, data in map.items():
                    price = data[0] if data[0] else "N/A"
                    link = data[1] if data[1] else "N/A"
                    writer.writerow([title, price, link]) 

        prices = {title: {'price': price, 'link': link, "image_url": image_url} for title, (price, link, image_url) in map.items() if price is not None}
        return prices

    def price_amzn(self, key):
        url_amzn = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)

        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        map = defaultdict(list)
        print("DATA:", map)
        home = 'https://www.amazon.in'
        source_code = requests.get(url_amzn, headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")

        for html in soup.find_all('div', {'class': 'sg-col-inner'}):
            title, link, price = None, None, None
            for heading in html.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
                title = heading.text
            for p in html.find_all('span', {'class': 'a-price-whole'}):
                price = p.text
            for l in html.find_all('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
                link = home + l.get('href')
            for img in html.find_all('img', {'class': 's-image'}):
                image_url = img.get('src')
            if title and link:
                map[title] = [price, link, image_url]

            with open(f'amazon_{key}.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Price", "Link"])
                for title, data in map.items():
                    price = data[0] if data[0] else "N/A"
                    link = data[1] if data[1] else "N/A"
                    writer.writerow([title, price, link]) 

        prices = {title: {'price': price, 'link': link, "image_url": image_url} for title, (price, link, image_url) in map.items() if price is not None}

        return prices
    
    def search(self):
        amzn_get = self.variable_amzn.get()
        self.opt_title.set(amzn_get)
        product = self.opt_title.get()
        price, self.product_link = self.looktable[product][0], self.looktable[product][1]
        self.var_amzn.set(price + '.00')
        flip_get = self.variable_flip.get()
        flip_price, self.link_flip = self.looktable_flip[flip_get][0], self.looktable_flip[flip_get][1]
        self.var_flipkart.set(flip_price + '.00')

    def visit_amzn(self):
        webbrowser.open(self.product_link)

    def visit_flip(self):
        webbrowser.open(self.link_flip)

if __name__ == "__main__":
    c = Price_compare(root)
    root.title('Price Comparison Engine')
    root.mainloop()

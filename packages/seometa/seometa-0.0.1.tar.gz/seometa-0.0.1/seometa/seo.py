import csv

from bs4 import BeautifulSoup
import requests


def read_txt(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()


def save_csv(path: str, row: list):
    with open(path, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerows([row])
    f.close()


class SEO:
    def __init__(self, url: str):
        if 'http' not in url:
            self.url = f'http://{url.strip()}'
        else:
            self.url = url
        self.html = None
        self.keywords = [self.url]
        self.path = None

    def get_website_html(self):
        try:
            headers = {
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            }

            response = requests.get(self.url, headers=headers)
            if response.status_code == 200:
                self.html = response.text
                return True
            else:
                print(f'warning: {self.url} not working')
                return False
        except Exception as e:
            print(f'error: {e}')

    def find_seo_keywords(self):
        soup = BeautifulSoup(self.html, features='html.parser')
        try:
            self.keywords.append(soup.find('meta', {'name': 'keywords'}).get('content'))
            print(f'valid: {self.url} {self.keywords[1]}')
        except Exception as e:
            print(f"info: {self.url} website don't have keywords")

    def save_csv(self):
        with open(self.path, 'a', encoding='utf-8', newline='') as f:
            w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerows([self.keywords])
        f.close()

    def run(self, path):
        self.path = path
        if self.get_website_html():
            self.find_seo_keywords()

        if len(self.keywords) > 1:
            self.save_csv()

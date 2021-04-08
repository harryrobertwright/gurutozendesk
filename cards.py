from bs4 import BeautifulSoup
import re

class Data:
    def __init__(self):
        self.dictionary = {}
        self.regex = re.compile(r'/card/(.+)/.+')

    def get_cards(self, html):
        '''Return a dicitionary of all verified cards from Guru HTML'''
        with open(html, 'r') as f:
            html_string = f.read()

        soup = BeautifulSoup(html_string, 'lxml')
        stuff = soup.find_all("a", class_="ghq-UnstyledLink ghq-KnowledgeBoardCardItem__info")

        for x in stuff:
            if 'ghq-KnowledgeBoardCardItemVerification ghq-is-trusted ghq-has-knowledge-sync-verifiers' in str(x):
                url = x['href']
                title = x.text
                try:
                    mo = re.search(self.regex, url)
                except AttributeError:
                    pass
                else:
                    card_id = mo.group(1)
                    self.dictionary[title] = card_id

        return self.dictionary

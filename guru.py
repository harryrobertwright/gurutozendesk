import requests
import json
import re
import sys
from cards import Data

class Card:
    def __init__(self, cardId):
        self.cardId = cardId
        self.content = ''

    def raw_contents(self):
        '''Pull the raw HTML content from Guru to JSON'''
        url = f"https://api.getguru.com/api/v1/cards/{self.cardId}/extended"

        headers = {
            "Accept": "application/json",
            "Authorization": "INSERT AUTH HERE"
        }

        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.text)
        self.content = data['content']
        return self.content

    def clean_contents(self):
        '''Remove class attributes from HTML tags and correctly space for Zendesk''''
        self.raw_contents()
        html_regex = re.compile(r'<[a-z]+(\s[^>]*>)')
        bad_html = re.findall(html_regex, self.content)

        for html in bad_html:
            self.content = self.content.replace(html, '>')

        self.content = self.content.replace('<p>', '<p><br></p><p>')
        self.content = self.content.replace('<p><br></p><p>Hi', '<p>Hi')
        self.content = self.content.replace('<li><p><br></p><p>', '<li><p>')
        self.content = self.content.replace('\u200b', '')

        return self.content

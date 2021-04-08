import sys
from guru import Card
from cards import Data
from zenpy import Zenpy
from zenpy.lib.api_objects import Macro
from zenpy.lib.api import *

credentials = {
    'email' : 'harry.wright@prolific.co',
    'token' : 'TOKEN GOES HERE',
    'subdomain': 'prolifichelp'
}

zenpy_client = Zenpy(**credentials)

# At the time of writing I didn't realise the capabilities of Guru's API so ended up scraping its HTML to find all the verified cards
cards = Data().get_cards('guru_html.html')

def import_to_zendesk(macros):
    '''Find corresponding Guru macro in Zendesk and update'''
    for macro in macros:
        for guru_title, id in cards.items():
            if guru_title == macro.title:
                for idx, action in enumerate(macro.actions):
                    if action['field'] == 'comment_value_html':
                        guru_card = Card(id)
                        content = guru_card.clean_contents()
                        action['value'] = content

                        # A janky way to resolve unicode printing problems
                        action['value'] = action['value'].replace('â€‹,', ',')
                        action['value'] = action['value'].replace('â€™', "'")

                        zenpy_client.macros.update(macro)
                        print(f'Updated {macro.title}')

import_to_zendesk(zenpy_client.macros())

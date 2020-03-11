from lxml import etree
import requests
from io import StringIO

def get_stats():
    headers = {"User-Agent": "James 1.0"}
    page = requests.get("https://www.overbuff.com/players/pc/Valkia/heroes/pharah?mode=competitive", headers=headers).text

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(page), parser)

    pharah_obj = tree.xpath("//div[@class='player-hero theme-hero theme-hero-pharah']")[0]
    pharah_str = str(etree.tostring(pharah_obj, method="html"))
    pharah = etree.parse(StringIO(pharah_str), parser)

    stats = pharah.xpath("//div[@class='stat boxed']")[0]
    labels = stats.xpath("//div[@class='label']/text()")[3:]
    values = stats.xpath("//div[@class='value']/text()")[1:]

    d = dict()
    
    for i in range(len(labels)):
         d[labels[i]] = values[i].rstrip()

    return d

    #for example:

    """
    {'Medals': '2.80 ', 'Time Played': '16 hours ', 'Win Rate': '54.12% ', 'On Fire': '12.9% ',
    'Eliminations': '24.88 ', 'Obj Kills': '8.01 ', 'Obj Time': '00:40 ', 'Damage': '16,722 ',
    'Deaths': '9.63 ', 'Weapon Acc': '50% ', 'Direct Hits': '51.51 ', 'Solo Kills': '3.48 ',
    'Final Blows': '14.90 ', 'Env Kills': '0.67 ', 'Barrage Kills': '5.93 ', 'E:D Ratio': '2.58 ',
    'Voting Cards': '0.40 ', 'Gold Medals': '1.26 ', 'Silver Medals': '0.86 ', 'Bronze Medals': '0.69 '}
    """
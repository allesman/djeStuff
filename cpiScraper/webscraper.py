import requests
from lxml import html

# headers, because the website doesn't allow scraping without a user agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

def getList(black):
    # gets the fatf grey or black list

    # open the website
    page=requests.get("https://www.knowyourcountry.com/fatf-aml-list/",headers=headers)
    # get the html tree
    tree = html.fromstring(page.content)
    # get the text
    text = tree.xpath(f"/html/body/div[1]/main/div[3]/div/section/div/div/div/div/div/p[{4 if black else 5}]/text()")
    # remove the first line, as it's just info text and not a country
    text=text[1:]
    # remove the first three characters from each line, only being enumeration (e.g. "1. ")
    text = [line[3:] for line in text]
    # remove any space character at the beginning or end of each line
    text = [line.strip() for line in text]
    # return the list
    return text

def getBothLists():
    # returns a list of two lists, the first being the fatf black list and the second being the fatf grey list
    output = []
    output.append(getList(True))
    output.append(getList(False))
    return output
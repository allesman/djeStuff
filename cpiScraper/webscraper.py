from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# print(getBothLists())

# old code, using selenium:

# def openWebsite():
#     # open the browser
#     options= webdriver.ChromeOptions()
#     options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
#     # open the website
#     driver.get("https://www.knowyourcountry.com/fatf-aml-list/")
#     # wait for the page to load
#     # waitTillLoaded(driver)
#     return driver

# def getList(driver,black):
    # get the text from the following xpath when its loaded: /html/body/div[2]/main/div[3]/div/section/div/div/div/div/div/p[4]
    # element = WebDriverWait(driver, 10).until()
    # element = driver.find_element(By.XPATH, f"/html/body/div[2]/main/div[3]/div/section/div/div/div/div/div/p[{4 if black else 5}]")
    # # get the text
    # if black:
    #     text = element.text.split("\n")[1:]
    # else:
    #     text = element.text.split("\n")[2:]
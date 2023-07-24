from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def waitTillLoaded(driver):
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
def openWebsite():
    # open the browser
    options= webdriver.ChromeOptions()
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # open the website
    driver.get("https://www.knowyourcountry.com/fatf-aml-list/")
    # wait for the page to load
    waitTillLoaded(driver)
    return driver
def getList(black,driver):
    # gets the fatf grey or black list
    # get the text from the following xpath when its loaded: /html/body/div[2]/main/div[3]/div/section/div/div/div/div/div/p[4]
    # element = WebDriverWait(driver, 10).until()
    element = driver.find_element(By.XPATH, f"/html/body/div[2]/main/div[3]/div/section/div/div/div/div/div/p[{4 if black else 5}]")
    # get the text
    if black:
        text = element.text.split("\n")[1:]
    else:
        text = element.text.split("\n")[2:]
    # remove the first three characters from each line
    text = [line[3:] for line in text]
    # remove any space character at the beginning or end of each line
    text = [line.strip() for line in text]
    # return the list
    return text

def getBothLists():
    # returns a list of two lists, the first being the fatf black list and the second being the fatf grey list
    driver = openWebsite()
    output = []
    output.append(getList(True,driver))
    output.append(getList(False,driver))
    return output

# print(getBothLists())

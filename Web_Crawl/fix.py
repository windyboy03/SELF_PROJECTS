from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
#Set up Chrome drive
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

page = driver.get('https://www.imdb.com/chart/top/')  # Getting page HTML through request
soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parsing content using beautifulsoup

totalScrapedInfo = []  # In this list we will save all the information we scrape
links = soup.select("table tbody tr td.titleColumn a")  # Selecting all of the anchors with titles
first10 = links[:10]  # Keep only the first 10 anchors
print(driver.get('https://www.imdb.com/chart/top/'))
for anchor in first10:
    driver.get('https://www.imdb.com/' + anchor['href'])
    infolist = driver.find_elements(By.CSS_SELECTOR, '.ipc-inline-list')[1]

    informations = infolist.find_elements(By.CSS_SELECTOR, "[role='presentation']")

    scrapedInfo = {
        "title": anchor.text,
        "year": informations[0].text,
        "duration": informations[2].text,
    }
    totalScrapedInfo.append(scrapedInfo)

print(totalScrapedInfo)
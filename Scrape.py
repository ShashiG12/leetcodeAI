#https://www.youtube.com/watch?v=XQgXKtPSzUI
import time
import urllib.error

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd

page_url = "https://github.com/wisdompeak/LeetCode"


uClient = uReq(page_url)


page_soup = soup(uClient.read(), "html.parser")
uClient.close()

allLinks = page_soup.findAll("a")
links = []

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

pName = []
pText = []
pType = []
count = 0
for link in allLinks:
    foundLeet = False
    if "https://github.com/wisdompeak/LeetCode/tree/master" in link.get('href'):
        if(link.get('href').split("/")[len(link.get('href').split("/")) - 2] == "master"):
            continue
        else:
            print(len(pName), len(pText), len(pType))
            count += 1
            print(f'{count}/{len(allLinks)}' + " ")
            pName.append(link.get('href').split("/")[len(link.get('href').split("/")) - 1])
            pType.append(link.get('href').split("/")[len(link.get('href').split("/")) - 2])

            try:
                newLink = link.get('href')
                uClient = uReq(newLink)
                page_soup1 = soup(uClient.read(), "html.parser")
                uClient.close()
                allNewLinks = page_soup1.findAll('a')
            except urllib.error.HTTPError:
                print("Page not found")
                pText.append("NOTFOUND")
                continue
            for link2 in allNewLinks:
                if link2.string == "Leetcode Link":
                    foundLeet = True
                    driver.get(link2.get('href'))
                    time.sleep(3)
                    page_source = driver.page_source
                    page = soup(page_source, 'html.parser')
                    problemText = ""
                    for paragraph in page.findAll('p'):
                        problemText += paragraph.text
                    if "sign in" not in problemText:
                        if problemText == "" or "Sorry" in problemText:
                            print("EMPTY")
                            pText.append("EMPTY")
                        else:
                            print(problemText)
                            pText.append(problemText)
                    else:
                        print("PREMIUMLOCKED")
                        pText.append("PREMIUMLOCKED")
            if (foundLeet == False):
                print("NOLEETCODELINK")
                pText.append("NOLEETCODELINK")


df = pd.DataFrame({'Name': pName, 'Text': pText, 'Type': pType})
df.to_csv('leetcodeData.csv', index=False, encoding='utf-8')
print(df.head())

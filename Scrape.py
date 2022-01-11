import time
import urllib.error
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd

# github page with leetcode links sorted by their problem type
# e.g. "two-pointer", "sliding window", etc.
page_url = "https://github.com/wisdompeak/LeetCode"

# request page with urllib
# more info at #https://www.youtube.com/watch?v=XQgXKtPSzUI
uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# variable to store all the links on the retrieved website
allLinks = page_soup.findAll("a")

# declares the browser to be used to open each link
# using selenium here instead of urllib to allow for leetcode webpage to load before grabbing HTML
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

# to be arrays of dataframe
pName = []
pText = []
pType = []

# keeps track of the link being opened when running the program
count = 0

# iterate through every link in the github page
for link in allLinks:
    # keeps track of whether a leetcode link has been found inside of the current link
    foundLeet = False

    # gets only the related github links from the original github page
    if "https://github.com/wisdompeak/LeetCode/tree/master" in link.get('href'):

        # filters title links
        if(link.get('href').split("/")[len(link.get('href').split("/")) - 2] == "master"):
            continue
        else:

            # added to make sure each dataframe column remains the same size
            print(len(pName), len(pText), len(pType))

            count += 1

            # program progress (e.g. currently on link "1/1224")
            print(f'{count}/{len(allLinks)}' + " ")

            # adds the problem name and type to the respective arrays
            # retrieved from the text of each link
            pName.append(link.get('href').split("/")[len(link.get('href').split("/")) - 1])
            pType.append(link.get('href').split("/")[len(link.get('href').split("/")) - 2])

            try:
                # opens the github page with the leetcode link
                newLink = link.get('href')
                uClient = uReq(newLink)
                page_soup1 = soup(uClient.read(), "html.parser")
                uClient.close()

                # all the link on the new github page
                allNewLinks = page_soup1.findAll('a')

            except urllib.error.HTTPError:
                print("Page not found")
                pText.append("NOTFOUND")
                continue
            # iterates through all the links on the new github page
            for link2 in allNewLinks:
                # retrieves only the relevant leetcode link
                if link2.string == "Leetcode Link":
                    foundLeet = True

                    # opens an instance of firefox to retrieve the html from
                    # the loaded leetcode page
                    driver.get(link2.get('href'))
                    time.sleep(3)
                    page_source = driver.page_source
                    page = soup(page_source, 'html.parser')

                    problemText = ""
                    for paragraph in page.findAll('p'):
                        problemText += paragraph.text

                    # check for unhelpful problem text results and filters them
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
            # if no leetcode link is found on the second github page
            if not foundLeet:
                print("NOLEETCODELINK")
                pText.append("NOLEETCODELINK")


# creates new dataframe from previously created columns
df = pd.DataFrame({'Name': pName, 'Text': pText, 'Type': pType})
df.to_csv('leetcodeData.csv', index=False, encoding='utf-8')
print(df.head())

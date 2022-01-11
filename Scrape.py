#https://www.youtube.com/watch?v=XQgXKtPSzUI
import time

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from urllib.request import Request
import requests
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import pandas as pd


# URl to web scrape from.
# in this example we web scrap graphics cards from Newegg.com
page_url = "https://github.com/wisdompeak/LeetCode"

# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# finds each product from the store page
allLinks = page_soup.findAll("a")
links = []

# for link in allLinks:
#     if "https://github.com/wisdompeak/LeetCode/tree/master" in link.get('href'):
#         print(link.get('href'))

# allLinks2 = page_soup.findAll("h4")
# for link in allLinks2:
#     if len(link.findAll('a')) > 1:
#         print(link.findAll('a')[1].string)

# # name the output file to write to local disk
# out_filename = "leetcodeData.csv"
# # header of csv file to be written
# headers = "name,text,type \n"
#
# # opens file, and writes headers
# f = open(out_filename, "w")
# f.write(headers)

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
# for link in allLinks:
#     if "https://github.com/wisdompeak/LeetCode/tree/master" in link.get('href'):
#         if(link.get('href').split("/")[len(link.get('href').split("/")) - 2] == "master"):
#             continue
#         else:
#             newLink = link.get('href')
#             uClient = uReq(newLink)
#             page_soup1 = soup(uClient.read(), "html.parser")
#             uClient.close()
#             allNewLinks = page_soup1.findAll('a')
#             for link2 in allNewLinks:
#                 if link2.string == "Leetcode Link":
#                     # print(link2.get('href'))
#                     # uClient = Request(link2.get('href'), headers={'User-Agent': 'Mozilla/5.0'})
#                     # page_soup2 = soup(uReq(uClient).read(), "html.parser")
#
#                     driver.get(link2.get('href'))
#                     time.sleep(4)
#                     page_source = driver.page_source
#                     time.sleep(4)
#                     page = soup(page_source, 'html.parser')
#                     problemText = ""
#                     for paragraph in page.findAll('p'):
#                         problemText += paragraph.text
#                     print(problemText)

pName = []
pText = []
pType = []
for link in allLinks:
    if "https://github.com/wisdompeak/LeetCode/tree/master" in link.get('href'):
        if(link.get('href').split("/")[len(link.get('href').split("/")) - 2] == "master"):
            continue
        else:

            pName.append(link.get('href').split("/")[len(link.get('href').split("/")) - 1])

            newLink = link.get('href')
            uClient = uReq(newLink)
            page_soup1 = soup(uClient.read(), "html.parser")
            uClient.close()
            allNewLinks = page_soup1.findAll('a')
            for link2 in allNewLinks:
                if link2.string == "Leetcode Link":
                    # print(link2.get('href'))
                    # uClient = Request(link2.get('href'), headers={'User-Agent': 'Mozilla/5.0'})
                    # page_soup2 = soup(uReq(uClient).read(), "html.parser")

                    driver.get(link2.get('href'))
                    time.sleep(4)
                    page_source = driver.page_source
                    time.sleep(4)
                    page = soup(page_source, 'html.parser')
                    problemText = ""
                    for paragraph in page.findAll('p'):
                        problemText += paragraph.text
                    pText.append(problemText)

            pType.append(link.get('href').split("/")[len(link.get('href').split("/")) - 2])

df = pd.DataFrame({'Name':pName,'Text':pText,'Type':pType})
print(df.head())

# # loops over each product and grabs attributes about
# # each product
# for container in containers:
#     # Finds all link tags "a" from within the first div.
#     make_rating_sp = container.div.select("a")
#
#     # Grabs the title from the image title attribute
#     # Then does proper casing using .title()
#     brand = make_rating_sp[0].img["title"].title()
#
#     # Grabs the text within the second "(a)" tag from within
#     # the list of queries.
#     product_name = container.div.select("a")[2].text
#
#     # Grabs the product shipping information by searching
#     # all lists with the class "price-ship".
#     # Then cleans the text of white space with strip()
#     # Cleans the strip of "Shipping $" if it exists to just get number
#     shipping = container.findAll("li", {"class": "price-ship"})[0].text.strip().replace("$", "").replace(" Shipping", "")
#
#     # prints the dataset to console
#     print("problem: " + problem + "\n")
#     print("type: " + type + "\n")
#
#     # writes the dataset to file
#     f.write(problem.replace(",", "|") + ", " + type + "\n")
#
# f.close()  # Close the file
#

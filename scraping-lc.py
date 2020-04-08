# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 19:38:14 2020

To scrape the problems list of Leetcode.
Prerequisites:
    
- Selenium
- A web browser and corresponding webdriver (I'm using Firefox and Geckodriver)



@author: yuany
"""

import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


os.chdir("OneDrive\Documents\Github\leetcode-problems-categorized")


# Initiate a webdriver and get the desired url
browserLC = webdriver.Firefox()
browserLC.get("https://leetcode.com/problemset/all/")

# define the relative xpath of the row selector 
# so that all problems are displayed on one page
xpath_rowselect = "//span[@class='row-selector']/select"
rowselector = Select(browserLC.find_element(By.XPATH, xpath_rowselect))
rowselector.select_by_visible_text("all")


# find all the href of problems listed on this page
xpath_problems = "//div[@class='table-responsive question-list-table']/table/tbody/tr/td/div/a"

list_problems = browserLC.find_elements(By.XPATH, xpath_problems)
list_href = []
for i in list_problems:
    href = i.get_attribute("href")
    list_href.append(href)

df = pd.DataFrame(data={"href": list_href})


df['title'] = ''
df['difficulty'] = ''
df['content'] = ''
df['complete'] = ''


# for each problem, load the url and extraxt the following info:
for i in range(df.size):
    href = df["href"][i]
    browserLC.get(href)
    browserLC.implicitly_wait(5) 
    title = browserLC.find_element(By.XPATH, 
                                   "//div[@data-cy='question-title']").text
    diff = browserLC.find_element(By.XPATH, 
                                  "//div[@diff='easy']|//div[@diff='medium']|//div[@diff='hard']").text
    content = browserLC.find_elements(By.XPATH, 
                                  "//div[contains(@class, 'question-content')]/div/p|//div[contains(@class, 'question-content')]/div/pre|//div[contains(@class, 'question-content')]/div/ul")
    contents = ""
    if len(content)>1:
        for j in content:
            contents += j.text + "\n"
    
    df['title'][i] = title
    df['difficulty'][i] = diff
    df['content'][i] = contents
    df['complete'][i] = 'y'
    
    
df.to_csv("LC_problems.csv")    
    
    













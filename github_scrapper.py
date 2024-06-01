from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

langs=[]
def eachRepoScrapper(driver):
    # get elements with attribute name data-ga-click and value = test
    
    elements = driver.find_elements(
        "css selector", "[data-ga-click='Repository, language stats search click, location:repo overview']")
    
    for element in elements:
        langs.append(element.text)

    



def gitHubLanguageScrapper(url):
    # open chrome
    driver = webdriver.Chrome()
    # open url
    driver.get(url)

    # get elements with calss name pinned-item-list-item-content
    repos = driver.find_elements(
        "css selector", ".pinned-item-list-item-content")

    for repo in repos:
        # get a tag
        aTag = repo.find_element("css selector", "a")
        aTag.send_keys(Keys.CONTROL + Keys.RETURN)

        driver.switch_to.window(driver.window_handles[1])

        # call the function to scrape the new page
        eachRepoScrapper(driver)

        # close the tab
        driver.close()

        # switch to main tab
        driver.switch_to.window(driver.window_handles[0])

        wait = WebDriverWait(driver, 10)

        repos = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".pinned-item-list-item-content")))
        
    alllangs=[]
    for i in langs:
        b=i.split("\n")
        if b[0] not in alllangs:
            alllangs.append(b[0])
    
    # print(alllangs)

    # close chrome
    driver.close()

    return alllangs



#!/usr/bin/env python
#-*- coding:utf-8 -*-

# ScrapingElements.py Contains methods to retrieve specific elements needed for scraping the Website LON-CAPA

# author: Nicolai Böttger

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import sys


class CustomDriver():

    # ---Login page---

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("enable-automation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")

        # may have to change paths to work on different os
        # remove options to see browser instance
        self.driver = webdriver.Chrome(str(sys.path[0]) + "/chromedriver", options=options)

    def openLON_CAPAHomepage(self):
        self.driver.get("https://loncapa.hs-hannover.de/adm/roles")

    def getLoginNameLabelText(self):
        return self.driver.find_element_by_css_selector("[for='uname']").text

    def getLoginPasswordLabelText(self):
        return self.driver.find_element_by_css_selector("[for^='upass']").text

    def getLoginNameInputElement(self):
        return self.driver.find_element_by_css_selector("#uname")

    def getLoginPasswordInputElement(self):
        return self.driver.find_element_by_css_selector("[name='client'] [name^='upass']")

    def getLoginSendFormButton(self):
        return self.driver.find_element_by_css_selector("[name='client'] [type='submit']")

    def waitForCourseSelectionPage(self):
        self.waitForPage("[class='LC_odd_row'],[class='LC_even_row']", 10)

    def getCourseSelectionPageIdentifierElement(self):
        return self.driver.find_elements_by_css_selector("[class*='LC_data_table'] [class='LC_header_row']")

    def getContentTablePageIdentifierElement(self):
        return self.driver.find_elements_by_css_selector("div.LC_Box div#maincoursedoc")

    def getExercisePageIdentifierElement(self):
        return self.driver.find_elements_by_css_selector("form[name='lonhomework']")

    # ---Course selection page---

    def getCourseSelectButtons(self):
        return self.driver.find_elements_by_css_selector("[name*='fhhannover']")

    def getCoursesElements(self):
        return self.driver.find_elements_by_css_selector("[class^='LC_data_table'] tr:nth-child(even):not(:last-child)")

    def getCourseInformationElements(self, course):
        return course.find_elements_by_css_selector("td")

    def waitForContentTablePage(self):
        self.waitForPage("[class^='LC_data_table'] td:first-of-type a:last-of-type", 150)

    # ---Content table page---

    def getContentTableElements(self):
        return self.driver.find_elements_by_css_selector("[class^='LC_data_table'] td:first-of-type a:last-of-type")

    # ---Exercise page---

    def getTextsElements(self, tree):
        return tree.xpath("//body/form[@name='lonhomework']/input[@value='yes']/following-sibling::text()")

    def getRadTextsElements(self, tree):
        return tree.xpath("//body/form[@name='lonhomework']/label/input/following-sibling::text()")

    def getMoveSiteButtons(self):
        return self.driver.find_elements_by_css_selector(
            "#LC_breadcrumbs .LC_breadcrumb_tools_navigation [class='LC_menubuttons_link']")

    def getSendFormButton(self):
        return self.driver.find_element_by_css_selector("[name='lonhomework'] table tbody tr td input[onmouseup]")

    def waitForServerResponse(self):
        self.waitForPage("[name='lonhomework'] table tbody tr td[class*='LC_answer']", 3)

    def getMathJaxUndefElements(self):
        return self.driver.find_elements_by_css_selector("[name='lonhomework'] [class='MathJax_Display']")

    def getSelectExerciseElements(self):
        return self.driver.find_elements_by_css_selector("[name='lonhomework'] select")

    def getExerciseSelectWithOptionsElements(self):
        return self.driver.find_elements_by_css_selector("[name='lonhomework'] select option")

    def getMoveToContentTableElement(self):
        return self.driver.find_element_by_css_selector("#LC_MenuBreadcrumbs li a")

    def getTrysLeftElement(self):
        return self.driver.find_element_by_css_selector("[name='lonhomework'] table tbody tr td span")

    def getExerciseResponseElement(self):
        return self.driver.find_elements_by_css_selector("[name='lonhomework'] table tbody tr td[class*='LC_answer']")

    def getExerciseRadioButtonElements(self):
        return self.driver.find_elements_by_css_selector("[name='lonhomework'] input[type='radio']")

    def getExerciseInputElements(self):
        return self.driver.find_elements_by_css_selector("[name='lonhomework'] input[onkeydown]")

    def openSite(self, url):
        self.driver.get(url)

    def getPageSource(self):
        return self.driver.page_source

    def waitForPage(self, cssString, timeoutInS):
        timeout = timeoutInS
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, cssString))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
    
    def close(self):
        self.driver.quit()

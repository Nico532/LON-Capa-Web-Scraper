#!/usr/bin/env python
#-*- coding:utf-8 -*-

# LonCapaScraper.py: Contains the class LonCapaScraper, which scrapes the LON-CAPA Website and emulates it.

# author = "Nicolai Böttger"

import io
import re
import sys
import ScrapingElements
from lxml import etree
from selenium.webdriver.support.ui import Select

class LonCapaScraper:

    def __init__(self):
        self.se = ScrapingElements.CustomDriver()

    def start(self):
        self.lonCapaLogin()

    # asks for userInput, inputs it in text fields and presses login button
    def lonCapaLogin(self):
        self.se.openLON_CAPAHomepage()
        benutzerkennung = self.se.getLoginNameLabelText()
        # -- User Input for login name
        print(benutzerkennung + ": ")
        userLogin = input()
        # --
        password = self.se.getLoginPasswordLabelText()
        # -- User Input for login password
        print(password + ": ")
        userPass = input()
        # --
        self.se.getLoginNameInputElement().send_keys(userLogin)
        self.se.getLoginPasswordInputElement().send_keys(userPass)
        self.se.getLoginSendFormButton().click()
        self.se.waitForCourseSelectionPage()
        self.loadSiteType()

    # def lonCapaLoginInstant(self):
    #     self.se.openLON_CAPAHomepage()
    #     self.se.getLoginNameInputElement().send_keys(self.username)
    #     self.se.getLoginPasswordInputElement().send_keys(self.password)
    #     self.se.getLoginSendFormButton().click()
    #     self.se.waitForCourseSelectionPage()
    #     self.loadSiteType()

    # shows all of the users available courses and waits for user to select a course
    def navigateCourseSelection(self):
        courses = []
        # all course "Select" buttons
        buttons = self.se.getCourseSelectButtons()
        # all courses
        for counter, course in enumerate(self.se.getCoursesElements(), 1):
            tds = self.se.getCourseInformationElements(course)
            courseInfo = {
                "button": tds[0],
                "role": tds[1].text,
                "courseName": tds[2].text,
                "beginDate": tds[3].text,
                "endDate": tds[4].text
            }
            courses.append(courseInfo)
        for c, course in enumerate(courses):
            print(str(c) + "\n" + course.get("role") + "\n" + course.get("courseName") + "\n" + course.get(
                "beginDate") + "\n" + course.get("endDate"))
        # -- User Input for course selection
        print("Welcher Kurs? ")
        userCourse = self.verifyInt(0, len(buttons)-1)
        # --
        buttons[userCourse].click()
        self.se.waitForContentTablePage()
        self.loadSiteType()

    # returns all select and options in a dict
    def getExerciseSelectWithOptions(self):
        # get dropdownmenus
        selectInputs = self.se.getSelectExerciseElements()
        selectsWithOptions = {}
        for c, o in enumerate(selectInputs):
            options = [option.text for option in Select(o).options]
            name = "select" + str(c)
            selectsWithOptions[name] = options

        return selectsWithOptions

    # shows all the chapters in the course
    def showContentResult(self):
        # table of content
        table = self.se.getContentTableElements()
        for c, topic in enumerate(table):
            print(str(c) + ": " + topic.text)
        print("\nWelcher Inhalt? ")
        userContent = self.verifyInt(0, len(table)-1)
        if userContent == -1:
            self.navigateCourseSelection()
        self.se.openSite(table[userContent].get_attribute("href"))
        self.loadSiteType()

    # prints exercise description and button options and asks user for input
    def radButtonExercise(self, texts, radTexts, radButtonFields):
        for i in texts:
            print(i)
        for i in range(len(radTexts)):
            print(str(i+1) + ": " + radTexts[i])

        print(self.se.getTrysLeftElement().text)

        print("Aufgabe bearbeiten? <j> | <n>\n")
        userAns = input()

        if userAns.lower() != 'j':
            self.commandLineControl()

        print("Welche Antwort <1-" + str(len(radButtonFields)) + ">")
        inputNumber = self.verifyInt(1, len(radButtonFields))
        radButtonFields[inputNumber - 1].click()

        self.getServerResponse()

    # prints exercise description and select options and asks user for input
    def selectExercise(self, texts, selectFieldsDict):
        selectInputs = self.se.getSelectExerciseElements()
        for i in range(len(texts)):
            if i >= len(texts) - len(selectFieldsDict):
                string = "select" + str(i - (len(texts) - len(selectFieldsDict)))
                selectFieldsList = selectFieldsDict.get(string)
                print(" ,".join(selectFieldsList) + ": " + texts[i])
            else:
                print(texts[i])

        print(self.se.getTrysLeftElement().text)

        print("Aufgabe bearbeiten? <j> | <n>\n")
        userAns = input()

        if userAns.lower() != 'j':
            self.commandLineControl()

        # user input (select option)
        for c, i in enumerate(selectInputs):
            print("Option <0-" + str(len(selectFieldsDict.get("select" + str(c))) - 1) + ">" + " für Aufgabe " + str(
                c + 1))
            inputNumber = self.verifyInt(0, len(selectFieldsDict.get("select" + str(c))) - 1)
            Select(i).select_by_index(inputNumber)

        self.getServerResponse()

    # prints exercise description and asks user for input
    def textInputExercise(self, texts, textInputFields):
        for i in texts:
            print(i)

        print(self.se.getTrysLeftElement().text)

        print("Aufgabe bearbeiten? <j> | <n>\n")
        userAns = input()

        if userAns.lower() != 'j':
            self.commandLineControl()

        # user input (write text)
        for c, i in enumerate(textInputFields):
            print("Eingabe für Aufgabe " + str(c + 1))
            inputText = input()
            i.send_keys(inputText)
            

        self.getServerResponse()

    # formats exercise site and calls 1 of the three exercise methods, depending on which type is present on the site
    def showExercise(self):
        # use xpath instead of css selector
        # create tree from html
        parser = etree.HTMLParser()
        source = self.se.getPageSource()
        # regex htmlcode, to remove MathJax part
        source = re.sub(r'<script type="math/tex;.*?>(.*?)</script>', r"\1", source, 0,
                        re.DOTALL)
        tree = etree.parse(io.StringIO(source), parser=parser)
        # exercise description
        texts = self.se.getTextsElements(tree)
        radTexts = self.se.getRadTextsElements(tree)
        # regex to remove entries with only whitespace
        texts = [x for x in texts if len(re.findall(r'[a-zA-Z0-9]', x)) != 0]
        radTexts = [x for x in radTexts if len(re.findall(r'[a-zA-Z0-9]', x)) != 0]
        # remove trailing and leading whitespace
        for c, t in enumerate(texts):
            texts[c] = t.rstrip().lstrip()
        for c, t in enumerate(radTexts):
            radTexts[c] = t.rstrip().lstrip()

        undefExercise = self.findUndefinedTypes()
        selectFields = self.se.getSelectExerciseElements()
        selectFieldsDict = self.getExerciseSelectWithOptions()
        radButtonFields = self.se.getExerciseRadioButtonElements()
        textInputFields = self.se.getExerciseInputElements()

        if undefExercise:
            self.printExerciseNotDefined()
        elif selectFields:
            self.selectExercise(texts, selectFieldsDict)
        elif radButtonFields:
            self.radButtonExercise(texts, radTexts, radButtonFields)
        elif textInputFields:
            # clear input fields before use (they don't clear automatically)
            for j in textInputFields:
                j.clear()
            self.textInputExercise(texts, textInputFields)

        else:
            self.checkIfAnswered()

        self.commandLineControl()

    # move to the next exercise (green forward arrow in lon-capa)
    def moveForward(self):
        moveButtons = self.se.getMoveSiteButtons()
        moveButtons[1].click()
        self.loadSiteType()

    # move to previous exercise (green backward arrow in lon-capa)
    def moveBackward(self):
        moveButtons = self.se.getMoveSiteButtons()
        moveButtons[0].click()
        self.loadSiteType()

    # sends exercise form and retrieves server response
    def getServerResponse(self):
        formButton = self.se.getSendFormButton()
        formButton.click()
        serverResponse = self.se.getExerciseResponseElement()
        for res in serverResponse:
            print(res.text)
        self.se.waitForServerResponse()

    def findUndefinedTypes(self):
        mathJaxUndef = self.se.getMathJaxUndefElements()
        return mathJaxUndef

    def printExerciseNotDefined(self):
        print("Aufgabentyp nicht definiert!")

    # checks if exercise was already answered
    def checkIfAnswered(self):
        answered = self.se.getExerciseResponseElement()
        if answered:
            print(answered[0].text)
        else:
            self.printExerciseNotDefined()

    # looks for element identifiers on the exercise page and calls matching exercise method
    def loadSiteType(self):
        courseSelectionSite = self.se.getCourseSelectionPageIdentifierElement()
        contentNavigationSite = self.se.getContentTablePageIdentifierElement()
        exerciseSite = self.se.getExercisePageIdentifierElement()

        if courseSelectionSite:
            self.navigateCourseSelection()
        if contentNavigationSite:
            self.showContentResult()
        if exerciseSite:
            self.showExercise()

    # controls loncapa via command line
    def commandLineControl(self):
        # define what the user can do (go back to contentSelection/ courseSelection (load link), move forward, backward, answer exercise (check it))
        print("""Eingabe: Was möchten Sie tun?\n
        - 0: Aufgabe bearbeiten\n
        - 1: Nächste Aufgabe\n
        - 2: Inhaltsverzeichnis\n
        - 3: Kursauswahl\n
        - 4: Beenden
        """)
        userInput = self.verifyInt(0, 4)
        if userInput == 0:
            self.showExercise()
        elif userInput == 1:
            self.moveForward()
        elif userInput == 2:
            self.se.getMoveToContentTableElement().click()
            self.se.waitForContentTablePage()
            self.loadSiteType()
        elif userInput == 3:
            self.se.openSite("http://loncapa.hs-hannover.de/adm/roles")
            self.se.waitForCourseSelectionPage()
            self.loadSiteType()
        elif userInput == 4:
            self.se.close()
            sys.exit()

    # verify if variable is an int and between {min} and {max}
    def verifyInt(self, min, max):
        while True:
            userAnswer = input()
            try:
                val = int(userAnswer)
                assert max >= val >= min
                break
            except ValueError:
                print("Not a number")
            except AssertionError:
                print("Number not in valid range.")
        return val
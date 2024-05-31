#!/usr/bin/env python
#-*- coding:utf-8 -*-

# ExerciseScraper.py: Contains the class ExerciseScraper, which scrapes an exercise Page from a LON-CAPA Website.
#                     Uses request manipulation to communicate with the LON-CAPA server.
#                     Needs LON-CAPA Session ID to reach site
#                     Only works with sites with input fields
#                     ONLY FOR DEMONSTRATION PURPOSE
# author = "Nicolai Böttger"

import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import io
import sys

class ExerciseScraper():

    # cookies format
    # cookies = [{
    #     'domain': 'loncapa.hs-hannover.de',
    #     'httpOnly': True,
    #     'name': 'lonID',
    #     'path': '/',
    #     'secure': False,
    #     'value': 'loncapa_session_id'}] --- dynamic session id

    # headers format
    # headers = {
    #     'Upgrade-Insecure-Requests': '1',
    #     'Origin': 'http://loncapa.hs-hannover.de',
    #     'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryIAMbTYO88ptABeDj',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    def __init__(self, lonID):
        self.session = requests.Session()
        cookies = [{'domain': 'loncapa.hs-hannover.de', 'httpOnly': True, 'name': 'lonID', 'path': '/', 'secure': False,
                    'value': lonID}]
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

    # creates and sends a request and outputs response afterwards
    def createAndSendRequest(self, url, inputs, texts):
        payload = {}
        # ask user for input and place user input in payload
        for i in range(len(inputs)):
            print(texts[len(texts) - len(inputs) + i] + " ", end="")
            payload[inputs[i]] = input()
        payload["submitted"] = "part_0"
        # send the request including the payload
        response = self.session.post(url, data=payload)
        # print the server response
        self.printResponse(response.text)

    # returns the name of all <input>-elements
    def getExerciseInputNames(self, html_doc):
        soup = BeautifulSoup(html_doc, "lxml")
        names = [name.get("name") for name in soup.select("[name='lonhomework'] input[onkeydown]")]
        return names

    # prints the server response
    def printResponse(self, html_doc):
        soup = BeautifulSoup(html_doc, "lxml")
        elem = soup.select("[class*='LC_answer']")
        if elem:
            print(elem[0].text)

    # formats exercise site and scrapes site texts
    def showExercise(self, url):
        site = None
        try:
            site = self.session.get(url).text
        except requests.exceptions.MissingSchema as v:
            print(str(v))
            sys.exit()
        # use xpath instead of css selector
        # create tree from html
        parser = etree.HTMLParser()
        source = site
        # regex htmlcode, to remove MathJax part
        source = re.sub(r'<script type="math/tex;".*?>(.*?)</script>', r"\1", source, 0,
                        re.DOTALL)
        tree = etree.parse(io.StringIO(source), parser=parser)
        # exercise description
        texts = self.getTextsElements(tree)
        # regex to remove entries with only whitespace
        texts = [x for x in texts if len(re.findall(r'[a-zA-Z0-9]', x)) != 0]
        # remove trailing and leading whitespace
        for c, t in enumerate(texts):
            texts[c] = t.rstrip().lstrip()
        textDescr = ""
        names = self.getExerciseInputNames(source)
        for i in range(len(texts)):
            if (i < len(texts) - len(names)):
                textDescr += texts[i]
        print(textDescr)
        self.printTrysLeft(source)
        self.createAndSendRequest(url, names, texts)

    # returns text elements
    def getTextsElements(self, tree):
        return tree.xpath("//body/form[@name='lonhomework']/input[@value='yes']/following-sibling::text()")

    # prints trys left text
    def printTrysLeft(self, html_doc):
        soup = BeautifulSoup(html_doc, "lxml")
        trysLeft = soup.select("td span[class=LC_nobreak]")
        if trysLeft:
            print(soup.select("td span[class=LC_nobreak]")[0].text)
        else:
            print()

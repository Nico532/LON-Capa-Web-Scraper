#!/usr/bin/env python
#-*- coding:utf-8 -*-

# author = "Nicolai Böttger"
import sys

import ExerciseScraper

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Ungültige Anzahl Parameter! Benutzung:\n\npython ExerciseScraperStarter <lonID> <URL>\n")
        sys.exit()
    # input lon-capa session id
    lonID = sys.argv[1]
    # input sites url
    url = sys.argv[2]

    es = ExerciseScraper.ExerciseScraper(lonID)
    es.showExercise(url)


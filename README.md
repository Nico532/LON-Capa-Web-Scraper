##### Inhalt:

- Bachelorarbeit (PDF)
- SeleniumScraper: 
  - enthält Python Dateien für Emulation mittels des Selenium Frameworks)
  - enthält ChromeDriver version 86 (muss gleiche Version wie installierter Chrome Browser sein, andere Version downloadbar unter https://chromedriver.chromium.org/downloads)
  - Falls anderer Driver benutzt werden soll, muss in ScrapingElements.py anstatt Chrome z.B. Firefox Driver instanziiert werden, Firefox (geckodriver): https://github.com/mozilla/geckodriver/releases
- RequestScraper (enthält Python Dateien für Emulation mittels manuellem Abschicken des Requests)
  - funktioniert nur für Aufgaben mit Eingabefeld
  - funktioniert teilweise für Aufgaben ohne punkte (Erste Eingabe immer falsch, da Lon-Capa bei Aktualisierung der Seite Aufgabenstellung verändert)
- requirements.txt (Benutzt um virtuelle Python Environment mit den benötigten Dependencies zu generieren)




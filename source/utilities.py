import re
from datetime import datetime

import spacy
nlp = spacy.load("en_core_web_sm")


def filterStopWords(abstract):
    abstract = re.sub(r'-', ' ', abstract)
    filtered = re.sub(r"[.,]", '', abstract)
    doc = nlp(filtered)
    filtered_words = [token.text for token in doc if not token.is_stop]
    return ' '.join(filtered_words)


def doiLink(DOI):
    return DOI.startswith("https://doi.org/")


def removeLink(DOI):
    return re.sub("https://doi.org/", "", DOI)


def getYear(articleDate):
    # Assumes articleDate like "20XX-XX-XX"
    return int(articleDate[:4])


def yearsArray(firstYear, secondYear):
    return [str(year) for year in range(firstYear + 1, secondYear + 1)]


class timeArray:
    def __init__(self):
        self.years = yearsArray(2015, 2025)  # ['2016', ..., '2025']
        self.YEARS = len(self.years)

        self.timeSpanList = []
        for _ in range(self.YEARS):
            self.timeSpanList.append({
                "Semiconductors": 0,
                "Printed Circuit Boards": 0,
                "Electronic Waste": 0,
                "Batteries": 0,
                "Emissions": 0,
                "Water Refinement": 0,
                "Total": 0,
                "Uncertain": 0
            })

    def add(self, row, citationLimit):
        
        try:
            if int(row[5]) < citationLimit:
                return
            year = getYear(row[3])
            label = row[6]
            year_str = str(year)

            if year_str in self.years:
                year_index = self.years.index(year_str)
                if label in self.timeSpanList[year_index]:
                    self.timeSpanList[year_index][label] += 1
                    self.timeSpanList[year_index]["Total"] += 1
                    
            else:
                print(f"Year {year} not in range")
        except Exception as e:
            print(f"Error processing row {row}: {e}")

    def __iter__(self):
        return iter(self.timeSpanList)

    def toJson(self):
        return self.timeSpanList

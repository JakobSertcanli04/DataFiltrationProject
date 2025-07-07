import csv, json, scopus_data
import utilities

def to_dict(DOI, title, abstract, coverDate, link, label):
    return {
        "DOI": DOI,
        "Title": title,
        "Abstract": abstract,
        "Date": coverDate,
        "Link": link,
        "Label": label
     }

class CategoryHandler:
    def __init__(self):
        pass

    @staticmethod    
    def categoryCount(file, citationCount = 15):
        timeSpan = utilities.timeArray()
        with open(file, 'r', encoding='utf-8') as f:  
            csv_reader = csv.reader(f, delimiter=";")
            next(f)
            for row in csv_reader:      
                timeSpan.add(row, citationCount)
        return timeSpan
    
    @staticmethod   
    def writeCategory(dictionaryArray):


        with open('categorySortedByDateV.txt', 'w', encoding='utf-8') as file:
            for dict in dictionaryArray:
                json.dump(dict, file, ensure_ascii=False, indent=4)
        
            




        
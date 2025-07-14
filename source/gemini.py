
from google import genai
from google.genai import types
from entryUtilities import CsvFile
import time

def myFunc(e):
    return e['Label']


def geminiClassify(input_csv_path, topics):
    
   
    csvFile_instance = CsvFile()
    articles = csvFile_instance.readData(input_csv_path) 
    articleList = []
    client = genai.Client(api_key="AIzaSyC8mhmqYSfMT1_X6TlT5WHZIJedhXubWvQ")

    for _, article in enumerate(articles):
        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents= f"Your job is to categorize the following text into one of these labels. The the needs to be closely related to this topic. The label should under no circumstances be modified and only the topic label should be returned. {topics} place it into a category named Undefined if it does not fit either of these labels. {article['Abstract']}",        

        )
        
       # print(article['Abstract'])
        print(response.text)
        if response.text != "Undefined":    
            article['Label'] = response.text
       
        articleList.append(article)
        time.sleep(2.5) #The api only accept a certain amount of calls per minute..
    
    articles.sort(key=myFunc)
    csvFile_instance.writeLabeledDataArticles(input_csv_path, articles)
    
    return articleList

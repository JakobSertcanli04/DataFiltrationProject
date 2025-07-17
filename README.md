# Article Labeling Tool with Scopus Integration and Gemini Classifier 

## Project Overview
This project is a Tkinter-based GUI application that helps researchers and data analysts to automatically label scientific articles using pretrained machine learning models to retrieve articles from Scopus based on ISSN and year range.

It includes features for:
- Auto-labeling articles based on their abstract content.
- Gemini-based topic classification.
- Article fetching from Scopus using ISSN and year range.
- Word cloud visualization of the abstract data.
- An interactive line chart showing category trends over time.

  
## How It Works
- Load an Article CSV: Provide a .csv file with article data.

- Label the Articles: Use SetFitModel to assign category labels.

- (Optional) Run Gemini: Further classify using Gemini AI for fine-grained categorization.

- Visualize: Generate word clouds from abstracts.

- Fetch Articles from Scopus: Input ISSN and date range to auto-fetch data and save as CSV.       

# Prerequisites
  Python: https://www.python.org/downloads/ Can alternatively be installed from Microsoft store


# Installation 

## 1. Clone the Repository

        git clone https://github.com/JakobSertcanli04/DataFiltrationProject
        cd DataFiltrationProject

## 2. Create a Virtual Environment
        
        python -m venv venv
        source venv/bin/activate   # On Windows: venv\Scripts\activate

## 3. Install Dependencies
        pip install -r requirements.txt


## 4. Download Tensorflow 
        pip install tensorflow


## 5. Download the SetFit Model

        Ensure you have the SetFitModel locally or download from HuggingFace if internet access is available. Update the model path in:
        model = SetFitModel.from_pretrained("path_to_your_local_model")


## 6. Get your api key
        You can get your api key over here: https://dev.elsevier.com/apikey/manage
        Insert the api key into the apiKey field inside the ScopusData class which lays inside the scopus_data.py file

        
## Running the App

   python main.py



## 📣 Notes


        Your input .csv must have at least the following column headers:
        DOI	Title	Abstract	Date	Link	CitationCount	Label
   
        The Gemini classifier assumes an internet or LLM backend—ensure this is configured.
        The Scopus fetching feature requires API access or internal tools for data scraping (please follow Scopus T&Cs).
        Make sure the model path is valid and the directory structure supports it.

## Manual

        Run setfit_run.py

        How to retrieve articles:
        
          Create a csv file, this is where all of the articles will be stored.
          Find the isnn for the journal you want to retrieve.
          Select the start year and end year.
          Wait for the program to fetch all of the articles.
          
        How to categorize articles:
          Select the csv file you have previously created.
          *OPTIONAL* Fill the gemini classification box for more accurate classification.
          Enter the labels, seperated by comma and no spaces, Example: Semiconductor,Battery,Printed Circuit Board,Electrical Waste,Water Refinement,Emission
          The Citation Limit input box lets you specify a minimum number of citations an article must have to be included in the labeling process.
          Press start labeling

        Generate a word cloud:
          Select the csv file you want to generate a word cloud from
          Press Generate Word Cloud
          

        Generate a graph:
          Open the graph.py file.
          Insert the directory of the file you want to display a graph for.
          Make sure that the file ends with .txt
          Example: with open('filepath.txt', 'r') as f:
          Run the program.
          

          
          
        
        
        

       

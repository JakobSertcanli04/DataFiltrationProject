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

## Running the App

   python main.py



## 📣 Notes


        Your input .csv must have at least the following column headers:
    <img width="337" alt="Screenshot 2025-07-07 135124" src="https://github.com/user-attachments/assets/a4775110-917a-45ad-8ef5-a9b9169b50f8" />

        The Gemini classifier assumes an internet or LLM backend—ensure this is configured.
        The Scopus fetching feature requires API access or internal tools for data scraping (please follow Scopus T&Cs).
        Make sure the model path is valid and the directory structure supports it.

        You can get your api key over here: https://dev.elsevier.com/apikey/manage

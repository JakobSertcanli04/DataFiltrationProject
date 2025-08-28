# Article Classification Tool - Gemini Edition

## Project Overview
This project is a Tkinter-based GUI application that helps researchers and data analysts to automatically classify scientific articles using Google's Gemini AI. It includes features for retrieving articles from Scopus and generating visualizations.

### Key Features:
- **Gemini AI Classification**: Advanced topic classification using Google's Gemini model
- **Scopus Integration**: Fetch articles from Scopus using ISSN and year range
- **Interactive Visualizations**: 
  - Word cloud generation from article abstracts
  - Interactive graphs showing article distribution over time
  - Citation analysis dashboards
- **Simplified Workflow**: Streamlined UI with fewer clicks for better user experience

## Installation 

### 1. Clone the Repository
```bash
git clone https://github.com/JakobSertcanli04/DataFiltrationProject
cd DataFiltrationProject
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
- **Scopus API**: Get your API key from [Elsevier Developer Portal](https://dev.elsevier.com/apikey/manage)
- **Gemini API**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Update the API keys in the respective files:
  - `source/scopus_data.py` - for Scopus API key
  - `source/gemini.py` - for Gemini API key

### 5. Download Required Models
```bash
python -m spacy download en_core_web_sm
```

## Usage

### Running the Application
```bash
python source/main.py
```

### Workflow

#### 1. Fetch Articles from Scopus
1. Enter the ISSN of the journal you want to retrieve
2. Specify the start and end years
3. Set a citation limit (optional)
4. Choose where to save the CSV file
5. Click "Fetch Articles"

#### 2. Classify Articles with Gemini
1. Select your CSV file using the browse button
2. Enter topics for classification (comma-separated)
   - Example: `Semiconductor,Battery,Printed Circuit Board,Electrical Waste,Water Refinement,Emission`
3. Set minimum citation count (default: 10)
4. Click "Run Gemini Classification"

#### 3. Generate Visualizations
- **Word Cloud**: Click "Generate Word Cloud" to create a word cloud from article abstracts
- **Graph**: Click "Generate Graph" to create an interactive chart showing article distribution over time

## Input CSV Format
Your input CSV must have the following column headers:
- `DOI`
- `Title` 
- `Abstract`
- `Date`
- `Link`
- `CitationCount`
- `Label` (will be added after classification)

## Notes
- The Gemini classifier requires an internet connection
- The Scopus fetching feature requires API access (follow Scopus Terms & Conditions)
- Visualizations are saved as files and opened in your default browser
- Word clouds are generated for articles with sufficient citations (default: 15+ citations)

## Troubleshooting
- Ensure all API keys are properly configured
- Check that your CSV file has the required column headers
- Make sure you have sufficient internet connectivity for Gemini API calls
- For large datasets, processing may take some time - check the log output for progress


       

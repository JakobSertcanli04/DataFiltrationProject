🧠 Article Labeling and Classification Tool
This is a Python-based GUI application designed to:

Fetch scientific articles from Scopus using ISSN and a date range.

Automatically label articles based on their abstracts using a fine-tuned SetFit model.

Optionally run Gemini-based classification for more detailed topic insights.

Export labeled results to a CSV file.

🖥️ Features
Tkinter GUI: Simple and intuitive interface for non-technical users.

Automated Labeling: Uses SetFit (Sentence Transformer + Classifier) for zero-shot or few-shot classification.

Sub-Label Assignment: Adds secondary labels using custom assignSubLabels.

Gemini Integration: Optionally classify with Gemini for advanced categorization.

Scopus Integration: Retrieve articles by ISSN and year range.

CSV I/O: Read and write article data in CSV format.


✅ Requirements
Python 3.8+

Tkinter (comes with Python)

setfit

sentence-transformers

pandas

scikit-learn

Custom modules (labelUtilities, scopus_data, etc.)

Gemini API key if using gemini.py

📦 Installation
bash
Copy
Edit
pip install setfit pandas scikit-learn sentence-transformers
Ensure the following directories and files are correctly structured and available:

Pretrained SetFit model at:
C:/Users/USERNAME/Project_setfit/src/mpnet-base-v2

CSV files with appropriate schema (Title, Abstract, etc.)

Your gemini.py must be configured with valid access if using Gemini classification.

🚀 Usage
1. Run the Application
bash
Copy
Edit
python main.py
2. Label Existing Articles
Click Browse to select a CSV file of articles.

Check "Run Gemini" to enable Gemini classification (optional).

Click "Start Labeling".

3. Fetch New Articles from Scopus
Enter:

ISSN

Start Year

End Year

Output filename (CSV)

Click "Fetch Articles".

Labeled results will be written to the specified file, and categories will be counted and saved.

📋 Output Format
The output CSV will include additional columns:

Label: Primary category (e.g., Semiconductors, Waste)

SubLabel: Secondary topic if assigned (via assignSubLabels)

Possibly Gemini-based topics if used.

A separate file (from CategoryHandler.writeCategory) summarizes label counts.

🔧 Customization
Edit candidate_labels in labelArticles() if you want different categories.

Modify SetFit model path to use your own pretrained model.

Sub-label logic can be extended in setfit_subcategory.py.

🛠️ Troubleshooting
Model Not Found?
Make sure mpnet-base-v2 directory exists and contains the proper model files.

No output or error?
Check log window for error messages.

Gemini errors?
Ensure API key and internet access are valid.

🧑‍💻 Contributors
Initial Author: [Your Name]

Dependencies: HuggingFace SetFit, Scikit-learn, Gemini API, Elsevier Scopus API (assumed)

📄 License
MIT License or appropriate license based on dependencies and usage.

Let me know if you want to generate a sample requirements.txt or setup.py file to package this!

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
from setfit import SetFitModel
from labelUtilities import CategoryHandler
from entryUtilities import CsvFile
import scopus_data
from setfit_subcategory import assignSubLabels
from gemini import geminiClassify

from wordcloud_graph import run_wordcloud

'''''
The code provided is a Python script that creates a GUI application using the tkinter
library for labeling articles and fetching articles from Scopus. The script includes functions for
labeling articles based on their abstracts, assigning labels to articles, fetching articles from
Scopus based on ISSN and year range, and running Gemini classification on the labeled articles.
'''''


def toAbstracts(articles):
    return [article["Abstract"] for article in articles]

def myFunc(e):
    return e['Label']

def assignLabels(articles, candidate_labels, threshold=0.6):
    model = SetFitModel.from_pretrained("sentence-transformers/all-mpnet-base-v2")
    abstracts = toAbstracts(articles)
    predictions = model.predict_proba(abstracts)
    labeled_articles = []

    for i, probs in enumerate(predictions):
        max_prob = max(probs)
        label_index = probs.tolist().index(max_prob)
        if max_prob >= threshold:
            articles[i]['Label'] = candidate_labels[label_index]
            labeled_articles.append(articles[i])

    labeled_articles.sort(key=myFunc)
    return labeled_articles

def labelArticles(input_csv_path, log_callback=None):
    try:
        csvFile_instance = CsvFile()
        articles = csvFile_instance.readData(input_csv_path) 
        candidate_labels = ['Printed Circuit Boards', 'Waste', 'Batteries', 'Semiconductors', 'Water Refinement', 'Emissions']
        if log_callback: log_callback("Labeling articles...")

        labeledArticles = assignLabels(articles, candidate_labels)
        csvFile_instance.writeLabeledDataArticles(input_csv_path, labeledArticles)

        if log_callback: log_callback("Labeling complete. Writing category counts...")
        categoryCountDict = CategoryHandler.categoryCount(input_csv_path)
        CategoryHandler.writeCategory(categoryCountDict)
        if log_callback: log_callback("Done.")
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        else:
            print(e)

def fetch_articles(issn, start_year, end_year, output_path, log_callback=None):
    try:
        if log_callback: log_callback(f"Fetching articles for ISSN {issn} from {start_year} to {end_year}...")
        scopus_instance = scopus_data.ScopusData()
        years = scopus_data.yearsArray(int(start_year), int(end_year))
        journal = scopus_instance.getJournal(issn, years)
        csv_instance = CsvFile()
        csv_instance.writeDataArticles(output_path, journal.articles)
        if log_callback: log_callback(f"Articles written to: {output_path}")
    except Exception as e:
        if log_callback: log_callback(f"Error: {e}")
        else: print(e)

def run_labeling(filepath, run_gemini, log_callback):
    def task():
        labelArticles(filepath, log_callback)
        if run_gemini:
            topics = ["Semiconductors", "Electronic Waste", "Emissions", "Printed Circuit Boards", "Batteries", "Water Refinement"]
            log_callback("Running Gemini classification...")
            geminiClassify(filepath, topics)
            log_callback("Gemini classification complete.")
            categoryCountDict = CategoryHandler.categoryCount(filepath)
            CategoryHandler.writeCategory(categoryCountDict)
    threading.Thread(target=task).start()

def run_fetch_articles(issn, start_year, end_year, output_path, log_callback):
    def task():
        fetch_articles(issn, start_year, end_year, output_path, log_callback)
    threading.Thread(target=task).start()
def labelArticles(input_csv_path, custom_labels, log_callback=None):
    try:
        csvFile_instance = CsvFile()
        articles = csvFile_instance.readData(input_csv_path)

        if not custom_labels:
            raise ValueError("No labels provided.")
        
        candidate_labels = custom_labels.split(",")  # Splitting by comma to allow multiple labels
        
        if log_callback: log_callback("Labeling articles...")

        labeledArticles = assignLabels(articles, candidate_labels)
        assignSubLabels(labeledArticles)

        csvFile_instance.writeLabeledDataArticles(input_csv_path, labeledArticles)

        if log_callback: log_callback("Labeling complete. Writing category counts...")
        categoryCountDict = CategoryHandler.categoryCount(input_csv_path)
        CategoryHandler.writeCategory(categoryCountDict)
        if log_callback: log_callback("Done.")
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        else:
            print(e)


def create_ui():
    window = tk.Tk()
    window.title("Article Labeling Tool")
    window.geometry("650x600")

    def log(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)

    # === File Selector ===
    file_frame = tk.LabelFrame(window, text="Label Existing CSV", padx=10, pady=10)
    file_frame.pack(fill="x", padx=10, pady=5)

    file_entry = tk.Entry(file_frame, width=50)
    file_entry.pack(side=tk.LEFT, padx=5)

    browse_btn = tk.Button(file_frame, text="Browse", command=lambda: file_entry.insert(0, filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])))
    browse_btn.pack(side=tk.LEFT)

    gemini_var = tk.BooleanVar()
    gemini_check = tk.Checkbutton(file_frame, text="Run Gemini", variable=gemini_var)
    gemini_check.pack(side=tk.LEFT, padx=5)

    # === Custom Labels Input ===
    tk.Label(file_frame, text="Enter Labels (comma-separated)").pack(side=tk.LEFT, padx=5)
    labels_entry = tk.Entry(file_frame, width=50)
    labels_entry.pack(side=tk.LEFT, padx=5)

    # === Custom Topics for Gemini ===
    tk.Label(file_frame, text="Enter Topics for Gemini (comma-separated)").pack(side=tk.LEFT, padx=5)
    gemini_topics_entry = tk.Entry(file_frame, width=50)
    gemini_topics_entry.pack(side=tk.LEFT, padx=5)

    start_labeling_btn = tk.Button(file_frame, text="Start Labeling", command=lambda: run_labeling(file_entry.get(), gemini_var.get(), log, labels_entry.get(), gemini_topics_entry.get()))
    start_labeling_btn.pack(side=tk.LEFT, padx=5)

    wordcloud_btn = tk.Button(file_frame, text="Generate Word Cloud", command=lambda: run_wordcloud(file_entry.get(), log))
    wordcloud_btn.pack(side=tk.LEFT, padx=5)

    fetch_frame = tk.LabelFrame(window, text="Fetch Articles from Scopus", padx=10, pady=10)
    fetch_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(fetch_frame, text="ISSN").grid(row=0, column=0)
    issn_entry = tk.Entry(fetch_frame)
    issn_entry.grid(row=0, column=1)

    tk.Label(fetch_frame, text="Start Year").grid(row=0, column=2)
    start_year_entry = tk.Entry(fetch_frame, width=5)
    start_year_entry.grid(row=0, column=3)

    tk.Label(fetch_frame, text="End Year").grid(row=0, column=4)
    end_year_entry = tk.Entry(fetch_frame, width=5)
    end_year_entry.grid(row=0, column=5)

    tk.Label(fetch_frame, text="Save As").grid(row=1, column=0)
    output_path_entry = tk.Entry(fetch_frame, width=40)
    output_path_entry.grid(row=1, column=1, columnspan=4)

    def browse_save_path():
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, filename)

    browse_output_btn = tk.Button(fetch_frame, text="Browse", command=browse_save_path)
    browse_output_btn.grid(row=1, column=5)

    fetch_btn = tk.Button(fetch_frame, text="Fetch Articles", command=lambda: run_fetch_articles(
        issn_entry.get(),
        start_year_entry.get(),
        end_year_entry.get(),
        output_path_entry.get(),
        log
    ))
    fetch_btn.grid(row=2, column=0, columnspan=6, pady=5)

    log_box = scrolledtext.ScrolledText(window, width=80, height=20)
    log_box.pack(padx=10, pady=10)

    window.mainloop()


def run_labeling(filepath, run_gemini, log_callback, custom_labels, custom_gemini_topics):
    def task():
        labelArticles(filepath, custom_labels, log_callback)
        if run_gemini:
            # Split the custom Gemini topics and pass them to the Gemini classification
            topics = custom_gemini_topics.split(",") if custom_gemini_topics else []
            log_callback("Running Gemini classification...")
            geminiClassify(filepath, topics)
            log_callback("Gemini classification complete.")
            categoryCountDict = CategoryHandler.categoryCount(filepath)
            CategoryHandler.writeCategory(categoryCountDict)
    threading.Thread(target=task).start()


if __name__ == "__main__":
    create_ui()




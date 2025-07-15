import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
from setfit import SetFitModel
from labelUtilities import CategoryHandler
from entryUtilities import CsvFile
import scopus_data
from gemini import geminiClassify
from wordcloud_graph import run_wordcloud
from transformers import pipeline


def myFunc(e):
    return e['Label']


def toAbstracts(articles):
    return [article["Abstract"] for article in articles]

def myFunc(e):
    return e['Label']

def assignLabels(articles, candidate_labels, threshold=0.55):
    classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1", device=0)
    abstracts = toAbstracts(articles)
    labeled_articles = []

    for i, abstract in enumerate(abstracts):
        print(i)
        print(candidate_labels)
        result = classifier(abstract, candidate_labels)
        scores = result['scores']
        labels = result['labels']
        
        max_score = scores[0]
        best_label = labels[0]
        
        if max_score >= threshold:
            articles[i]['Label'] = best_label
            labeled_articles.append(articles[i])

    labeled_articles.sort(key=myFunc)
    return labeled_articles

def labelArticles(input_csv_path, custom_labels, citation_threshold, log_callback=None):
    try:
        csvFile_instance = CsvFile()
        articles = csvFile_instance.readData(input_csv_path)

        # Filter based on citation count
        if citation_threshold is not None:
            citation_threshold = int(citation_threshold)
            articles = [article for article in articles if int(article.get("CitationCount", 0)) >= citation_threshold]
            print(articles)
        if not custom_labels:
            raise ValueError("No labels provided.")
        
        candidate_labels = custom_labels.split(",")  # Comma-separated input
        
        if log_callback: log_callback("Labeling articles...")

        labeledArticles = assignLabels(articles, candidate_labels)
        csvFile_instance.writeLabeledDataArticles(input_csv_path, labeledArticles)
        categoryCountDict = CategoryHandler.categoryCount(articles)
        CategoryHandler.writeCategory(categoryCountDict, input_csv_path)
        
        if log_callback: log_callback("Done.")
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        else:
            print(e)

def fetch_articles(issn, start_year, end_year, output_path, citation_limit=0, log_callback=None):
    try:
        if log_callback: log_callback(f"Fetching articles for ISSN {issn} from {start_year} to {end_year}...")
        scopus_instance = scopus_data.ScopusData()
        years = scopus_data.yearsArray(int(start_year), int(end_year))
        citation_limit = int(citation_limit) if citation_limit else 0

        journal = scopus_instance.getJournal(issn, years, citation_limit)

        csv_instance = CsvFile()
        csv_instance.writeDataArticles(output_path, journal.articles)

        if log_callback: log_callback(f"{len(journal.articles)} articles written to: {output_path}")
    except Exception as e:
        if log_callback: log_callback(f"Error: {e}")
        else: print(e)

def run_labeling(filepath, run_gemini, log_callback, custom_labels, citation_threshold):
    def task():
        labelArticles(filepath, custom_labels, citation_threshold, log_callback)
        if run_gemini:
            topics = custom_labels.split(",") if custom_labels else []
            log_callback("Running Gemini classification...")

            articles = geminiClassify(filepath, topics)
            log_callback("Gemini classification complete.")
            categoryCountDict = CategoryHandler.categoryCount(articles)

            CategoryHandler.writeCategory(categoryCountDict, filepath)
    threading.Thread(target=task).start()

def run_fetch_articles(issn, start_year, end_year, output_path, citation_limit, log_callback):
    def task():
        fetch_articles(issn, start_year, end_year, output_path, citation_limit, log_callback)
    threading.Thread(target=task).start()

def create_ui():
    window = tk.Tk()
    window.title("Article Labeling Tool")
    window.geometry("750x650")

    def log(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)

    # === Label Existing CSV Frame ===
    file_frame = tk.LabelFrame(window, text="Label Existing CSV", padx=10, pady=10)
    file_frame.pack(fill="x", padx=10, pady=5)

    file_entry = tk.Entry(file_frame, width=50)
    file_entry.pack(side=tk.LEFT, padx=5)

    browse_btn = tk.Button(file_frame, text="Browse", command=lambda: file_entry.insert(0, filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])))
    browse_btn.pack(side=tk.LEFT)

    gemini_var = tk.BooleanVar()
    gemini_check = tk.Checkbutton(file_frame, text="Run Gemini", variable=gemini_var)
    gemini_check.pack(side=tk.LEFT, padx=5)

    label_frame = tk.Frame(window)
    label_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(label_frame, text="Labels / Gemini Topics (comma-separated):").grid(row=0, column=0, sticky="w")
    labels_entry = tk.Entry(label_frame, width=70)
    labels_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(label_frame, text="Min Citation Count:").grid(row=1, column=0, sticky="w")
    citation_threshold_entry = tk.Entry(label_frame, width=10)
    citation_threshold_entry.grid(row=1, column=1, sticky="w", padx=5)

    control_frame = tk.Frame(window)
    control_frame.pack(fill="x", padx=10, pady=5)

    start_labeling_btn = tk.Button(control_frame, text="Start Labeling", command=lambda: run_labeling(
        file_entry.get(),
        gemini_var.get(),
        log,
        labels_entry.get(),
        citation_threshold_entry.get()
    ))
    start_labeling_btn.pack(side=tk.LEFT, padx=5)

    wordcloud_btn = tk.Button(control_frame, text="Generate Word Cloud", command=lambda: run_wordcloud(file_entry.get(), log))
    wordcloud_btn.pack(side=tk.LEFT, padx=5)

    # === Fetch Articles Frame ===
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

    tk.Label(fetch_frame, text="Citation Limit").grid(row=2, column=0)
    citation_limit_fetch_entry = tk.Entry(fetch_frame, width=5)
    citation_limit_fetch_entry.grid(row=2, column=1)

    fetch_btn = tk.Button(fetch_frame, text="Fetch Articles", command=lambda: run_fetch_articles(
        issn_entry.get(),
        start_year_entry.get(),
        end_year_entry.get(),
        output_path_entry.get(),
        citation_limit_fetch_entry.get(),
        log
    ))
    fetch_btn.grid(row=2, column=2, columnspan=4, pady=5)

    # === Log Output Box ===
    log_box = scrolledtext.ScrolledText(window, width=90, height=20)
    log_box.pack(padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_ui()

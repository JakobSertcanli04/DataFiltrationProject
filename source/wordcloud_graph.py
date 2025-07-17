from entryUtilities import CsvFile
from utilities import filterStopWords  # Ensure this is implemented
from wordcloud import WordCloud, STOPWORDS
import threading
import matplotlib.pyplot as plt



def run_wordcloud(filepath, log_callback):
    def task():
        try:
            log_callback("Generating Word Cloud...")
            csvFile_instance = CsvFile()
            articles = csvFile_instance.readData(filepath)

            abstracts = " ".join([
                filterStopWords(article["Abstract"])
                for article in articles
                if int(article.get('CitationCount', 0)) >= 15
            ])

            if not abstracts.strip():
                log_callback("No valid abstracts with sufficient citations.")
                return

            stopwords = set(STOPWORDS)
            wordcloud = WordCloud(
                max_font_size=50,
                max_words=100,
                stopwords=stopwords,
                background_color="white"
            ).generate(abstracts)

            wordcloud.to_file("wordcloud.png")

            plt.figure()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()

            log_callback("Word Cloud generated and saved as 'wordcloud.png'")
        except Exception as e:
            log_callback(f"Error generating word cloud: {e}")
    threading.Thread(target=task).start()

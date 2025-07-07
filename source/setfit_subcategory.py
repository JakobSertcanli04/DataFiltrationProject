
from setfit import SetFitModel
from labelUtilities import CategoryHandler
from utilities import filterStopWords
from entryUtilities import CsvFile
import scopus_data
import numpy as np


def toAbstracts(articles):
    abstracts = []
    for article in articles:
        abstracts.append(article["Abstract"])  # get abstracts by key
    return abstracts

def assignSubLabels(articles, threshold=0.55):

 
    candidate_labels = [
       
        'Electronic Waste', 
        'General Waste'
    ]

    # Load fine-tuned SetFit model
    model = SetFitModel.from_pretrained("C:/Users/sejaser1/Project_setfit/src/mpnet-base-v2-sub-waste")

    # Collect Waste-labeled articles
    subCategory = []
    subCategoryIndex = []
    uncertain_indices = []

    for i, article in enumerate(articles):
        if article["Label"] == "Waste":
            subCategory.append(article["Abstract"])  # Assuming the text is stored under "text"
            subCategoryIndex.append(i)

    # Predict probabilities
    predictions = model.predict_proba(subCategory)

    print(predictions)

    for i, idx in enumerate(subCategoryIndex):
        pred_probs = predictions[i]
        max_prob = max(pred_probs)
        label_index = np.argmax(pred_probs)
        
        if max_prob >= threshold and candidate_labels[label_index] == "Electronic Waste":
            label = candidate_labels[label_index]
        else:
            label = "Uncertain"
            uncertain_indices.append(idx)
        
        articles[idx]['Label'] = label
    
    for idx in sorted(uncertain_indices, reverse=True):
        del articles[idx]    


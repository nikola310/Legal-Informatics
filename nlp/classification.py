import json
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pylab as pl
from nltk import pos_tag
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from sklearn import model_selection, naive_bayes, svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

serbian_stop_words = ["biti", "ne", "jesam", "sam", "jesi", "si", "je", "jesmo", "smo", "jeste", "ste", "jesu", "su",
                    "nijesam", "nisam", "nijesi", "nisi", "nije", "nijesmo", "nismo", "nijeste", "niste", "nijesu", "nisu",
                    "budem", "budeš", "bude", "budemo", "budete", "budu","budes", "bih",  "bi", "bismo", "biste", "biše", "bise",
                    "bio", "bili", "budimo", "budite", "bila", "bilo", "bile", "cu", "ceš", "ce", "cemo", "cete", "necu", "neceš", "nece", 
                    "necemo", "necete", "cu", "ces", "ce", "cemo", "cete", "necu", "neces", "nece", "necemo", "necete", "mogu", "možeš", 
                    "može", "možemo", "možete", "mozes", "moze", "mozemo", "mozete", "i", "a", "ili", "ali", "pa", "te", "da", "u", "po", "na"]


def runScript():
    #np.random.seed(500)
    Corpus = pd.read_csv(r"out_training.csv", encoding='utf-8')
    Test_corpus = pd.read_csv(r"out_test.csv", encoding='utf-8')

    # Plot number of entities by class
    s = Corpus['LABEL'].value_counts()
    x = []
    y = []
    for i, v in s.items():
        x.append(i)
        y.append(v)
        print('class: ', i, 'number: ', v)
    
    plt.bar(x,y)
    plt.gca().set(xlabel='Type of judgements', ylabel='Number of judgements')
    plt.show()

    print('Processing data started.')
    # Remove blank rows if any.
    Corpus['TEXT'].dropna(inplace=True)
    Test_corpus['TEXT'].dropna(inplace=True)

    # Change all the text to lower case.
    Corpus['TEXT'] = [entry.lower() for entry in Corpus['TEXT']]
    Test_corpus['TEXT'] = [entry.lower() for entry in Test_corpus['TEXT']]

    # Tokenization
    Corpus['TEXT']= [word_tokenize(entry) for entry in Corpus['TEXT']]
    Test_corpus['TEXT']= [word_tokenize(entry) for entry in Test_corpus['TEXT']]

    print('Tokenization successful.')

    # Remove Stop words
    removeStopWords(Corpus)
    removeStopWords(Test_corpus)

    print('Stop words removed.')

    # Encode labels and transform text to document-term matrix
    Encoder = LabelEncoder()
    Train_Y = Encoder.fit_transform(Corpus['LABEL'])
    Test_Y = Encoder.fit_transform(Test_corpus['LABEL'])

    print('Encoding successful.')

    Tfidf_vect = TfidfVectorizer(max_features=5000)
    Tfidf_vect.fit(Corpus['TEXT_FINAL'])
    
    Train_X_Tfidf = Tfidf_vect.transform(Corpus['TEXT_FINAL'])
    Test_X_Tfidf = Tfidf_vect.transform(Test_corpus['TEXT_FINAL'])

    # Fit the training dataset on the NB classifier and predict on test dataset
    Naive = naive_bayes.MultinomialNB()
    Naive.fit(Train_X_Tfidf, Train_Y)
    print('Naive Bayes fit successful.')
    predictions_NB = Naive.predict(Test_X_Tfidf)
    print("Naive Bayes Accuracy Score -> ", accuracy_score(predictions_NB, Test_Y)*100)

    # Fit the training dataset on the SVM classifier and predict on test dataset
    SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    SVM.fit(Train_X_Tfidf, Train_Y)
    print('SVM fit successful.')
    predictions_SVM = SVM.predict(Test_X_Tfidf)    
    print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM, Test_Y)*100)
    
    # Save to JSON files
    labels_nb = Encoder.inverse_transform(predictions_NB)
    labels_svm = Encoder.inverse_transform(predictions_SVM)
    saveToJSON(Encoder, Test_corpus, labels_nb, 'predictions_bayes.json')
    saveToJSON(Encoder, Test_corpus, labels_svm, 'predictions_svm.json')
    print('Results saved to JSON files.')


def removeStopWords(Corpus):
    for index,entry in enumerate(Corpus['TEXT']):
        Final_words = []
        for word in entry:
            if word not in serbian_stop_words:
                Final_words.append(word)
        Corpus.loc[index,'TEXT_FINAL'] = str(Final_words)

def saveToJSON(Encoder, corpus, predictions, file_name):
    toSave = {}
    for index, row in corpus.iterrows():
        toSave[row['ID']] = predictions[index]
    with open(file_name, 'w') as f:
        json.dump(toSave, f, sort_keys=True, indent=4)

if __name__ == "__main__":
    runScript()
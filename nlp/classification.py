import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
import json

serbian_stop_words = ["biti", "ne", "jesam", "sam", "jesi", "si", "je", "jesmo", "smo", "jeste", "ste", "jesu", "su",
                    "nijesam", "nisam", "nijesi", "nisi", "nije", "nijesmo", "nismo", "nijeste", "niste", "nijesu", "nisu",
                    "budem", "budeš", "bude", "budemo", "budete", "budu","budes", "bih",  "bi", "bismo", "biste", "biše", "bise",
                    "bio", "bili", "budimo", "budite", "bila", "bilo", "bile", "cu", "ceš", "ce", "cemo", "cete", "necu", "neceš", "nece", 
                    "necemo", "necete", "cu", "ces", "ce", "cemo", "cete", "necu", "neces", "nece", "necemo", "necete", "mogu", "možeš", 
                    "može", "možemo", "možete", "mozes", "moze", "mozemo", "mozete", "i", "a", "ili", "ali", "pa", "te", "da", "u", "po", "na"]


def runScript():
    np.random.seed(500)
    Corpus = pd.read_csv(r"out_training.csv", encoding='utf-8')
    Test_corpus = pd.read_csv(r"out_test.csv", encoding='utf-8')

    # Remove blank rows if any.
    Corpus['TEXT'].dropna(inplace=True)
    Test_corpus['TEXT'].dropna(inplace=True)

    # Change all the text to lower case.
    Corpus['TEXT'] = [entry.lower() for entry in Corpus['TEXT']]
    Test_corpus['TEXT'] = [entry.lower() for entry in Test_corpus['TEXT']]

    # Tokenization
    Corpus['TEXT']= [word_tokenize(entry) for entry in Corpus['TEXT']]
    Test_corpus['TEXT']= [word_tokenize(entry) for entry in Test_corpus['TEXT']]

    # Remove Stop words, Non-Numeric and perfom Word Stemming/Lemmenting.
    removeStopWords(Corpus)
    removeStopWords(Test_corpus)

    Encoder = LabelEncoder()
    Train_Y = Encoder.fit_transform(Corpus['LABEL'])
    Test_Y = Encoder.fit_transform(Test_corpus['LABEL'])

    Tfidf_vect = TfidfVectorizer(max_features=5000)
    Tfidf_vect.fit(Corpus['TEXT_FINAL'])

    Train_X_Tfidf = Tfidf_vect.transform(Corpus['TEXT_FINAL'])
    Test_X_Tfidf = Tfidf_vect.transform(Test_corpus['TEXT_FINAL'])

    # fit the training dataset on the NB classifier
    Naive = naive_bayes.MultinomialNB()
    Naive.fit(Train_X_Tfidf, Train_Y)

    # predict the labels on validation dataset
    predictions_NB = Naive.predict(Test_X_Tfidf)

    # Use accuracy_score function to get the accuracy
    print("Naive Bayes Accuracy Score -> ", accuracy_score(predictions_NB, Test_Y)*100)

    # Classifier - Algorithm - SVM
    # fit the training dataset on the classifier
    SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    SVM.fit(Train_X_Tfidf, Train_Y)

    # predict the labels on validation dataset
    predictions_SVM = SVM.predict(Test_X_Tfidf)
    
    # Use accuracy_score function to get the accuracy
    print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM, Test_Y)*100)
    
    # Save to JSON files
    labels_nb = Encoder.inverse_transform(predictions_NB)
    labels_svm = Encoder.inverse_transform(predictions_SVM)
    saveToJSON(Encoder, Test_corpus, labels_nb, 'predictions_bayes.json')
    saveToJSON(Encoder, Test_corpus, labels_svm, 'predictions_svm.json')


def removeStopWords(Corpus):
    # WordNetLemmatizer requires Pos tags to understand if the word is noun or verb or adjective etc. By default it is set to Noun
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV

    for index,entry in enumerate(Corpus['TEXT']):
        # Declaring Empty List to store the words that follow the rules for this step
        Final_words = []
        # Initializing WordNetLemmatizer()
        word_Lemmatized = WordNetLemmatizer()
        # pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
        for word, tag in pos_tag(entry):
            # Below condition is to check for Stop words and consider only alphabets
            if word not in serbian_stop_words:
                word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
                Final_words.append(word_Final)
        # The final processed set of words for each iteration will be stored in 'text_final'
        Corpus.loc[index,'TEXT_FINAL'] = str(Final_words)

def saveToJSON(Encoder, corpus, predictions, file_name):
    toSave = {}
    for index, row in corpus.iterrows():
        toSave[row['ID']] = predictions[index]
    
    with open(file_name, 'w') as f:
        json.dump(toSave, f, sort_keys=True, indent=4)

if __name__ == "__main__":
    runScript()
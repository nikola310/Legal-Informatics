import gensim
import os
import tkinter as tk
from tkinter import filedialog
from nltk.tokenize import word_tokenize

serbian_stop_words = ["biti", "ne", "jesam", "sam", "jesi", "si", "je", "jesmo", "smo", "jeste", "ste", "jesu", "su",
                    "nijesam", "nisam", "nijesi", "nisi", "nije", "nijesmo", "nismo", "nijeste", "niste", "nijesu", "nisu",
                    "budem", "budeš", "bude", "budemo", "budete", "budu","budes", "bih",  "bi", "bismo", "biste", "biše", "bise",
                    "bio", "bili", "budimo", "budite", "bila", "bilo", "bile", "cu", "ceš", "ce", "cemo", "cete", "necu", "neceš", "nece", 
                    "necemo", "necete", "cu", "ces", "ce", "cemo", "cete", "necu", "neces", "nece", "necemo", "necete", "mogu", "možeš", 
                    "može", "možemo", "možete", "mozes", "moze", "mozemo", "mozete", "i", "a", "ili", "ali", "pa", "te", "da", "u", "po", "na"]

def start_program():
    root = tk.Tk()
    root.withdraw()
    corpus_path = filedialog.askdirectory()
    create_corpus(corpus_path)

def create_corpus(corpus_path):
    judgements_corpus = []

    for filename in os.listdir(corpus_path):
        if filename.startswith('presuda_text_') and filename.endswith('.txt'):
            file_fullpath = corpus_path + os.path.sep + filename
            with open(file_fullpath, 'r', encoding = 'utf-8') as judgement_file:
                judgement_text = judgement_file.read()
                judgements_corpus.append({'judgement_filename' : filename, 'judgement_filepath' : file_fullpath, 'judgement_text' : judgement_text.replace('\n', ' ')})

    create_dictionary_and_bow_representation(judgements_corpus)

def create_dictionary_and_bow_representation(judgements_corpus):
    judgements_words = [[word.lower() for word in word_tokenize(judgement['judgement_text']) if word.lower() not in serbian_stop_words]
                         for judgement in judgements_corpus]

    dictionary = gensim.corpora.Dictionary(judgements_words)
    bow_representation = [dictionary.doc2bow(judgement_word) for judgement_word in judgements_words]
    create_tf_idf_and_similarity_measure(judgements_corpus,dictionary,bow_representation)

def create_tf_idf_and_similarity_measure(judgements_corpus,dictionary,bow_representation):
    tf_idf = gensim.models.TfidfModel(bow_representation)
    output = "judgementSimilarityOutput" + os.path.sep
    if not os.path.exists(output):
        os.mkdir(output)
    sims = gensim.similarities.Similarity(output,tf_idf[bow_representation],num_features=len(dictionary),num_best=10)
    create_query_doc(judgements_corpus,tf_idf,sims,dictionary)

def create_query_doc(judgements_corpus,tf_idf,sims,dictionary):
    root = tk.Tk()
    root.withdraw()
    with open(filedialog.askopenfilename(filetypes=[("Text files","*.txt")]), 'r', encoding='utf-8') as query_doc_file:
        query_doc = [query_doc_word.lower() for query_doc_word in word_tokenize(query_doc_file.read().replace('\n', ' ')) if query_doc_word.lower() not in serbian_stop_words] 
        query_doc_bow = dictionary.doc2bow(query_doc)
        query_doc_tf_idf = tf_idf[query_doc_bow]

        results = sims[query_doc_tf_idf]
        for result in results:
            print(judgements_corpus[result[0]]['judgement_filename'] + "," + judgements_corpus[result[0]]['judgement_filepath'] + "," + str(results[1]))

if __name__ == "__main__":
    start_program()
import nltk, io, os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw() 
directory = filedialog.askdirectory() 

files=[e for e in os.listdir(directory) if e.endswith('.txt')]
if not os.path.exists(directory + os.path.sep + 'out'):
    os.mkdir(directory + os.path.sep + 'out')

for index,fl in enumerate(files):
    print('Processing',index+1,'/',len(files))
    judgement_id = fl.split('_')[-1][:-4]
    with io.open(directory + os.path.sep + 'out' + os.path.sep + 'presuda_tokenized_' + judgement_id + '.txt', "w+", encoding = "UTF-8") as tokenized_file:
        with io.open(os.path.join(directory, fl), 'r', encoding = "UTF-8") as text:
            sentences = nltk.sent_tokenize(text.read())
            for i, sentece in enumerate(sentences):
                tokenized = nltk.word_tokenize(sentece)
                for j, token in enumerate(tokenized):
                    tokenized_file.write(judgement_id + '~' + str(i) + '~' + str(j) + '\t' + token + '\tO\n')

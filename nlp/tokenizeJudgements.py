import io, os
import tkinter as tk
import xml.etree.cElementTree as xmlET
from tkinter import filedialog
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

def startProgram():
    root = tk.Tk()
    root.withdraw() 
    directory = filedialog.askdirectory()
    tokenizeFiles(directory)

def tokenizeFiles(directory):
    files=[e for e in os.listdir(directory) if e.endswith('.xml')]
    if not os.path.exists(directory + os.path.sep + 'out'):
        os.mkdir(directory + os.path.sep + 'out')

    for index,fl in enumerate(files):
        print('Processing',index+1,'/',len(files))
        judgement_id = fl.split('_')[-1][:-4]
        with io.open(directory + os.path.sep + 'out' + os.path.sep + 'presuda_tokenized_' + judgement_id + '.txt', "w+", encoding = "UTF-8") as tokenized_file:
            xmlRoot = xmlET.parse(os.path.join(directory, fl)).getroot()
            tags = xmlRoot.find("TAGS").getchildren()
            textTag = xmlRoot.find("TEXT")
            text = textTag.text
            sentences = sent_tokenize(text)
            offset = 0
            for i, sentece in enumerate(sentences):
                tokenized = word_tokenize(sentece)
                for j, token in enumerate(tokenized):
                    offset = text.find(token,offset)
                    startOffset = offset
                    offset += len(token)
                    nerTag = findInTags(tags, startOffset, offset)
                    tokenized_file.write(judgement_id + '~' + str(i) + '~' + str(j) + '\t' + token + '\t' +'\t'+nerTag+'\n')
        
        tokenized_file.close()

def findInTags(tags, startOffset, endOffset):

    for tag in tags:
        tagName = tag.tag
        tagOffset = tag.attrib.get("spans").split("~")
        tagStart = int(tagOffset[0])
        tagEnd = int(tagOffset[1])
        if startOffset >= tagStart and startOffset <= tagEnd and endOffset >= tagStart and endOffset <= tagEnd:
            if startOffset == tagStart:
                return "B-" + tagName
            else:
                return "I-" + tagName

    return "O"

if __name__ == "__main__":
    startProgram()
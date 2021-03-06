import io, os
import tkinter as tk
import xml.etree.cElementTree as xmlET
from tkinter import filedialog
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from tokeniser import generate_tokenizer, process, tokenize_sentences

def startProgram():
    filename = input("Unesite naziv fajle koja ce se izgenerisati:")
    root = tk.Tk()
    root.withdraw() 
    directory = filedialog.askdirectory()
    tokenizeFiles(directory,filename)

def tokenizeFiles(directory,filename):
    files=[e for e in os.listdir(directory) if e.endswith('.xml')]

    lang = 'sr'
    mode = 'standard'
    tokenizer=generate_tokenizer(lang)

    with io.open(directory + os.path.sep + filename, "w+", encoding = "UTF-8") as tokenized_file:
        for index,fl in enumerate(files):
            print('Processing',index+1,'/',len(files))
            judgement_id = fl.split('_')[-1][:-4]
            xmlRoot = xmlET.parse(os.path.join(directory, fl)).getroot()
            tags = xmlRoot.find("TAGS").getchildren()
            textTag = xmlRoot.find("TEXT")
            text = splitJudgement(textTag.text)
            sentences = tokenize_sentences(process[mode](tokenizer,text,lang))
            offset = 0
            for sentence in sentences:
                if sentence:
                    for token in sentence:
                        if token:
                            offset = text.find(token,offset)
                            startOffset = offset
                            offset += len(token)
                            nerTag = findInTags(tags, startOffset, offset)
                            tokenized_file.write(judgement_id + '~' + str(startOffset) + '~' + str(offset) + '\t' + token + '\t' + str(token.istitle()) + '\t' + str(any(char.isdigit() for char in token)) + '\t' +nerTag+'\n')
                tokenized_file.write('\n')

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

def splitJudgement(text):

    if "O b r a z l o ž e nj e" in text:
        return text.split("O b r a z l o ž e nj e",1)[0]
    elif "O b r a z l o ž e n j e" in text:
        return text.split("O b r a z l o ž e n j e",1)[0]
    elif "Obrazloženje" in text:
        return text.split("Obrazloženje",1)[0]
    else:
        return text

if __name__ == "__main__":
    startProgram()
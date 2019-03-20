import html2text
import os
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
from markdown import markdown

def convert_judgementHtml_to_judgementText(judgementsPath):
    for filename in os.listdir(judgementsPath):
        file_fullpath = judgementsPath+ "/" + filename
        if os.path.isfile(file_fullpath) and filename.startswith('presuda_html_') and filename.endswith('.txt'):
            with open(file_fullpath, 'r', encoding='utf-8') as htmlFile:  
                judgement_text_filename = judgementsPath + "/" + 'presuda_text_' + filename.replace("presuda_html_","")
                if not os.path.isfile(judgement_text_filename):
                    w = open(judgement_text_filename, 'w+', encoding='utf-8')
                    html = htmlFile.read()
                    markdownText = str(html2text.html2text(str(html)))
                    textToWrite = ''.join(BeautifulSoup(markdown(markdownText), "html.parser").findAll(text=True))
                    w.write(textToWrite)
                    htmlFile.close()
                    w.close()
        elif os.path.isdir(file_fullpath):
            convert_judgementHtml_to_judgementText(file_fullpath)

def startConverting():
    root = tk.Tk()
    root.withdraw() 
    judgementsPath = filedialog.askdirectory() 
    convert_judgementHtml_to_judgementText(judgementsPath)

if __name__ == "__main__":
    startConverting()





import io, os
import csv
import tkinter as tk
from tkinter import filedialog
import xml.etree.cElementTree as xmlET
import tokenizeJudgements

class JudgementEntity:

    def __init__(self, id, text, label=""):
        self._id = id
        self._text = text
        self._label = label

if __name__ == "__main__":
        root = tk.Tk()
        root.withdraw() 
        directory = filedialog.askdirectory() 

        list_of_files = []
        for (dirpath, dirnames, filenames) in os.walk(directory):
                for dirname in dirnames:
                        files=[(directory + os.path.sep + dirname + os.path.sep + e) for e in os.listdir(directory + os.path.sep + dirname) if e.endswith('.xml')]
                        list_of_files = list_of_files + files


        entities = {}
        for filename in list_of_files:
                with io.open(filename, "r", encoding="utf-8") as xml_file:
                        xmlRoot = xmlET.parse(filename).getroot()
                        textTag = xmlRoot.find("TEXT")
                        text = tokenizeJudgements.splitJudgement(textTag.text)
                        judgement_id = filename.split('_')[-1][:-4]
                        judgement_type = filename.split(os.path.sep)[-2]
                        if judgement_id in entities:
                                if judgement_type == 'conditional':
                                        entities[judgement_id]._label = 'conditional'
                                elif judgement_type == 'verdict':
                                        entities[judgement_id]._label = 'verdict'
                                elif judgement_type == 'acquittal':
                                        entities[judgement_id]._label = 'acquittal'
                                elif judgement_type == 'rejected':
                                        entities[judgement_id]._label = 'rejected'
                                else:
                                        print('Error')
                        else:
                                judgement = JudgementEntity(id=judgement_id, text=text)
                                if judgement_type == 'conditional':
                                        judgement._label = 'conditional'
                                elif judgement_type == 'verdict':
                                        judgement._label = 'verdict'
                                elif judgement_type == 'acquittal':
                                        judgement._label = 'acquittal'
                                elif judgement_type == 'rejected':
                                        judgement._label = 'rejected'
                                else:
                                        print('Error')
                                entities[judgement_id] = judgement


        with open(directory + os.path.sep + 'out.csv', 'w', encoding='utf-8') as csvfile:
                wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
                wr.writerow(['ID', 'TEXT', 'LABEL'])
                for key, value in entities.items():
                        wr.writerow([key, value._text, value._label])
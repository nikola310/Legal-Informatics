import io, os
import csv
import tkinter as tk
from tkinter import filedialog
import xml.etree.cElementTree as xmlET
from judgement_entity import JudgementEntity

root = tk.Tk()
root.withdraw() 
directory = filedialog.askdirectory() 

list_of_files = []
for (dirpath, dirnames, filenames) in os.walk(directory):
    for dirname in dirnames:
        
        files=[(directory + os.path.sep + dirname + os.path.sep + e) for e in os.listdir(directory + os.path.sep + dirname) if e.endswith('.xml')]
        list_of_files = list_of_files + files


entities = {}
#print(len(list_of_files))
#print(list_of_files)
for filename in list_of_files:
    with io.open(filename, "r", encoding="utf-8") as xml_file:
        xmlRoot = xmlET.parse(filename).getroot()
        textTag = xmlRoot.find("TEXT")
        text = textTag.text
        judgement_id = filename.split('_')[-1][:-4]
        judgement_type = filename.split(os.path.sep)[-2]
        if judgement_id in entities:
                if judgement_type == 'acquittal':
                        entities[judgement_id]._acquittal = True
                elif judgement_type == 'conditional':
                        entities[judgement_id]._conditional = True
                elif judgement_type == 'rejected':
                        entities[judgement_id]._rejected = True
                elif judgement_type == 'verdict':
                        entities[judgement_id]._verdict = True
                elif judgement_type == 'warning':
                        entities[judgement_id]._warning = True
                else:
                        print('Error')
        else:
                judgement = JudgementEntity(id=judgement_id, text=text)
                if judgement_type == 'acquittal':
                        judgement._acquittal = True
                elif judgement_type == 'conditional':
                        judgement._conditional = True
                elif judgement_type == 'rejected':
                        judgement._rejected = True
                elif judgement_type == 'verdict':
                        judgement._verdict = True
                elif judgement_type == 'warning':
                        judgement._warning = True
                else:
                        print('Error')
                entities[judgement_id] = judgement
        

with open(directory + os.path.sep + 'out.csv', 'w', encoding='utf-8') as csvfile:
    #w = csv.DictWriter(csvfile, entities.keys())
    #w.writeheader()
    #w.writerow(entities)
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
    wr.writerow(['ID', 'TEXT', 'ACQUITTAL', 'CONDITIONAL', 'REJECTED', 'VERDICT', 'WARNING'])
    for key, value in entities.items():
            wr.writerow([key, value._text, value._acquittal, value._conditional, value._rejected, value._verdict, value._warning])
    #for key in entities:
    #    wr.writerow(entities[key])
    
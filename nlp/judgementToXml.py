import xml.etree.cElementTree as xmlET
import tkinter as tk
import os, io
from tkinter import filedialog

def startProgram():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    exportXml(directory)

def exportXml(directory):

    files=[e for e in os.listdir(directory) if e.startswith('presuda_text_') and e.endswith('.txt')]
    if not os.path.exists(directory + os.path.sep + 'out'):
        os.mkdir(directory + os.path.sep + 'out')

    for index,fl in enumerate(files):
        print('Processing',index+1,'/',len(files))
        with io.open(os.path.join(directory,fl), "r", encoding = "UTF-8") as textFile:
            judgement_id = fl.split('_')[-1][:-4]
        
            root = xmlET.Element("JudgementsTask")
            judgementText = xmlET.SubElement(root, "TEXT")
            judgementText.append(xmlET.Comment(' --><![CDATA[' + textFile.read().replace('\n', ' ').replace(']]>', ']]]]><![CDATA[>') + ']]><!-- '))
            tags = xmlET.SubElement(root, "TAGS").text = " "

            tree = xmlET.ElementTree(root)
            tree.write(directory + os.path.sep + 'out' + os.path.sep + "presuda_xml_"+judgement_id+".xml", encoding='UTF-8', xml_declaration=True)

        textFile.close()
        
if __name__ == "__main__":
    startProgram()
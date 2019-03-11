import csv, os
import tkinter as tk
from tkinter import filedialog

def startProgram():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    judgementDirectory = filedialog.askdirectory()
    parseFile(filename,judgementDirectory)

def parseFile(filename,judgementDirectory):
    with open(filename, "r", newline='') as judgementEntitiesFile:
        reader = csv.reader(judgementEntitiesFile, delimiter = '\t')
        judgement = {'judgementId' : '', 'judge' : '', 'clerk' : '', 'probationer' : '', 'council_president' : '', 'council_members' : [], 'violations' : [], 'regulations' : []}        
        entityObj = {'beginOffset' : -1, 'endOffset' : -1, 'type' : ''}  
        for line in reader:
            if len(line) > 0:
                code = line[0]
                entity = line[len(line)-1]
                codeSplits = code.split('~')
                id = codeSplits[0]
                startOffset = int(codeSplits[1])
                endOffset = int(codeSplits[2])
                if '-' in entity:
                    entitySplits = entity.split('-')
                    entityPosition = entitySplits[0]
                    entityType = entitySplits[1]
                else:
                    entityPosition = entity
                    entityType = entity
                if judgement['judgementId'] != id:
                    if judgement['judgementId'] != '':
                        print(judgement)
                        judgement['judgementId'] = ''
                        judgement['judge'] = ''
                        judgement['clerk'] = ''
                        judgement['probationer'] = ''
                        judgement['council_president'] = ''
                        judgement['council_members'] = []
                        judgement['violations'] = []
                        judgement['regulations'] = []
                    judgement['judgementId'] = id
                if entityPosition == 'B':
                    if entityObj['type'] != entityType:
                        findAndSaveEntity(judgementDirectory,judgement,entityObj)
                    entityObj['beginOffset'] = startOffset
                    entityObj['type'] = entityType
                elif entityPosition == 'I' and entityObj['type'] == entityType:
                    entityObj['endOffset'] = endOffset
                else:
                    findAndSaveEntity(judgementDirectory,judgement,entityObj)

        if judgement['judgementId'] != '':
            print(judgement)

def findAndSaveEntity(judgementDirectory,judgement,entityObj):

    if entityObj['beginOffset'] == -1 or entityObj['endOffset'] == -1 or entityObj['type'] == '':
        return

    with open(judgementDirectory + os.path.sep + "presuda_one_line_"+judgement['judgementId']+".txt", encoding = "UTF-8") as judgementTextFile:
        judgementText = judgementTextFile.read()
        entityText = judgementText[entityObj['beginOffset']:entityObj['endOffset']]
        entityType = entityObj['type'] 
        if entityType == 'judge':
            if judgement['judge'] == '':
                judgement['judge'] = entityText
        elif entityType == 'clerk':
            if judgement['clerk'] == '':
                judgement['clerk'] = entityText
        elif entityType == 'probationer':
            if judgement['probationer'] == '':
                judgement['probationer'] = entityText
        elif entityType == 'council_president':
            if judgement['council_president'] == '':
                judgement['council_president'] = entityText
        elif entityType == 'council_member':
            judgement['council_members'].append(entityText)
        elif entityType == 'violation':
            judgement['violations'].append(entityText)
        elif entityType == 'regulation':
            judgement['regulations'].append(entityText)

    entityObj['beginOffset'] = -1
    entityObj['endOffset'] = -1
    entityObj['type'] = ''

if __name__ == "__main__":
    startProgram()
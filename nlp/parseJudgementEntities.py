import csv, os, re
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
            judgement['violations'].append(parseViolationsRegulations(entityText))
        elif entityType == 'regulation':
            judgement['regulations'].append(parseViolationsRegulations(entityText))

    entityObj['beginOffset'] = -1
    entityObj['endOffset'] = -1
    entityObj['type'] = ''

def parseViolationsRegulations(text):

    text = re.sub("\\s*,",",",text)
    while True:
        toReplace = re.search("[0-9]+\\s*\\.\\s*[0-9]+",text) 
        if toReplace is None:
            break
        toReplaceText = text[toReplace.span()[0]:toReplace.span()[1]]
        numbers = re.findall("[0-9]+",toReplaceText)

        text = text[:toReplace.span()[0]] + numbers[0]+", "+numbers[1] + text[toReplace.span()[1]:]

    while True:
        toReplace = re.search("[0-9]+,\\s*i\\s*",text) 
        if toReplace is None:
            break
        toReplaceText = text[toReplace.span()[0]:toReplace.span()[1]]
        text = text[:toReplace.span()[0]] + toReplaceText.replace(","," ") + text[toReplace.span()[1]:]

    replace = text.replace("-a","").replace("."," ")
    splits = replace.split()
    for i,split in enumerate(splits):
        if split.startswith("čl"):
            splits[i] = "član"
        elif split.startswith("st"):
            splits[i] = "stav"
        elif split.startswith("tač"):
            splits[i] = "tačka"

    text = " ".join(splits)

    while True:
        toReplace = re.search("[0-9]+\\s*-\\s*[0-9]+",text) 
        if toReplace is None:
            break

        toReplaceText = text[toReplace.span()[0]:toReplace.span()[1]]
        numbers = re.findall("[0-9]+",toReplaceText)
        num1 = numbers[0]
        num2 = numbers[1]

        inBetweenList = list(range(int(num1),int(num2)))
        inBetween = ", ".join([str(inBetweenElem) for inBetweenElem in inBetweenList])

        toInsert = inBetween + ", "+num2 if (toReplace.span()[1]<len(text) and text[toReplace.span()[1]] == ",") or (toReplace.span()[1]+3<len(text) and text[toReplace.span()[1]:toReplace.span()[1]+3] == " i ") else inBetween + " i "+num2

        text = text[:toReplace.span()[0]] + toInsert + text[toReplace.span()[1]:]

    return text

if __name__ == "__main__":
    startProgram()
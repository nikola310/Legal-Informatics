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
    with open(filename, "r", newline='', encoding='utf-8') as judgementEntitiesFile:
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

    replace = text.replace("-a","").replace("."," ").replace(":"," ")
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

    regExp1 = "(?:(?:član|stav|tačka|alineja)\\s[0-9]+(?:\\,\\s{0,1}[0-9]+)+(?:\\si\\s[0-9]+){0,1})"
    regExp2 = "(?:(?:član|stav|tačka|alineja)\\s[0-9]+\\si\\s[0-9]+)"

    regExp = regExp1 + "|" +regExp2
    
    loop = 0
    foundEndPart = ""
    
    while True:
        result = re.search(regExp,text)
        if result is None:
            break
        textPart = text[result.span()[0]:result.span()[1]]
        textPartBeginningResult = re.search("^član|stav|tačka|alineja",textPart)
        textPartBeginning = textPart[textPartBeginningResult.span()[0]:textPartBeginningResult.span()[1]]
        if loop == 0:
            foundEndPart = textPartBeginning

        loop+= 1
        textPartEndResult = re.search("i\\s[0-9]+$",textPart)
        textPartEndToInsert = ""
        if textPartEndResult is not None:
            textPartNumbersText = textPart[textPartBeginningResult.span()[1]:textPartEndResult.span()[0]]
            textPartEnd = textPart[textPartEndResult.span()[0]:textPartEndResult.span()[1]]
            textPartEndNumber = re.findall("[0-9]+",textPartEnd)
            textPartEndToInsert = " i "+ textPartBeginning + " " + textPartEndNumber[0]
            foundEndPart = textPartBeginning
        else:
            textPartNumbersText = textPart[textPartBeginningResult.span()[1]:result.span()[1]]
            prevText = text[:result.span()[1]]
            restText = text[result.span()[1]:]
            while True:
                firstCondition = re.search("(?:\\si\\s[0-9]+){2}",restText)
                secondCondition = re.search("\\si\\s[0-9]+(?:\\,\\s{0,1}[0-9]+)+(?:\\si\\s[0-9]+){0,1}",restText)
                thirdCondition = re.search("\\si\\s[0-9]+",restText)
                if firstCondition != None or secondCondition != None or thirdCondition != None:
                    foundEndPart = textPartBeginning

                if secondCondition != None:
                    secondConditionText = restText[secondCondition.span()[0]:secondCondition.span()[1]]
                    secondConditionBeginning = re.search("\\si\\s[0-9]+\\,",secondConditionText)
                    secondConditionBeginningText = secondConditionText[secondConditionBeginning.span()[0]:secondConditionBeginning.span()[1]]
                    secondConditionEnd = re.search("i\\s[0-9]+$",secondConditionText)
                    secondConditionEndToInsert = ""
                    secondConditionEndExists = False
                    if secondConditionEnd is not None:
                        secondConditionToInsertNumbersText = secondConditionText[secondConditionBeginning.span()[1]:secondConditionEnd.span()[0]]
                        secondConditionEndText = secondConditionText[secondConditionEnd.span()[0]:secondConditionEnd.span()[1]]
                        secondConditionEndNumber = re.findall("[0-9]+", secondConditionEndText)
                        secondConditionEndToInsert = " i " + textPartBeginning + " " + secondConditionEndNumber[0]
                        secondConditionEndExists = True
                    else:
                        secondConditionToInsertNumbersText = secondConditionText[secondConditionBeginning.span()[1]:]

                    secondConditionNumbers = re.findall("[0-9]+",secondConditionToInsertNumbersText)  
                    secondConditionNumbersToInsert = ""
                    for i,secondConditionNumber in enumerate(secondConditionNumbers):
                        if i==0:
                            insertBeginning = textPartBeginning
                        else:
                            insertBeginning = foundEndPart

                        if i == len(secondConditionNumbers)-1:
                            secondConditionNumbersToInsert += insertBeginning + " " + secondConditionNumber
                        else:
                            secondConditionNumbersToInsert += insertBeginning + " " + secondConditionNumber + ", "

                    prevText += restText[:secondCondition.span()[0]] + secondConditionBeginningText + " " + secondConditionNumbersToInsert + secondConditionEndToInsert
                    restText = restText[secondCondition.span()[1]:]

                    text = prevText + restText
                    if secondConditionEndExists:
                        break

                elif firstCondition != None:
                    firstConditionText = restText[firstCondition.span()[0]:firstCondition.span()[1]]
                    firstConditionNumbers = re.findall("[0-9]+",firstConditionText)
                    text = prevText + restText[:firstCondition.span()[0]] + " i " + firstConditionNumbers[0] + " i " + textPartBeginning + " " + firstConditionNumbers[1] + restText[firstCondition.span()[1]:]
                    break

                elif thirdCondition != None:
                    thirdConditionText = restText[thirdCondition.span()[0]:thirdCondition.span()[1]]
                    thirdConditionNumber = re.findall("[0-9]+",thirdConditionText)
                    text = prevText + restText[:thirdCondition.span()[0]] + " i " + textPartBeginning + " " + thirdConditionNumber[0] + restText[thirdCondition.span()[1]:]
                    break
                else:
                    break

        textPartNumbers = re.findall("[0-9]+",textPartNumbersText)  
        textPartNumbersToInsert = ""
        for i,textPartNumber in enumerate(textPartNumbers):
            
            if i==0:
                insertBeginning = textPartBeginning
            else:
                insertBeginning = foundEndPart

            if i == len(textPartNumbers)-1:
                textPartNumbersToInsert += insertBeginning + " " + textPartNumber
            else:
                textPartNumbersToInsert += insertBeginning + " " + textPartNumber + ", "
        text = text[:result.span()[0]] + textPartNumbersToInsert + textPartEndToInsert + text[result.span()[1]:]
    
    splits = re.split("(?:\\,\\s*)|(?:\\si\\s)", text)

    return text

if __name__ == "__main__":
    startProgram()
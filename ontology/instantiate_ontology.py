import owlready2
from owlready2 import onto_path
from owlready2 import get_ontology
from owlready2 import sync_reasoner
import os.path
import tkinter as tk
from tkinter import filedialog
import json

#set java path for local setup (used for HermiT reasoner)
owlready2.JAVA_EXE = "C:\\Program Files\\Java\\jre1.8.0_191\\bin\\java.exe"

my_path = os.path.abspath(os.path.dirname(__file__))
path = my_path + os.path.sep + "Montenegro judgements ontology" + os.path.sep
dataPath = my_path + os.path.sep + "data" + os.path.sep

class DataWrapper:
    def __init__(self, logData, metaData, verdictInfo):
        self.logData = logData
        self.metaData = metaData
        self.verdictInfo = verdictInfo

def startProgram():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    if directory:
        loadData(directory)

def loadData(directory):
    f = open(dataPath + "instantiateJudgements", "r", encoding="UTF-8")
    lines = f.readlines()
    s = open(dataPath + "predictions_svm_instantiate.json", "r", encoding="UTF-8")
    sData = s.read()
    svmJson = json.loads(sData)
    
    instances = []
    for line in lines:
        line = line.replace("'", '"')
        lineJson = json.loads(line)
        id = lineJson["judgementId"]
        j = open(directory + os.path.sep + "presuda_meta_" + str(id) + ".json", "r", encoding="UTF-8")
        jData = j.read()
        jData = jData.replace("'", '"')
        metaJson = json.loads(jData)
        verdictInfo = svmJson[str(id)]
        if verdictInfo:
            wrpr = DataWrapper(lineJson, metaJson, verdictInfo)
            instances.append(wrpr)
    loadOntology(instances)

def loadOntology(instances):
    onto_path.append(path)
    onto_path.append(path + "judo-master")
    onto_path.append(path + "lkif-core-master" + os.path.sep)

    montenegro_judgements = get_ontology("http://www.semanticweb.org/tima/ontologies/2019/2/cbr_judgements.owl").load()
    instantiateOntology(montenegro_judgements, instances)

def instantiateOntology(montenegro_judgements, instances):
    importedOntos = list(montenegro_judgements.imported_ontologies)
    judging_onto = importedOntos[0]

    imported_J_ontos = list(judging_onto.imported_ontologies)

    j_core_onto = imported_J_ontos[0]

    lkif_role_onto = importedOntos[1]
    lkif_action_onto = list(lkif_role_onto.imported_ontologies)[0]
    lkif_legal_role_onto = list(lkif_role_onto.imported_ontologies)[1]

    for instance in instances:
        #Judgement individual
        caseNo = instance.metaData["Broj predmeta"]
        caseNo = caseNo.replace(' ', '_')        
        jDate = instance.metaData["Datum vijećanja"]
        jDate = jDate.replace(' ', '_')
        jType = instance.metaData["Vrsta odluke"]
        jType = jType.replace(' ', '_')
        department = instance.metaData["Odjeljenje"]
        department = department.replace(' ', '_')
        cType = instance.metaData["Vrsta predmeta"]
        cType = cType.replace(' ', '_')

        test_judgement = j_core_onto.Judgement(caseNo, namespace = montenegro_judgements)
        test_judgement.comment.append(jType)
        test_judgement.judgement_date.append(jDate)
        test_judgement.judgement_department.append(department)
        test_judgement.judgement_type.append(cType)

        #Jurisdiction individual
        court = instance.metaData["Sud"]
        court = court.replace(' ', '_')
        test_jurisdiction = j_core_onto.Jurisdiction(court, namespace = montenegro_judgements)
        test_judgement.considered_by.append(test_jurisdiction)

        #Judge individial
        judge = instance.logData["judge"]
        if judge:
            judge = judge.replace(' ', '_')
            test_judge = lkif_action_onto.Person(judge, namespace = montenegro_judgements)
            test_legal_role_j = lkif_legal_role_onto.Legal_Role("Sudija", namespace = montenegro_judgements)
            test_judge.plays.append(test_legal_role_j)
            test_judge.partaker.append(test_judgement)

        #Clerk individual
        clerk = instance.logData["clerk"]
        if clerk:
            clerk = clerk.replace(' ', '_')
            test_clerk = lkif_action_onto.Person(clerk, namespace = montenegro_judgements)
            test_legal_role_c = lkif_legal_role_onto.Legal_Role("Zapisničar", namespace = montenegro_judgements)
            test_clerk.plays.append(test_legal_role_c)
            test_clerk.partaker.append(test_judgement)

        #Probationer individual
        probationer = instance.logData["probationer"]
        if probationer:
            probationer = probationer.replace(' ', '_')
            test_probationer = lkif_action_onto.Person(probationer, namespace = montenegro_judgements)
            test_legal_role_p = lkif_legal_role_onto.Legal_Role("Pripravnik", namespace = montenegro_judgements)
            test_probationer.plays.append(test_legal_role_p)
            test_probationer.partaker.append(test_judgement)

        #Council_president individual
        council_president = instance.logData["council_president"]
        if council_president:
            council_president = council_president.replace(' ', '_')
            test_council_president = lkif_action_onto.Person(council_president, namespace = montenegro_judgements)
            test_legal_role_cp = lkif_legal_role_onto.Legal_Role("Predsjednik_vijeća", namespace = montenegro_judgements)
            test_council_president.plays.append(test_legal_role_cp)
            test_council_president.partaker.append(test_judgement)

        #Council_member individuals
        council_members = instance.logData["council_members"]
        for cm in council_members:
            if cm:
                cm = cm.replace(' ', '_')
                test_council_member = lkif_action_onto.Person(cm, namespace = montenegro_judgements)
                test_legal_role_cm = lkif_legal_role_onto.Legal_Role("Član_vijeća", namespace = montenegro_judgements)
                test_council_member.plays.append(test_legal_role_cm)
                test_council_member.partaker.append(test_judgement)

        #Violation individuals
        violations = instance.logData["violations"]
        for vi in violations:
            if vi:
                vi = vi.replace(' ', '_')
                test_violation = j_core_onto.Legal_Rule(vi, namespace = montenegro_judgements)
                test_violation.comment.append("KRIVIČNO_DELO")
                test_judgement.considers.append(test_violation)

        #Judicial_outcome individual
        judicial_outcome = instance.verdictInfo
        if judicial_outcome:
            judicial_outcome = judicial_outcome.replace(' ', '_')
            test_judicial_outcome = j_core_onto.Judicial_Outcome(judicial_outcome, namespace = montenegro_judgements)
            test_judgement.applies.append(test_judicial_outcome)

        #Regulation individuals
        regulations = instance.logData["regulations"]
        for re in regulations:
            if re:
                re = re.replace(' ', '_')
                test_regulation = j_core_onto.Legal_Rule(re, namespace = montenegro_judgements)
                test_regulation.comment.append("SANKCIJA")
                test_judgement.considers.append(test_regulation)

    #Fixed RuntimeError with download of HermiT from websource and setting it in AppData/Local/Python...
    with montenegro_judgements:
        sync_reasoner(infer_property_values = True)

    saveOntology(montenegro_judgements)

def saveOntology(montenegro_judgements):
    montenegro_judgements.save()

if __name__ == "__main__":
    startProgram()
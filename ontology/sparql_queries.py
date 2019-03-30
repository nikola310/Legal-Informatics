from owlready2 import onto_path
from owlready2 import get_ontology
from owlready2 import default_world
import os
import json

my_path = os.path.abspath(os.path.dirname(__file__))
path = my_path + os.path.sep + "Montenegro judgements ontology" + os.path.sep
dataPath = my_path + os.path.sep + "data" + os.path.sep

class DataWrapper:
    def __init__(self, logData, verdictInfo):
        self.logData = logData
        self.verdictInfo = verdictInfo

def startProgram():
    loadData()

def loadData():
    f = open(dataPath + "queryJudgements", "r", encoding="UTF-8")
    lines = f.readlines()
    s = open(dataPath + "predictions_svm_query.json", "r", encoding="UTF-8")
    sData = s.read()
    svmJson = json.loads(sData)
    queryObjs = []
    for line in lines:
        line = line.replace("'", '"')
        lineJson = json.loads(line)
        id = lineJson["judgementId"]
        verdictInfo = svmJson[str(id)]
        if verdictInfo:
            wrpr = DataWrapper(lineJson, verdictInfo)
            queryObjs.append(wrpr)
    loadOntology(queryObjs)

def loadOntology(queryObjs):
    onto_path.append(path)
    onto_path.append(path + "judo-master")
    onto_path.append(path + "lkif-core-master" + os.path.sep)

    montenegro_judgements = get_ontology("http://www.semanticweb.org/tima/ontologies/2019/2/cbr_judgements.owl").load()
    doQueries(queryObjs,montenegro_judgements)

def doQueries(queryObjs,montenegro_judgements):
    
    graph = default_world.as_rdflib_graph()
    mngj_pref = "PREFIX mngj: <http://www.semanticweb.org/tima/ontologies/2019/2/cbr_judgements#>"
    lkif_process_pref = "PREFIX lkif_process: <http://www.estrellaproject.org/lkif-core/process.owl#>"
    lkif_role_pref = "PREFIX lkif_role: <http://www.estrellaproject.org/lkif-core/role.owl#>"
    judo_core_pref = "PREFIX judo_core: <http://codexml.cirsfid.unibo.it/ontologies/Judging_Contracts_Core.owl#>"
    rdfs_pref = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"

    queryResultsDirectory = my_path + os.path.sep + 'queryResults'
    if not os.path.exists(queryResultsDirectory):
        os.mkdir(queryResultsDirectory)

    for queryObj in queryObjs:
        queryResultsFile = queryResultsDirectory + os.path.sep + "queryResults_" + queryObj.logData["judgementId"]+".txt"
        with open(queryResultsFile, "w", encoding = "UTF-8") as queryResultsFile:
            judge = queryObj.logData["judge"]

            if judge:
                judge_query = "mngj:"+ judge.replace(' ', '_')
                q1 = list(graph.query_owlready(mngj_pref + lkif_process_pref + lkif_role_pref + """
                        SELECT ?judgement {""" + judge_query + """ lkif_process:participant ?judgement . """ + judge_query + """ lkif_role:plays mngj:Sudija .}
                    """))

                writeMessage(queryResultsFile, "Presude u kojima učestvuje sudija: " + judge)
                writeQueryResults(queryResultsFile, q1)

                q2 = list(graph.query_owlready(mngj_pref + lkif_process_pref + lkif_role_pref + """
                        SELECT ?judgement ?person WHERE { 
                        ?person	lkif_process:participant ?judgement .
                        ?person lkif_role:plays mngj:Sudija .
                        FILTER NOT EXISTS {""" + judge_query + """ lkif_process:participant ?judgement . }
                        }
                    """))
                
                writeMessage(queryResultsFile, "Presude u kojima ne učestvuje sudija: " + judge + " i imena sudija tih presuda:")
                writeQueryResults(queryResultsFile, q2)

                judicial_outcome = queryObj.verdictInfo
                judicial_outcome_query = judicial_outcome.replace(' ', '_')
                q3 = list(graph.query_owlready(mngj_pref + lkif_process_pref + lkif_role_pref + judo_core_pref + """
                        SELECT ?judgement ?judgement_type ?judgement_department ?judgement_date
                        WHERE { 
                            ?judgement judo_core:applies mngj:"""+ judicial_outcome_query + """ .
                            """ + judge_query + """ lkif_process:participant ?judgement .
                            """ + judge_query + """ lkif_role:plays mngj:Sudija .
                            ?judgement mngj:judgement_date ?judgement_date .
                            ?judgement mngj:judgement_type ?judgement_type .
                            ?judgement mngj:judgement_department ?judgement_department .
                        }
                        """))

                writeMessage(queryResultsFile, "Presude u kojima učestvuje sudija: " + judge + " i u kojima je ishod isti (" + judicial_outcome + ")")
                writeQueryResults(queryResultsFile, q3)

            else:
                writeMessage(queryResultsFile, "Presuda ne sadrži sudiju pa nema rezultata za upite 1,2 i 3")

            council_president = queryObj.logData["council_president"]
            council_members = queryObj.logData["council_members"]

            if council_president and len(council_members) > 0:
                council_president_query_element = "mngj:" + council_president.replace(' ', '_')
                council_president_query = council_president_query_element + """ lkif_role:plays mngj:Predsjednik_vijeća . """ + council_president_query_element + """ lkif_process:participant ?judgement . """
                q4 = list(graph.query_owlready(mngj_pref + lkif_process_pref + lkif_role_pref + """
	                    SELECT ?judgement {""" + council_president_query + """}
	                """))

                writeMessage(queryResultsFile, "Presude u kojima učestvuje predsednik veća: " + council_president)
                writeQueryResults(queryResultsFile, q4)

                council_members_query = ""
                for council_member in council_members:
                    council_member_element = "mngj:" + council_member.replace(' ','_')
                    council_members_query += council_member_element + " lkif_process:participant ?judgement . " + council_member_element + " lkif_role:plays mngj:Član_vijeća . "

                q5 = list(graph.query_owlready(mngj_pref + lkif_process_pref + lkif_role_pref + """
                        SELECT ?judgement {""" + council_president_query + council_members_query + """}
                    """))

                writeMessage(queryResultsFile, "Presude u kojima učestvuje predsednik veća: " + council_president + " članovi veća: " + ", ".join(council_members))
                writeQueryResults(queryResultsFile, q5)
            
            else:
                writeMessage(queryResultsFile, "Presuda ne sadrži predsednika veća ni članove veća pa nema rezultata za upite 4 i 5")
            
            violations = queryObj.logData["violations"]
            if len(violations) > 0:
                violations_query_in = ",".join(["mngj:" + violation.replace(' ','_') for violation in violations])
                
                q6 = list(graph.query_owlready(mngj_pref + judo_core_pref + rdfs_pref + """
                    SELECT DISTINCT ?judgement
                    WHERE { 
                        ?judgement judo_core:considers ?violation . ?violation rdfs:comment 'KRIVIČNO_DELO' . FILTER (?violation IN (""" + violations_query_in + """)) . }
                    """))

                writeMessage(queryResultsFile, "Presude u kojima se spominju neka od krivičnih dela: " + ", ".join(violations))
                writeQueryResults(queryResultsFile, q6)

            else:
                writeMessage(queryResultsFile, "Presuda ne sadrži krivična dela pa nema rezultata za upit 6")

            regulations = queryObj.logData["regulations"]
            if len(regulations) > 0:
                regulations_query_in = ",".join(["mngj:" + regulation.replace(' ','_') for regulation in regulations])
                
                q7 = list(graph.query_owlready(mngj_pref + judo_core_pref + rdfs_pref + """
                    SELECT DISTINCT ?regulation
                    WHERE { 
                        ?judgement judo_core:considers ?regulation . ?regulation rdfs:comment 'SANKCIJA' . FILTER (?regulation IN (""" + regulations_query_in + """)) . } 
                    """))
                
                writeMessage(queryResultsFile, "Presude u kojima se spominju neke od sankcija: " + ", ".join(regulations))
                writeQueryResults(queryResultsFile, q7)

            else:
                writeMessage(queryResultsFile, "Presuda ne sadrži sankcije pa nema rezultata za upit 7")

def writeMessage(queryResultsFile, message):
    queryResultsFile.write(message + "\n")

def writeQueryResults(queryResultsFile, queryResults):
    for queryResult in queryResults:
        queryResultsToWrite = ""
        for i, queryResultElement in enumerate(queryResult):
            queryResultsToWrite += str(queryResultElement)
            if i==len(queryResult)-1:
                queryResultsToWrite += "\n"
            else:
                queryResultsToWrite += "\t"
    
        queryResultsFile.write(queryResultsToWrite)

if __name__ == "__main__":
    startProgram()
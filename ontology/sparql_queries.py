from owlready2 import onto_path
from owlready2 import get_ontology
from owlready2 import default_world
import os.path

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "Montenegro judgements ontology\\")

def startProgram():
    loadOntology()

def loadOntology():
    onto_path.append(path)
    onto_path.append(path + "judo-master")
    onto_path.append(path + "lkif-core-master\\")

    montenegro_judgements = get_ontology("http://www.semanticweb.org/tima/ontologies/2019/2/montenegro_judgements_1.owl").load()
    doQueries(montenegro_judgements)

def doQueries(montenegro_judgements):
    #SPARQL queries
    graph = default_world.as_rdflib_graph()

    #find all judgements where Anđelić_Mihailu is a participant
    q1 = list(graph.query_owlready("""
        PREFIX mngj: <http://www.semanticweb.org/tima/ontologies/2019/2/montenegro_judgements_1#>
        PREFIX lkif_process: <http://www.estrellaproject.org/lkif-core/process.owl#>

        SELECT ?judgement {mngj:Anđelić_Mihailu lkif_process:participant ?judgement .}
        """))

    #find all judgements and judges where Anđelić_Mihailu is not a participant
    q2 = list(graph.query_owlready("""
        PREFIX mngj: <http://www.semanticweb.org/tima/ontologies/2019/2/montenegro_judgements_1#>
        PREFIX lkif_process: <http://www.estrellaproject.org/lkif-core/process.owl#>
        PREFIX lkif_role: <http://www.estrellaproject.org/lkif-core/role.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?judgement ?person
        WHERE { 
            ?person	lkif_process:participant ?judgement .
            ?person lkif_role:plays mngj:Sudija .
            FILTER NOT EXISTS { mngj:Anđelić_Mihailu lkif_process:participant ?judgement . }
        }
        """))

    #find all judgements that are verdicts
    q3 = list(graph.query_owlready("""
        PREFIX mngj: <http://www.semanticweb.org/tima/ontologies/2019/2/montenegro_judgements_1#>
        PREFIX judo_core: <http://codexml.cirsfid.unibo.it/ontologies/Judging_Contracts_Core.owl#>

        SELECT ?judgement
        WHERE { 
            ?judgement judo_core:applies mngj:verdict .
        }
        """))

    #find all judgements (with their data props) that are verdicts and where the judge is Anđelić_Mihailu
    q4 = list(graph.query_owlready("""
        PREFIX mngj: <http://www.semanticweb.org/tima/ontologies/2019/2/montenegro_judgements_1#>
        PREFIX judo_core: <http://codexml.cirsfid.unibo.it/ontologies/Judging_Contracts_Core.owl#>
        PREFIX lkif_process: <http://www.estrellaproject.org/lkif-core/process.owl#>
        PREFIX lkif_role: <http://www.estrellaproject.org/lkif-core/role.owl#>

        SELECT ?judgement ?judgement_type ?judgement_department ?judgement_date
        WHERE { 
            ?judgement judo_core:applies mngj:verdict .
            mngj:Anđelić_Mihailu lkif_process:participant ?judgement .
            mngj:Anđelić_Mihailu lkif_role:plays mngj:Sudija .
            ?judgement mngj:judgement_date ?judgement_date .
            ?judgement mngj:judgement_type ?judgement_type .
            ?judgement mngj:judgement_department ?judgement_department .
        }
        """))

if __name__ == "__main__":
    startProgram()
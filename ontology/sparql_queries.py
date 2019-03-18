from owlready2 import *
import os.path

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "Montenegro judgements ontology\\")

onto_path.append(path)
onto_path.append(path + "judo-master")
onto_path.append(path + "lkif-core-master\\")

montenegro_judgements = get_ontology("http://www.semanticweb.org/tima/ontologies/2019/2/montenegro_judgements_1.owl").load()

#SPARQL querries
graph = default_world.as_rdflib_graph()

q1 = list(graph.query_owlready("""PREFIX mngj:<http://www.semanticweb.org/tima/ontologies/2019/2/montenegro_judgements_1#>
    PREFIX lkif_role:<http://www.estrellaproject.org/lkif-core/role.owl#>
    PREFIX lkif_legal_role:<http://www.estrellaproject.org/lkif-core/legal-role.owl#>
        SELECT ?person {?person lkif_role:plays mngj:Sudija}"""))

q2 = list(graph.query_owlready("""
    PREFIX mngj: <http://www.semanticweb.org/tima/ontologies/2019/2/montenegro_judgements_1#>
    PREFIX lkif_process: <http://www.estrellaproject.org/lkif-core/process.owl#>
    SELECT ?judgement {mngj:Testimir_Pekic lkif_process:participant ?judgement .}
    """))

print("END")
from rdflib import Graph, RDF, Namespace
from rdflib.plugins.sparql import prepareQuery
from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics

# Define namespaces
BASE = Namespace("http://www.semanticweb.org/team15/ontologies/2024/4/M1-ontology-2#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

def load_ontology(file_path, rule_path):
    # Load the TTL file into an RDF graph
    g = Graph()
    g.parse(file_path, format='ttl')
    g.parse(rule_path, format='ttl')
    # Apply Deductive Closure reasoning with RDFS semantics to the graph
    DeductiveClosure(OWLRL_Semantics).expand(g)
    return g

def get_actor_directors(graph):
    persons = set()
    # Prepare a SPARQL query from the text
    query = prepareQuery("""
        SELECT DISTINCT ?actorDirector
        WHERE {
            ?actorDirector rdf:type base:ActorDirector .
        }
        """, initNs={"rdf": RDF, "base": BASE})
    # Execute the query and collect the results
    results = graph.query(query)
    for row in results:
        persons.add(row["actorDirector"])
    return persons

def display_actor_directors(file_path, rule_path):
    # Load the ontology
    graph = load_ontology(file_path, rule_path)

    # Get all the actor-directors from the ontology
    actor_directors = get_actor_directors(graph)

    # Display the actor-directors
    print("Actor-Directors:")
    for actor_director in actor_directors:
        print(actor_director)

# Example usage
if __name__ == "__main__":
    ttl_file = "Ontology_phase1_team15.ttl"  # Path to your TTL file
    rule_file = "rule.ttl"
    display_actor_directors(ttl_file, rule_file)

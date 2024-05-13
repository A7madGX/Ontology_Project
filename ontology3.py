from rdflib import Graph, RDF, RDFS, OWL, Namespace
from owlrl import DeductiveClosure, RDFS_Semantics

def load_ontology(file_path):
    # Load the TTL file into an RDF graph
    g = Graph()
    g.parse(file_path, format='ttl')
        
    # Apply Deductive Closure reasoning with RDFS semantics to the graph
    DeductiveClosure(RDFS_Semantics).expand(g)
    return g

def get_actors(graph, ns):
    actors = set()
    # Iterate through all inferred triples in the graph
    for subj, pred, obj in graph:
        # Check if the subject is an Actor
        if (subj, RDF.type, ns.Actor) in graph:
            actors.add(subj)
    return actors

def display_actors(file_path):
    # Load the ontology and apply Deductive Closure reasoning
    graph = load_ontology(file_path)
    # Define namespace
    ns = Namespace("http://www.semanticweb.org/team15/ontologies/2024/4/M1-ontology-2/")
    # Get all the Actors from the ontology
    actors = get_actors(graph, ns)
    # Display the Actors
    print("Actors Using Inference without query")
    for actor in actors:
        print(actor)

# Example usage
if __name__ == "__main__":
    ttl_file = "Ontology_phase1_team15.ttl"  # Path to your TTL file
    display_actors(ttl_file)

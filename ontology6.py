from rdflib import Graph, RDF, Namespace, OWL
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

def get_actor_writer(graph):
    actor_writers = set()
    # Iterate through all inferred triples in the graph
    for subj, pred, obj in graph:
        # Check if the subject is an ActorWriter
        if (subj, RDF.type, BASE.ActorWriter) in graph:
            actor_writers.add(subj)
    return actor_writers
def display_actor_writer(file_path, rule_path):
    # Load the ontology
    graph = load_ontology(file_path, rule_path)

    # Get all the actor-directors from the ontology
    actor_writers = get_actor_writer(graph)

    # Display the actor-directors
    print("ActorWriter:")
    for actor_writer in actor_writers:
        print(actor_writer)

def get_director_writer(graph):
    director_writers = set()
    # Iterate through all inferred triples in the graph
    for subj, pred, obj in graph:
        # Check if the subject is an ActorWriter
        if (subj, RDF.type, BASE.WriterDirector) in graph:
            director_writers.add(subj)
    return director_writers
def display_director_writer(file_path, rule_path):
    # Load the ontology
    graph = load_ontology(file_path, rule_path)

    # Get all the actor-directors from the ontology
    director_writers = get_director_writer(graph)

    # Display the actor-directors
    print("DirectorWriter:")
    for director_writer in director_writers:
        print(director_writer)

def get_director_writer_actor(graph):
    director_writers_actor = set()
    # Iterate through all inferred triples in the graph
    for subj, pred, obj in graph:
        # Check if the subject is an ActorWriter
        if (subj, RDF.type, BASE.ActorWriterDirector) in graph:
            director_writers_actor.add(subj)
    return director_writers_actor
def display_director_writer_actor(file_path, rule_path):
    # Load the ontology
    graph = load_ontology(file_path, rule_path)

    # Get all the actor-directors from the ontology
    director_writers_actor = get_director_writer_actor(graph)

    # Display the actor-directors
    print("DirectorWriterActor:")
    for director_writer_actor in director_writers_actor:
        print(director_writer_actor)

# Example usage
if __name__ == "__main__":
    ttl_file = "Ontology_phase1_team15.ttl"  # Path to your TTL file
    rule_file = "rule.ttl"
    display_actor_writer(ttl_file, rule_file)
    display_director_writer(ttl_file, rule_file)
    display_director_writer_actor(ttl_file,rule_file)

from rdflib import Graph
from rdflib.tools.rdf2dot import rdf2dot

def load_ontology(file_path):
    # Load the TTL file into an RDF graph
    g = Graph()
    g.parse(file_path, format='ttl')
    return g

def get_persons(graph):
    persons = set()
    # Iterate through all triples in the graph
    for subj, pred, obj in graph:
        # Check if the predicate is 'rdf:type' and the object is 'Person'
        if pred.endswith('type') and (str(obj).endswith('Actor') or str(obj).endswith('Writer') or str(obj).endswith('Director')):
            persons.add(subj)
    return persons

def display_persons(file_path):
    # Load the ontology
    graph = load_ontology(file_path)
    # Get all the Persons from the ontology
    persons = get_persons(graph)
    # Display the Persons
    print("Persons Without Using Inference and Query:")
    for person in persons:
        print(person)

def visualize_graph(file_path, output_file):
    # Load the ontology
    graph = load_ontology(file_path)
    # Create a stream to write DOT data
    with open(output_file, 'w') as f:
        # Convert RDF graph to DOT format and write to the stream
        rdf2dot(graph, f)

# Example usage
if __name__ == "__main__":
    ttl_file = "Ontology_phase1_team15.ttl"  # Path to your TTL file
    output_dot_file = "graph.dot"  # Output DOT file
    display_persons(ttl_file)
    visualize_graph(ttl_file, output_dot_file)

from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery

# Define namespaces
BASE = Namespace("http://www.semanticweb.org/team15/ontologies/2024/4/M1-ontology-2/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

def load_ontology(file_path):
    # Load the TTL file into an RDF graph
    g = Graph()
    g.parse(file_path, format='ttl')
    return g

def read_query_from_file(query_file):
    # Read the SPARQL query from the file
    with open(query_file, 'r') as f:
        query_text = f.read()
    return query_text

def get_persons_with_query(graph, query_text):
    persons = set()
    # Prepare a SPARQL query from the text
    query = prepareQuery(query_text, initNs={"rdf": RDF, "base": BASE})
    # Execute the query and collect the results
    results = graph.query(query)
    for row in results:
        persons.add(row.person)
    return persons

def display_persons_with_query(file_path, query_file):
    # Load the ontology
    graph = load_ontology(file_path)
    # Read the SPARQL query from the file
    query_text = read_query_from_file(query_file)
    # Get all the Persons who are actors, directors, or writers using SPARQL query
    persons = get_persons_with_query(graph, query_text)
    # Display the Persons
    print("Persons:")
    for person in persons:
        print(person)

# Example usage
if __name__ == "__main__":
    ttl_file = "Ontology_phase1_team15.ttl"  # Path to your TTL file
    query_file = "query.txt"    # Path to your SPARQL query text file
    display_persons_with_query(ttl_file, query_file)

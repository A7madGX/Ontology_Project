from rdflib import Graph, RDF, RDFS, OWL, Namespace, Literal
from owlrl import DeductiveClosure, RDFS_Semantics

def load_ontology(file_path):
    # Load the TTL file into an RDF graph
    g = Graph()
    g.parse(file_path, format='ttl')
        
    # Apply Deductive Closure reasoning with RDFS semantics to the graph
    DeductiveClosure(RDFS_Semantics).expand(g)
    return g

def get_movie_info(graph, ns, movie_name):
    movie_info = {}
    # Iterate through all inferred triples in the graph
    for subj, pred, obj in graph:
        # Check if the subject is an instance of Movie with the given name
        if (subj, RDF.type, ns.Movie) in graph and (subj, ns.hasTitle, Literal(movie_name)) in graph:
            # Get movie year, country, genres, and actors
            year = graph.value(subj, ns.hasYear)
            country = graph.value(subj, ns.hasCountry)
            genres = [genre for genre in graph.objects(subj, ns.hasGenre)]
            actors = [actor for actor in graph.objects(subj, ns.hasActor)]
            movie_info = {
                'Year': year,
                'Country': country,
                'Genres': genres,
                'Actors': actors
            }
            break
    return movie_info

def display_movie_info(file_path, movie_name):
    # Load the ontology and apply Deductive Closure reasoning
    graph = load_ontology(file_path)
    # Define namespace
    ns = Namespace("http://www.semanticweb.org/team15/ontologies/2024/4/M1-ontology-2/")
    # Get movie information
    movie_info = get_movie_info(graph, ns, movie_name)
    # Display movie information
    if movie_info:
        print("Movie Information:")
        print("Name:", movie_name)
        print("Year:", movie_info.get('Year'))
        print("Country:", movie_info.get('Country'))
        print("Genres:", ', '.join(movie_info.get('Genres')))
        print("Actors:", ', '.join(movie_info.get('Actors')))
    else:
        print("Error: Movie '{}' not found.".format(movie_name))

# Example usage
if __name__ == "__main__":
    ttl_file = "Ontology_phase1_team15.ttl"  # Path to your TTL file
    movie_name = input("Enter the name of the movie: ")
    display_movie_info(ttl_file, movie_name)
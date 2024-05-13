from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, XSD

BASE = Namespace("http://www.semanticweb.org/team15/ontologies/2024/4/M1-ontology-2/")
BASE2 = Namespace("http://www.semanticweb.org/team15/ontologies/2024/4/M1-ontology-2#")

# Define a Movie class to represent each movie
class Movie:
    def __init__(self, title, actors, director, genres, year):
        self.title = title
        self.actors = actors
        self.director = director
        self.genres = genres
        self.year = year

# Define a class to manage the movie database
class MovieDatabase:
    def __init__(self):
        self.movies = []

    def load_from_ttl(self, ttl_file):
        g = Graph()
        g.parse(ttl_file, format="ttl")

        # Iterate over all triples in the graph
        for subj, pred, obj in g:
            # Check if the subject is a movie
            if (subj, RDF.type, BASE.Movie) in g:
                # Initialize variables to store movie details
                title = None
                actors = set()
                director = None
                genres = set()
                year = None

                # Extract movie details from triples
                if (subj, BASE.hasTitle, None) in g:
                    title = str(g.value(subj, BASE.hasTitle))
                if (subj, BASE.hasActor, None) in g:
                    actors.update(str(actor) for actor in g.objects(subj, BASE.hasActor))
                if (subj, BASE.hasDirector, None) in g:
                    director = str(g.value(subj, BASE.hasDirector))
                if (subj, BASE.hasGenre, None) in g:
                    genres.update(str(genre) for genre in g.objects(subj, BASE.hasGenre))
                if (subj, BASE.hasYear, None) in g:
                    year = int(g.value(subj, BASE.hasYear))

                # Create a Movie object and append it to the list of movies
                movie = Movie(title, list(actors), director, list(genres), year)
                self.movies.append(movie)


    def search_movies(self, included_actors=[], included_directors=[], included_genres=[], excluded_actors=[], excluded_directors=[], excluded_genres=[]):
        result = []

        for movie in self.movies:
            if (not included_actors or set(movie.actors).intersection(included_actors)) \
                    and (not included_directors or movie.director in included_directors) \
                    and (not included_genres or set(movie.genres).intersection(included_genres)) \
                    and (not excluded_actors or not set(movie.actors).intersection(excluded_actors)) \
                    and (not excluded_directors or movie.director not in excluded_directors) \
                    and (not excluded_genres or not set(movie.genres).intersection(excluded_genres)):
                result.append(movie)

        return result

def prompt_and_process_input(prompt):
    """
    Prompt the user for input and process it into URIs.
    """
    names = input(prompt).split(',')
    if not names:
        return []
    else:
        return [BASE + name.strip() for name in names]

def prompt_and_process_input_for_genres(prompt):
    """
    Prompt the user for input and process it into URIs.
    """
    names = input(prompt).split(',')
    if not names:
        return []
    else:
        return [BASE2 + name.strip() for name in names]
    
# Main function
def main():
    # Create a movie database
    movie_database = MovieDatabase()

    # Load movie data from TTL file
    movie_database.load_from_ttl("Ontology_phase1_team15.ttl")
            
    # Take input from User
    included_actor_uris = prompt_and_process_input("Actor names to include separated by commas: ")
    excluded_actor_uris = prompt_and_process_input("Actor names to exclude separated by commas: ")
    included_genre_uris = prompt_and_process_input_for_genres("Genre types to include separated by commas: ")
    excluded_genre_uris = prompt_and_process_input_for_genres("Genre types to exclude separated by commas: ")
    included_director_uris = prompt_and_process_input("Director names to include separated by commas: ")
    excluded_director_uris = prompt_and_process_input("Director names to exclude separated by commas: ")

    # Check if any of the lists are empty and replace them with []
    included_actor_uris = included_actor_uris if included_actor_uris!=[BASE] else []
    excluded_actor_uris = excluded_actor_uris if excluded_actor_uris!=[BASE] else []
    included_director_uris = included_director_uris if included_director_uris!=[BASE] else []
    excluded_director_uris = excluded_director_uris if excluded_director_uris!=[BASE] else []
    included_genre_uris = included_genre_uris if included_genre_uris!=[BASE2] else []
    excluded_genre_uris = excluded_genre_uris if excluded_genre_uris!=[BASE2] else []

    # Search for movies based on criteria
    found_movies = movie_database.search_movies(
                                                included_actors=included_actor_uris, 
                                                included_genres=included_genre_uris,
                                                included_directors=included_director_uris,
                                                excluded_actors=excluded_actor_uris,
                                                excluded_genres=excluded_genre_uris,
                                                excluded_directors=excluded_director_uris,
                                            )

    # Display the found movies
    print("------------------------------------------------------------------")
    if found_movies:
        print("Found movies:")
        printed_titles = set()  # Set to store encountered titles
        for movie in found_movies:
            if movie.title not in printed_titles:  # Check if title is not already printed
                print("Movie Title:", movie.title)
                print("Movie Release Year:", movie.year)
                print("Movie Genre:", ", ".join(movie.genres))
                print("Movie Director Name:", movie.director)
                print("Movie Actor Name:", ", ".join(movie.actors))
                print("----------")
                printed_titles.add(movie.title)  # Add title to printed set
    else:
        print("There are no movies with this info.")


if __name__ == "__main__":
    main()

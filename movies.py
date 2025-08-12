import os
import requests
import movie_storage_sql as storage
from dotenv import load_dotenv
import statistics
import random
import re

# Load environment variables from .env file
load_dotenv()


def command_list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies in the database.")
        return
    print(f"\n{len(movies)} movies in total")
    for movie in movies:
        print(f"  {movie['title']} ({movie['year']}): {movie['rating']}")


def command_add_movie(movie_title=None):
    """
    Add a new movie to the database by fetching data from OMDb API.
    If movie_title is not provided, it will prompt for input.
    """
    if movie_title is None:
        movie_title = input("Enter movie title: ")

    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        print("Error: OMDB_API_KEY not found. "
              "Please set it in your .env file.")
        return False

    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        movie_data = response.json()

        if movie_data.get("Response") == "True":
            title = movie_data["Title"]
            year_str = movie_data["Year"]
            year = int(''.join(filter(str.isdigit, year_str))[:4])
            rating = float(movie_data["imdbRating"])
            poster_url = movie_data["Poster"]

            storage.add_movie(title, year, rating, poster_url)
            print(f"Movie '{title}' successfully added.")
            return True
        else:
            print(f"Error: Movie '{movie_title}' not found on OMDb.")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to OMDb API: {e}")
        return False
    except (KeyError, ValueError) as e:
        print(f"Error parsing movie data: {e}")
        return False


def command_delete_movie():
    """Deletes a movie from the database."""
    title = input("Enter movie title to delete: ")
    if storage.delete_movie(title):
        print(f"Movie '{title}' deleted successfully.")
    else:
        print(f"Movie '{title}' not found.")


def command_update_movie():
    """Updates the rating of a movie in the database."""
    title = input("Enter movie title to update: ")
    try:
        new_rating = float(input("Enter new rating: "))
        if storage.update_movie(title, new_rating):
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")
    except ValueError:
        print("Invalid rating. Please enter a number.")


def command_stats():
    """Prints statistics for the movies in the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies to calculate stats for.")
        return

    ratings = [movie['rating'] for movie in movies]
    print(f"\nAverage rating: {statistics.mean(ratings):.2f}")
    print(f"Median rating: {statistics.median(ratings):.2f}")

    best_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)
    worst_movies = sorted(movies, key=lambda x: x['rating'])

    print("\nBest movie(s):")
    for movie in best_movies:
        if movie['rating'] == best_movies[0]['rating']:
            print(f"  {movie['title']}: {movie['rating']:.2f}")
        else:
            break

    print("\nWorst movie(s):")
    for movie in worst_movies:
        if movie['rating'] == worst_movies[0]['rating']:
            print(f"  {movie['title']}: {movie['rating']:.2f}")
        else:
            break


def command_random_movie():
    """Selects and displays a random movie from the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies to choose from.")
        return

    random_movie = random.choice(movies)
    print(f"\nYour random movie for tonight: {random_movie['title']} "
          f"({random_movie['year']}) with a rating of "
          f"{random_movie['rating']:.2f}")


def command_search_movie():
    """Searches for movies in the database by title."""
    term = input("Enter search term: ")
    movies = storage.list_movies()
    found_movies = [movie for movie in movies if re.search(
        term, movie['title'], re.IGNORECASE)]

    if not found_movies:
        print("No movies found for that search term.")
        return

    print(f"\nFound {len(found_movies)} movie(s):")
    for movie in found_movies:
        print(f"  {movie['title']}")


def command_movies_by_rating():
    """Displays movies sorted by their rating."""
    movies = storage.list_movies()
    if not movies:
        print("No movies to sort.")
        return

    sorted_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)
    print("\nMovies sorted by rating:")
    for movie in sorted_movies:
        print(f"  {movie['title']}: {movie['rating']:.2f}")


def command_generate_website():
    """
    Generates a static website from the movie data and saves it in the src
    directory.
    """
    movies = storage.list_movies()

    # Read the template
    try:
        with open("_static/index_template.html", "r") as f:
            template_html = f.read()
    except FileNotFoundError:
        print("Error: Template file '_static/index_template.html' not found.")
        return

    # Generate the movie grid HTML
    movie_grid_html = ""
    for movie in movies:
        movie_grid_html += f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{movie['poster_image_url']}"
                     title="{movie['title']}">
                <div class="movie-title">{movie['title']}</div>
                <div class="movie-year">{movie['year']}</div>
            </div>
        </li>
        """

    # Replace placeholders in the template
    website_html = template_html.replace("__TEMPLATE_TITLE__", "My Movie App")
    website_html = website_html.replace(
        "__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    # Ensure the src directory exists
    os.makedirs("src", exist_ok=True)

    # Write the new HTML file to the src directory
    with open("src/index.html", "w") as f:
        f.write(website_html)

    # Copy the CSS file to the src directory
    try:
        with open("_static/style.css", 'r') as f_css:
            with open("src/style.css", 'w') as f_css_out:
                f_css_out.write(f_css.read())
    except FileNotFoundError:
        print("Warning: _static/style.css not found, "
              "website may not be styled correctly.")

    print("Website was generated successfully in the 'src' directory.")


def main():
    """Main function to run the movie database application."""
    storage.setup_database()  # Setup the database and table

    commands = {
        "0": {"function": exit, "description": "Exit"},
        "1": {"function": command_list_movies, "description": "List movies"},
        "2": {"function": command_add_movie, "description": "Add movie"},
        "3": {"function": command_delete_movie, "description": "Delete movie"},
        "4": {"function": command_update_movie, "description": "Update movie"},
        "5": {"function": command_stats, "description": "Stats"},
        "6": {"function": command_random_movie,
              "description": "Random movie"},
        "7": {"function": command_search_movie,
              "description": "Search movie"},
        "8": {"function": command_movies_by_rating,
              "description": "Movies sorted by rating"},
        "9": {"function": command_generate_website,
              "description": "Generate website"},
    }

    while True:
        print("\n********** My Movies Database **********")
        for key, value in sorted(commands.items()):
            print(f"{key}. {value['description']}")

        choice = input("Enter choice: ")

        command = commands.get(choice)
        if command:
            if command['description'] == "Exit":
                break
            # For "Add movie", we call it without arguments to get user input
            if command['description'] == "Add movie":
                command["function"]()
            else:
                command["function"]()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

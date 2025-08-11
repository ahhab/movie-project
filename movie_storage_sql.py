from sqlalchemy import create_engine, text, exc

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL)

# --- Schema Setup ---


def setup_database():
    """
    Creates the movies table if it does not exist.
    """
    with engine.connect() as connection:
        # Drop the table to ensure a fresh start with the new schema
        # connection.execute(text("DROP TABLE IF EXISTS movies"))
        # Create the table with the new schema
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster_image_url TEXT
            )
        """))
        connection.commit()

# --- CRUD Functions ---


def list_movies():
    """
    Retrieves all movies from the database.

    Returns:
        list: A list of dictionaries, where each dictionary represents a movie.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster_image_url FROM movies"))
        movies = []
        for row in result.fetchall():
            movies.append({
                "title": row[0],
                "year": row[1],
                "rating": row[2],
                "poster_image_url": row[3]
            })
        return movies


def add_movie(title, year, rating, poster_image_url):
    """
    Adds a new movie to the database.

    Args:
        title (str): The title of the movie.
        year (int): The release year of the movie.
        rating (float): The rating of the movie.
        poster_image_url (str): The URL of the movie's poster image.
    """
    with engine.connect() as connection:
        try:
            query = text(
                "INSERT INTO movies (title, year, rating, poster_image_url) "
                "VALUES (:title, :year, :rating, :poster_image_url)"
            )
            connection.execute(query, {
                "title": title,
                "year": year,
                "rating": rating,
                "poster_image_url": poster_image_url
            })
            connection.commit()
        except exc.IntegrityError:
            print(f"Error: Movie '{title}' already exists in the database.")
            connection.rollback()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            connection.rollback()


def delete_movie(title):
    """
    Deletes a movie from the database by its title.

    Args:
        title (str): The title of the movie to delete.

    Returns:
        bool: True if a movie was deleted, False otherwise.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"), {"title": title})
        connection.commit()
        return result.rowcount > 0


def update_movie(title, rating):
    """
    Updates the rating of a movie in the database.

    Args:
        title (str): The title of the movie to update.
        rating (float): The new rating for the movie.

    Returns:
        bool: True if the movie was updated, False otherwise.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating WHERE title = :title"),
            {"title": title, "rating": rating}
        )
        connection.commit()
        return result.rowcount > 0

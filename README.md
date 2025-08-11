# Movie Database Project

This project is a command-line application for managing a movie database. It is designed to demonstrate how to interact with a SQL database and external APIs in Python.

## Features

*   **List movies**: View all movies in the database.
*   **Add a movie**: Add a new movie by providing its title. The application will automatically fetch the movie's details (year, rating, poster URL) from the OMDb API.
*   **Delete a movie**: Remove a movie from the database.
*   **Update a movie**: Update the rating of an existing movie.
*   **Statistics**: View statistics about the movies in the database, including the average, median, best, and worst ratings.
*   **Random movie**: Get a random movie from the database.
*   **Search**: Search for movies by title.
*   **Generate website**: Create a static `index.html` file in the `src` directory, which can be served by a Flask application. The website is generated from a template located in the `_static` directory.

## How it Works

The application is structured into two main files:

*   `movies.py`: This file contains the main application logic, including the user menu and the functions for interacting with the user.
*   `movie_storage_sql.py`: This file handles all interactions with the SQLite database. It uses the SQLAlchemy library to execute SQL queries.

When a user adds a movie, the application sends a request to the OMDb API to retrieve the movie's information. This data is then stored in the `movies.db` SQLite database.

## Getting Started

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set up your environment variables**: Create a `.env` file in the root of the project and add your OMDb API key:
    ```
    OMDB_API_KEY=your_api_key
    ```
3.  **Run the application**:
    ```bash
    python movies.py
    ```

## Acknowledgements

Thank you to Masterschool for providing the inspiration and guidance for this project.

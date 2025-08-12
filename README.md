# Movie Database Project

This project is a command-line application for managing a movie database, designed to demonstrate how to interact with a SQL database and external APIs in Python. As a bonus, it also includes a dynamic web interface built with Flask.

## Features

*   **List movies**: View all movies in the database.
*   **Add a movie**: Add a new movie by providing its title. The application will automatically fetch the movie's details (year, rating, poster URL) from the OMDb API.
*   **Delete a movie**: Remove a movie from the database.
*   **Update a movie**: Update the rating of an existing movie.
*   **Statistics**: View statistics about the movies in the database, including the average, median, best, and worst ratings.
*   **Random movie**: Get a random movie from the database.
*   **Search**: Search for movies by title.
*   **Generate website**: Create a static `index.html` file in the `src` directory, which can be served by a Flask application. The website is generated from a template located in the `_static` directory.

## Bonus Feature: Dynamic Web Interface

In addition to the command-line interface, this project also includes a dynamic web interface powered by Flask. The `main.py` file launches a web server that:

*   **Dynamically Generates the Homepage**: The `index.html` page is generated on the fly, ensuring that the movie list is always up-to-date.
*   **Adds Movies from the Web**: The homepage features a form that allows users to add new movies to the database directly from the browser.

This feature demonstrates how a simple Flask application can be used to create a dynamic and interactive frontend for a database-driven application.

## How it Works

The application is structured into three main files:

*   `movies.py`: This file contains the main application logic, including the user menu and the functions for interacting with the user.
*   `movie_storage_sql.py`: This file handles all interactions with the SQLite database. It uses the SQLAlchemy library to execute SQL queries.
*   `main.py`: This file contains the Flask web server that powers the dynamic web interface.

When a user adds a movie, either through the command-line or the web interface, the application sends a request to the OMDb API to retrieve the movie's information. This data is then stored in the `movies.db` SQLite database.

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
    *   **Command-line interface**:
        ```bash
        python movies.py
        ```
    *   **Web interface**:
        ```bash
        ./devserver.sh
        ```

## Disclaimer

This project is intended for educational purposes only and is not production-ready. It lacks several important security features, including but not limited to:

*   **Input sanitization**: The application does not thoroughly sanitize user input, which could leave it vulnerable to injection attacks.
*   **Spam protection**: There are no measures in place to prevent spam or abuse.
*   **Error handling**: While some basic error handling is in place, it is not robust enough for a production environment.
*   **User management**: This app has no user management, thus its an ever growing list of movies, if hosted. 

## Acknowledgements

Thank you to Masterschool for providing the inspiration and guidance for this project.

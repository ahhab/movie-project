from flask import Flask, render_template_string, request, redirect, send_from_directory
import os
import movies as movie_commands
import movie_storage_sql as storage

app = Flask(__name__)

# --- Dynamic Website Generation ---
def generate_movie_grid(movies):
    """Generates the HTML for the movie grid."""
    grid_html = ""
    for movie in movies:
        grid_html += f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{movie['poster_image_url']}"
                     title="{movie['title']}">
                <div class="movie-title">{movie['title']}</div>
                <div class="movie-year">{movie['year']}</div>
            </div>
        </li>
        """
    return grid_html

@app.route('/')
def serve_index():
    """Dynamically generates and serves the index.html page."""
    storage.setup_database()  # Ensure the database is ready
    movies = storage.list_movies()
    movie_grid_html = generate_movie_grid(movies)

    try:
        with open("_static/index_template.html", "r") as f:
            template_html = f.read()
    except FileNotFoundError:
        return "Error: Template file not found.", 500

    website_html = template_html.replace("__TEMPLATE_TITLE__", "My Movie App")
    website_html = website_html.replace(
        "__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    return website_html

# --- Static File Serving ---
@app.route('/style.css')
def serve_css():
    """Serves the style.css file."""
    return send_from_directory('_static', 'style.css')

# --- API Routes ---
@app.route('/add', methods=['POST'])
def add_movie_from_web():
    """Adds a movie from the web form."""
    movie_title = request.form.get("movie_title")
    if movie_title:
        movie_commands.command_add_movie(movie_title=movie_title)
    return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)

from flask import render_template

from project.config import config
from project.models import Genre, Movie, Director
from project.server import create_app, db

app = create_app(config)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Movie": Movie,
        "Director": Director
    }


if __name__ == '__main__':
    app.run(debug=True)

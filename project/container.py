from project.dao.main import GenresDAO, MoviesDAO, DirectorsDAO, UserDAO

from project.services.movies_service import MovieService
from project.services.genres_service import GenresService
from project.services.director_service import DirectorService
from project.services.auth_service import AuthService
from project.services.users_service import UserService

from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
movie_dao = MoviesDAO(db.session)
director_dao = DirectorsDAO(db.session)
user_dao = UserDAO(db.session)

# Services
genre_service = GenresService(dao=genre_dao)
movie_service = MovieService(dao=movie_dao)
director_service = DirectorService(dao=director_dao)
user_service = UserService(user_dao)
auth_service = AuthService(user_service)

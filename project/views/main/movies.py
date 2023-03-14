from flask_restx import Namespace, Resource

from project.container import movie_service
from project.setup.api.models import movie
from project.setup.api.parsers import page_parser, status_parser

api = Namespace('movies')


@api.route('/')
class MovieView(Resource):
    @api.expect(page_parser, status_parser)
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all movies
        """
        return movie_service.get_all(**status_parser.parse_args(), **page_parser.parse_args())


@api.route('/<int:movie_id>/')
class MovieView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(movie, code=200, description='OK')
    def get(self, movie_id: int):
        """
        Get one movie by pk
        """
        return movie_service.get_one(movie_id)

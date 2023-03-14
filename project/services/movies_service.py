from typing import Optional

from project.dao.main import MoviesDAO
from project.exceptions import ItemNotFound
from project.models import Movie


class MovieService:
    def __init__(self, dao: MoviesDAO):
        self.dao = dao

    def get_all(self, status: Optional[str] = None, page: Optional[int] = None) -> list[Movie]:
        return self.dao.get_all_by_status(status=status, page=page)

    def get_one(self, pk: int) -> Movie:
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f'Фильма с pk {pk} не существует')



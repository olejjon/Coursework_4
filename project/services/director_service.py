from typing import Optional

from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import Director


class DirectorService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_one(self, director_id: int) -> Director:
        if director := self.dao.get_by_id(director_id):
            return director
        raise ItemNotFound(f'Director with pk={director_id} not exists')

    def get_all(self, page: Optional[int] = None) -> list[Director]:
        return self.dao.get_all(page=page)

from typing import Optional

from werkzeug.exceptions import NotFound
from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre

class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_by_status(self, status: Optional[str] = None,
                          page: Optional[int] = None):
        stmt = self._db_session.query(Movie)
        if status:
            if status == 'new':
                stmt = stmt.order_by(-Movie.year)

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []

        return stmt.all()


class UserDAO(BaseDAO[User]):
    __model__ = User

    def get_by_email(self, email: str):
        return self.db_session.query(User).filter(User.email == email).first()

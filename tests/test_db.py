from sqlalchemy.orm import Session

from app.db import get_db


def test_get_db():
    get_db_generator = get_db()
    assert isinstance(next(get_db_generator), (Session,))

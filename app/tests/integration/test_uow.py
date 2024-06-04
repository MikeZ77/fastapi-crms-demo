from sqlalchemy import text
from sqlalchemy.orm import Session


def test_insert_into_content(session: Session):
    session.execute(text("INSERT INTO content (version) VALUES (1)"))
    results = session.execute(text("SELECT version FROM content"))
    assert list(results) == [(1,)]

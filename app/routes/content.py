from fastapi import APIRouter
from pydantic import UUID4

from app.routes.types import ContentRequest
from app.services.content import add_content, get_content
from app.services.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter()


@router.get("/{content_id}")
def read_content(content_id: UUID4):
    return get_content(content_id, SqlAlchemyUnitOfWork())


@router.post("/")
def create_content(content: ContentRequest):
    return add_content(content, SqlAlchemyUnitOfWork())

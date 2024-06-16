from pydantic import UUID4

from app.domain.content import Content
from app.routes.types import ContentRequest
from app.services.domain_services import assign_offer_to_content
from app.services.unit_of_work import AbstractUnitOfWork


def add_content(content: ContentRequest, uow: AbstractUnitOfWork):
    with uow:
        content_model = Content()
        content_id = uow.content.add_content(content_model)
        assign_offer_to_content(**content.model_dump(), content=content_model, uow=uow)
        uow.commit()
    return content_id


def get_content(content_id: UUID4, uow: AbstractUnitOfWork):
    with uow:
        content = uow.content.get_content(content_id)
        return content.sqlalchemy_to_dict()

import uuid

from pydantic import UUID4

from app.domain.contracts import DomainModel


class InvalidContent(Exception): ...


class Content(DomainModel):
    def __init__(self, offer_name: str = None, version: int = 0):
        self.content_id = uuid.uuid4()
        self.offer_name = offer_name
        self.version = version

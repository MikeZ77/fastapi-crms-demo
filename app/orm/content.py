from sqlalchemy import UUID, Column, Index, Integer, String, Table

import app.domain.content as model
from app.orm import mapper_registry

# Content can have an offer assigned to it, but we do not create this relationship
# because aggegrates should be treated as seperate units in the database. This
# relationship gets managed in the application code. Digging more into larger DDD
# examples would be useful to see if this is the right approach.
content = Table(
    "content",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("content_id", UUID(as_uuid=True), nullable=False, unique=True),
    Column("offer_name", String, nullable=True),
    Column("version", Integer, nullable=False, default=1),
    Index("ix_content_content_id", "content_id"),
)


def start_mappers():
    mapper_registry.map_imperatively(model.Content, content)

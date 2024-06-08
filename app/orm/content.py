from sqlalchemy import Column, Integer, Table

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
    Column("offer_id", Integer, nullable=True),
    Column("version", Integer, nullable=False, default=1),
)


def start_mappers():
    mapper_registry.map_imperatively(model.Content, content)

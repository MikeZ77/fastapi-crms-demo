from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import registry

mapper_registry = registry()

contracts = Table(
    "contracts",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("studio", String, nullable=False),
)

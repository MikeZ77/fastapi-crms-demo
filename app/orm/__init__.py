from sqlalchemy.orm import registry

mapper_registry = registry()

# If we have a lot of aggegrates, we could use importlib to dynamically import and
# make this less verbose.
from .content import start_mappers as start_content_mappers  # noqa: E402
from .contracts import start_mappers as start_contracts_mappers  # noqa: E402

mappers = [start_content_mappers, start_contracts_mappers]


def map_models():
    for mapper in mappers:
        mapper()

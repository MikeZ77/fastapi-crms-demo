from .content import mapper_registry as content_mapper_registry
from .content import start_mappers as start_content_mappers
from .contracts import mapper_registry as contracts_mapper_registry
from .contracts import start_mappers as start_contracts_mappers

registries = [content_mapper_registry, contracts_mapper_registry]
mappers = [start_content_mappers, start_contracts_mappers]

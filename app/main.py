# import debugpy
from alembic import command
from alembic.config import Config
from fastapi import FastAPI

from app.routes.router import api_router

# When the application starts, we run any pending migrations
alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")

# debugpy.listen(("0.0.0.0", 5678))
app = FastAPI()

app.include_router(api_router, prefix="/api")

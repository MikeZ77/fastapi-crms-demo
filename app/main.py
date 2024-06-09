import debugpy
from alembic import command
from alembic.config import Config
from fastapi import FastAPI

# from app.middleware.exception_handlers import license_exception_handler
from app.orm import map_models
from app.routes.router import api_router

# Map our domain models to our data
map_models()
# When the application starts, we run any pending migrations
alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")

try:
    # To prevent the debugger from trying to attach to the same port
    debugpy.listen(("0.0.0.0", 5679))
except RuntimeError:
    ...

app = FastAPI()
# Register our exception handling and routes
# app.add_exception_handler(license_exception_handler())
app.include_router(api_router, prefix="/api")

import debugpy
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from sqlalchemy import text

from app.middleware.exception_handlers import ExceptionHandlers
from app.orm import map_models
from app.routes.router import api_router
from app.services.unit_of_work import SessionFactory

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
ExceptionHandlers.register_exception_handlers(app)
app.include_router(api_router, prefix="/api")


# Health endpoint isn't part of our domain so we will just add it here.
@app.get("/health")
def health_check():
    with SessionFactory() as session:
        session.execute(text("SELECT 1"))
    return "Healthy"

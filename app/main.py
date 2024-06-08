# import debugpy
from fastapi import FastAPI

from app.orm import start_all_mappers
from app.routes.router import api_router

# debugpy.listen(("0.0.0.0", 5678))
app = FastAPI()
start_all_mappers()

app.include_router(api_router, prefix="/api")

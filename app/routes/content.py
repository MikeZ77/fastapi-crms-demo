from fastapi import APIRouter

router = APIRouter()


@router.get("/{id}")
def get_content(id: int):
    return {"message": id}

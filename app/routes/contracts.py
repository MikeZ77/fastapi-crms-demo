from fastapi import APIRouter

router = APIRouter()


@router.get("/offers")
def get_offers():
    return {"message": "Offers"}

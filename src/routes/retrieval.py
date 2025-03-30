from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/")
async def retrieval_page(request: Request):
    return {"message": "Retrieval page"}
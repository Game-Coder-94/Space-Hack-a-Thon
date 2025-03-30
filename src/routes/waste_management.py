from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/")
async def waste_management_page(request: Request):
    return {"message": "Waste Management page"}
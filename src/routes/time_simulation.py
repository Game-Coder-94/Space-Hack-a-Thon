from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/")
async def time_simulation_page(request: Request):
    return {"message": "Time Simulation page"}
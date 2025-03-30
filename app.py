from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from src.routes.search import router as search_router
from src.routes.placement import router as placement_router
from src.routes.retrieval import router as retrieval_router
from src.routes.waste_management import router as waste_management_router
from src.routes.time_simulation import router as time_simulation_router

app = FastAPI()

# Set up templates
templates = Jinja2Templates(directory="front_end")

# Register routers
app.include_router(search_router, prefix="/api/search", tags=["Search"])
app.include_router(placement_router, prefix="/api/placement", tags=["Placement"])
app.include_router(retrieval_router, prefix="/api/retrieval", tags=["Retrieval"])
app.include_router(waste_management_router, prefix="/api/waste", tags=["Waste Management"])
app.include_router(time_simulation_router, prefix="/api/time-simulation", tags=["Time Simulation"])

@app.get("/")
async def index(request):
    return templates.TemplateResponse("index.html", {"request": request})

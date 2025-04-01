from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from src.routes.search import router as search_router
from src.routes.placement import router as placement_router
from src.routes.retrieval import router as retrieval_router
from src.routes.waste_management import router as waste_management_router
from src.routes.place import router as place_router
from src.routes.return_plan import router as return_plan_router
from src.routes.complete_undocking import router as complete_undocking_router
from src.routes.time_simulation import router as time_simulation_router
from src.routes.import_items import router as import_items_router
from src.routes.import_containers import router as import_containers_router
from src.routes.export_arrangement import router as export_arrangement_router
from src.routes.logs import router as logs_router

app = FastAPI()

# Set up templates
templates = Jinja2Templates(directory="front_end")

# Register routers
app.include_router(search_router, prefix="/api/search", tags=["Search"])
app.include_router(placement_router, prefix="/api/placement", tags=["Placement"])
app.include_router(retrieval_router, prefix="/api/retrieval", tags=["Retrieval"])
app.include_router(waste_management_router, prefix="/api/waste", tags=["Waste Management"])
app.include_router(time_simulation_router, prefix="/api", tags=["Time Simulation"])
app.include_router(place_router, prefix="/api", tags=["Placement"])
app.include_router(return_plan_router, prefix="/api/waste", tags=["Return Planner"])
app.include_router(complete_undocking_router, prefix="/api/waste", tags=["Complete Undocking"])
app.include_router(import_items_router, prefix="/api", tags=["Import Items"])
app.include_router(import_containers_router, prefix="/api", tags=["Import Containers"])
app.include_router(export_arrangement_router, prefix="/api", tags=["Export Arrangement"])
app.include_router(logs_router, prefix="/api", tags=["Logs"])

@app.get("/")
async def index(request):
    return templates.TemplateResponse("index.html", {"request": request})

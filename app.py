from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.rearrangement import RearrangementOptimizer
from src.config import CONTAINER_CAPACITIES, INITIAL_STOWAGE_SOLUTION

app = FastAPI()

# Set up templates
templates = Jinja2Templates(directory="front_end")

# Initialize optimizer
rearrangement_optimizer = RearrangementOptimizer(INITIAL_STOWAGE_SOLUTION, CONTAINER_CAPACITIES)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
async def submit(request: Request):
    data = await request.json()  # Get JSON data from frontend

    new_item = {
        "id": data["id"],
        "name": data["name"],
        "width": data["width"],
        "depth": data["depth"],
        "height": data["height"],
        "mass": data["mass"],
        "priority": data["priority"],
        "expiry": data["expiry"],
        "usage": data["usage"],
        "preferred-zone": data["preferred_zone"]
    }

    # Run rearrangement logic
    result = rearrangement_optimizer.suggest_rearrangement(new_item)
    
    return JSONResponse(content=result)

# Serve static files if needed
app.mount("/static", StaticFiles(directory="front_end/static"), name="static")

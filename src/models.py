from pydantic import BaseModel
from typing import Optional

class SearchRequest(BaseModel):
    itemId: Optional[str] = None
    itemName: Optional[str] = None
    userId: Optional[str] = None

class SearchResponse(BaseModel):
    message: str
    containerId: Optional[str] = None

# Container model
class Container(BaseModel):
    name: str
    location: str

# Item model
class Item(BaseModel):
    name: str
    weight: float
    container_id: Optional[str]  # Reference to a container
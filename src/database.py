from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection string
MONGO_URI = "mongodb://localhost:27017"

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGO_URI)

# Access the database
db = client["hackathon_db"]

# Simulated Database
# Search logic using this database
containers = {
    "A1": [{"itemId": "101", "itemName": "Oxygen Tank", "userId": "U123"},
           {"itemId": "102", "itemName": "Water Supply", "userId": "U124"}],
    "B1": [{"itemId": "201", "itemName": "Medical Kit", "userId": "U123"},
           {"itemId": "202", "itemName": "Food Pack", "userId": "U125"}]
}

def get_all_items():
    all_items = []
    for container_id, items in containers.items():
        for item in items:
            all_items.append({**item, "containerId": container_id})
    return sorted(all_items, key=lambda x: x['itemId'])
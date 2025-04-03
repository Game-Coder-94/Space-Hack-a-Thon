from pymongo import MongoClient

def get_current_arrangement():
    """
    Retrieves the current arrangement of items in containers.

    Returns:
        list: A list of dictionaries representing the arrangement.
    """
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["space_hackathon"]  # Replace with your database name
    collection = db["arrangements"]  # Replace with your collection name

    # Retrieve arrangement data from MongoDB
    arrangement = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB _id field
    
    return arrangement
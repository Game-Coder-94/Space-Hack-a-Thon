# Log logic not not implemented

from datetime import datetime
from pymongo import MongoClient

def get_logs(start_date, end_date, item_id=None, user_id=None, action_type=None):
    """
    Fetches logs based on the provided query parameters.

    Args:
        start_date (str): Start date in ISO format.
        end_date (str): End date in ISO format.
        item_id (str, optional): Filter by item ID.
        user_id (str, optional): Filter by user ID.
        action_type (str, optional): Filter by action type.

    Returns:
        list: A list of logs matching the query parameters.
    """
    # Validate the date formats
    try:
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)
    except ValueError:
        raise ValueError("Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")

    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["space_hackathon"]  # Replace with your database name
    logs_collection = db["logs"]  # Replace with your collection name

    # Fetch logs from MongoDB
    query = {
        "timestamp": {
            "$gte": start_date.isoformat(),
            "$lte": end_date.isoformat()
        }
    }
    if item_id:
        query["itemId"] = item_id
    if user_id:
        query["userId"] = user_id
    if action_type:
        query["actionType"] = action_type

    logs = list(logs_collection.find(query))

    # Filter logs based on query parameters
    filtered_logs = [
        log for log in logs
        if start_date <= datetime.fromisoformat(log["timestamp"]) <= end_date
        and (not item_id or log["itemId"] == item_id)
        and (not user_id or log["userId"] == user_id)
        and (not action_type or log["actionType"] == action_type)
    ]

    return filtered_logs
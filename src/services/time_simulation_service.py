from datetime import datetime, timedelta

def simulate_day(num_of_days=None, to_timestamp=None, items_to_be_used_per_day=None):
    """
    Simulates the passage of days and updates item statuses.

    Args:
        num_of_days (int): The number of days to simulate.
        to_timestamp (str): The target timestamp in ISO format.
        items_to_be_used_per_day (list): A list of items to be used per day.

    Returns:
        dict: The simulation results, including new date and changes to items.
    """
    # Determine the target date
    current_date = datetime.now()
    if to_timestamp:
        try:
            target_date = datetime.fromisoformat(to_timestamp)
        except ValueError:
            raise ValueError("Invalid 'toTimestamp' format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")
    elif num_of_days is not None:
        target_date = current_date + timedelta(days=num_of_days)
    else:
        raise ValueError("Either 'numOfDays' or 'toTimestamp' must be provided.")

    # Simulate item usage
    items_used = []
    items_expired = []
    items_depleted_today = []

    for item in items_to_be_used_per_day:
        # Simulate usage
        remaining_uses = item.get("remainingUses", 10) - (target_date - current_date).days
        if remaining_uses <= 0:
            items_depleted_today.append({"itemId": item["itemId"], "name": item.get("name", "Unknown")})
        else:
            items_used.append({"itemId": item["itemId"], "name": item.get("name", "Unknown"), "remainingUses": remaining_uses})

        # Simulate expiry
        expiry_date = datetime.now() + timedelta(days=5)  # Example expiry logic
        if expiry_date < target_date:
            items_expired.append({"itemId": item["itemId"], "name": item.get("name", "Unknown")})

    # Return the simulation results
    return {
        "newDate": target_date.isoformat(),
        "changes": {
            "itemsUsed": items_used,
            "itemsExpired": items_expired,
            "itemsDepletedToday": items_depleted_today
        }
    }
def get_all_items():
    all_items = []
    for container_id, items in containers.items():
        for item in items:
            all_items.append({**item, "containerId": container_id})
    return sorted(all_items, key=lambda x: x['itemId'])

def binary_search(data, key, search_by):
    low, high = 0, len(data) - 1

    while low <= high:
        mid = (low + high) // 2
        if data[mid][search_by] == key:
            return data[mid]
        elif data[mid][search_by] < key:
            low = mid + 1
        else:
            high = mid - 1
    return None

def search_item(itemId=None, itemName=None, userId=None):
    data = get_all_items()

    # Search by itemId using Binary Search if itemId is provided
    if itemId:
        result = binary_search(data, itemId, 'itemId')
        if result and (not userId or result['userId'] == userId):
            return result
        else:
            return None

    # Linear Search if itemName is provided
    elif itemName:
        for item in data:
            if item['itemName'].lower() == itemName.lower() and (not userId or item['userId'] == userId):
                return item
    return None

from apicaller import fetch_adjacent_items
from calc import calc_distance, calc_point


# POST /items
# --- Request body ---
# houseType: str
# params: [p1, p2, p3, ...]
# p in params: {name: str, std: int, weight: int, exp: bool}
# location: [lat, lng]
# --- Response body ---
# items: [i1, i2, i3, ...]
# i in items: 
# {
# item_id: str,
# title: str,
# area: float,
# distance: float,
# location: [lat, lng],
# point: float,
# thumbnail_url: str,
# deposit: int,
# rent: int
# }
# location: [lat, lng]
def items(req: dict) -> dict:
    target_location = tuple(req['location'])
    params = req['params']
    items = fetch_adjacent_items(target_location, req['houseType'])
    resp = {}
    resp_items = []
    for item in items:
        item_location = item['random_location']['lat'], item['random_location']['lng']
        distance = calc_distance(item_location, target_location)
        resp_item = {
            'item_id': item['item_id'],
            'title': item['title'],
            'area': item['전용면적']['m2'],
            'distance': distance,
            'location': list(item_location),
            'point': calc_point(item, params, distance),
            'thumbnail_url': item['images_thumbnail'],
            'deposit': item['deposit'],
            'rent': item['rent']
        }
        resp_items.append(resp_item)
    resp_items.sort(key=lambda x: x['point'], reverse=True)
    return {'items': resp_items[:100], 'location': req['location']}


if __name__ == '__main__':
    jeju_univ_location = 33.45646911357635, 126.56238281848411
    cau_loc = 37.50555114192287, 126.95947698946811
    params = [
        {"name": "area", "std": 55, "weight": 10},
        {"name": "rent", "std": 55, "weight": -10},
        {"name": "deposit", "std": 500, "weight": -1},
        {"name": "distance", "std": 5, "weight": -0.1}]
    resp_items = items({'houseType': 'oneroom', 'params': params, 'location': list(cau_loc)})
    for item in resp_items['items']:
        print(f"[{item['point']}] ({item['deposit']}/{item['rent']}) {item['title']} 면적:{item['area']} 거리: {item['distance']}km")

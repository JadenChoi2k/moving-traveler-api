from apicaller import fetch_adjacent_items
from calc import calc_distance, calc_point


# POST /items
# --- Request body ---
# houseType: str (oneroom, villa, apt)
# salesType: str (월세, 전세, 매매)
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
    items = fetch_adjacent_items(target_location, req['houseType'], req['salesType'])
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
    return {'adj_size': len(resp_items), 'items': resp_items[:100], 'location': req['location']}


if __name__ == '__main__':
    from time import time
    jeju_univ_location = 33.45646911357635, 126.56238281848411
    cau_loc = 37.50555114192287, 126.95947698946811
    cau_ans_loc = 37.006879507825275, 127.22926008576495
    house_type = "oneroom"
    sales_type = "월세"
    loc = cau_loc
    params = [
        {"name": "area", "std": 50, "weight": 5},
        {"name": "rent", "std": 50, "weight": -7},
        {"name": "deposit", "std": 500, "weight": -2},
        {"name": "distance", "std": 5, "weight": -5}]
    st = time()
    resp_items = items({
        'houseType': house_type,
        'salesType': sales_type,
        'params': params,
        'location': list(loc)
        })
    print(f'response time: {time() - st}s')
    for item in resp_items['items']:
        print(f"[{item['point']}] ({item['deposit']}/{item['rent']}) {item['title']} 면적:{item['area']} 거리: {item['distance']}km")

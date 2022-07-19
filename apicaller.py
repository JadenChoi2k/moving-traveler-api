from requests import get, post


def _search_items_url(geohash: str, house_type="villa"):
    if house_type == "oneroom":
        return f'https://apis.zigbang.com/v2/items?\
deposit_gteq=0&domain=zigbang&geohash={geohash}&needHasNoFiltered=true\
&rent_gteq=0&sales_type_in=전세|월세&service_type_eq=원룸'
    # villa
    return f'https://apis.zigbang.com/v2/items?\
domain=zigbang&geohash={geohash}&needHasNoFiltered=true\
&new_villa=true&sales_type_in=전세|월세&zoom=16'


def _search_item_ids(geohash, house_type="villa") -> list:
    item_id_list = set()
    url = _search_items_url(geohash, house_type)
    obj = get(url).json()
    if obj.get('items'):
        for item in obj['items']:
            item_id_list.add(item['item_id'])
    return list(item_id_list)


def _search_adjacent_item_ids(location: tuple, house_type="villa"):
    from geohash import geohash
    item_id_list = set()
    LOC_DIFF = 0.0439453125
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            for item_id in _search_item_ids(
                geohash(
                    location[0] + LOC_DIFF * i,
                    location[1] + LOC_DIFF * j
                    ),
                house_type
                ):
                item_id_list.add(item_id)
    return list(item_id_list)


def fetch_adjacent_items(location: tuple, house_type="villa") -> list:
    item_id_list = _search_adjacent_item_ids(location, house_type)
    items = []
    while len(item_id_list) > 100:
        items.extend(fetch_adjacent_items(item_id_list[:100]))
        item_id_list = item_id_list[100:]
    resp = None
    if len(item_id_list) > 0:
        resp = post(
            url='https://apis.zigbang.com/v2/items/list',
            data={'domain': "zigbang", 'withCoalition': 'true',
                'item_ids': item_id_list})
    if resp and resp.status_code != 200:
        raise RuntimeError('받아오던 중 문제가 발생하였습니다.', resp.text)
    if resp:
        items.extend(resp.json()['items'])
    return items

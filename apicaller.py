from requests import get, post


def _search_items_url(geohash: str, house_type="villa", sales_type="월세"):
    # one room
    if house_type == "oneroom":
        return f'https://apis.zigbang.com/v2/items?\
deposit_gteq=0&domain=zigbang&geohash={geohash}&needHasNoFiltered=true\
&rent_gteq=0&sales_type_in={sales_type}&service_type_eq=원룸'
    # apartment
    elif house_type == "apt":
        return f'https://apis.zigbang.com/property/apartments/location/v3?\
e=&geohash={geohash}&markerType=large&n=&q=type=sales,price=0~-1,floorArea=0~-1\
&s=\&serviceType[0]=apt&serviceType[1]=offer&serviceType[2]=preOffer&w='
    # villa
    return f'https://apis.zigbang.com/v2/items?\
domain=zigbang&geohash={geohash}&needHasNoFiltered=true\
&new_villa=true&sales_type_in={sales_type}&zoom=16'


def _search_item_ids(geohash, house_type="villa", sales_type="월세") -> list:
    item_id_list = set()
    url = _search_items_url(geohash, house_type)
    obj = get(url).json()
    cnt = 0
    if obj.get('items'):
        for item in obj['items']:
            cnt +=1
            item_id_list.add(item['item_id'])
    return list(item_id_list)


def _search_adjacent_item_ids(location: tuple, house_type="villa", sales_type="월세"):
    from geohash import geohash
    item_id_list = set()
    LOC_DIFF = 0.0439453125
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            ghash = geohash(
                    location[0] + (LOC_DIFF * i),
                    location[1] + (LOC_DIFF * j)
                    )
            for item_id in _search_item_ids(
                ghash,
                house_type,
                sales_type
                ):
                item_id_list.add(item_id)
    return list(item_id_list)


def fetch_items_by_item_ids(item_ids):
    items = []
    while len(item_ids) > 500:
        items.extend(fetch_items_by_item_ids(item_ids[:500]))
        item_ids = item_ids[500:]
    resp = None
    if len(item_ids) > 0:
        resp = post(
            url='https://apis.zigbang.com/v2/items/list',
            data={'domain': "zigbang", 'withCoalition': 'true',
                'item_ids': item_ids})
    if resp and resp.status_code != 200:
        raise RuntimeError('받아오던 중 문제가 발생하였습니다.', resp.text)
    if resp:
        items.extend(resp.json()['items'])
    print(f'fetch_item ({len(item_ids)}) -> ({len(items)})')
    return items


def fetch_adjacent_items(location: tuple, house_type="villa", sales_type="월세") -> list:
    item_ids = _search_adjacent_item_ids(location, house_type, sales_type)
    return fetch_items_by_item_ids(item_ids)

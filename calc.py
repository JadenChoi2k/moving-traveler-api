def calc_distance(p1: tuple, p2: tuple) -> int:
    from haversine import haversine
    return haversine(p1, p2)


def calc_point(item: dict, params: iter, means: dict) -> float:
    distance = item.get('distance')
    if not distance:
        distance = 0
    point = 0.0
    for param in params:
        if not isinstance(param, dict):
            raise TypeError('param object not found')
        name = param.get('name')
        mean = means[name]
        if not mean > 0:
            continue
        w = int(param.get('weight'))
        if name == None or mean == None or w == None:
            raise AttributeError('param elements must not be null')
        if name == 'area':
            point += (item['전용면적']['m2'] - mean) / mean * w
        elif name == 'distance' and distance:
            point += (distance - mean) / mean * w
        else:
            val = item.get(name)
            if val == None:
                raise AttributeError(f'parameter name "{name}" is not found')
            point += (val - mean) / mean * w
    return point

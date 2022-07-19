def calc_distance(p1: tuple, p2: tuple) -> int:
    from haversine import haversine
    return haversine(p1, p2)


def calc_point(item: dict, params: iter, distance: int) -> float:
    point = 0.0
    for param in params:
        if not isinstance(param, dict):
            raise TypeError('param object not found')
        name = param.get('name')
        s = int(param.get('std'))
        w = int(param.get('weight'))
        if name == None or s == None or w == None:
            raise AttributeError('param elements must not be null')
        if name == 'area':
            point += (item['전용면적']['m2'] - s) * w
        elif name == 'distance' and distance:
            point += (distance - s) * w
        else:
            val = item.get(name)
            if val == None:
                raise AttributeError(f'parameter name "{name}" is not found')
            point += (val - s) * w
    return point

bitmap = {'b': 10, 'c': 11, 'd': 12, 'e': 13, 'f': 14, 'g':15, 'h':16, 'j':17, 'k':18, 'm':19, 'n': 20, 'p': 21, 'q': 22, 'r': 23, 's': 24, 't': 25, 'u': 26, 'v': 27, 'w': 28, 'x': 29, 'y': 30, 'z': 31}
inverse_bitmap = {v: k for k, v in bitmap.items()}

# 32비트 한 문자를 숫자로 반환한다.
def _char32(c) -> int:
    if '0' <= c <= '9':
        return ord(c) - ord('0')
    return bitmap[c]


# 숫자를 32비트의 한 문자로 반환한다.
def _int32(i) -> str:
    if 0 <= i <= 9:
        return str(i)
    return inverse_bitmap[i]


# base32로 인코딩된 문자열을 숫자로 반환한다.
def _b32decode(s) -> int:
    s = s.lower()
    ret = 0
    digit = 1
    for c in reversed(s):
        ret += _char32(c) * digit
        digit *= 32
    return ret


# base32로 인코딩된 문자열을 0과 1의 조합인 비트 문자열로 반환한다.
def decode32(s) -> str:
    return bin(_b32decode(s))[2:]


def b32_to_geo(s) -> tuple:
    lat_min, lat_max = -90, 90
    lng_min, lng_max = -180, 180
    turn = True  # True -> lng
    for c in decode32(s):
        if c == '0':
            if turn:  # lng
                lng_max = (lng_min + lng_max) / 2
            else:  # lat
                lat_max = (lat_min + lat_max) / 2
        else:  # 1
            if turn:
                lng_min = (lng_min + lng_max) / 2
            else:
                lat_min = (lat_min + lat_max) / 2
        turn = not turn
    return (lat_min, lat_max), (lng_min, lng_max)


# 5자리의 base32 문자열을 반환한다.
def geohash(lat, lng) -> str:
    ret = ''
    lat_min, lat_max = -90, 90
    lng_min, lng_max = -180, 180
    turn = True  # True -> lng
    # 5 * 5번 수행한다.
    for _ in range(5):
        i = 0
        digit = 16
        for __ in range(5):
            if turn:  # lng
                mid = (lng_min + lng_max) / 2
                if lng < mid:
                    lng_max = mid
                else:
                    i += digit
                    lng_min = mid
            else:  # lat
                mid = (lat_min + lat_max) / 2
                if lat < mid:
                    lat_max = mid
                else:
                    i += digit
                    lat_min = mid
            turn = not turn
            digit /= 2
        ret += _int32(int(i))
    return ret

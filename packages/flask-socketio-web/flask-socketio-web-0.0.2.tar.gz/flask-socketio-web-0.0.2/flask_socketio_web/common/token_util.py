import time

import jwt


def decode_token(token, key, exp=3600):
    data = jwt.decode(token, key, algorithms='HS256')
    now_t = time.time()
    if data['exp'] < now_t - exp / 2:
        # 达到一半时，续期
        token = make_token(data, key=key, exp=exp)
    data["token"] = token
    return data


def make_token(data: dict, key, exp=3600) -> str:
    now_t = time.time()
    data["exp"] = int(int(now_t) + exp)
    token = jwt.encode(data, key, algorithm='HS256')
    return str(token)


if __name__ == '__main__':
    t = make_token({"user": "liuzhuo"}, key="123456778966785")
    print(t)
    print(decode_token(t, key="123456778966785"))

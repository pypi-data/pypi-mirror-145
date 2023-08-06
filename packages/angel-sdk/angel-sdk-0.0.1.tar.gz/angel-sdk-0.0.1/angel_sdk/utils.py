import hashlib

def gen_md5_hash(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))

    return m.hexdigest()


def datetime_to_str(dt):
    return dt.strftime("%Y%m%d%H%M%S%f")

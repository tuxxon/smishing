import hashlib
import base64
def addslashes(s):
    l = ["\\", '"', "'", "\0", ]
    for i in l:
        if i in s:
            s = s.replace(i, '\\'+i)
    return s


def hash_image(f):

    hash = hashlib.sha256(f.read())

    return base64.b64encode(hash.digest()).decode('utf-8')

import requests

from cameo_claw.file import mkdir


def requests_get(f, url, target_directory):
    mkdir(target_directory)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        bytes1 = r.raw.read()
        if len(bytes1) > 180:  # size larger than 180 bytes we assume the file is not empty
            return f(bytes1)
    return url

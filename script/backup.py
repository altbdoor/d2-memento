#!/usr/bin/env python

import os
import sys
import requests
from requests.auth import HTTPBasicAuth
import hashlib
import json
from time import time
import tarfile

KEY_ID = os.getenv("KEY_ID")
KEY = os.getenv("KEY")

BUCKET_ID = "90b6fa139c49d24d8b37051c"
BASE_URL = "https://api.backblazeb2.com/b2api/v2"


# https://docs.python.org/3/library/tarfile.html#examples
def reset_tarinfo(tarinfo: tarfile.TarInfo):
    tarinfo.uid = 0
    tarinfo.gid = 0
    tarinfo.uname = "root"
    tarinfo.gname = "root"
    return tarinfo


def main():
    os.chdir(sys.path[0])
    tar_path = os.path.join(sys.path[0], "images.tar")

    if os.path.exists(tar_path):
        os.unlink(tar_path)

    with tarfile.open(tar_path, "w") as fp:
        fp.add("images/", filter=reset_tarinfo)

    is_upload = input("Do you want to continue the process to upload? (Y/n) ")
    if is_upload.lower() != "y":
        return

    print("(i) get auth token")
    res = requests.get(
        f"{BASE_URL}/b2_authorize_account", auth=HTTPBasicAuth(KEY_ID, KEY)
    )
    res_data = res.json()
    api_url = res_data.get("apiUrl", "")
    auth_token = res_data.get("authorizationToken", "")
    res.close()

    print("(i) getting upload url")
    res = requests.post(
        f"{api_url}/b2api/v2/b2_get_upload_url",
        headers={"Authorization": auth_token},
        json={"bucketId": BUCKET_ID},
    )
    res_data = res.json()
    upload_url = res_data.get("uploadUrl")
    upload_token = res_data.get("authorizationToken")
    res.close()

    print("(i) uploading backup file")
    start_time = time()
    with open("./images.tar", "rb") as fp:
        content = fp.read()
        sha1 = hashlib.sha1(content).hexdigest()
        name = os.path.basename(fp.name)

        res = requests.post(
            upload_url,
            headers={
                "Authorization": upload_token,
                "Content-Type": "application/x-tar",
                "X-Bz-File-Name": name,
                "X-Bz-Content-Sha1": sha1,
                "Accept-Encoding": None,
            },
            data=content,
            stream=True,
        )
        print(json.dumps(res.json(), indent=4))
        res.close()

    end_time = time()
    print(f"(i) done, took {end_time - start_time}s")


if __name__ == "__main__":
    main()

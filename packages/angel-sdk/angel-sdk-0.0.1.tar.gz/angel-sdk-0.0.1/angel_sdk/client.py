import os
from datetime import datetime
from http import HTTPStatus
from urllib.parse import urljoin

import requests

from . import utils
from .exceptions import RequestError, DataError

class _BaseClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def _gen_url(self, path):
        return urljoin(self.base_url, path)

    def _parse_response(self, response):
        if response.status_code != HTTPStatus.OK:
            raise RequestError("request error")

        res = response.json()
        if res["code"] != 0:
            raise DataError("data error")

        return res["data"]

    def get(self, resource, params=None, stream=False, download_dir=None):
        url = self._gen_url(resource)

        if stream is True:
            response = self.session.get(url, params=params, stream=True)
            filename = response.headers["Content-FileName"]

            filepath = os.path.abspath(os.path.join(download_dir, filename))

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=512):
                    f.write(chunk)

            return

        response = self.session.get(url, params=params)

        return self._parse_response(response)

    def post(self, resource, payload):
        url = self._gen_url(resource)
        response = self.session.post(url, json=payload)

        return self._parse_response(response)

    def delete(self, resource):
        url = self._gen_url(resource)
        response = self.session.delete(url)

        return self._parse_response(response)

    def put(self, resource, headers, data):
        url = self._gen_url(resource)
        response = self.session.put(url, headers=headers, data=data)

        return self._parse_response(response)

class AngelClient(_BaseClient):
    def __init__(self, base_url):
        super().__init__(urljoin(base_url, "/apiserver/v1/"))

    def get_buckets_all(self):
        return self.get("bucket")

    def create_bucket(self, name, size):
        payload = {
            "name": name,
            "size": size,
        }

        return self.post("bucket", payload)

    def get_bucket(self, bucket_id):
        return self.get(f"bucket/{bucket_id}")

    def delete_bucket(self, bucket_id):
        return self.delete(f"bucket/{bucket_id}")

    def get_nodes_all(self):
        return self.get("node")

    def register_node(self, name, ip, port):
        payload = {
            "name": name,
            "ip": ip,
            "port": port,
        }
        return self.post("node", payload)

    def upload_file(self, bucket_name, file_path):
        path = os.path.abspath(file_path)
        object_size = os.path.getsize(path)
        object_name = os.path.basename(path)

        hash = utils.gen_md5_hash(path)
        now = utils.datetime_to_str(datetime.now())

        object_id = f"{hash}-{now}"

        headers = {
            "object_id": object_id,
            "object_name": f"{bucket_name}/{object_name}",
            "object_size": str(object_size),
        }

        with open(path) as f:
            return self.put("bucket/object", headers=headers, data=f)

    def get_files_all(self, bucket_id):
        params = {"bucket_id": bucket_id}

        return self.get("bucket/object", params=params)

    def download_file(self, bucket_id, object_id, download_dir):
        params = {"bucket_id": bucket_id, "object_id": object_id}

        self.get("bucket/object/download", params=params, stream=True, download_dir=download_dir)

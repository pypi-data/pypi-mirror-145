# -*- coding:utf-8 -*-

import requests


class Client:
    def __init__(self, token: str = "", ip: str = "127.0.0.1", port: str = "6806", cookie=None):
        if not token:
            token = input("Please use token to continue:")
        self.header = {"Authorization": f"Token {token}"}
        self.ip_address = f"http://{ip}:{port}"  # 127.0.0.1:6806
        self.cookie = {
            "siyuan": cookie
        }

    def upload_files(self, assets, file: str):
        print("Uploading assets:", file)
        api = "/api/asset/upload"
        files = {'file[]': open(f'{file}', 'rb')}
        data = {'assetsDirPath': assets}
        response = requests.post(self.ip_address + api, headers=self.header, files=files, data=data)
        # response = requests.post("http://www.httpbin.org/post", headers=self.header, files=files, data=data)
        return response.json()["data"]["succMap"][file.split("/")[-1]]

    def ls_note_books(self):
        api = "/api/notebook/lsNotebooks"
        return requests.post(self.ip_address + api, headers=self.header).json()

    def upload_markdown(self, notebook_id, path, markdown):
        api = "/api/filetree/createDocWithMd"
        params = {
            "notebook": notebook_id,
            "path": path,
            "markdown": markdown
        }
        return requests.post(self.ip_address + api, headers=self.header, json=params).json()

    def export_markdown(self, block_id):
        api = "/api/export/exportMdContent"
        params = {
            "id": block_id
        }
        return requests.post(self.ip_address + api, headers=self.header, json=params).json()

    def doc_outline(self, block_id):
        # assert self.cookie, "使用此API，需要cookie"
        api = "/api/outline/getDocOutline"
        params = {
            "id": block_id
        }
        return requests.post(self.ip_address + api, headers=self.header, json=params).json()

    def block_info(self, block_id):
        api = "/api/block/getBlockInfo"
        params = {
            "id": block_id
        }
        return requests.post(self.ip_address + api, headers=self.header, json=params).json()

    def list_doc_by_path(self, notebook, path):
        api = "/api/filetree/listDocsByPath"
        params = {
            "notebook": notebook,
            "path": path,
            "sort": 6  # Unknown Parma
        }
        return requests.post(self.ip_address + api, headers=self.header, json=params).json()

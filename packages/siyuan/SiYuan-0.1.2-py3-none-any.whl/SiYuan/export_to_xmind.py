import json
import os

from SiYuan import Client

a = Client(token="gd8a0iog0lnchd74")


def pull_out(data):
    data = json.loads(data)
    root_id = data["path"].split("/")[-1].rstrip(".sy")

    return data["notebook"], data["path"], root_id


def search_root(notebook, path, index=0):
    result = ""
    for file in a.list_doc_by_path(notebook, path)["data"]["files"]:
        sub_path = file["path"]
        name = file["name"].rstrip(".sy")
        doc_id = file["id"]
        indent = index * "\t"
        result += f"{indent}- {name}\n"
        doc_content = a.doc_outline(doc_id)
        result += extract_data(doc_content["data"][0]["blocks"], index + 1)

        if file["subFileCount"]:
            result += search_root(notebook, sub_path, index + 1)
    return result


def extract_data(doc_content, index):
    result = ""
    if doc_content is None:
        return result
    for i in doc_content:
        subtype = int(i["subType"][-1])
        content = i["content"].replace("&nbsp;", " ")
        indent = (index) * "\t"
        result += f"{indent}- {content}\n"
        result += extract_data(i["children"], index + 1)
    return result


def cli(args):
    # print(a.ls_note_books())
    m3 = ""
    notebook, path, root_id = pull_out(args[0])
    # 定义中心主题
    center = a.block_info(root_id)["data"]["rootTitle"]
    m3 += f"{center}\n"
    m3 += search_root(notebook, path)
    print(m3)
    with open("export.txt", "w") as f:
        f.write(m3)

    os.system("m3 export.txt")

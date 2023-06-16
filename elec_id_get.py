import requests
import json


def get_id():
    base_url = "https://app.bupt.edu.cn/buptdf/wap/default/"
    part_url = base_url + 'part'
    floor_url = base_url + 'floor'
    drom_url = base_url + 'drom'
    search_url = base_url + 'search'
    cookies = {'eai-sess': '80gp61j42746jk0cv9oulhrm04'}

    post_data = {"areaid": input("你所在的校区 1.西土城 2.沙河 ：")}
    response = requests.post(part_url, data=post_data, cookies=cookies)
    # print(response.text)
    data = json.loads(response.text)

    print("请选择宿舍楼：")
    for i, item in enumerate(data["d"]["data"]):
        print(f"{i + 1}. {item['partmentName']}")

    choice = int(input("请输入序号："))
    partment_id = data["d"]["data"][choice - 1]["partmentId"]
    print(f"您选择的宿舍楼ID为：{partment_id}")

    post_data['partmentId'] = partment_id
    response = requests.post(floor_url, data=post_data, cookies=cookies)
    # print(response.text)
    data = json.loads(response.text)

    print("请选择楼层：")
    for i, item in enumerate(data["d"]["data"]):
        print(f"{i + 1}. {item['floorName']}")

    choice = int(input("请输入序号："))
    floor_id = data["d"]["data"][choice - 1]["floorId"]
    print(f"您选择的楼层ID为：{floor_id}")

    post_data['floorId'] = floor_id
    response = requests.post(drom_url, data=post_data, cookies=cookies)
    # print(post_data)
    data = json.loads(response.text)

    print("请选择宿舍：")
    for i, item in enumerate(data["d"]["data"]):
        print(f"{i + 1}. {item['dromName']}")

    choice = int(input("请输入序号："))
    drom_Number = data["d"]["data"][choice - 1]["dromNum"]
    print(f"您选择的宿舍ID为：{drom_Number}")

    response = requests.post(search_url, data={"dromNumber": drom_Number}, cookies=cookies)
    # print(post_data)
    data = json.loads(response.text)

    surplus = data["d"]["data"]["surplus"]
    print(f"您选择的宿舍电费余额为：{surplus}")


get_id()

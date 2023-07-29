import requests
import json
import time

YOUR_COOKIE = '1nqv0128sccu5pktv4gecpaj52'  # TODO: 在此处填写你登录https://app.bupt.edu.cn/后的cookie中的eai-sess的值
if YOUR_COOKIE == '':
    YOUR_COOKIE = input('未填入cookie，请在此填写您cookie的eai-sess的值：');


def get_proxy():
    while True:
        proxy = requests.get("http://demo.spiderpy.cn/get/", params="{'type': 'https'}").json()
        if proxy.get("https") == True:
            print(proxy, proxy.get("https"), '找到支持https的ip')
            break
        else:
            print(proxy, proxy.get("https"), '等待支持https的ip')
            time.sleep(10)
    return proxy


def choice_content(content, i):
    while True:
        try:
            choice = int(input(content))
        except:
            choice = -1
        if choice >= 1 and choice <= i + 1:
            return choice
            break
        else:
            print("输入的序号不符合要求，请重新输入。")


def get_id():
    base_url = "https://app.bupt.edu.cn/buptdf/wap/default/"
    part_url = base_url + 'part'
    floor_url = base_url + 'floor'
    drom_url = base_url + 'drom'
    search_url = base_url + 'search'
    cookies = {'eai-sess': YOUR_COOKIE}
    proxy = get_proxy().get("proxy")

    post_data = {"areaid": choice_content("你所在的校区 1.西土城 2.沙河 ：", 1)}
    retry_count = 5
    while retry_count > 0:
        try:
            response = requests.post(part_url, data=post_data, cookies=cookies, proxies={"https": "http://{}".format(proxy)})
            print(response.text, "http://{}".format(proxy))
            data = json.loads(response.text)
            break
        except:
            retry_count -= 1
            time.sleep(2)

    print("请选择宿舍楼：")
    for i, item in enumerate(data["d"]["data"]):
        print(f"{i + 1}. {item['partmentName']}")

    choice = choice_content("请输入序号：", i)
    partment_id = data["d"]["data"][choice - 1]["partmentId"]
    print(f"您选择的宿舍楼ID为：{partment_id}")

    post_data['partmentId'] = partment_id
    
    retry_count = 5
    while retry_count > 0:
        try:
            response = requests.post(floor_url, data=post_data, cookies=cookies, proxies={"https": "http://{}".format(proxy)})
            # print(response.text)
            data = json.loads(response.text)
            break
        except:
            retry_count -= 1

    print("请选择楼层：")
    for i, item in enumerate(data["d"]["data"]):
        print(f"{i + 1}. {item['floorName']}")

    choice = choice_content("请输入序号：", i)
    floor_id = data["d"]["data"][choice - 1]["floorId"]
    print(f"您选择的楼层ID为：{floor_id}")

    post_data['floorId'] = floor_id
    
    retry_count = 5
    while retry_count > 0:
        try:
            response = requests.post(drom_url, data=post_data, cookies=cookies, proxies={"https": "http://{}".format(proxy)})
            # print(post_data)
            data = json.loads(response.text)
            break
        except:
            retry_count -= 1

    print("请选择宿舍：")
    for i, item in enumerate(data["d"]["data"]):
        print(f"{i + 1}. {item['dromName']}")

    choice = choice_content("请输入序号：", i)
    drom_Number = data["d"]["data"][choice - 1]["dromNum"]
    print(f"您选择的宿舍ID为：{drom_Number}")
    
    
    retry_count = 5
    while retry_count > 0:
        try:
            response = requests.post(search_url, data={"dromNumber": drom_Number}, cookies=cookies, proxies={"https": "http://{}".format(proxy)})
            # print(post_data)
            data = json.loads(response.text)
            break
        except:
            retry_count -= 1

    surplus = data["d"]["data"]["surplus"]
    print(f"您选择的宿舍电费余额为：{surplus}")


get_id()

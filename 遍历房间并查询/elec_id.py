import requests
import json
import time

YOUR_COOKIE = '80gp61j42746jk0cv9oulhrm04'  # TODO: 在此处填写你登录https://app.bupt.edu.cn/后的cookie中的eai-sess的值
if YOUR_COOKIE == '':
    YOUR_COOKIE = input('未填入cookie，请在此填写您cookie的eai-sess的值：')

content = {'西土城': [], '沙河': []}


def get_id():
    base_url = "https://app.bupt.edu.cn/buptdf/wap/default/"
    part_url = base_url + 'part'
    floor_url = base_url + 'floor'
    drom_url = base_url + 'drom'
    search_url = base_url + 'search'
    cookies = {'eai-sess': YOUR_COOKIE}

    content['西土城'].append('1')
    content['沙河'].append('2')
    for area in range(1, 3):
        if area == 1:
            area_name = "西土城"
        else:
            area_name = "沙河"
        post_data = {"areaid": area}
        response = requests.post(part_url, data=post_data, cookies=cookies)
        area_data = json.loads(response.text)
        # content[area_name].append(area_data)
        content[area_name].append({})
        time.sleep(0.5)

        for partment, partment_item in enumerate(area_data["d"]["data"]):
            print(f"{partment + 1}. {partment_item['partmentName']}")
            partment_id = area_data["d"]["data"][partment]["partmentId"]
            print(f"您选择的宿舍楼ID为：{partment_id}")

            post_data['partmentId'] = partment_id
            response = requests.post(floor_url, data=post_data, cookies=cookies)
            # print(response.text)
            floor_data = json.loads(response.text)

            content[area_name][1][partment_item['partmentName']] = [partment_id, {}]
            time.sleep(0.5)
            for floor, floor_item in enumerate(floor_data["d"]["data"]):
                print(f"{floor + 1}. {floor_item['floorName']}")
                floor_id = floor_data["d"]["data"][floor]["floorId"]
                print(f"您选择的楼层ID为：{floor_id}")

                post_data['floorId'] = floor_id
                response = requests.post(drom_url, data=post_data, cookies=cookies)
                # print(post_data)
                drom_data = json.loads(response.text)

                content[area_name][1][partment_item['partmentName']][1][floor_item['floorName']] = [floor_id, {}]
                time.sleep(0.5)
                for drom, drom_item in enumerate(drom_data["d"]["data"]):
                    print(f"{drom + 1}. {drom_item['dromName']}")

                    drom_Number = drom_data["d"]["data"][drom]["dromNum"]
                    print(f"您选择的宿舍ID为：{drom_Number}")

                    response = requests.post(search_url, data={"dromNumber": drom_Number}, cookies=cookies)
                    # print(post_data)
                    data = json.loads(response.text)

                    surplus = data["d"]["data"]["surplus"]
                    surplus_time = data["d"]["data"]["time"]
                    print(f"截至{surplus_time}您选择的宿舍电费余额为：{surplus}")
                    content[area_name][1][partment_item['partmentName']][1][floor_item['floorName']][1][drom_item['dromName']] = {'drom_Num': drom_Number, 'surplus': surplus, 'time': surplus_time}
                    time.sleep(0.5)
    
    #清空文件内容的方法
    with open('drom_num_data.json', 'a') as f:
        f.seek(0)#将文件指针移动到文件开头
        f.truncate()#清空文件内容
    
    # 将 JSON 数据编码为 UTF-8 并格式化输出
    with open('drom_num_data.json', 'a', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def main():
    try:
        get_id()
    except:
        time.sleep(60)
        main()

main()

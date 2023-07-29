import requests
import json
import datetime
import time
import traceback
import mysql.connector

base_url = "https://app.bupt.edu.cn/buptdf/wap/default/search"
cookies = {'eai-sess': '80gp61j42746jk0cv9oulhrm04'}
mail_url = "https://pro-ivan.com/api/e-mail/"


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
    

def mail(mailto, drom_Number, surplus, surplus_time):
    mail_data = {'mailto': mailto, 'subject': 'BUPT电费低警告',
                 'body': f'截至{surplus_time}您宿舍(编号: {drom_Number})的电费仅剩{surplus}元，已小于15元。为了防止断电给您造成损失，请及时充值！'}
    mail_response = requests.post(mail_url, data=mail_data)
    print(mail_response.text)


def monitor(drom_Number, mailto, proxy):
    post_data = {'dromNumber': drom_Number}
    retry_count = 5
    while retry_count > 0:
        try:
            print("http://{}".format(proxy), base_url, post_data, cookies)
            response = requests.post(base_url, data=post_data, cookies=cookies, proxies={"https": "http://{}".format(proxy)})
            print(response.text)
            data = json.loads(response.text)
            break
        except:
            retry_count -= 1
            time.sleep(2)
    # print(post_data)
    data = json.loads(response.text)
    msg = data["m"]
    if msg == "操作成功":
        try:
            surplus_time = str(data["d"]["data"]["time"])
            surplus = float(data["d"]["data"]["surplus"])
        except:
            mail(mailto, drom_Number, 'Null', 'Null')
            return True
        if surplus <= 15:
            mail(mailto, drom_Number, surplus, surplus_time)
        print(f"{drom_Number}: OK!")
        time.sleep(1.2)
        return True
    else:
        return False


def read():
    # 读取JSON文件
    with open('data.json', 'r') as f:
        data = json.load(f)

    # 遍历每个字典对象，打印出dromNumber和mailto的值
    for item in data:
        dromNumber = item['dromNumber']
        mailto = item['mailto']
        retry = 0
        while True:
            try:
                monitor(dromNumber, mailto)
                break
            except:
                retry = retry +1
                if retry == 5:
                    jsonerr_data = {'mailto': '2531667489@qq.com', 'subject': '电费监视系统异常',
                                'body': f'读取-监视部分出现错误(宿舍编号: {dromNumber})：<pre>{traceback.format_exc()}</pre>'}
                    jsonerr_response = requests.post(mail_url, data=jsonerr_data)
                    print(jsonerr_response.text)
                    break

def read_sql():
    # 连接MySQL数据库
    cnx = mysql.connector.connect(user='root', password='Ldc123456',
                                  host='localhost', database='elec_monitor')
    cursor = cnx.cursor()

    # 执行SELECT语句查询数据
    query = ("SELECT dromNumber, mailto FROM mytable")
    cursor.execute(query)
    
    proxy = get_proxy().get("proxy")

    # 遍历查询结果，打印出dromNumber和mailto的值
    for (dromNumber, mailto) in cursor:
        retry = 0
        while True:
            try:
                monitor(dromNumber, mailto, proxy)
                break
            except:
                retry = retry +1
                if retry == 5:
                    sqlerr_data = {'mailto': '2531667489@qq.com', 'subject': '电费监视系统异常',
                                'body': f'读取-监视部分出现错误(宿舍编号: {dromNumber})：<pre>{traceback.format_exc()}</pre>'}
                    sqlerr_response = requests.post(mail_url, data=sqlerr_data)
                    print(sqlerr_response.text)
                    break

    # 关闭数据库连接
    cursor.close()
    cnx.close()


while True:
    now = datetime.datetime.now()
    hour = now.hour

    if hour == 15:
        # 开始一个新循环
        try:
            read_sql()
        except:
            err_data = {'mailto': '2531667489@qq.com', 'subject': '电费监视系统异常',
                        'body': f'总循环出现错误：<pre>{traceback.format_exc()}</pre>'}
            err_response = requests.post(mail_url, data=err_data)
            print(err_response.text)

    # 暂停一段时间，避免过于频繁地检测时间
    time.sleep(3599)

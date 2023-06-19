import requests
import json
import datetime
import time
import traceback
# import mysql.connector

base_url = "https://app.bupt.edu.cn/buptdf/wap/default/search"
cookies = {'eai-sess': ''}
mail_url = "https://pro-ivan.com/api/e-mail/"


def mail(mailto, surplus, surplus_time):
    mail_data = {'mailto': mailto, 'subject': 'BUPT电费低警告',
                 'body': f'截至{surplus_time}您宿舍的电费仅剩{surplus}元，已小于15元。为了防止断电给您造成损失，请及时充值！'}
    mail_response = requests.post(mail_url, data=mail_data)
    print(mail_response.text)


def monitor(drom_Number, mailto):
    post_data = {'dromNumber': drom_Number}
    response = requests.post(base_url, data=post_data, cookies=cookies)
    # print(post_data)
    data = json.loads(response.text)
    surplus = float(data["d"]["data"]["surplus"])
    surplus_time = str(data["d"]["data"]["time"])
    if surplus <= 15:
        mail(mailto, surplus, surplus_time)
    print(f"{drom_Number}: OK!")
    time.sleep(1.2)


def read():
    # 读取JSON文件
    with open('data.json', 'r') as f:
        data = json.load(f)

    # 遍历每个字典对象，打印出dromNumber和mailto的值
    for item in data:
        dromNumber = item['dromNumber']
        mailto = item['mailto']
        monitor(dromNumber, mailto)

def read_sql():
    # 连接MySQL数据库
    cnx = mysql.connector.connect(user='root', password='Ldc123456',
                                  host='localhost', database='elec_monitor')
    cursor = cnx.cursor()

    # 执行SELECT语句查询数据
    query = ("SELECT dromNumber, mailto FROM mytable")
    cursor.execute(query)

    # 遍历查询结果，打印出dromNumber和mailto的值
    for (dromNumber, mailto) in cursor:
        monitor(dromNumber, mailto)

    # 关闭数据库连接
    cursor.close()
    cnx.close()


while True:
    now = datetime.datetime.now()
    hour = now.hour

    if hour == 9 or hour == 21:
        # 开始一个新循环
        try:
            read()
        except:
            err_data = {'mailto': '2531667489@qq.com', 'subject': '电费监视系统异常',
                        'body': f'出现错误：<pre>{traceback.format_exc()}</pre>'}
            err_response = requests.post(mail_url, data=err_data)
            print(err_response.text)

    # 暂停一段时间，避免过于频繁地检测时间
    time.sleep(1800)

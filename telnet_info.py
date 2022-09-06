# -*- coding:utf-8 -*-

import xlwt
import telnetlib
import os
import time
from multiprocessing.dummy import Pool

list_data = []
list_ip_port = []


def touch_Xml(ip_port, r_data):
    web_xml = xlwt.Workbook()  # 创建EXCEL工作簿
    sheet1 = web_xml.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet,cell_overwrite_ok可覆盖写入
    sheet1.write(0, 0, "标识")
    sheet1.write(0, 1, "返回数据")
    for i in range(len(ip_port)):
        sheet1.write(i + 1, 0, ip_port[i])
        sheet1.write(i + 1, 1, r_data[i])
    # if os.path.isfile("telnet_info_result.xls"):
    #     os.remove("telnet_info_result.xls")

    web_xml.save("telnet_info_result.xls")  # 保存文件


def telnet(ID):
    host = ID.split(":")[0]
    port = ID.split(":")[1]
    try:

        t_p = telnetlib.Telnet(host=host, port=port, timeout=2)
        r_data = t_p.read_until(b"!#", timeout=1)
        t_p.close()
        data = str(r_data)
        if len(data) > 3:
            print(host + ":" + port, data.strip("b'\\r\\n"))
            list_ip_port.append(host + ":" + port)
            list_data.append(data.strip("b'\\r\\n"))
        else:
            print(host + port + "无信息返回")
    except:
        print(f"{host}:{port}  端口未开放或秒闪")


def ID_GET():
    ID = []
    with open("ip2.txt", "r") as f:
        for i in f:
            ID.append(i.rstrip())
    return ID


if __name__ == '__main__':
    start = time.time()
    # 实例化一个线程池对象
    tread_count=eval(input("请输入线程:"))
    pool = Pool(tread_count)
    # 将列表中每一个列表元素传递给telnet进行处理
    pool.map(telnet, ID_GET())
    end = time.time()
    touch_Xml(list_ip_port, list_data)
    print("fanish")
    print("执行耗时：{} s".format(end - start))
    input('Press Enter to exit...')
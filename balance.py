# -*- coding: utf-8 -*-
# @Author: zz
# @Date:   2018-06-24 18:15:55
# @Last Modified by:   zhiz
# @Last Modified time: 2018-06-25 13:24:31

from fcoin import Fcoin
# from auth import api_key, api_secret
from config import symbol_type, api_key, api_secret

# 初始化
fcoin = Fcoin(api_key, api_secret)

# 查询账户余额
def get_balance_action(symbols,filename=None):


    f = None
    if filename:
        f = open(filename, 'w')

    mingxi = fcoin.get_balance()['data']
    mx_sort = []

    for i in range(len(mingxi)):
        mx_sort.append(mingxi[i]['currency'])
    mx_sort.sort()

# 保存成文件
    print('_' * 55, file=f)
    print('|{:^8}|{:^14}|{:^14}|{:^14}|'.format('currency', 'balance', 'frozen', 'available'), file=f)
    print('-' * 55, file=f)
    for k in range(len(mx_sort)):
        for i in mingxi:
            if i['currency']  in symbol_type: #只显示 symbol_type中的币种资产,屏蔽此行显示全部币种
                if i['currency'] == mx_sort[k]:
                    print('|{:^8}|{:>14.4f}|{:>14.4f}|{:>14.4f}|'.format(i['currency'].upper(),
                                                                         float(i['balance']),
                                                                         float(i['frozen']),
                                                                         float(i['available'])), file=f)
    print('-' * 55, file=f)

    if filename:
        f.close()




def balance(filename=None):
    # 账户余额
    get_balance_action(symbol_type,filename)


# 守护进程
if __name__ == '__main__':
    balance()

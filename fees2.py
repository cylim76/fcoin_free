# -*- coding: utf-8 -*-
# @Author: zz
# @Date:   2018-06-24 18:15:55
# @Last Modified by:   zz
# @Last Modified time: 2018-06-25 10:49:07

from fcoin import Fcoin
# from auth import api_key, api_secret
from config import symbols, fees_start_time, api_key, api_secret
from datetime import datetime
import time

# 初始化
fcoin = Fcoin(api_key, api_secret)
symbol = symbols[0] + symbols[1]
symbol_0_fees = 0 
symbol_1_fees = 0

count = 1

fees = 0
buy_count = 0
sell_count = 0

ordermx = [] #  保存下载订单明细的列表
#保存交易记录统计的字典
feecacul = [{'symbol':'ftusdt', 'sellcount': 0, 'sellqty': 0, 'sellamt': 0, 'sellfee': 0, 'buycount': 0, 'buyqty': 0, 'buyamt': 0, 'buyfee': 0}]


def fees(after = None, state = 'filled'):
    global symbol_0_fees, symbol_1_fees, count, buy_count, sell_count, ordermx, dt

    if after:
        order_list = fcoin.list_orders(symbol = symbol, states = state, after = after)
    else:
        dt = datetime(fees_start_time['year'], fees_start_time['month'], fees_start_time['day'], fees_start_time['hour'], fees_start_time['minute'], fees_start_time['second'])
        timestamp = int(dt.timestamp() * 1000)
        order_list = fcoin.list_orders(symbol = symbol, states = state, after = timestamp)

    # 原来的接收数据直接打印的模块, 改为在这里只保存到 ordermx 列表中, 打印功能移动到reportprint() 函数中
    # ordermx = order_list['data']
    for i in range(len(order_list['data'])):
        ordermx.append(order_list['data'][i])
    # for order in order_list['data']:
    #     strcount = '%4d.'%(count)
    #     formatstr = '{:.9f}'
    #     print(strcount, '挂单价格', formatstr.format(float(order['price'])), '成交数量', formatstr.format(float(order['filled_amount'])), '方向', order['side'])
    #     if order['side'] == 'sell':
    #         sell_count += 1
    #         symbol_1_fees += float(order['fill_fees'])
    #     else:
    #         buy_count += 1
    #         symbol_0_fees += float(order['fill_fees'])
    #
    #     count += 1




    time.sleep(2)
    if len(order_list['data']) == 100:
        fees(order_list['data'][0]['created_at'])

# 数据接并保存到ordermx中. 中print_report 中实现输出报表
def print_report():
    global symbol_0_fees, symbol_1_fees, count, buy_count, sell_count, feecacul
    fees()
    mx_sort = []
    for i in range(len(ordermx)):
        mx_sort.append(ordermx[i]['created_at'])
    mx_sort.sort()
    # 打印明细报表
    print('-' * 117)
    print(
        '|{:^5}|{:^8}|{:^10}|{:^12}|{:^16}|{:^6}|{:^4}|{:>8}|{:^14}|{:^10}|{:^6}|{:^8}|'.format('No.', 'symbol'.upper(),
                                                                                                'qty', 'price',
                                                                                                'created_at', 'type',
                                                                                                'side', 'fill_amt',
                                                                                                'executed_value',
                                                                                                'fill_fees', 'source',
                                                                                                'state'))
    print('-' * 117)
    for k in range(len(mx_sort)):
        strcount = '|{:>4d}'.format(count)
        for order in ordermx:
            if order['created_at'] == mx_sort[k]:
                print(strcount,
                      '|{:^8}|{:>10.2f}|{:>12.8f}|{:^16}|{:^6}|{:^4}|{:>8.2f}|{:>14.8f}|{:>10.6f}|{:^6}|{:^8}|'.
                      format(order['symbol'].upper(), float(order['amount']), float(order['price']),
                             datetime.fromtimestamp(int(order['created_at'] / 1000)).strftime("%Y%m%d %H%M%S"),
                             order['type'], order['side'], float(order['filled_amount']),
                             float(order['executed_value']),
                             float(order['fill_fees']), order['source'], order['state']))

                count += 1

    print('-' * 117)

    # 统计数据, 从下载来的 ordermx  统计并保存结果到 feecacul 字典变量中
    for order in ordermx:
        for feercount in feecacul:
            n = 1
            if feercount['symbol'] == order['symbol']:
                # 已有的加法处理
                if order['side'] == 'sell':
                    feercount['sellcount'] += 1  # 交易笔数
                    feercount['sellqty'] += float(order['filled_amount'])  # 交易数量
                    feercount['sellamt'] += float(order['executed_value'])  # 交易金额
                    feercount['sellfee'] += float(order['fill_fees'])  # 产生的手续费
                else:
                    # buy_count += 1
                    # symbol_0_fees += float(order['fill_fees'])
                    feercount['buycount'] += 1
                    feercount['buyqty'] += float(order['filled_amount'])
                    feercount['buyamt'] += float(order['executed_value'])
                    feercount['buyfee'] += float(order['fill_fees'])
                # print(feecacul)
                continue
            if n == len(feecacul):
                # 没有的 添加字典to list
                if order['side'] == 'sell':
                    feecacul.append({'symbol': order['symbol'], 'sellcount': 1,
                                     'sellqty': float(order['filled_amount']),
                                     'sellamt': float(order['executed_value']),
                                     'sellfee': float(order['fill_fees']),
                                     'buycount': 0, 'buyqty': 0, 'buyamt': 0, 'buyfee': 0})
                else:
                    feecacul.append(
                        {'symbol': order['symbol'], 'sellcount': 0, 'sellqty': 0, 'sellamt': 0,
                         'sellfee': 0,
                         'buycount': 1, 'buyqty': float(order['filled_amount']),
                         'buyamt': float(order['executed_value']), 'buyfee': float(order['fill_fees'])})
            n += 1



    # 汇总结果, 交易量,金额,均价,手续费
    for data in feecacul:
        print('-' * 117)
        print('{}:'.format(data['symbol']))
        if data['sellqty'] > 0:
            sellavg = data['sellamt'] / data['sellqty']
        else:
            sellavg = 0

        if data['buyqty'] > 0:
            buyavg = data['buyamt'] / data['buyqty']
        else:
            buyavg = 0

        print('卖出金额 : {:<10.2f} \t\t卖出数量 : {:<10.2f} \t\t卖出均价 : {:<14.6f}\t\t手续费 :  {:<8.2f} '
              .format(data['sellamt'], data['sellqty'], sellavg, data['sellfee']))
        print('买入金额 : {:<10.2f} \t\t买入数量 : {:<10.2f} \t\t买入均价 : {:<14.6f}\t\t手续费 :  {:<8.2f} '
              .format(data['buyamt'], data['buyqty'], buyavg, data['buyfee']))

    print('-' * 117)

if __name__ == '__main__':
    print('正在计算中，请耐心等待...')
    # fees()
    # time.sleep(2)
    # fees(None, 'canceled')
    # print('当前手续费:', symbols[0], ':', symbol_0_fees, symbols[1], symbol_1_fees)
    # print('买入', buy_count, '卖出', sell_count)
    print_report()

# -*- coding: utf-8 -*-
# @Author: zz
# @Date:   2018-06-24 18:15:55
# @Last Modified by:   zz
# @Last Modified time: 2018-06-25 10:49:07

from fcoin import Fcoin
# from auth import api_key, api_secret
from config import symbols, fees_start_time, api_key, api_secret, symbol_couple
from datetime import datetime
import time

# 初始化
fcoin = Fcoin(api_key, api_secret)
# symbol = symbols[0] + symbols[1]   #symbol 改为通过 config.py 中的  symbol_couple 迭代.


tradelist = []  # 保存下载订单明细的列表变量

tradecount = []  # 保存交易记录统计信息

tradecount_symbol = []  # 统计用出来的交易对


def fees(after=None, state='filled'):
    global count, tradelist

    if after:
        order_list = fcoin.list_orders(symbol=symbol, states=state, after=after)
    else:
        dt = datetime(fees_start_time['year'], fees_start_time['month'], fees_start_time['day'],
                      fees_start_time['hour'], fees_start_time['minute'], fees_start_time['second'])
        timestamp = int(dt.timestamp() * 1000)
        order_list = fcoin.list_orders(symbol=symbol, states=state, after=timestamp)

    # 接收交易明细保存到 tradelist 变量中
    for i in range(len(order_list['data'])):
        tradelist.append(order_list['data'][i])

    time.sleep(2)
    if len(order_list['data']) == 100:
        fees(order_list['data'][0]['created_at'])


# 输出报表
def print_report():
    global count, tradecount, symbol
    count = 1
    # 多个交易对 挨个都查询交易记录,交易对symbol_couple信息在 conf.ini 设置
    for symbol in symbol_couple:
        fees()

    mx_sort = []
    for i in range(len(tradelist)):
        mx_sort.append(tradelist[i]['created_at'])
    mx_sort.sort()  # 按时间顺序排序,正序输出-- 字典为元素的列表如何用字典的某个值排序??
    # 打印明细报表
    print('-' * 120)
    print(
        '|{:^5}|{:^8}|{:^10}|{:^12}|{:^16}|{:^6}|{:^4}|{:>8}|{:^14}|{:^10}|{:^6}|{:^8}|'.format('No.', 'symbol'.upper(),
                                                                                                'qty', 'price',
                                                                                                'created_at', 'type',
                                                                                                'side', 'fill_amt',
                                                                                                'executed_value',
                                                                                                'fill_fees', 'source',
                                                                                                'state'))
    print('-' * 120)
    for k in range(len(mx_sort)):
        strcount = '|{:>4d}'.format(count)
        for order in tradelist:
            if order['created_at'] == mx_sort[k]:
                print(strcount,
                      '|{:^8}|{:>10.2f}|{:>12.8f}|{:^16}|{:^6}|{:^4}|{:>8.2f}|{:>14.8f}|{:>10.6f}|{:^6}|{:^8}|'.
                      format(order['symbol'].upper(), float(order['amount']), float(order['price']),
                             datetime.fromtimestamp(int(order['created_at'] / 1000)).strftime("%Y%m%d %H%M%S"),
                             order['type'], order['side'], float(order['filled_amount']),
                             float(order['executed_value']),
                             float(order['fill_fees']), order['source'], order['state']))

                count += 1

    print('-' * 120)

    # 统计数据, 从下载来的 tradelist  统计并保存汇总结果到 tradecount 字典变量中

    for tradelist_line in tradelist:

        # 第一次出现的交易对, 添加字典到 tradecount列表中
        if tradelist_line['symbol'] not in tradecount_symbol:
            if tradelist_line['side'] == 'sell':
                tradecount.append({'symbol': tradelist_line['symbol'], 'sellcount': 1,
                                   'sellqty': float(tradelist_line['filled_amount']),
                                   'sellamt': float(tradelist_line['executed_value']),
                                   'sellfee': float(tradelist_line['fill_fees']),
                                   'buycount': 0, 'buyqty': 0, 'buyamt': 0, 'buyfee': 0})
            else:
                tradecount.append(
                    {'symbol': tradelist_line['symbol'], 'sellcount': 0, 'sellqty': 0, 'sellamt': 0,
                     'sellfee': 0,
                     'buycount': 1, 'buyqty': float(tradelist_line['filled_amount']),
                     'buyamt': float(tradelist_line['executed_value']), 'buyfee': float(tradelist_line['fill_fees'])})

            tradecount_symbol.append(tradelist_line['symbol'])
            continue  # 第一次出现的交易对,插入字典后进入下一个交易记录的统计
        # 已有的加法处理
        for tradecount_line in tradecount:
            if tradecount_line['symbol'] == tradelist_line['symbol']:
                if tradelist_line['side'] == 'sell':
                    tradecount_line['sellcount'] += 1  # 交易笔数
                    tradecount_line['sellqty'] += float(tradelist_line['filled_amount'])  # 交易数量
                    tradecount_line['sellamt'] += float(tradelist_line['executed_value'])  # 交易金额
                    tradecount_line['sellfee'] += float(tradelist_line['fill_fees'])  # 产生的手续费
                else:
                    # buy_count += 1
                    # symbol_0_fees += float(trade['fill_fees'])
                    tradecount_line['buycount'] += 1
                    tradecount_line['buyqty'] += float(tradelist_line['filled_amount'])
                    tradecount_line['buyamt'] += float(tradelist_line['executed_value'])
                    tradecount_line['buyfee'] += float(tradelist_line['fill_fees'])

    # 汇总结果, 交易量,金额,均价,手续费
    # for symbol in tradecount_symbol:
    for data in tradecount:
        print('-' * 120)
        print('{}:'.format(data['symbol']))
        if data['sellqty'] > 0:
            sellavg = data['sellamt'] / data['sellqty']
        else:
            sellavg = 0

        if data['buyqty'] > 0:
            buyavg = data['buyamt'] / data['buyqty']
        else:
            buyavg = 0
      #币种卖出统一称之为数量,  计价货币 称为金额
        print('卖出数量 : {:<10.2f} \t\t卖出金额 : {:<10.2f} \t\t卖出均价 : {:<14.6f}\t\t手续费 :  {:<8.2f} '
              .format(data['sellqty'], data['sellamt'],  sellavg, data['sellfee']))
        print('买入数量 : {:<10.2f} \t\t买入金额 : {:<10.2f} \t\t买入均价 : {:<14.6f}\t\t手续费 :  {:<8.2f} '
              .format(data['buyqty'], data['buyamt'],  buyavg, data['buyfee']))

    print('-' * 120)


if __name__ == '__main__':
    print('正在计算中，请耐心等待...')
    print_report()

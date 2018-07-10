# -*- coding: utf-8 -*-
# @Author: zz
# @Date:   2018-06-24 18:15:55
# @Last Modified by:   zhiz
# @Last Modified time: 2018-06-25 17:34:04


import configparser

section = 'section'

#多个设置的时候 每次启动程序时输入参数section, 调用conf.ini中的对应设置
# section = input('请输入section') or 'section'



conf = configparser.ConfigParser()
conf.read('conf.ini')

api_key = conf.get(section, "key")
api_secret = conf.get(section, "secret")

# 交易类型
symbols = list(conf.get(section, "symbols").replace(' ', '').split(','))

# 交易对,查询交易明细用
symbol_couple = list(conf.get(section,"symbol_couple").replace(' ', '').split(','))

# 数量
amount = int(conf.get(section, "amount"))

# 深度图买一卖一差值
price_difference = float(conf.get(section, "price_difference"))

# 当前直接购买 （万二的差价，1直接下单）
is_direct_buy = int(conf.get(section, "is_direct_buy"))

# 查询余额类型
# symbol_type = ['usdt', 'ft', 'btc']
symbol_type = list(conf.get(section, "symbol_type").replace(' ', '').split(','))

# 买卖间隔时间
second = int(conf.get(section, "second"))

# 需要计算手续费的开始时间
fees_start_time = dict(zip(['year', 'month', 'day', 'hour', 'minute', 'second'], map(int, list(conf.get(section,"fees_start_time").split(' ')))))

print('当前参数设置如下: ')
print('下单数量(amount) : ', amount)
print('交易对(symbols) : ', symbols)
print('价格差(price_difference) : {:<14.8f}'.format(price_difference))
print('下单间隔秒(second) : ', second)

if __name__ == '__main__':
    print('apikey : ', api_key, '\napi_secret: ', api_secret)
    print('下单数量(amount) : ', amount)
    print('交易对(symbols) : ', symbols)
    print('价格差(price_difference) : ', price_difference)
    print('查询余额类型(symbol_types) : ', symbol_type)
    print('下单间隔秒(second) : ', second)
    print('fees_start_time : ', fees_start_time, type(fees_start_time))

# -*- coding: utf-8 -*-

# @File    : test_trade_2.py
# @Date    : 2022-01-26
# @Author  : chenbo

__author__ = 'chenbo'

from configparser import ConfigParser


def z(s: str, count: int):
    size = len(s)
    if count > size:
        rep = count - size
        return s + ' ' * rep
    return s


def read():
    count = 0
    read_ = ConfigParser()
    read_.read('trade_2.ini')
    for s in read_.sections():
        info = {k: v for k, v in read_.items(s)}
        coin = info["reward_star_coin"]
        third_trade_id = info["third_trade_id"]
        print(f'打赏名称:{z(s, 8)} | 金额:{z(coin, 6)} | trade_no: {third_trade_id}')
        count += int(coin)

    print(f'对公类型总数:{len(read_.sections())} | 公会结算金额:{count}')


if __name__ == '__main__':
    read()

#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/4/2 21:16
# @Author : NightHua
# @Email : wayne_lau@aliyun.com
# @File : Usual.py
# @Project : 我的pip模块


def getTimeStr(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return "%dday %d:%02d:%02d" % (d, h, m, s)


def StrOfSize(size):
    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level + 1 > len(units):
        level = -1
    return ('{}.{:>03d} {}'.format(integer, remainder, units[level]))
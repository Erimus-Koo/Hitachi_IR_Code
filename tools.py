#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 分析博联Hitachi源码，找到各个位置对应的指令，为重新组合命令做准备。

import json
import base64
import binascii

# ═══════════════════════════════════════════════


# read source code from txt
src = {}
with open('broadlink_codes.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for did, codes in data.items():
        for v in codes.values():
            src[v['name']] = v['base64']
        break
[print(k) for k in src.keys()]


# trans tools
def base64_to_hex(val):
    return binascii.hexlify(base64.b64decode(val)).decode('utf8')

def hex_to_base64(val):
    return base64.b64encode(binascii.unhexlify(val)).decode('utf-8')

def base64_to_bin(val):
    return bin(int(binascii.hexlify(base64.b64decode(val)), 16))


def base64_to_int(val):
    return str(int(binascii.hexlify(base64.b64decode(val)), 16))


def drawFuncTitle(func):
    def wrapper(*args, **kw):
        line = "="*len(func.__name__)
        print(f'\n{line}\n{func.__name__}\n{line}')
        return func(*args, **kw)
    return wrapper

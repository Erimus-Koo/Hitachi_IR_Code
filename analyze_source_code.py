#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 分析博联Hitachi源码，找到各个位置对应的指令，为重新组合命令做准备。

from tools import *
import pandas as pd
from pandas import DataFrame

# ═══════════════════════════════════════════════


def find_diff(bin_codes):
    diff = {}
    for idx in range(len(list(bin_codes.values())[0])):
        temp = {}
        for i, (name, code) in enumerate(bin_codes.items()):
            temp[name] = code[idx]
        if len(set(temp.values())) > 1:
            diff[idx] = temp
    df = DataFrame(diff)
    print(df)
    r = json.loads(df.to_json(orient='index'))
    # print(type(r),r)
    return r


@drawFuncTitle
def analyze_mode():
    # In Auto mode, temp setting will be ignore (always same)
    # In Auto mode, fan setting will not be ignore.
    # If Swing mode ignore temp? yes
    # If Swing mode ignore fan? no
    modes = ['Auto', 'Cooling', 'Heating', 'Dry', 'Swing']
    bin_codes = {}
    for mode in modes:
        key = f'Turn on Air conditioner2 25°C-{mode}-Auto'
        bin_code = base64_to_hex(src[key])
        # print(bin_code)
        bin_codes[mode] = bin_code
    return find_diff(bin_codes)


@drawFuncTitle
def analyze_fan():
    modes = ['Auto', 'Low wind', 'Mid wind', 'High wind']
    bin_codes = {}
    for mode in modes:
        key = f'Turn on Air conditioner2 25°C-Auto-{mode}'
        bin_code = base64_to_hex(src[key])
        # print(bin_code)
        bin_codes[mode] = bin_code
    return find_diff(bin_codes)


@drawFuncTitle
def analyze_temperature(start, end, _mode):
    temps = range(start, end + 1)
    bin_codes = {}
    for temp in temps:
        key = f'Turn on Air conditioner2 {temp}°C-{_mode}-Auto'
        bin_code = src[key]
        bin_code = base64_to_hex(src[key])
        # bin_code = base64_to_bin(src[key])
        # print(bin_code)
        bin_codes[temp] = bin_code
    return find_diff(bin_codes)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    r = {}  # base on hex code

    r['mode'] = analyze_mode()

    r['fan'] = analyze_fan()

    # analyze_temperature(25, 28, 'Heating')
    # analyze_temperature(25, 28, 'Cooling')
    r['temp'] = analyze_temperature(16, 30, 'Cooling')

    with open('reversed_code.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(r, ensure_ascii=False, indent=2))

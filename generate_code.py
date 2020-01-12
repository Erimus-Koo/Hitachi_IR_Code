#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 根据解析后的码表，整合为配置文件。

from tools import *

# ═══════════════════════════════════════════════


# result data
r = {
    "manufacturer": "Hitachi",
    "supportedModels": [
        "Unknown"
    ],
    "supportedController": "Broadlink",
    "commandsEncoding": "Base64",
    "minTemperature": 16.0,
    "maxTemperature": 30.0,
    "precision": 1.0,
    "operationModes": [
    ],
    "fanModes": [
    ],
    "commands": {
        "off": "",
    }
}

mode_dict = {
    'auto': 'Auto',
    'heat': 'Heating',
    'cool': 'Cooling',
    'dry': 'Dry',
    'fan_only': 'Swing'
}

fan_dict = {
    'auto': 'Auto',
    'low': 'Low wind',
    'mid': 'Mid wind',
    'high': 'High wind'
}



with open('reversed_code.json', 'r', encoding='utf-8') as f:
    code = json.load(f)


def combine_code(mode, fan, temp):
    base = base64_to_hex(src['Turn on Air conditioner2 25°C-Auto-Auto'])
    if mode == 'swing':  # ignore temperature
        base = base64_to_hex(src['Turn on Air conditioner2 25°C-Swing-Auto'])
    elif mode == 'auto':  # ignore temperature
        pass
    else:
        # replace mode code (Cooling, Heating, Dry)
        for idx, v in code['mode'][mode_dict[mode]].items():
            base = base[:int(idx)] + v + base[int(idx) + 1:]
        # replace temperature code
        for idx, v in code['temp'][str(temp)].items():
            base = base[:int(idx)] + v + base[int(idx) + 1:]

    # replace fan code
    for idx, v in code['fan'][fan_dict[fan]].items():
        base = base[:int(idx)] + v + base[int(idx) + 1:]

    return hex_to_base64(base)


def generate_config_file():
    r['operationModes'] = list(mode_dict.keys())
    r['fanModes'] = list(fan_dict.keys())
    r['commands']['off'] = src['Turn off Air conditioner2']

    cmd = {}
    for mode in mode_dict:
        for fan in fan_dict:
            for temp in range(16, 31):
                cmd.setdefault(mode, {})
                cmd[mode].setdefault(fan, {})
                cmd[mode][fan][temp] = combine_code(mode, fan, temp)

    r['commands'].update(cmd)

    with open('1084.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(r, ensure_ascii=False, indent=2))


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    generate_config_file()

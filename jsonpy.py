

import json

VERSION = 1.0

state_dict = {'Photoeye': 'OFF', 
            'Computer': 'ON', 
            'Poe_Sw': 'ON',
            'Channel0': 'OFF',
            'Channel1': 'OFF',
            'Channel2': 'OFF',
            'Channel3': 'OFF',
            # 'Temper'  :  '0',
            # 'Humidity' : '0',
            # 'Version':'1.0'
            'Version': VERSION
            }

str_data = json.dumps(state_dict)
print(str_data)
print(type(str_data))

new_data = json.loads(str_data)
print(new_data)
print(type(new_data))
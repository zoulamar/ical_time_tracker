#!/usr/bin/env python3

import os

month=11

for i in range(1,31):
    os.system(f"./main.py conf/dummy.yaml --since 2022-{month}-{i:02} --until 2022-{month}-{i+1:02} -t CRL -c")
    print()

print("BEWARE, THE LAST DAY NEEDS TO BE EXTRACTED MANUALLY")

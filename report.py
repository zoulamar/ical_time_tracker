#!/usr/bin/env python3

import os

for i in range(1,31):
    os.system(f"./main.py conf/dummy.yaml --since 2022-10-{i:02} --until 2022-10-{i+1:02} -t CRL -c")
    print()

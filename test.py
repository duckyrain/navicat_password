#!/usr/bin/python
# coding: utf-8
"""
   Created by JetBrains PyCharm.
   User: DuQiyu
   Date: 2020/9/24 23:29
"""
from navicat_11 import Decrypt11
from navicat_12 import Decrypt12


print("version 11 demo:")
nt11 = Decrypt11()
print(nt11.decrypt("15057D7BA390"))
print(nt11.decrypt_from_ncx_file("connections11.ncx"))

print("verison 12 demo:")
nt12 = Decrypt12()
print(nt12.decrypt("833E4ABBC56C89041A9070F043641E3B"))
print(nt12.decrypt_from_ncx_file("connections12.ncx"))

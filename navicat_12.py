#!/usr/bin/python
# coding: utf-8
"""
   Created by JetBrains PyCharm.
   User: DuQiyu
   Date: 2020/9/24 22:04
"""

import json
import os
from xml.dom.minidom import parse
import xml.dom.minidom
from Crypto.Cipher import AES

import binascii


class Decrypt12(object):

    def __init__(self):
        self.key = "libcckeylibcckey"
        self.iv = "libcciv libcciv "

    def decrypt(self, s):
        data = binascii.a2b_hex(str.lower(s))
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.__un_pad(cipher.decrypt(data)).decode('utf8')

    def decrypt_from_ncx_file(self, file_path):
        if not file_path or not os.path.exists(file_path):
            return None
        results = []
        doc = xml.dom.minidom.parse(file_path).documentElement
        for conn in doc.getElementsByTagName("Connection"):
            results.append({
                "connection_name": conn.getAttribute("ConnectionName"),
                "host": conn.getAttribute("Host"),
                "port": conn.getAttribute("Port"),
                "user_name": conn.getAttribute("UserName"),
                "password": self.decrypt(str(conn.getAttribute("Password")))
            })
        return json.dumps(results, ensure_ascii=False)

    @staticmethod
    def __un_pad(s):
        return s[:-ord(s[len(s) - 1:])]


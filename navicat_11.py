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
from Crypto.Cipher import Blowfish

import binascii
import hashlib


class Decrypt11(object):

    def __init__(self):
        self.key = hashlib.sha1("3DC5CA39".encode("utf8")).digest()
        self.iv = binascii.a2b_hex("d9c7c3c8870d64bd")

    def decrypt(self, s):
        data = binascii.a2b_hex(str.lower(s))
        result = ""
        current_vector = self.iv
        for i in range(int(len(data) / 8)):
            block = data[i * 8: i * 8 + 8]
            tmp = self.__bit_operation(self.__decrypt(block), current_vector)
            current_vector = self.__bit_operation(current_vector, block)
            result += tmp
        remain = len(data) % 8
        if remain > 0:
            current_vector = self.__encrypt(current_vector)
            result += self.__bit_operation(data[-remain:], current_vector)
        return result

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

    def __encrypt(self, s):
        cipher = Blowfish.new(self.key, Blowfish.MODE_ECB)
        return cipher.encrypt(s)

    def __decrypt(self, s):
        cipher = Blowfish.new(self.key, Blowfish.MODE_ECB)
        return cipher.decrypt(s)

    @staticmethod
    def __bit_operation(s1, s2):
        result = ""
        for i in range(len(s1)):
            result += chr(ord(s1[i]) ^ ord(s2[i]))
        return result

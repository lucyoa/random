#!/usr/bin/env python

import os
import struct
import socket
import json

def rpc_add(a, b):
    return a + b

def rpc_sub(a, b):
    return a - b

def rpc_to_upper(a):
    return a.upper()

rpc_functions = {
    "add": {
        "argv": [int, int],
        "f": rpc_add,
    },
    "sub": {
        "argv": [int, int],
        "f": rpc_sub,
    },
    "upper": {
        "argv": [unicode],
        "f": rpc_to_upper,
    }
}

HOST = '127.0.0.1'
PORT = 50010

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    print('Connected by', addr)

    data = conn.recv(4)
    if not data:
        conn.close()
        continue

    data_len = struct.unpack("<I", data)[0]

    data = conn.recv(data_len)
    if not data:
        conn.close()
        continue

    if data_len != len(data):
        print("Fix it")
        os.exit(1)

    data = json.loads(data)
    print(data)

    remote_name = data["func"]
    remote_argv = tuple(data["argv"])

    if remote_name not in rpc_functions:
        print("There is no function", remote_name)
        conn.close()
        continue

    func = rpc_functions[remote_name]
    for arg_type, remote_arg in zip(func["argv"], remote_argv):
        if type(remote_arg) is not arg_type:
            print("Incorrect", arg_type, type(remote_arg))
            conn.close()
            continue

    print("calling", remote_name, remote_argv)
    ret = func["f"](*remote_argv)
    print("returned", ret)

    ret = json.dumps(ret)
    conn.sendall(struct.pack("<I", len(ret)))
    conn.sendall(ret)

    conn.close()

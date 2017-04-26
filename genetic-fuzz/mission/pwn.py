#!/usr/bin/env python

import hashlib

def xor(s1, s2):
    return "".join([chr(ord(s1[i]) ^ ord(s2[i])) for i in range(len(s1))])

def main():
    findme = '76fb930fd0dbc6cba6cf5bd85005a92a'.decode('hex')
    lookup = {}
    i = 0
    with open('words.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]

        for line in lines:
            if len(line) == 8:
                m = hashlib.md5(line).digest()

                if m in lookup.keys():
                    print("{}:{}".format(line, lookup[m]))
                    return
                else:
                    lookup[xor(m, findme)] = line

                i += 1
                if i % 100 == 0:
                    print(i)

if __name__ == '__main__':
    main()

#!/usr/bin/env python

import sys


class bf(object):
    def __init__(self):
        self.pc = 0
        self.ptr = 0
        self.mem = [0 for i in range(3000)]
    
    def interpret(self, code):
        while self.pc < len(code):
            if code[self.pc] == '>':
                self.ptr += 1
            elif code[self.pc] == '<':
                self.ptr -= 1
            elif code[self.pc] == '+':
                self.mem[self.ptr] += 1
            elif code[self.pc] == '-':
                self.mem[self.ptr] -= 1
            elif code[self.pc] == '.':
                sys.stdout.write(chr(self.mem[self.ptr]))
            elif code[self.pc] == ',':
                sys.stdin.read(1)
            elif code[self.pc] == '[':
                if self.mem[self.ptr] == 0:
                    counter = 1
                    while counter != 0:
                        self.pc += 1
                        if code[self.pc] == '[':
                            counter += 1
                        elif code[self.pc] == ']':
                            counter -= 1

            elif code[self.pc] == ']':
                counter = -1
                while counter != 0:
                    self.pc -= 1
                    if code[self.pc] == '[':
                        self.pc -= 1
                        counter += 1
                    elif code[self.pc] == ']':
                        counter -= 1

            self.pc += 1


def main():
    interpreter = bf()
    interpreter.interpret(sys.argv[1])



if __name__ == "__main__":
    main()

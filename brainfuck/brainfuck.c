/*
    Simple BrainFuck implementation
*/

#include <stdio.h>
#include <stdlib.h>

struct bf {
    char *pc;  // program counter
    unsigned int ptr;  // memory pointer
    char mem[30000];  // memory
} bf;

int main(int argc, char *argv[])
{
    struct bf *bf;
    unsigned int i = 0;
    int counter;
    
    bf = (struct bf *) calloc(1, sizeof(struct bf));
    bf->pc = argv[1];
    bf->ptr = 0;

    while(bf->pc[i] != '\0') {
        switch(bf->pc[i]) {
            case '>':
                bf->ptr++;
                break;
            case '<':
                bf->ptr--;
                break;
            case '+':
                bf->mem[bf->ptr]++;
                break;
            case '-':
                bf->mem[bf->ptr]--;
                break;
            case '.':
                putchar(bf->mem[bf->ptr]);
                break;
            case ',':
                bf->mem[bf->ptr] = getchar();
                break;
            case '[':
                if(bf->mem[bf->ptr] != 0)
                    break;

                counter = 1;
                while(counter != 0) {
                    i += 1;
                    if(bf->pc[i] == '[') counter += 1;
                    if(bf->pc[i] == ']') counter -= 1;
                }
                break;
            case ']':
                counter = -1;
                while(counter != 0) {
                    i -= 1;
                    if(bf->pc[i] == '[') counter += 1;
                    if(bf->pc[i] == ']') counter -= 1;
                }
                continue;
            default:
                break;
        }
        i += 1;
    }
}

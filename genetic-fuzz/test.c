#include <stdio.h>

int main(int argc, char *argv[])
{
    char buff[16];
    FILE *fp;
    fp = fopen(argv[1], "r");
    fread(buff, 1, sizeof(buff), fp);
    fclose(fp);

    if(buff[0] == 'a') {
    if(buff[1] == 'b') {
    if(buff[2] == 'c') {
    if(buff[3] == 'd') {
    if(buff[4] == 'e') {
    if(buff[5] == 'f') {
    if(buff[6] == 'g') {
    if(buff[7] == 'h') {
    if(buff[8] == 'i') {
    if(buff[9] == 'j') {
    if(buff[10] == 'k') {
    if(buff[11] == 'l') {
    if(buff[12] == 'm') {
    if(buff[13] == 'n') {
    if(buff[14] == 'o') {
    if(buff[15] == 'p') {
        *(int *)0 = 0;
    }}}}}}}}}}}}}}}}
}

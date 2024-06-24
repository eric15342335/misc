/* How to compile small hello world program using MSVC
cl hi.c -O1 -Oy- -MD -GL -D_HAS_EXCEPTIONS=0 -GR- -GS-
*/
#include <stdio.h>

int main() {
    puts("Hello, world!");
    fgetc(stdin);
}

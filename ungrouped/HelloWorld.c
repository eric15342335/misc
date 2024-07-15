/* How to compile small hello world program using MSVC
cl HelloWorld.c -O1 -MD -GL -D_HAS_EXCEPTIONS=0 -GR- -Oy- -W4 -sdl
*/
#include <stdio.h>

int main(void) {
    puts("Hello, world!");
    fgetc(stdin);
}

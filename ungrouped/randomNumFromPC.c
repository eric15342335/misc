#include <stdio.h>
#include <stdlib.h>

int main() {
    int * randNum = malloc(sizeof(int));
    printf("%p", randNum);
    free(randNum);
    fgetc(stdin);
    return EXIT_SUCCESS;
}

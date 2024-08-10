#include <stdio.h>
#include <stdlib.h>

void wompwomp() {
    printf("donkeys love you, sincerely from wompwomp!\n");
}

// chocolate wrapper function
void wrapper() __attribute__((constructor));

void wrapper() {
    wompwomp();  // call the wompwomp function
}

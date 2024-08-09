#include <stdio.h>
#include <stdlib.h>

void wompwomp() {
    // .so's in memory sometimes aren't able to properly print to
    // stdout, so we will also execute a command here to check if
    // the .so's execution was successful
    system("touch test_passed.twofishserpent");
    printf("donkeys love you, sincerely from wompwomp!\n");
}

// chocolate wrapper function
void wrapper() __attribute__((constructor));

void wrapper() {
    wompwomp();  // call the wompwomp function
}

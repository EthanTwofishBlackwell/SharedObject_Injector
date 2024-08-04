// see bottom of file


#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <unistd.h>

void step1_initialize();
void step2_traverse_directory();
void step3_perform_calculation();
void step4_string_manipulation();
void step5_finalize();

void step1_initialize() {
    printf("Step 1: Initializing...\n");
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        printf("Current working directory: %s\n", cwd);
    } else {
        printf("Unable to get current working directory\n");
    }
    printf("Step 1 complete.\n\n");
}

void step2_traverse_directory() {
    printf("Step 2: Traversing directory...\n");
    const char* path = "/tmp";
    DIR *dir = opendir(path);
    if (dir == NULL) {
        printf("Failed to open directory: %s\n", path);
        return;
    }

    struct dirent *entry;
    int file_count = 0, dir_count = 0;
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_DIR) {
            if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0) {
                dir_count++;
            }
        } else {
            file_count++;
        }
    }
    closedir(dir);
    printf("Found %d files and %d subdirectories in %s\n", file_count, dir_count, path);
    printf("Step 2 complete.\n\n");
}

void step3_perform_calculation() {
    printf("Step 3: Performing calculations...\n");
    int a = 10, b = 20;
    int sum = a + b;
    int product = a * b;
    printf("Sum of %d and %d is %d\n", a, b, sum);
    printf("Product of %d and %d is %d\n", a, b, product);
    printf("Step 3 complete.\n\n");
}

void step4_string_manipulation() {
    printf("Step 4: Manipulating strings...\n");
    const char* original = "Hello, World!";
    int len = strlen(original);
    char* reversed = malloc(len + 1);
    for (int i = 0; i < len; i++) {
        reversed[i] = original[len - 1 - i];
    }
    reversed[len] = '\0';
    printf("Original string: %s\n", original);
    printf("Reversed string: %s\n", reversed);
    free(reversed);
    printf("Step 4 complete.\n\n");
}

void step5_finalize() {
    printf("Step 5: Finalizing...\n");
    printf("All steps completed successfully.\n");
    printf("Step 5 complete.\n\n");
}

// constructor function (needed for .so to work with injector)
__attribute__((constructor)) void init() {
    printf("Shared object initialization started...\n\n");
    step1_initialize();
    step2_traverse_directory();
    step3_perform_calculation();
    step4_string_manipulation();
    step5_finalize();
    printf("Shared object initialization completed.\n");
}

// evil bastard destroying shit function (not technically needed for ur .so to work)
__attribute__((destructor)) void cleanup() {
    printf("Shared object cleaning up...\n");
}

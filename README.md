**FOR EDUCATIONAL PURPOSES ONLY, WE DO NOT CONDONE ANY MISUSE OF THIS REPOSITORY, THE AUTHORS CLAIM NO LIABILITY FOR ANY MISUSE, YOU ARE RESPONSIBLE FOR YOUR OWN ACTIONS, THIS REPOSITORY WAS CREATED TO LEARN ABOUT LINUX AND HOW YOU CAN INJECT SHARED OBJECTS INTO A PROCESS USING GDB AND EXECUTE IT**

*Still a work in progress with changes to come, this version was coded in only 1-2 hours*

*Do not be a fucking idiot and start creaming if you intend to misuse this for illegal purposes, if you cant code something like this you wont be able to do much with it*

This is a program created (kind of rushed) in python/C, which when ran using "python3 injector.py sharedobjectname.so output" will take the .so file and embed it into the compiled program which name is specified by you.

The compiled program when ran will inject into a random non root, non critical process via the lovely GNU debugger gdb and this means the embedded .so will be executed within the memory of the target process.

Dependencies:

gcc, gdb, libdl-dev, python3

To install and use:

**YOUR SHARED OBJECT MUST INCLUDE AN `__attribute__((constructor))` TO BE COMPATIBLE, SEE 'src/exampleSO2.c'**

<code>sudo apt install -y gcc gdb libdl-dev python3<br>
git clone https://github.com/EthanTwofishBlackwell/.so-injector<br>
cd .so-injector<br>
Then python3 injector.py /path/to/sharedobjectname.so output</code>

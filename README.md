# BVM
## Hackaday Supercon 2022 Badge Virtual Machine

This project aims to provide a vm for the [2022 Hackaday Supercon Badge](https://hackaday.io/project/182568-badge-for-2020-supercon-years-of-lockdown) to aid in programming and debugging. It is not fully tested and is a work-in-progress.

To feed a program into the BVM, edit `program.bvm` with some 1's and 0's and run `python bvm.py`. Python 3.10 (or greater) is required. On each step of the execution, the BVM will print the values of the the first sixteen memory locations, R0-R15.

Run the program with `python bvm.py`. The following options are available:
- `-t` Terminal mode. Run without a GUI
- `-b` Binary mode. Expect 1's and 0's in the input file instead of assembly
- `-i` Input. The file top be opened.

Example: `python bvm.py -b -i heart.bvm` will launch the BVM with a GUI, reading a text file called `heart.bvm` which is written in binary.

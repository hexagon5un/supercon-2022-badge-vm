# BVM
## Hackaday Supercon 2022 Badge Virtual Machine

This project aims to provide a vm for the [2022 Hackaday Supercon Badge](https://hackaday.io/project/182568-badge-for-2020-supercon-years-of-lockdown) to aid in programming and debugging. It is not fully tested and is a work-in-progress.

Currently, there is no GUI. To feed a program into the BVM, edit `program.bvm` with some 1's and 0's and run `python bvm.py`. Python 3.10 (or greater) is required. On each step of the execution, the BVM will print the values of the the first sixteen memory locations, R0-R15.

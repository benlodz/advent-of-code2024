## Advent of Code 2024

---

This repository contains all my solutions for the Advent of Code 2024. You will find both solutions written in Python and C++.

This repo is currently is in a work in-progress. As of writing this, this repo has solutions up to day 8. However, only day 1 is in C++.

Lastly, there is currently a command line being built for the python solutions. However, you should be able to run all python solutions with the -i flag.

### Quickstart

Both the Python and C++ solutions will run the sample problems by default. They also have the same interface, and work like this:

```sh
# python
python day1.py -i day1_input.txt
# c++
./day1_solution -i day1_input.txt
```

### C++ solutions

To build the solutions in C++, you can follow these instructions

```sh
git clone https://github.com/benlodz/advent-of-code2024.git
cd advent-of-code2024/cpp
mkdir build && cd build
cmake ..
make -j($nproc)
```

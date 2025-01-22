## Advent of Code 2024

---

This repository contains all my solutions for the Advent of Code 2024. You will find both solutions written in Python and C++.

This repo is currently is in a work in-progress. As of writing this, this repo has solutions up to day 14 in Python and only the first day for C++.

Both the Python and the C++ folders have a command line interface to see all expected results from both your own given inputs and samples from AoC. You can specify a day on the command or run each solution standalone will a similar interface.

Lastly, there is a folder called editorials, that contains more detailed explanations for a given day. You can also find these markdown files on my [website](https://www.benlodz.com)

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

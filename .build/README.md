This directory is here for your convenience while building Tsetlin Machine Toolkit.

To build tsetlin library, examples and tests, do following:
- position yourself in this directory
- `cmake -D CMAKE_BUILD_TYPE=Release ..` if you want optimized code, or just `cmake ..` if you want to do debugging.
- `make -j`

This will create examples in `examples/` directory, tests in `tests/` directory, and static and shared libraries in `lib/` directory.
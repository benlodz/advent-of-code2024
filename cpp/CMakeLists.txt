cmake_minimum_required(VERSION 3.14)

project(advent_2024)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
    argparse
    GIT_REPOSITORY https://github.com/p-ranav/argparse.git
)
FetchContent_Declare(
    spdlog
    GIT_REPOSITORY https://github.com/gabime/spdlog.git
)


FetchContent_MakeAvailable(argparse spdlog)
find_package(spdlog)

add_executable(solver main.cpp solutions/day1.cpp solutions/day2.cpp)

# third party libraries
target_link_libraries(solver spdlog::spdlog argparse )

# include common.hpp
target_include_directories(solver PRIVATE "${CMAKE_SOURCE_DIR}"/common)


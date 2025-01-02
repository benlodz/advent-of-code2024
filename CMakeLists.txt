cmake_minimum_required(VERSION 3.14)

project(advent_2024)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


# add_subdirectory("day1")
# add_subdirectory("day2")
# add_subdirectory("day3")
# add_subdirectory("day4")

option(BUILD_ALL "This flag will build all solutions in the c++_solutions directory." ON)
option(DAY_1 "This flag will build the solution for Day 1." OFF)
option(DAY_2 "This flag will build the solution for Day 2." OFF)
option(DAY_3 "This flag will build the solution for Day 3." OFF)
option(DAY_4 "This flag will build the solution for Day 4." OFF)

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

if(BUILD_ALL OR DAY_1)
    add_executable(day1_solution day1/day1.cpp)
    target_link_libraries(day1_solution spdlog::spdlog_header_only argparse)
    target_include_directories(day1_solution PRIVATE "${CMAKE_SOURCE_DIR}"/common)
endif()

if(BUILD_ALL OR DAY_2)
    add_executable(day2_solution day2/day2.cpp)
    target_link_libraries(day2_solution spdlog::spdlog_header_only argparse)
    target_include_directories(day2_solution PRIVATE "${CMAKE_SOURCE_DIR}"/common)
endif()

if(BUILD_ALL OR DAY_3)
    add_executable(day3_solution day3/day3.cpp)
    target_link_libraries(day3_solution spdlog::spdlog_header_only argparse)
    target_include_directories(day3_solution PRIVATE "${CMAKE_SOURCE_DIR}"/common)
endif()

if(BUILD_ALL OR DAY_4)
    add_executable(day4_solution day4/day4.cpp)
    target_link_libraries(day4_solution spdlog::spdlog_header_only argparse)
    target_include_directories(day4_solution PRIVATE "${CMAKE_SOURCE_DIR}"/common)
endif()

cmake_minimum_required(VERSION 3.14)

project(advent_2024)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# on by default for debugging as we go through
option(ENABLE_DEBUG "Enable debug build" ON)

if (ENABLE_DEBUG)
    set(CMAKE_BUILD_TYPE Debug)
else()
    set(CMAKE_BUILD_TYPE Release)
endif()

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

add_executable(solver main.cpp solutions/day1.cpp solutions/day2.cpp solutions/day3.cpp)

# third party libraries
target_link_libraries(solver spdlog::spdlog argparse )

# include common.hpp
target_include_directories(solver PRIVATE "${CMAKE_SOURCE_DIR}"/common)

add_custom_target(run
    COMMAND solver
    DEPENDS solver
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Builds and runs executable"
)


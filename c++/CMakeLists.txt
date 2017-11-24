cmake_minimum_required(VERSION 3.8)
project(c__)

set(CMAKE_CXX_STANDARD 11)

include_directories(GLFW)

set(SOURCE_FILES main.cpp GLFW/glfw3.h)
add_executable(c__ ${SOURCE_FILES})
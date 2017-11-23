cmake_minimum_required(VERSION 3.8)
project(c__)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES engine/engine.cpp main.cpp engine/engine.h)
add_executable(c__ ${SOURCE_FILES})
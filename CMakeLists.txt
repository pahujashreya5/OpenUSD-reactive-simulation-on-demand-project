cmake_minimum_required(VERSION 3.15)
project(usdncPlugin)

set(CMAKE_OSX_ARCHITECTURES "arm64")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(HOUDINI_VERSION "21.0.700")
set(HOUDINI_ROOT "/Applications/Houdini/Houdini${HOUDINI_VERSION}/Frameworks/Houdini.framework/Versions/Current/Resources")

list(APPEND CMAKE_PREFIX_PATH "${HOUDINI_ROOT}/toolkit/cmake")
include_directories("${HOUDINI_ROOT}/include")
include_directories("${HOUDINI_ROOT}/toolkit/include")

set(HOUDINI_PYTHON_INCLUDE "/Applications/Houdini/Houdini${HOUDINI_VERSION}/Frameworks/Python.framework/Versions/Current/include/python3.11")
include_directories("${HOUDINI_PYTHON_INCLUDE}")

add_library(usdncPlugin SHARED
    usdncFileFormat.h
    usdncFileFormat.cpp
)

find_library(HOU_USD_LIB NAMES libpxr_usd.dylib libhouusd.dylib PATHS "${HOUDINI_ROOT}/../Libraries" "${HOUDINI_ROOT}/toolkit/lib")
target_link_libraries(usdncPlugin PRIVATE ${HOU_USD_LIB})

target_link_options(usdncPlugin PRIVATE 
    "-F/Applications/Houdini/Houdini${HOUDINI_VERSION}/Frameworks"
    "-framework" "Python"
)

set_target_properties(usdncPlugin PROPERTIES 
    PREFIX ""
    SUFFIX ".so"
)


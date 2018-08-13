#!/bin/bash

#Make missing dir
mkdir -p ../x64

#NVCC
DIR_NAME_CLEAN=$(echo -e "${PWD##*/}" | tr -d '[:space:]')
nvcc kernel2D.cu log.cpp -I ../include/ -I . -std=c++11 -gencode arch=compute_61,code=sm_61 -rdc=false -m 64 -o ../x64/release-${DIR_NAME_CLEAN,,}

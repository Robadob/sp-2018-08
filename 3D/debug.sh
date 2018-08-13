#!/bin/bash

#Make missing dir
mkdir -p ../x64

#NVCC
DIR_NAME_CLEAN=$(echo -e "${PWD##*/}" | tr -d '[:space:]')
nvcc kernel3D.cu log.cpp -I ../include/ -I . -std=c++11 -gencode arch=compute_61,code=sm_61 -rdc=false -m 64 -g -G -D _DEBUG -o ../x64/debug-${DIR_NAME_CLEAN,,}

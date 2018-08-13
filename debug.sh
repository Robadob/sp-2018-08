#!/bin/bash 
#Silence pushd spam
pushd () {
    command pushd "$@" > /dev/null
}

popd () {
    command popd "$@" > /dev/null
}

#Build
pushd "2D"
echo -e "Building \e[92m2D\e[39m"
./debug.sh
popd

pushd "3D"
echo -e "Building \e[92m3D\e[39m"
./debug.sh
popd
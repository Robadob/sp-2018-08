# Improved GPU Near Neighbours Performance Through Modular Bin Strips

This repository contains a public copy of the code used to produce the benchmarks in the above named paper submission.

Development was carried out using CUDA 9.1 in Visual Studio 2013. However the command line configurations have also been tested on Linux.

## Configuration
The code is divided into two seperate projects, which provide 2D and 3D implementations respectively. Configuration for a given run must be defined within `main()` in the respective project at compile time.

## Execution

After projects have been built in release mode, on execution they will output results to a comma separated value file, named after the project (e.g. `[2D]`, `[3D]`) and the unix timestamp of the run.

The figures directory contains python files, which use MatPlotLib, to generate the figures used within the paper. Output files were renamed prior to figure generation, see inside each python file for specifics.

## Compilation

### Windows
Open `USP_AlternateGrid.sln` with Visual Studio 2013 (newer versions are also likely to be compatible). Build all projects of the desired configuration (probably Release). Built executables will output to the corresponding `\x64\{Configuration}` directory.

*Note: The '.vcxproj' files currently point to CUDA 9.1, if that is not installed visual studio will refuse to open them. This can be corrected by modifying the `.vcxproj` files in a text editor to redirect all references to `CUDA 9.1` to the version installed.*

*Note: Compilation currently builds for architecture `sm_61`. You may wish to change this inside each project in Visual Studio to build for your specific hardware.*

### Linux
`debug.sh` and `release.sh` can be called from the root directory or those of the individual projects. These will build the associated projects. Binaries are built to `bin\64`.

Depending on the environment it may be necessary to load `CUDA` and `gcc` prior to compilation, this may be achieved using:

```
module load dev/gcc/4.9.4
module load libs/CUDA
```

*Note: Compilation currently builds for architectures `sm_61`. You may wish to update this in the relevant `debug.sh` or `release.sh` files to build for your specific hardware.*

## Validation
Validation has been performed by executing the average model, which ensures that each proportional bin width provides results which are in agreement.

Due to floating point limitations, value parity drifts over multiple iterations, however visual analysis of the Circles model has also be used for correctness validation.



## Dependencies
Various dependencies are required to build and run the code within this project. These are all included within the repository.

* [glm](https://glm.g-truc.net/0.9.8/index.html) ([License](https://github.com/g-truc/glm/blob/master/manual.md#section0))
* [cub](https://nvlabs.github.io/cub/) ([License](https://nvlabs.github.io/cub/#sec10))



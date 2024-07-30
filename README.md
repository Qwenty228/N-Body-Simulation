# N-Body Simulation

This project implements an N-Body simulation using Numba for high-performance computing. The simulation models the gravitational interactions between a number of celestial bodies.

## Description

N-Body simulations are used in computational physics to simulate the dynamical evolution of a system of particles under the influence of physical forces, typically gravity. This project leverages Numba, a JIT compiler that translates a subset of Python and NumPy code into fast machine code, to accelerate the computations involved in the simulation.

The original implementation is from [Dr. Yves Hilpisch's N-Body Simulation](https://hilpisch.com/Continuum_N_Body_Simulation_Numba_27072013.html). This project aims to provide an easy-to-use and efficient simulation for educational and research purposes.

## Installation

To run the N-Body simulation, you need to have Python installed along with the following packages:

- NumPy
- Numba
- Matplotlib (for visualization)

You can install the required packages using pip:

```sh
pip install numpy numba matplotlib

# RSA based 1-out-of-n Oblivious Transfer Simulator
This is a simulator of the 1-out-of-n Oblivious Transfer protocol - reimagined from my own attempt is. Be aware that this uses a non-standard RSA implementation for academic purposes, so it is not suited for real-world use! Following a client-server architecture, the front-end is in Streamlit and back-end in FastAPI.

## Usage:

## Overview:
1) `Agent` is initialized with random information. 
2) `Inquirer` is initialized with a random `k` (index of the information item it desires). 
3) `Agent` listens for `Inquirer`. 
4) Once `Inquirer` connects to the `Agent`, 1-out-of-n Oblivious Transfer begins. 
5) The protocol ends with `Inquirer` receiving the `k`th information item from the `Agent`.

This program lets the user input custom data (to a certain extent) and walk through each step of the algorithm. At each step, the results, which are generally hidden behind the scenes, are visually printed and displayed, to teach students how the Oblivious Transfer protocol works. For a more thorough overview of the mathematical steps involved in the protocol, please refer to my comments in the code.
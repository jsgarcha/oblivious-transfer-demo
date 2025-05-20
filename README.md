# RSA based 1-out-of-n Oblivious Transfer Simulator
A simulator of the 1-out-of-n Oblivious Transfer protocol - redone in Python from my own earlier project in [Java](https://github.com/jsgarcha/oblivious-transfer-simulator). As opposed to sockets, this follows a REST API architecture. The front-end is in Streamlit and back-end in FastAPI.
Beware: the program implements non-standard RSA (for academic purposes), so it is not suited for real-world use! Furthermore, only a numeric message is currently supported as input to simplify encryption/decryption operations.

## Usage:
This simulator lets the user select or input a few pieces of data and walk through each step of the 1-out-of-n Oblivious Transfer protocol. At each step, the results, which are generally hidden behind the scenes, are visually printed and displayed, to teach the user how the protocol works. 

## Overview:
1) `Agent` is initialized with random information. 
2) `Inquirer` is initialized with a random `k` (index of the information item it desires). 
3) `Agent` listens for `Inquirer`. 
4) Once `Inquirer` connects to the `Agent`, 1-out-of-n Oblivious Transfer begins. 
5) The protocol ends with `Inquirer` receiving the `k`th information item from the `Agent`.

For a more thorough overview of the mathematical steps involved in the protocol, please refer to my comments in the code.
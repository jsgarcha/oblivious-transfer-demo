#Agent (sender/server)
import random
from fastapi import FastAPI, Request
from RSA_module import RSA
from Crypto.Random import get_random_bytes

app = FastAPI()

#Initialize globals, but safely
app.state.rsa = None
app.state.total_information_items = 10 #n
app.state.information_items = [random.randint(0, 9999) for _ in range(app.state.total_information_items)] #Randomly generated information for sake of simulation
app.state.RN = [int.from_bytes(get_random_bytes(4), byteorder="big") for _ in range(app.state.total_information_items)] #Generate Agent's random numbers, RN[].

#Agent initialization - send/receive initial data
@app.post("/step0")
async def step0(request: Request):
    global rsa, information_items

    step0_data = await request.json()
    key_size = step0_data.get("key_size") #Allow user to select key size, rather than default of 256
    #Receive k from inquirer!
    message_index = step0_data.get("message_index") 
    message = step0_data.get("message") #Allow user to input message in addition to randomly generated

    app.state.rsa = RSA(key_size) #Generate key pair
    app.state.information_items[message_index] = message #Insert/replace user inputted secret message into randomly generated information 

    return {
        "public_key": app.state.rsa.public_key, #Send public key to Inquirer
        "modulus": app.state.rsa.modulus, #Send modulus to Inquirer
        "n": len(app.state.information_items), #Send number of information items (=total_information_items) to Inquirer
    }

#Step 1: Agent sends random numbers RN[1],...,RN[n] to Inquirer
@app.get("/step1")
async def step1():
    global RN
    return {
        "RN": app.state.RN 
    }

#Step 2: Agent receives K+(IRN)+RN[k] from Inquirer.
@app.post("/step2")
async def step2(request: Request):
    step2_data = await request.json()
    step2_value =  step2_data.get("step2_value")
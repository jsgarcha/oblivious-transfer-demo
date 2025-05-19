#Agent (sender/server)
import random
from fastapi import FastAPI, Request
from RSA_module import RSA
from Crypto.Util import get_random_bytes

app = FastAPI()

#Initialize globals
total_information_items = 10 #n
rsa = None
information_items = [random.randint(0, 9999) for _ in range(total_information_items)] #Randomly generated information for sake of simulation
RN = [int.from_bytes(get_random_bytes(4), byteorder="big") for _ in range(total_information_items)] #Generate random numbers RN[].

@app.post("/step0")
async def step0(request: Request):
    global rsa, information_items, RN

    step0_data = await request.json()
    key_size = step0_data.get("key_size") #Allow user to select, rather than default
    #Receive k from inquirer!
    index = step0_data.get("index") 
    message = step0_data.get("message") #Allow user to input, rather than randomly generated

    rsa = RSA(key_size)
    information_items[index] = message #Insert/replace user inputted secret message into randomly generated information 

    return {
        "public_key": rsa.public_key, #Send public key to inquirer.
        "modulus": rsa.modulus, #Send modulus to inquirer.
        "information_items": information_items,
        "n": len(information_items), #(= total_information_items) Send number of information items to inquirer
        "RN": RN #Step 1: Agent sends random numbers RN[1],...,RN[n] to the inquirer:
    }
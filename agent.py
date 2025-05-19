#Agent (sender/server)
import random
from fastapi import FastAPI, Request
from RSA_module import RSA
from Crypto.Util import get_random_bytes

app = FastAPI()

total_information_items = 10 #n

@app.post("/step0")
async def step0(request: Request):
    step0_data = await request.json()
    key_size = step0_data.get("key_size")
    index = step0_data.get("index")
    message = step0_data.get("message")

    rsa = RSA(key_size)
    information = [random.randint(0, 9999) for _ in range(total_information_items)] #Randomly generated information for sake of simulation
    information[index] = message #Insert/replace user inputted secret message into randomly generated information 
    RN = [int.from_bytes(get_random_bytes(4), byteorder="big") for _ in range(total_information_items)]

    return {
        "public_key": rsa.public_key,
        "modulus": rsa.modulus,
        "information": information,
        "n": len(information), # = total_information_items
        "RN": RN #Step 1: Agent sends random numbers RN[1],...,RN[n] to the inquirer:
    }
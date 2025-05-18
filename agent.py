from Crypto.Random import get_random_bytes
from fastapi import FastAPI, Query
from pydantic import BaseModel

from RSA_module import RSA

app = FastAPI()

#Defaults
default_key_size = 256
total_info_items = 10

#Simulate Agent initialization
rsa = RSA(default_key_size) 
I = list(range(total_info_items)) #Agent's secret information items
RN = [int.from_bytes(get_random_bytes(4), byteorder="big") for _ in I] #Generate random numbers RN[]

#Initialization & Step 1:
@app.get("/init")
def init(key_size: int = Query(default_key_size, description="RSA key size in bits")):
    global rsa, RN
    rsa = RSA(key_size)
    return {
        "n": len(I),
        "public_key": rsa.public_key,
        "modulus": rsa.modulus,
        "RN": RN
    }

class Step2Input(BaseModel):
    step2_value: str  #Encrypted+masked IRN (as string)
    k: int            #Index selected by Inquirer

@app.post("/step3")
def process_step2(data: Step2Input):
    step2_val = int(data.step2_value)
    responses = []

    for i in range(total_info_items):
        decrypted = rsa.decrypt(step2_val-RN[i])%rsa.n 
        response = decrypted + I[i]
        responses.append(response)

    return {"responses": responses}
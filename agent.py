from fastapi import FastAPI
from pydantic import BaseModel
from RSA_module import RSA
from Crypto.Random import get_random_bytes

app = FastAPI()

rsa = RSA(256)
I = list(range(10))  #Information items
RN = [get_random_bytes(32) for _ in I ]

class Step2Input(BaseModel):
    step2_value: str  # Changed from int to str
    k: int

@app.get("/init")
def init():
    return {
        "n": len(I), #Send number of information items to inquirer.
        "public_key": rsa.public_key,
        "modulus": rsa.modulus,
        "RN": RN
    }

@app.post("/step3")
def process_step2(data: Step2Input):
    step2_val = int(data.step2_value)  # Convert back to int
    responses = []
    for i in range(len(info_items)):
        diff = (step2_val - RN[i]) % rsa.n
        decrypted = rsa.decrypt(diff)
        response = decrypted + info_items[i]
        responses.append(response)
    return {"responses": responses}
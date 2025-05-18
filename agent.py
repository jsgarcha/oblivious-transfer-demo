from fastapi import FastAPI
from pydantic import BaseModel
from RSA_module import RSA
from Crypto.Random import get_random_bytes

app = FastAPI()

rsa = RSA(256)
I = list(range(10)) #Information items
RN = [int.from_bytes(get_random_bytes(4), byteorder="big") for _ in I] #Generate random numbers RN[].

#Initialization & Step 1:
@app.get("/init")
def init():
    return {
        #Initialization -
        "n": len(I), #Send number of information items to inquirer.
        "public_key": rsa.public_key, #Send public key to inquirer.
        "modulus": rsa.modulus,
        #Step 1: Agent sends random numbers RN[1],...,RN[n] to the inquirer - 
        "RN": RN 
    }

#Assume inquirer wants to know the k-th information unit: I[k].	
class Step2Input(BaseModel):
    step2_value: str  
    k: int

#Step 3: Agent sends the inquirer the following n items K-(K+(IRN)+RN[k]-RN[i])+I[i] for i=1,...,n.	
@app.post("/step3")
def process_step2(data: Step2Input):
    step2_value = int(data.step2_value) #Convert back to int
    responses = []
    n = len(I) #n Items.
    for i in range(n):
        derived = (step2_value-RN[i])%rsa.n #The agent derives n terms K+(IRN)+RN[k]-RN[i] for i=1,...,n.
        decrypted = rsa.decrypt(derived) #Then the agent applies the decryption function K- to each of the n terms K+(IRN)+RN[k]-RN[i].
        response = decrypted + I[i] #And adds I[i] to each corresponding ith outcome of applying the decryption function: K-(K+(IRN)+RN[k]-RN[i])+I[i].
        responses.append(response)
    return {"responses": responses} #Returns result of step 3.
#Finally, note also that without knowing IRN, the agent could not know the specific kth item the inquirer is asking.
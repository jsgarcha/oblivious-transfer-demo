#Inquirer (receiver/client)
import streamlit as st
import pandas as pd
import requests
from Crypto.Random import get_random_bytes
from Crypto.Util.number import getRandomNBitInteger
from RSA_module import RSA

st.set_page_config("🔐 Inquirer - RSA based 1-out-of-n Oblivious Transfer Simulator", layout="wide")
st.title("🔐 RSA based 1-out-of-n Oblivious Transfer Simulator")
st.header("Inquirer")

agent_url = "http://localhost:8000"
total_information_items = 10 #n

if "step" not in st.session_state: st.session_state.step = 0 #Session state management of steps

#Parameters to initialize Agent in sidebar
st.sidebar.header("Step 0:")
key_size = st.sidebar.selectbox("Key Size (bits)", [256, 512, 1024])
message = st.sidebar.text_input("Secret Message")
message_index = st.sidebar.selectbox("Index (k)", options=list(range(total_information_items)))
step_0 = st.sidebar.button("🔄 Initialize **Agent**")

#Session state management of protocol
if "RN" not in st.session_state: st.session_state.RN = []
if "IRN" not in st.session_state: st.session_state.IRN = getRandomNBitInteger(32) #Generate Inquirer's random number (IRN); random 32-bit integer
if "message_index" not in st.session_state: st.session_state.message_index = message_index

#Step 0
if st.session_state.step == 0 and step_0:
    try:
        request = {
            "key_size": key_size,
            "message": message,
            "message_index": message_index
        }
        response = requests.post(f"{agent_url}/step0", json=request)
        if response.status_code == 200:
            st.success(f"**Sent** key size (`{key_size}`-bit), message (`{message}`), and message index (`{message_index}`) to **Agent**.")
            st.success("✅ **Agent** initialized!")

            step0_data = response.json()
            st.session_state.public_key = step0_data["public_key"]
            st.session_state.modulus = step0_data["modulus"]
            st.session_state.n = step0_data["n"]

            st.info(f"**Received** public key, modulus, and number of information items (`{st.session_state.n}`) from **Agent**.")
            st.session_state.step = 1
    except Exception as e:
        st.error("❌ Failed to initialize **Agent**.")
        st.exception(e)

#Step 1
if st.session_state.step == 1:
    if st.button("▶️ Step 1"):
        try:
            response = requests.get(f"{agent_url}/step1")

            if response.status_code == 200:
                step1_data = response.json()
                st.session_state.RN = step1_data["RN"]

                st.info("**Received** random numbers (`RN[0],...,RN[n-1]`) from **Agent**.")

                st.subheader("**Agent**'s random numbers (`RN[]`):")
                st.dataframe(pd.DataFrame(st.session_state.RN, columns=['Agent random number (RN[i])']))

                st.session_state.step = 2
        except Exception as e:
            st.error("❌ Failed to contact **Agent**.")
            st.exception({e})


#Step 2: Inquirer sends K+(IRN)+RN[k] to Agent
if st.session_state.step == 2:
    if st.button("▶️ Step 2"):
        #Step 2_1: Encrypt Inquirer's random number (IRN)
        rsa = RSA(bit_length=key_size, public_key=st.session_state.public_key, modulus=st.session_state.modulus)
        st.session_state.encrypted_IRN = rsa.encrypt(st.session_state.IRN)
        #Step 2_2: Add Inquirer's random numbers (IRN) to Agent's random numbers
        st.session_state.step2_value = st.session_state.encrypted_IRN+st.session_state.RN[st.session_state.message_index]  
        try:
            response = requests.post(f"{agent_url}/step2", json={"step2_value": str(st.session_state.step2_value)})
            if response.status_code == 200:
                st.subheader(f"Inquirer's random number (`IRN`) = `{st.session_state.IRN}`", divider=True)
                st.subheader(f"Encrypted `IRN` = `{st.session_state.encrypted_IRN}`", divider=True)
                st.success(f"**Sent** `{st.session_state.step2_value}` (`K+(IRN)+RN[k]`) to **Agent**")   
                st.session_state.step = 3
        except Exception as e:
            st.error("❌ Failed to contact **Agent**.")
            st.exception({e})

#Step 3:
if st.session_state.step == 3:
        if st.button("▶️ Step 3"):
            try:
                response = requests.get(f"{agent_url}/step3")
                st.session_state.responses = response["responses"]
                    st.session_state.final_values = [
                        r - st.session_state.IRN for r in st.session_state.responses
                    ]
            except Exception as e:
                st.error("❌ Failed to contact **Agent**.")
                st.exception({e})
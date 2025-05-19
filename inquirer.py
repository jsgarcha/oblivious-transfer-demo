#Inquirer (receiver/client)
import streamlit as st
import requests

st.set_page_config("🔐 Inquirer - RSA based 1-out-of-n Oblivious Transfer Simulator", layout="wide")
st.title("🔐 Inquirer - RSA based 1-out-of-n Oblivious Transfer Simulator")

agent_url = "http://localhost:8000"
total_information_items = 10 #n

st.sidebar.header("Step 0:")
key_size = st.sidebar.selectbox("Key Size (bits)", [256, 512, 1024])
message = st.sidebar.text_input("Secret Message")
index = st.sidebar.selectbox("Index (k)", options=list(range(total_information_items)))
step0 = st.sidebar.button("Initialize Agent")

#Session state management
if "step0" not in st.session_state:
    st.session_state.step0 = False
    st.session_state.step1 = False

#Step 0
if step0:
    try:
        request = {
            "key_size": key_size,
            "message": message,
            "index": index
        }
        response = requests.post(f"{agent_url}/step0", json=request)

        if response.status_code == 200:
            st.success("✅ Agent initialized!")
            st.session_state.step0 = True

            step1_data = response.json()
            st.session_state.public_key = step1_data["public_key"]
            st.session_state.modulus = step1_data["modulus"]
            st.session_state.information_items = step1_data["information_items"]
            st.session_state.n = step1_data["n"]
            st.session_state.RN = step1_data["RN"]

            st.success("Received public key & modulus from Agent.")

            #Received number of information items (n) from Agent:
		    #Step 1: Received n random numbers from Agent.

    except Exception as e:
        st.error("❌ Failed to initialize Agent.")

#Step 1
if st.session_state.step0 and not st.session_state.step1:
    st.button("▶️ Step 1: Generate IRN and Encrypt")

    st.session_state.step1_done = True
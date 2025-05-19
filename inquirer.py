# inquirer.py
import streamlit as st
import requests
import random

agent_url = "http://localhost:8000"

total_information_items = 10

st.title("🔐 Inquirer - RSA based 1-out-of-n Oblivious Transfer Simulator")

st.sidebar.header("Step 0:")
key_size = st.sidebar.selectbox("Key Size (bits)", [256, 512, 1024])
message = st.sidebar.text_input("Secret Message")
index = st.sidebar.selectbox("Index (k)", options=list(range(10)))

step0 = st.sidebar.button("Initialize Agent")

# Step 0
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
        
        
    except Exception as e:
        st.error(f"❌ Failed to initialize Agent.")


import streamlit as st
import requests

st.set_page_config(page_title="Inquirer - Oblivious Transfer", layout="wide")
st.title("📡 Inquirer - RSA based 1-out-of-n Oblivious Transfer Simulator")

agent_url = "http://localhost:8000"

# Step 0: Initialize with Agent
with st.spinner("Connecting to Agent..."):
    try:
        request = requests.get(f"{agent_url}/init")
        init_data_= request.json()
    except Exception as e:
        st.error(f"Failed to connect to agent: {e}")
        st.stop()
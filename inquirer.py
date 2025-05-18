import streamlit as st
import requests
import random
import pandas as pd

st.set_page_config(page_title="Inquirer - Oblivious Transfer", layout="wide")
st.title("📡 Inquirer (Client) - RSA 1-out-of-n Oblivious Transfer")

# Sidebar controls
st.sidebar.header("🔧 Parameters")
rsa_key_size = st.sidebar.selectbox("RSA Key Size (bits)", [256, 512, 1024], index=0)
k = st.sidebar.number_input("Select index k", min_value=0, max_value=9, value=0)

agent_url = "http://localhost:8000"

# Main Protocol Trigger
if st.button("Run Protocol"):

    with st.spinner("Contacting Agent..."):
        try:
            init_data = requests.get(f"{agent_url}/init", params={"key_size": rsa_key_size}).json()
        except Exception as e:
            st.error(f"❌ Could not connect to Agent API: {e}")
            st.stop()

    n = init_data["n"]
    public_key = init_data["public_key"]
    modulus = init_data["modulus"]
    RN = init_data["RN"]

    st.subheader("Step 1: Agent's Random Numbers (RN[i])")
    st.dataframe(pd.DataFrame({"Index": list(range(n)), "RN[i]": RN}))

    # Generate IRN and encrypted message
    IRN = int.from_bytes(random.randbytes(4), byteorder="big")
    encrypted_irn = pow(IRN, public_key, modulus)
    step2_value = encrypted_irn + RN[k]

    st.subheader("Step 2: Inquirer Encrypts IRN and Sends to Agent")
    st.code(f"IRN = {IRN}\nEncrypted IRN = {encrypted_irn}\nSent to Agent: step2_value = {step2_value}")

    # Step 3: Send to agent
    try:
        response = requests.post(f"{agent_url}/step3", json={
            "step2_value": str(step2_value),
            "k": k
        }).json()
    except Exception as e:
        st.error(f"❌ Failed to complete step3: {e}")
        st.stop()

    agent_responses = response["responses"]

    st.subheader("Step 3: Agent’s Responses")
    st.write(agent_responses)

    # Step 4: Inquirer computes final values
    final_values = [r - IRN for r in agent_responses]

    st.subheader("Step 4: Final Values (Decrypted)")
    result_df = pd.DataFrame({
        "Index": list(range(n)),
        "Response from Agent": agent_responses,
        "Final Value": final_values
    })

    # Convert large numbers to string to avoid OverflowError
    display_df = result_df.copy()
    display_df["Response from Agent"] = display_df["Response from Agent"].astype(str)
    display_df["Final Value"] = display_df["Final Value"].astype(str)

    def highlight_row(row):
        return ['background-color: lightgreen' if row.Index == k else '' for _ in row]

    st.dataframe(display_df.style.apply(highlight_row, axis=1))

    st.success(f"✔️ Inquirer successfully retrieved: I[{k}] = {final_values[k]}")

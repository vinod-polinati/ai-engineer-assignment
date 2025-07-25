import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Excel AI Interviewer", page_icon="🧠", layout="centered")
st.title("🧠 Excel Mock Interview")

API_URL = "http://localhost:8000/chat"

# 🔄 Session ID setup
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

SESSION_ID = st.session_state.session_id

# 🔁 Restart button
if st.button("🔄 Restart Interview"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = [{
        "sender": "bot",
        "text": "Hi, I'm your AI Excel interviewer. Type anything to begin."
    }]
    st.rerun()

# 🧠 Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "sender": "bot",
        "text": "Hi, I'm your AI Excel interviewer. Type anything to begin."
    }]

# 💬 Display message history
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["sender"] == "user" else "assistant"):
        st.markdown(msg["text"])

# 📥 Input + Backend communication
if prompt := st.chat_input("Type your response here..."):
    # User input
    st.session_state.messages.append({"sender": "user", "text": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Backend call
    try:
        res = requests.post(API_URL, json={
            "session_id": SESSION_ID,
            "message": prompt
        })
        res.raise_for_status()
        bot_reply = res.json()["response"]
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    # Bot reply
    st.session_state.messages.append({"sender": "bot", "text": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

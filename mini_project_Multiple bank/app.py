import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import speech_recognition as sr
import pyttsx3
from datetime import datetime, timedelta
import time
import threading

# Ensure Python can find auth module
sys.path.append(os.path.abspath("auth"))

# Import authentication functions
try:
    from auth.auth import login, logout
except ImportError:
    st.error("❌ Authentication module not found! Ensure `auth/auth.py` exists.")
    st.stop()

# Load Fraud Detection Model
model_path = "models/fraud_detection.pkl"  # ✅ Store path as a string
if not os.path.exists(model_path):  
    st.error(f"🚨 Missing model file: {model_path}. Please train and save the model first.")
    st.stop()
else:
    model = joblib.load(model_path)  # ✅ Load the


# Load Transaction Dataset
csv_path = "data/transactions.csv"
if not os.path.exists(csv_path):
    st.warning("⚠️ No transactions found! Using sample data.")
    df = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=5, freq="D"),
        "Amount": [20, 150, 300, 50, 800],
        "Category": ["Food", "Shopping", "Travel", "Bills", "Salary"],
        "Bank": ["HDFC", "SBI", "ICICI", "HDFC", "SBI"]
    })
else:
    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"])

# Authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()

# Sidebar
st.sidebar.title(f"👋 Welcome, {st.session_state.get('username', 'User')}")
if st.sidebar.button("Logout"):
    logout()
    st.experimental_rerun()

st.title("🏦 Multi-Bank Account & Fraud Detection System")

# --- Display Bank Accounts ---
st.subheader("📄 Your Bank Accounts")
bank_accounts = {"HDFC": 5000, "SBI": 7000, "ICICI": 10000}  # Sample balances
st.table(pd.DataFrame(bank_accounts.items(), columns=["Bank", "Balance"]))

# --- Fraud Detection ---
st.subheader("🔍 Detect Fraudulent Transactions")
amount = st.number_input("💰 Enter Transaction Amount", min_value=1)
if st.button("🚨 Predict Fraud"):
    prediction = model.predict(np.array([[amount]]))[0]
    if prediction == -1:
        reason = "🚨 Fraudulent: High-risk amount detected!"
    else:
        reason = "✅ Safe Transaction."
    st.write(f"**Transaction Status: {reason}**")
    engine = pyttsx3.init()
    engine.say(reason)
    engine.runAndWait()

# --- Automatic Money Withdrawal ---
st.subheader("⚡ Schedule Automatic Withdrawals")
scheduled_amount = st.number_input("💸 Enter Amount to Withdraw", min_value=1)
scheduled_date = st.date_input("📅 Select Date for Withdrawal")
selected_bank = st.selectbox("🏦 Choose Bank Account", list(bank_accounts.keys()))
if st.button("📅 Schedule Withdrawal"):
    st.session_state["scheduled_withdrawal"] = {
        "amount": scheduled_amount,
        "date": scheduled_date,
        "bank": selected_bank,
    }
    st.success(f"✅ Withdrawal of {scheduled_amount} scheduled for {scheduled_date} from {selected_bank}")

def automatic_withdrawal():
    while True:
        time.sleep(10)  # Check every 10 seconds
        if "scheduled_withdrawal" in st.session_state:
            withdrawal = st.session_state["scheduled_withdrawal"]
            today = datetime.today().date()
            if withdrawal["date"] == today:
                bank_accounts[withdrawal["bank"]] -= withdrawal["amount"]
                st.success(f"💰 {withdrawal['amount']} withdrawn from {withdrawal['bank']}")
                engine = pyttsx3.init()
                engine.say(f"{withdrawal['amount']} has been withdrawn from {withdrawal['bank']}")
                engine.runAndWait()
                del st.session_state["scheduled_withdrawal"]

threading.Thread(target=automatic_withdrawal, daemon=True).start()

# --- Voice Command for Transactions ---
st.subheader("🗣️ Voice Command for Transactions")

def listen_to_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening for a command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        st.success(f"✅ You said: {command}")
        return command
    except sr.UnknownValueError:
        st.error("❌ Could not understand the command.")
        return None
    except sr.RequestError:
        st.error("❌ Speech Recognition service unavailable.")
        return None

if st.button("🎙️ Use Voice Command"):
    command = listen_to_voice()
    if command:
        if "last week" in command:
            start_date = datetime.today() - timedelta(days=7)
            filtered_df = df[df["Date"] >= start_date]
        elif "last month" in command:
            start_date = datetime.today() - timedelta(days=30)
            filtered_df = df[df["Date"] >= start_date]
        elif "food" in command:
            filtered_df = df[df["Category"] == "Food"]
        elif "shopping" in command:
            filtered_df = df[df["Category"] == "Shopping"]
        elif "salary" in command:
            filtered_df = df[df["Category"] == "Salary"]
        else:
            st.warning("⚠️ Command not recognized!")
            filtered_df = df
        st.dataframe(filtered_df)

# --- Visualization ---
st.subheader("📊 Transaction Analysis")
col1, col2 = st.columns(2)
with col1:
    st.write("### Transaction Categories")
    category_counts = df["Category"].value_counts()
    st.bar_chart(category_counts)
with col2:
    st.write("### Transactions Over Time")
    st.line_chart(df.set_index("Date")["Amount"])

st.success("✅ Analysis Complete!")



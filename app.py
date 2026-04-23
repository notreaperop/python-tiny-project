import streamlit as st
st.set_page_config(layout="wide")
import pickle
import numpy as np
import matplotlib.pyplot as plt

# ---------- LOAD MODEL ----------
model = pickle.load(open("model.pkl", "rb"))

# ---------- TITLE ----------
st.markdown(
    "<h1 style='text-align: center;'>🏦 Loan Classifier</h1>",
    unsafe_allow_html=True
)

# ---------- MAIN LAYOUT ----------
left, right = st.columns([1, 1.2])

# 🔹 LEFT SIDE → INPUTS
with left:
    st.header("📥 Enter Details")

    income = st.number_input("Monthly Income (₹)", value=50000)
    dependents = st.number_input("Dependents", step=1)
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    credit = st.selectbox("Credit History", ["Good", "Bad"])

    st.subheader("💰 Loan Details")
    loan_amount = st.number_input("Loan Amount (₹)", value=200000)
    rate = st.number_input("Interest Rate (% per annum)", value=10.0)
    tenure = st.number_input("Tenure (years)", value=5)

    check = st.button("Check Eligibility")

# 🔹 RIGHT SIDE → OUTPUT
with right:
    st.header("📊 Results")

    if check:

        # convert input
        edu_val = 1 if education == "Graduate" else 0
        credit_val = 1 if credit == "Good" else 0

        data = np.array([[income, dependents, edu_val, credit_val]])
        result = model.predict(data)

        # EMI function
        def calculate_emi(P, R, N):
            R = R / (12 * 100)
            N = N * 12
            return (P * R * (1 + R)**N) / ((1 + R)**N - 1)

        emi = calculate_emi(loan_amount, rate, tenure)

        # 🔥 RESULT CARD
        if result[0] == 1:
            st.markdown(f"""
            <div class="card">
                <h3>✅ Loan Approved</h3>
                <p>Suggested Loan Amount: ₹{income * 5}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            reason = "Low Income" if income < 3000 else "Poor Credit History"
            st.markdown(f"""
            <div class="card">
                <h3>❌ Loan Rejected</h3>
                <p>Reason: {reason}</p>
            </div>
            """, unsafe_allow_html=True)

        # 💰 EMI CARD
        st.markdown(f"""
        <div class="card">
            <h3>💰 EMI Details</h3>
            <p>Monthly EMI: ₹{round(emi, 2)}</p>
        </div>
        """, unsafe_allow_html=True)

        # 📊 GRAPH CARD
        loan_range = np.linspace(50000, loan_amount, 10)
        emi_values = [calculate_emi(l, rate, tenure) for l in loan_range]

        fig, ax = plt.subplots()
        ax.plot(loan_range, emi_values)
        ax.set_xlabel("Loan Amount")
        ax.set_ylabel("EMI")
        ax.set_title("Loan vs EMI")

        st.pyplot(fig)
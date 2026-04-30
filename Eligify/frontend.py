

import streamlit as st
from backend import predict, fmt_inr   # <-- single import from backend

# ──────────────────────────────────────────────────────────────
#  Page config
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Loan Eligibility",
    page_icon="🏦",
    layout="centered",
)

# ──────────────────────────────────────────────────────────────
#  Custom CSS
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 760px; }

.portal-header { text-align: center; padding: 1.5rem 0 2rem 0; }
.portal-header h1 { font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem; }
.portal-header p  { color: #888; font-size: 0.95rem; }

.section-card {
    background: #f9f9fb;
    border: 1px solid #e8e8ec;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.section-title {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.75rem;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
#  Header
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="portal-header">
    <h1>🏦 Eligify - Check Your Eligibility</h1>
    <p>Instant loan eligibility — know your status in seconds</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
#  Section 1 – Personal details
# ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">Personal details</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    income     = st.slider("Annual income (₹)", 100_000, 2_000_000, 500_000, 10_000, format="₹%d")
    dependents = st.slider("Dependents", 0, 6, 1)
with c2:
    loan_req = st.slider("Loan amount requested (₹)", 50_000, 5_000_000, 500_000, 50_000, format="₹%d")
    age      = st.slider("Age", 18, 65, 30)
st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
#  Section 2 – Background
# ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">Background</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    education = st.selectbox("Education", ["Graduate", "Not graduate"])
with c2:
    employment = st.selectbox("Employment", ["Salaried", "Self-employed", "Business owner"])
with c3:
    property_area = st.selectbox("Property area", ["Urban", "Semi-urban", "Rural"])
st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
#  Section 3 – Credit profile
# ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">Credit profile</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    credit_history = st.radio("Credit history", ["Clean history", "Has defaults"], horizontal=False)
    credit_val = 1 if credit_history == "Clean history" else 0
with c2:
    cibil = st.slider("CIBIL score", 300, 900, 700, 10)
with c3:
    emi = st.slider("Existing EMIs (₹/mo)", 0, 100_000, 0, 1_000, format="₹%d")
st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
#  Submit button → call backend
# ──────────────────────────────────────────────────────────────
st.write("")
if st.button("✦ Check eligibility", use_container_width=True, type="primary"):

    result = predict(
        income, loan_req, dependents, age,
        education, employment, property_area,
        credit_val, cibil, emi,
    )

    approved    = result["approved"]
    score       = result["score"]
    reasons     = result["reasons"]
    max_loan    = result["max_loan"]
    rate        = result["rate"]
    tenure      = result["tenure"]


    st.divider()

    # ── Result banner ──────────────────────────────────────────
    if approved:
        st.success("## ✅ Congratulations, your loan qualifies!")
        reason_text = "✔️ All eligibility criteria met. Offer valid for 30 days."
    else:
        st.error("## ❌ Your application was not approved.")
        reason_text = (
            "⚠️ Primary factors: "
            + (", ".join(reasons) if reasons else "overall risk score below threshold")
            + "."
        )

    # ── Eligibility score bar ──────────────────────────────────
    st.write(f"**Eligibility Score: {score}%**")
    st.progress(score / 100)
    st.write("")

    # ── Metric columns ─────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("💰 Loan Amount",  fmt_inr(max_loan) if approved else "—")
    with m2:
        st.metric("📈 Interest Rate", f"{rate:.1f}% p.a." if approved else "—")
    with m3:
        st.metric("📅 Max Tenure",   f"{tenure} years"  if approved else "—")

    # ── Reason box ─────────────────────────────────────────────
    st.write("")
    if approved:
        st.info(f"**Reason for decision:** {reason_text}")
    else:
        st.warning(f"**Reason for decision:** {reason_text}")



# ──────────────────────────────────────────────────────────────
#  Footer
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Eligify · Powered by Logistic Regression · "
    "For demo purposes only — not financial advice."
)


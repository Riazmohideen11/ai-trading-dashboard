import streamlit as st
import yfinance as yf
import pandas as pd
from mftool import Mftool

from agents.market_analyst import MarketAnalyst
from agents.strategist import Strategist
from agents.risk_manager import RiskManager


st.set_page_config(page_title="Trading Dashboard", layout="wide")

st.title("📊 AI Trading Dashboard")

# Select Asset
asset_type = st.selectbox(
    "Select Asset Type",
    ["Stock", "Mutual Fund"],
)

# ------------------------------------------------
# STOCK MODE
# ------------------------------------------------
if asset_type == "Stock":

    symbol = st.text_input("Enter Stock Symbol", "ONGC.NS")

    if st.button("Analyze Stock"):

        analyst = MarketAnalyst()
        strategist = Strategist()
        risk_manager = RiskManager()

        analysis = analyst.analyze(symbol)
        news = analysis.get("news", {})

        decision = strategist.decide(analysis)
        plan = risk_manager.assess(decision, analysis)

        # News Sentiment
        st.subheader("📰 AI News Sentiment")

        sentiment_score = news.get("score", 0)

        if sentiment_score > 0.2:
            st.success(f"Bullish Sentiment: {sentiment_score:.2f}")
        elif sentiment_score < -0.2:
            st.error(f"Bearish Sentiment: {sentiment_score:.2f}")
        else:
            st.warning(f"Neutral Sentiment: {sentiment_score:.2f}")

        st.write("### Latest Headlines")

        for headline in news.get("headlines", []):
            st.write("•", headline)

        # Market Data
        data = yf.download(symbol, period="3mo")

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data['SMA_5'] = data['Close'].rolling(5).mean()
        data['SMA_20'] = data['Close'].rolling(20).mean()

        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Price Chart")
            st.line_chart(data[['Close', 'SMA_5', 'SMA_20']])

        with col2:
            st.subheader("📊 Analysis")
            st.write(f"**Current Price:** {analysis.get('price')}")
            st.write(f"**Signal:** {analysis.get('signal')}")
            st.write(f"**Decision:** {decision}")

        if isinstance(plan, dict):

            st.success("Trade Opportunity")

            st.write(f"Action: {plan['action']}")
            st.write(f"Stop Loss: {plan['stop_loss']:.2f}")
            st.write(f"Take Profit: {plan['take_profit']:.2f}")

        else:
            st.warning("No Trade Recommended")

        st.subheader("📉 RSI Indicator")
        st.line_chart(data['RSI'])


# -----------------------------
# MUTUAL FUND MODE
# -----------------------------
mf = Mftool()

mf_schemes = {
    "Bandhan Small Cap Fund Reg (G)": "118834",
    "Quant Small Cap Fund (G)": "120828",
    "Nippon India Small Cap Fund (G)": "118989"
}

selected_fund = st.selectbox(
    "Select Mutual Fund",
    list(mf_schemes.keys())
)

scheme_code = mf_schemes[selected_fund]

# Fetch historical NAV
history = mf.get_scheme_historical_nav(scheme_code)

if history and "data" in history:

    df = pd.DataFrame(history["data"])

    df["date"] = pd.to_datetime(df["date"])
    df["nav"] = df["nav"].astype(float)

    df = df.sort_values("date")

    nav = df.iloc[-1]["nav"]
    nav_date = df.iloc[-1]["date"]

    st.subheader("📊 Mutual Fund NAV")
    st.write("**Fund Name:**", selected_fund)
    st.write("**Latest NAV:**", nav)
    st.write("**NAV Date:**", nav_date)

    st.subheader("📈 NAV History")
    st.line_chart(df.set_index("date")["nav"])
    

else:
    st.error("Unable to fetch NAV data.")

st.subheader("💰 Mutual Fund Return Calculator")

calc_type = st.radio(
    "Investment Type",
    ["SIP", "Lumpsum"]
)

expected_return = st.slider(
    "Expected Annual Return (%)",
    5, 25, 12
)

years = st.slider(
    "Investment Duration (Years)",
    1, 30, 10
)

rate = expected_return / 100
months = years * 12

# --------------------
# SIP CALCULATOR
# --------------------
if calc_type == "SIP":

    sip_amount = st.number_input(
        "Monthly SIP Amount (₹)",
        500,
        1000000,
        5000
    )

    monthly_rate = rate / 12

    future_value = sip_amount * (
        ((1 + monthly_rate)**months - 1) / monthly_rate
    ) * (1 + monthly_rate)

    invested = sip_amount * months
    profit = future_value - invested

    st.write("### 📊 SIP Results")
    st.write(f"Total Invested: ₹{invested:,.0f}")
    st.write(f"Estimated Value: ₹{future_value:,.0f}")
    st.write(f"Profit: ₹{profit:,.0f}")

# --------------------
# LUMPSUM CALCULATOR
# --------------------
else:

    amount = st.number_input(
        "Investment Amount (₹)",
        1000,
        10000000,
        100000
    )

    future_value = amount * (1 + rate) ** years
    profit = future_value - amount

    st.write("### 📊 Lumpsum Results")
    st.write(f"Invested Amount: ₹{amount:,.0f}")
    st.write(f"Estimated Value: ₹{future_value:,.0f}")
    st.write(f"Profit: ₹{profit:,.0f}")

# -----------------------------
# AI Mutual Fund Rating
# -----------------------------
st.subheader("🤖 AI Mutual Fund Rating")

# Calculate returns
df["return"] = df["nav"].pct_change()

# Average return
avg_return = df["return"].mean() * 100

# Volatility
volatility = df["return"].std() * 100

# NAV trend
nav_growth = ((df["nav"].iloc[-1] - df["nav"].iloc[0]) / df["nav"].iloc[0]) * 100

score = 0

# Scoring logic
if avg_return > 0.5:
    score += 2
elif avg_return > 0.2:
    score += 1

if volatility < 2:
    score += 2
elif volatility < 4:
    score += 1

if nav_growth > 20:
    score += 2
elif nav_growth > 10:
    score += 1

# Rating decision
if score >= 5:
    rating = "⭐⭐⭐⭐⭐ Excellent Fund"
elif score >= 4:
    rating = "⭐⭐⭐⭐ Good Fund"
elif score >= 3:
    rating = "⭐⭐⭐ Average Fund"
else:
    rating = "⭐⭐ Risky Fund"

# Display results
st.write("**Average Return:**", f"{avg_return:.2f}%")
st.write("**Volatility:**", f"{volatility:.2f}%")
st.write("**NAV Growth:**", f"{nav_growth:.2f}%")

st.success(f"AI Rating: {rating}")

# -----------------------------
# Mutual Fund Risk Score
# -----------------------------
st.subheader("⚠️ Fund Risk Score")

# Daily returns
df["return"] = df["nav"].pct_change()

# Volatility (risk indicator)
volatility = df["return"].std() * 100

# Risk classification
if volatility < 0.5:
    risk = "Low Risk 🟢"
elif volatility < 1.5:
    risk = "Moderate Risk 🟡"
else:
    risk = "High Risk 🔴"

# Risk score out of 10
risk_score = min(round(volatility * 5, 2), 10)

st.write("**Volatility:**", f"{volatility:.2f}%")
st.write("**Risk Score (0–10):**", risk_score)
st.write("**Risk Level:**", risk)
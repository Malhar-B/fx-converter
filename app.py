import datetime as dt
import streamlit as st

from frankfurter import (
    list_currencies,
    get_latest_rate,
    get_rate_on,
    get_timeseries,  # optional; small trend chart
)
from currency import render_conversion_text

st.set_page_config(page_title="FX Converter", page_icon="↔️", layout="centered")
st.title("FX Converter  ↔️")

@st.cache_data(show_spinner=False, ttl=60 * 60)
def _currencies_cached():
    # cache the currency list for 1 hour
    return list_currencies()

# --- inputs ---
st.write("Enter the amount to be converted:")
amount = st.number_input("", min_value=0.0, value=50.0, step=1.0, format="%.2f")

currencies = _currencies_cached()
codes = sorted(currencies.keys())

col1, col2 = st.columns(2)
with col1:
    st.write("From Currency:")
    from_ccy = st.selectbox("", codes, index=codes.index("AUD") if "AUD" in codes else 0)
with col2:
    st.write("To Currency:")
    to_ccy = st.selectbox("", codes, index=codes.index("USD") if "USD" in codes else 0)

# --- latest rate ---
if st.button("Get Latest Rate", type="primary"):
    with st.spinner("Fetching latest rate…"):
        date_iso, rate = get_latest_rate(from_ccy, to_ccy)
    st.subheader("Latest Conversion Rate")
    st.write(
        render_conversion_text(
            date=date_iso, from_ccy=from_ccy, to_ccy=to_ccy, from_amount=amount, rate=rate
        )
    )
    # Optional: show 3-year trend if available
    try:
        start = (dt.date.fromisoformat(date_iso) - dt.timedelta(days=365 * 3)).isoformat()
        series = get_timeseries(from_ccy, to_ccy, start, date_iso)
        if series:
            st.subheader("Rate Trend Over the Last 3 years")
            st.line_chart(series, y="rate", x="date", height=240)
    except Exception:
        pass

# --- historical rate ---
st.write("Select a date for historical rates:")
hist_date = st.date_input(
    "",
    value=dt.date.today() - dt.timedelta(days=365),
    max_value=dt.date.today(),
    help="Pick a past date to see the rate on that day.",
)

if st.button("Conversion Rate"):
    with st.spinner("Fetching historical rate…"):
        date_iso, rate = get_rate_on(hist_date.isoformat(), from_ccy, to_ccy)
    st.subheader("Conversion Rate")
    st.write(
        render_conversion_text(
            date=date_iso, from_ccy=from_ccy, to_ccy=to_ccy, from_amount=amount, rate=rate
        )
    )

st.caption("Source: frankfurter.app • For educational use only.")

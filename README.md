# FX Converter (Streamlit + Frankfurter API)

**Student:** Malhar Bhavik Brahmbhatt  
**Student ID:** 26150110

## Overview
A Streamlit web app that converts an amount between two currencies using the free [Frankfurter](https://www.frankfurter.app/) API.  
Features:
- Latest exchange rate + converted amount
- Historical rate on a chosen date
- Inverse rate for the selected pair
- Small rate trend chart

## Project Structure
app.py # Streamlit UI (inputs, buttons, outputs)
api.py # Minimal HTTP client with retries/timeouts
frankfurter.py # Frankfurter-specific endpoint wrappers
currency.py # Formats the exact output sentence
README.md # You are here


### Key Functions
- `api.API.get(path, params=None, retries=2) -> dict`
- `frankfurter.list_currencies() -> dict[str,str]`
- `frankfurter.get_latest_rate(from_ccy, to_ccy) -> (date_iso, rate: float)`
- `frankfurter.get_rate_on(date_iso, from_ccy, to_ccy) -> (date_iso_returned, rate: float)`
- `frankfurter.get_timeseries(from_ccy, to_ccy, start_iso, end_iso) -> list[{date, rate}]`
- `currency.render_conversion_text(date, from_ccy, to_ccy, from_amount, rate) -> str`

The sentence format follows the assignment exactly:
> The conversion rate on \<date> from \<from currency> to \<to currency> was \<rate>.  
> So \<from amount> in \<from currency> correspond to \<to amount> in \<to currency>  
> The inverse rate was \<inverse rate>.

---

## How to Run

### A) GitHub Codespaces (recommended for easy grading)
1. Open your repo → **Code** → **Codespaces** → **Create codespace on main**.
2. In the Codespaces terminal:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   streamlit run app.py --server.address 0.0.0.0 --server.port 8080
3. When prompted, Open in Browser for port 8080.

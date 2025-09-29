# FX Converter (Streamlit + Frankfurter)

**Student:** <Your Name>  
**Student ID:** <Your Student ID>

## What it does
A Streamlit web app that fetches currency rates from https://www.frankfurter.app and shows:
- Latest conversion + inverse
- Historical conversion on a chosen date
- (Optional) 3-year trend chart

## How to run
```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install streamlit requests
streamlit run app.py

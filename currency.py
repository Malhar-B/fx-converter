from __future__ import annotations

def _fmt_amount(x: float) -> str:
    return f"{x:.2f}"

def _fmt_rate(x: float) -> str:
    s = f"{x:.5f}".rstrip("0").rstrip(".")
    if "." not in s:
        s += ".00"
    elif len(s.split(".")[1]) < 2:
        s = f"{x:.2f}"
    return s

def render_conversion_text(*, date: str, from_ccy: str, to_ccy: str, from_amount: float, rate: float) -> str:
    to_amount = from_amount * rate
    inverse = 0.0 if rate == 0 else 1.0 / rate
    return (
        f"The conversion rate on {date} from {from_ccy} to {to_ccy} was {_fmt_rate(rate)}. "
        f"So {_fmt_amount(from_amount)} in {from_ccy} correspond to {_fmt_amount(to_amount)} in {to_ccy} "
        f"The inverse rate was {_fmt_rate(inverse)}."
    )

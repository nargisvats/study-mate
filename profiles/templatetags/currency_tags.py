from django import template
from django.utils.safestring import mark_safe

register = template.Library()

SYMBOLS = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
}

@register.filter
def currency_symbol(code):
    return SYMBOLS.get((code or "").upper(), code)

@register.filter(is_safe=True)
def format_currency(amount, code="INR"):
    code = (code or "").upper()
    try:
        amount_str = f"{amount:.2f}"
    except Exception:
        amount_str = str(amount)
    if code == "INR":
        return mark_safe(f"{SYMBOLS.get('INR')}" + amount_str)
    symbol = SYMBOLS.get(code)
    if symbol:
        return mark_safe(f"{symbol}" + amount_str)
    return f"{amount_str} {code}"

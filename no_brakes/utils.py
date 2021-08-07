import re
import json


def extract_stock_symbols(title: str) -> set[str]:
    """Extract potential stock symbols from submission titles"""
    return set(re.findall(r"\$?\b[A-Z^/]{1,5}\b", title))

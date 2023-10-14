"""
0.999012321    -> 0.999012321
01.45211234    -> 1.4521
14.234554545    -> 14.2345
456.345211      -> 456.34
4500.001234252 -> 4500.00
1,450,123.88492 -> 1,450,123.89
"""

def format_number(balance: float) -> float:
    balance_str = str(f"{balance:.20f}")
    try:
        whole, decimal = balance_str.split(".")
    except ValueError:
        return f"{balance:.2f}"
    if float(whole) <= 0:
        if balance == 0:
            return 0.00
        total_count = 0
        for d,i in enumerate(decimal,start=1):
            if int(i) > 0 :
                total_count = d + 4
                break
            
        return f"{balance:.{total_count}f}"
            
    elif len(whole) < 3:
        return f"{balance:.4f}"
    else:
        return f"{balance:.2f}"



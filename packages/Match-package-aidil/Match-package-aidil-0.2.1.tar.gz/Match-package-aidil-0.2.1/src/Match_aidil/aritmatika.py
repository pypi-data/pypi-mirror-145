def penjumalah(a, b):
    try:
        return a + b
    except Exception:
        return None

def pengurangan(a, b):
    try:
        return a - b
    except Exception:
        return None

def perkalian(a, b):
    try:
        return a * b
    except Exception:
        return None

def pembagian(a, b)
    try:
        return a / b
    except ValueError:
        return None
    except ZeroDivisionError:
        return 0
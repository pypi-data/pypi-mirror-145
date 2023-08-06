def penjumlahan(a, b):
    try:
        return a + b
    except ValueError:
        return None
    except ZeroDivisionError:
        return None

def pengurangan(a, b):
    try:
        return a - b
    except ValueError:
        return None
    except ZeroDivisionError:
        return None

def perkalian(a, b):
    try:
        return a * b
    except ValueError:
        return None
    except ZeroDivisionError:
        return None

def pembagian(a, b):
    try:
        return a / b
    except ValueError:
        return None
    except  ZeroDivisionError:
        return None

def sisa_bagi(a, b):
    try:
        return a % b
    except ValueError:
        return None
    except ZeroDivisionError:
        return None
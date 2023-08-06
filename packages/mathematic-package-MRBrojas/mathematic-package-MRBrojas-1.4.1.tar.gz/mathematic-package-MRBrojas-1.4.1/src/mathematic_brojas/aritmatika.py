import logging


def penjumlahan(a, b):
    logging.info("penjumlahan digunakan")
    try:
        return a + b
    except ValueError:
        return None
    except ZeroDivisionError:
        return None
    except TypeError:
        return None

def pengurangan(a, b):
    logging.info("pengurangan digunakan")
    try:
        return a - b
    except ValueError:
        return None
    except ZeroDivisionError:
        return None
    except TypeError:
        return None

def perkalian(a, b):
    logging.info("perkalian digunakan")
    try:
        return a * b
    except ValueError:
        return None
    except ZeroDivisionError:
        return None
    except TypeError:
        return None

def pembagian(a, b):
    logging.info("pembagian digunakan")
    try:
        return a / b
    except ValueError:
        return None
    except ZeroDivisionError:
        return None
    except TypeError:
        return None
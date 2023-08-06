import logging

logging.basicConfig(
    level=logging.INFO,
    format="('%(asctime)s: %(levelname)s : %(name)s: %(message)s')",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)
log.info("Hello world")

def penjumlahan(a, b):
    logging.info("Penjumlahan digunakan!")
    try:
        return a + b
    except:
        return None

def pengurangan(a, b):
    logging.info("Pengurangan digunakan!")
    try:
        return a - b
    except:
        return None

def perkalian(a, b):
    return a * b

def pembagian(a, b):
    try:
        return a / b
    except ValueError:
        return None
    except ZeroDivisionError:
        return 0
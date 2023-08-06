import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s : %(name)s : %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)









def penjumlahan(a, b):
    log.info("Penjumlahan digunakan!")
    try:
        return a + b
    except Exception as e:
        log.error(e)
        return None
def pengurangan(a, b):
    log.info("Pengurangan digunakan!")
    try:
        return a - b
    except Exception as e:
        log.error(e)
        return None
def perkalian(a, b):
    log.info("Perkalian digunakan!")
    try:
        return a * b
     except Exception as e:
         log.error(e)
         return None
def pembagian (a, b):
    log.info("Pembagian digunakan!")
    try:
        return a / b
    except ValueError:
        log.error(e)
        return None
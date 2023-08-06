import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("mainlog.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)



def penjumalah(a, b):
    log.info('proses penjumlahan digunakan')
    try:
        return a + b
    except Exception as e:
        log.error(e)
        return None

def pengurangan(a, b):
    log.info('proses pengurangan digunakan')
    try:
        return a - b
    except Exception as e:
        log.error(e)
        return None

def perkalian(a, b):
    log.info('proses perkalian digunakan')
    try:
        return a * b
    except Exception as e:
        log.error(e)
        return None

def pembagian(a, b):
    log.info('proses pembagian digunakan')
    try:
        return a / b
    except ValueError as e:
        log.error(e)
        return None
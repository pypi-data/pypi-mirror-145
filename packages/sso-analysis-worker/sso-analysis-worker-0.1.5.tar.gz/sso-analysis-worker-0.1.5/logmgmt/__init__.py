import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s | %(filename)s', level=logging.WARNING)
logger = logging.getLogger("ssoworker")
logger.setLevel(logging.INFO)

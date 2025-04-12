import logging

__all__ = 'logger', '__version__'

logger = logging.getLogger('fsetools')
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'))
logger.addHandler(c_handler)
logger.setLevel(logging.DEBUG)

__version__ = "0.0.6"

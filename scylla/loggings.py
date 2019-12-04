import logging
import sys

_formatter = logging.Formatter(fmt="[%(asctime)s] [%(process)d] [%(levelname)s] [%(pathname)s:%(lineno)d]: %(message)s")
_ch = logging.StreamHandler(sys.stdout)
_ch.setLevel(logging.DEBUG)
_ch.setFormatter(_formatter)

# _fh = logging.FileHandler("mylog.log", "w")
# _fh.setLevel(logging.DEBUG)
# _fh.setFormatter(_formatter)

logger = logging.getLogger('scylla')
logger.setLevel(logging.DEBUG)

logger.addHandler(_ch)
# logger.addHandler(_fh)

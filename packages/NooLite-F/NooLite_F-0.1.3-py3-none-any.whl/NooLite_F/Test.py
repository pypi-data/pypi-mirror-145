import logging

_LOGGER = logging.getLogger("MTRF64USBAdapter")
_LOGGER.setLevel(logging.DEBUG)
_LOGGER_HANDLER = logging.StreamHandler()
_LOGGER_HANDLER.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
_LOGGER.addHandler(_LOGGER_HANDLER)


test = None

if test:
    _LOGGER.debug("success")

_LOGGER.debug("finish")

from logging.handlers import SysLogHandler
import logging


logger = logging.getLogger()
# change IP to your own public IP of the vm
logger.addHandler(SysLogHandler(address=('34.118.106.180', 514)))

logging.warning("Siema")

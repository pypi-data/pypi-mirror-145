# Written by Sumit Khanna
# License: AGPLv3
# https://battlepenguin.com
import logging
from rich.logging import RichHandler


logging.basicConfig(format='%(message)s', datefmt="[%X]", handlers=[RichHandler()])
log = logging.getLogger("dav-xmpp-sync")

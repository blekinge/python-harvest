import logging
from logging import Logger

logger = logging.getLogger(__name__) # type: Logger

from statsbiblioteket.harvest.synch.harvest_synch \
    import \
    create_parser # This import is important for the sphinx-argparse docs

logging.getLogger(__name__).addHandler(logging.NullHandler())

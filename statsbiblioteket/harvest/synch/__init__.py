import logging

from python_log_indenter import IndentedLoggerAdapter

logger = IndentedLoggerAdapter(logging.getLogger(__name__))

from statsbiblioteket.harvest.synch.harvest_synch \
    import \
    create_parser # This import is important for the sphinx-argparse docs


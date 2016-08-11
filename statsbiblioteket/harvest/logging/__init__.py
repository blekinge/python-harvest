from logging import Logger, Formatter


class HarvestLogger(Logger):
    """
    Docs
    """

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, **kwargs):
        if extra is None:
            extra = {}
        extra.update(kwargs)
        super()._log(level, msg, args, exc_info, extra, stack_info)



class DoubleFormatter(Formatter):

    def format(self, record):
        """
        Calls the standard formatter, but will indent all of the log messages
        by our current indentation level.
        """

        message = record.getMessage()
        message = message.format(**record.__dict__)
        message = message.format(record.args)
        record.msg = message
        formatted = Formatter.format(self, record)

        return formatted


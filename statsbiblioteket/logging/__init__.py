import logging


class KeywordLogger(logging.Logger):

    """
    A logger that takes keyword arguments so you can use modern string formatting
    """
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, **kwargs):
        if extra is None:
            extra = {}
        extra['keywords'] = kwargs #Add the keyword args to the record dict, so they can be used by the double formatter below
        super()._log(level, msg, args, exc_info, extra, stack_info)

logging.setLoggerClass(KeywordLogger)


class CurlyBraceFormatter(logging.Formatter):

    def format(self, record):
        """
        Calls the standard formatter, but will furthermore format the log
        message with all fields from the record
        """
        message = record.getMessage() # type: Str
        if record.keywords:
            message = message.format(**record.keywords)
        if record.args:
            message = message.format(record.args)
        record.msg = message
        formatted = super().format(record)

        return formatted



class IndentedMessage(object):

    indent = 0

    @classmethod
    def add_indent(cls):
        cls.indent += 1

    @classmethod
    def sub_indent(cls):
        cls.indent -= 1


class BraceMessage(IndentedMessage):
    """Utility class for {} formatting of messages for logging."""

    def __init__(self, fmt: str, *args, **kwargs):
        """
        A formatted version of fmt, using substitutions from args and kwargs.
        The substitutions are identified by braces ('{' and '}').
        """
        self.fmt = '{indent}'+fmt
        self.args = args
        self.kwargs = kwargs
        kwargs['indent'] = ' ' * (BraceMessage.indent * 4)

    def __str__(self) -> str:
        return self.fmt.format(*self.args, **self.kwargs)


logformat = BraceMessage

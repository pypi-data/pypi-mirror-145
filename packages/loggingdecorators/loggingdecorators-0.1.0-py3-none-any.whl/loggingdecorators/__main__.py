import loggingdecorators as log
import logging
from dataclasses import dataclass
from collections import defaultdict

# Create logger
logger = logging.getLogger("demo")
logger.setLevel(logging.DEBUG)
initLogger = logging.getLogger("init")
initLogger.setLevel(logging.DEBUG)

# Create formatter for messages.log
formatter = logging.Formatter(fmt="{levelname:<6}:{name}:{filename}:{lineno}: {message}", style="{")
fileHandler = logging.FileHandler("messages.log")
fileHandler.setFormatter(formatter)

# Create formatter for init.log
initFormatter = logging.Formatter(fmt="[{levelname:<5}] [{name}] at {filename}:{lineno} in {funcName}: {message}", style="{")
initFileHandler = logging.FileHandler("init.log")
initFileHandler.setFormatter(initFormatter)

# Add handlers
logger.addHandler(fileHandler)
initLogger.addHandler(initFileHandler)


class Widget:

    def __init__(self, *args, **kwargs):
        self.keys = kwargs.keys()
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __repr__(self):
        return f"""{self.__class__.__name__}({", ".join([f"{k}={self.__getattribute__(k)}" for k in self.keys])})"""

    @log.on_call(logger, logargs=False)
    def do_nothing(self, *args, **kwargs):
        pass


# Subclass with decorated init
class LoggingWidget(Widget):

    @log.on_init(logger=initLogger)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Mixin with decorated init
class LoggingMixin:

    @log.on_init(logger=initLogger)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Subclass which logs via the decorated mixin
class OtherLoggingWidget(LoggingMixin, Widget):
    pass


# Subclasses of a decorated class will inherit the logging behaviour (as long as super().__init__ is called)
class SpecialWidget(LoggingWidget):
    pass


# Decorated subclass
@log.on_init(logger=initLogger, logargs=False)
class WrappedWidget(Widget):
    pass


@log.on_init(logger=initLogger, logargs=True)
@dataclass
class Data:
    foo: int = 0
    bar: str = "NONE"


@log.on_init(logger=initLogger, logargs=True)
class LogData(Data):
    pass


@log.on_init(logger=initLogger, logargs=True)
class LogDefaultdict(defaultdict):
    pass


defaultdict = LogDefaultdict


def do_stuff_that_is_fun():
    for k in range(5):
        SpecialWidget(k**k)


def main():

    initLogger.info("+++ BEGIN")
    logger.info(">>> STARTING")

    data = {
        "spam": list(),
        "eggs": (0, int, ()),
        "ham": range(5)
        }

    ArgLogWidget = log.on_call(logger)(Widget)

    logger.info(">>> w1 = Widget(**data)")
    w1 = Widget(**data)
    w1.do_nothing("spam", "eggs", pi=22/7)

    data.update({'sam': 'I am!'})
    del data['eggs']

    logger.info(">>> w2 = LoggingWidget(**data)")
    w2 = LoggingWidget(**data)

    logger.info(">>> w3 = WrappedWidget(**data)")
    w3 = WrappedWidget(**data)

    logger.info(""">>> w4 = ArgLogWidget("hello!", **data)""")
    w4 = ArgLogWidget("hello!", **data, pi=3.00)

    logger.info(""">>> w4.do_nothing()""")
    w4.do_nothing()

    logger.info(""">>> w5 = SpecialWidget()""")
    w5 = SpecialWidget()

    logger.info(""">>> w6 = OtherLoggingWidget()""")
    w6 = OtherLoggingWidget()

    do_stuff_that_is_fun()

    data1 = Data(99, "deadparrot")
    print(data1)

    dd = defaultdict(Widget)
    print(dd)

    initLogger.info("+++ END")
    logger.info(">>> DONE")


main()

import datetime

class Logger:
    def __init__(self, verbose=False, use_timestamps=True):
        self.verbose = verbose
        self.use_timestamps = use_timestamps

    def log(self, message, logging_level=0):
        """
        Logs a message to the console.
        If not verbose, will only output messages with logging level ERROR.
        """
        if self.verbose or logging_level == LoggingLevel.ERROR:
            self.__output(message, logging_level)

    def __output(self, message, logging_level=0):
        """
        Outputs a message to the console with prefix and optional timestamp.
        """
        output = self.__get_prefix(logging_level)
        if self.use_timestamps:
            # add system time
            output += f" {datetime.datetime.now().strftime('%H:%M:%S')}"
        output += f" {message}"
        print(output)     

    def __get_prefix(self, logging_level):
        """
        Returns the prefix for the message based on the logging level.
        """
        if logging_level == LoggingLevel.DEBUG:
            return "[DEBUG]"
        elif logging_level == LoggingLevel.WARNING:
            return "[WARNING]"
        elif logging_level == LoggingLevel.ERROR:
            return "[ERROR]"
        

class LoggingLevel:
    """
    Enum for logging levels.
    """
    DEBUG = 0
    WARNING = 1
    ERROR = 2
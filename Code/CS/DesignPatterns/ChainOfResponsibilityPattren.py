# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建抽象的记录器类。
class AbstractLogger(object):
    INFO = 1
    DEBUG = 2
    ERROR = 3
    def __init__(self, level):
        self.level = level
        self.nextLogger = None
    def setNextLogger(self, nextLogger):
        self.nextLogger = nextLogger
    def logMessage(self, level: int, message: str):
        if self.level <= level:
            self.write(message)
        if self.nextLogger is not None:
            self.nextLogger.logMessage(level, message)
    def write(self, message: str):
        pass

# 创建扩展了该记录器类的实体类。
class ConsoleLogger(AbstractLogger):
    def __init__(self, level: int):
        super(ConsoleLogger, self).__init__(level)
    def write(self, message: str):
        print("Standard  Console::Logger: {}".format(message))
class ErrorLogger(AbstractLogger):
    def __init__(self, level: int):
        super(ErrorLogger, self).__init__(level)
    def write(self, message: str):
        print("Error  Console::Logger: {}".format(message))
class FileLogger(AbstractLogger):
    def __init__(self, level: int):
        super(FileLogger, self).__init__(level)
    def write(self, message: str):
        print("File::Logger: {}".format(message))

# 创建不同类型的记录器。赋予它们不同的错误级别，并在每个记录器中设置下一个记录器。每个记录器中的下一个记录器代表的是链的一部分。
def getChainOfLogger():
    errorLogger = ErrorLogger(AbstractLogger.ERROR)
    fileLogger = FileLogger(AbstractLogger.DEBUG)
    consoleLogger = ConsoleLogger(AbstractLogger.INFO)

    errorLogger.setNextLogger(fileLogger)
    fileLogger.setNextLogger(consoleLogger)
    return errorLogger

if __name__ == '__main__':
    loggerChain = getChainOfLogger()
    loggerChain.logMessage(AbstractLogger.INFO, "This is an information.")
    loggerChain.logMessage(AbstractLogger.DEBUG, "This is a debug level information.")
    loggerChain.logMessage(AbstractLogger.ERROR, "This is a error level information.")
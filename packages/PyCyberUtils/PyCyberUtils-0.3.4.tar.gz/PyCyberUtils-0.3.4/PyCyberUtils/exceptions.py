class ExceptionModel(Exception):

    def __init__(self, message="Main config missing"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class CyberUtilConfigMissing(ExceptionModel):
    """Raised when missing CyberUtils main config"""
    pass


class CyberCallerConfigMissing(ExceptionModel):
    """Raised when missing CyberCaller config"""
    pass


class CyberDBConfigMissing(ExceptionModel):
    """Raised when missing CyberDB config"""
    pass


class CyberLoggerConfigMissing(ExceptionModel):
    """Raised when missing CyberDB config"""
    pass


class DatabaseConnectionError(Exception):
    """Raised when MongoDB dosn't respond"""
    pass

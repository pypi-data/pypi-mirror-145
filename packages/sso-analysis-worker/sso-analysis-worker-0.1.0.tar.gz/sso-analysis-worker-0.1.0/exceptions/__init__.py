class CancleCurrentSiteException(Exception):
    pass


class ConfigInvalidException(Exception):
    pass


class ManualAnalysisNeededException(Exception):
    pass


class ParameterException(Exception):
    def __init__(self, msg):
        self.msg = msg


class RenewalRequestNeededException(Exception):
    pass


class ResetProcessException(Exception):
    pass


class RetryException(Exception):
    pass


class SiteNotResolvableException(Exception):
    pass

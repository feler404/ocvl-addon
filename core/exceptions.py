class OCVLNodeException(Exception):
    pass


class LackRequiredSocketException(OCVLNodeException):
    pass


class LackRequiredTypeDataSocketException(OCVLNodeException):
    pass


class IncorrectTypeInStringSocketException(OCVLNodeException):
    pass

from creationism.registration.factory import RegistrantFactory
from creationism.utils import first_lowered

DEFAULT_MODE = "default"


class Mode(RegistrantFactory):
    STATIC = True
    AUTO = True
    CONVERT_NAME = first_lowered


class DefaultMode(Mode):
    ...

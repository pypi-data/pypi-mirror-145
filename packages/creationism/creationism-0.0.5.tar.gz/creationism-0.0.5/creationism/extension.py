from abc import abstractstaticmethod
from pathlib import Path
from creationism.registration.factory import RegistrantFactory

class Extension(RegistrantFactory):
    STATIC = True

    @classmethod
    def has_extension(cls, path: Path, extension: "Extension"):
        return cls.create(path.suffix, return_type=True) == extension
    
    @classmethod
    def is_extension(cls, extension_name, extension):
        return issubclass(cls.create(extension_name, return_type=True), extension)



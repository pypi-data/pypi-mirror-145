from functools import lru_cache
from typing import Union

from creationism.registration.registrar import Registrar

cache = lru_cache(maxsize=None)
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class RegistrantNotRegisteredError(Exception):
    """Raised when registrant name does not exist in the register"""

    cls: type
    registrant_name: str
    register: Optional[dict]

    def __post_init__(self):
        super().__init__(self._message())

    def _message(self):
        if self.register is None:
            return self._empty_register_message()
        return self._register_name_not_found_message()

    def _prefix_message(self):
        return f"Registrant '{self.registrant_name}' is not found in the register of class '{self.cls.__name__}'"

    def _empty_register_message(self):
        return f"""
        {self._prefix_message()} with an empty register.
        """

    def _register_name_not_found_message(self):
        return f"""
        {self._prefix_message()} with registrant names {tuple(self.register.keys())} and register classes {tuple(self.register.values())}.
        """



class RegistrantFactory(Registrar):
    """Factory class for creating instances or retreive object references

    Class Atributes:
        STATIC (bool): Create static instances if the instantiation is identical

    Raises:
        RegistrantNotRegisteredError: raised when registrant name is not in the register

    """

    STATIC = False

    @classmethod
    def create(
        cls,
        registrant_name: Union[str, type],
        return_type: bool = False,
        *args,
        **kwargs
    ):
        """Creates from registrant a type or instance

        Args:
            registrant_name (Union[str, type]): name of the registrant that should be created
            return_type (bool, optional): if True only the type of the registrant is returened otherwise it will create and return an instance. Defaults to False.

        Raises:
            RegistrantNotRegisteredError: raises when the registrant is nog registered

        Returns:
            Any: type or instance of the registrant
        """

        if cls._REGISTER is None:
            raise RegistrantNotRegisteredError(
                cls=cls,
                registrant_name=registrant_name,
                register=cls._REGISTER,
            )

        if issubclass(type(registrant_name), cls):
            return registrant_name

        if callable(registrant_name) and registrant_name in cls._REGISTER.values():
            class_type = registrant_name
        elif registrant_name in cls._REGISTER:
            class_type = cls.get_registrant(registrant_name)
        else:
            raise RegistrantNotRegisteredError(
                cls=cls,
                registrant_name=registrant_name,
                register=cls._REGISTER,
            )

        if return_type:
            return class_type

        if cls.STATIC:
            return cls._static_create(class_type, *args, **kwargs)
        return cls._create(class_type, *args, **kwargs)

    @classmethod
    @cache
    def _static_create(cls, class_type, *args, **kwargs):
        return cls._create(class_type, *args, **kwargs)

    @classmethod
    def _create(cls, class_type, *args, **kwargs):
        return class_type(*args, **kwargs)

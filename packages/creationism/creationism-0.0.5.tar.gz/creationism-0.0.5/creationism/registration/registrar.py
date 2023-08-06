import warnings
from abc import ABC
from typing import Tuple, Callable
from creationism.registration.warnings import DuplicateRegistrantNameWarning
from functools import wraps

class Registrar(ABC):
    """Registrable class that can be used to register subclasses.

    Class Attributes:
        AUTO (bool): when enabled a subclass will be automatically registered with its class name
        REPLACE (bool): Replace registeration if new class is registered under same name
        CONVERT_NAME (Callable): function that converts the class name
        RECURSIVE (bool): recursively register subclasses

    Warnings:
        DuplicateRegistrantNameWarning:

    """

    AUTO = False
    REPLACE = True
    CONVERT_NAME = None
    RECURSIVE = False

    _REGISTER = None

    @property
    def name(self):
        return self.__class__.class_name()

    @classmethod
    def names(cls):
        return tuple(cls._REGISTER)

    @classmethod
    def registered(cls, name):
        return name in cls._REGISTER

    @classmethod
    def __init_subclass__(cls):
        if cls.AUTO:
            cls._register(
                bases=cls.__bases__,
                registrant_names=(cls.class_name(),),
                replace=cls.REPLACE,
                recursive=cls.RECURSIVE
            )

    @classmethod
    def class_name(cls):
        if cls.CONVERT_NAME is None:
            return cls.__name__
        return cls.CONVERT_NAME(cls.__name__)

    @classmethod
    def get_registrant(cls, registrant_name):
        if isinstance(registrant_name, type) and registrant_name in cls._REGISTER.values():
            return registrant_name
        return cls._REGISTER[registrant_name]

    @classmethod
    def register(cls, registrant_names: Tuple, replace=False, recursive=False):
        @wraps(cls.register)
        def decorator(registrant: Registrar):
            registrant._register(
                registrant.__bases__,
                registrant_names=registrant_names,
                replace=replace,
                recursive=recursive
            )
            return registrant

        return decorator

    @classmethod
    def register_func(cls, registrant_names: Tuple, replace=False):
        @wraps(cls.register_func)
        def decorator(registrant: Callable):
            cls._initialize_REGISTER()
            cls._add_to_register(registrant, registrant_names, replace)
            return registrant
        return decorator

    @classmethod
    def _register(cls, bases: Tuple, registrant_names: Tuple[str], replace: bool, recursive: bool):
        for base in bases:
            if issubclass(base, Registrar) and base is not Registrar:
                cls._add_to_base_registers(base, registrant_names, replace)
                if recursive:
                    cls._register(
                        bases=base.__bases__,
                        registrant_names=registrant_names,
                        replace=replace,
                        recursive=recursive,
                    )
                cls._deinitialize_REGISTER()

    @classmethod
    def _add_to_base_registers(
        cls, base: "Registrar", registrant_names: Tuple, replace: bool
    ):
        if Registrar in base.__bases__:
            return
        base._initialize_REGISTER()
        base._add_to_register(
            subclass=cls, registrant_names=registrant_names, replace=replace
        )

    @classmethod
    def _initialize_REGISTER(cls):
        if cls._REGISTER is None:
            cls._REGISTER = {}

    @classmethod
    def _deinitialize_REGISTER(cls):
        cls._REGISTER = None

    @classmethod
    def _add_to_register(
        cls, subclass: "Registrar", registrant_names: Tuple, replace: bool
    ):
        for name in registrant_names:
            if name in cls._REGISTER and not cls.REPLACE:
                warnings.warn(
                    DuplicateRegistrantNameWarning(cls, name, subclass, cls._REGISTER)
                )
                continue

            if name is not None:
                cls._REGISTER[name] = subclass

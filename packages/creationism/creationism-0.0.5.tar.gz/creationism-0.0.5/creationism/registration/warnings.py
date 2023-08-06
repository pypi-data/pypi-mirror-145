from dataclasses import dataclass
from typing import Optional

from creationism.registration.utils import Text

@dataclass(frozen=True)
class DuplicateRegistrantNameWarning(Warning):
    """Warning for when a registrant name is already registered.

    Args:
        cls (type): The class that contains the register.
        registrant_name (str): The name of the registrant that is already used.
        registrant (type): The registrant to be placed in the register.
        register (dict): The register of cls.
)
    Returns:
        str: Text that explains the warning
    """


    cls: type
    registrant_name: str
    registrant: type
    register: Optional[dict]

    def __str__(self):

        bold = Text.BOLD
        bold_end = Text.BOLD_END

        return (
            f"Unable to register {bold + self.registrant.__name__ + bold_end} with registrant name {bold + self.registrant_name + bold_end} "
            f"because registrant {bold + self.register[self.registrant_name].__name__+ bold_end} is already registerd "
            f"with registrant name {bold + self.registrant_name + bold_end} in the register of {bold + self.cls.__name__ + bold_end}."
        )

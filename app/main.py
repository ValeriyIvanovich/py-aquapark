from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self._min_amount = min_amount
        self._max_and_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.protected_name = "_" + name

    def __get__(self, obj: object, objtype: type = None) -> int:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: object, value: int) -> None:
        if not (self._min_amount <= value <= self._max_and_amount):
            raise ValueError(f"Value for "
                             f"{self.protected_name} must be between "
                             f"{self._min_amount} and "
                             f"{self._max_and_amount}")
        setattr(obj, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, visitor: Visitor) -> None:
        self.visitor = visitor

    @abstractmethod
    def validate(self) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator, ABC):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def validate(self) -> bool:
        valid_age = 4 <= self.visitor.age <= 14
        valid_height = 80 <= self.visitor.height <= 120
        valid_weight = 20 <= self.visitor.weight <= 50
        return valid_age and valid_height and valid_weight


class AdultSlideLimitationValidator(SlideLimitationValidator, ABC):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def validate(self) -> bool:
        valid_age = 14 <= self.visitor.age <= 60
        valid_height = 120 <= self.visitor.height <= 220
        valid_weight = 50 <= self.visitor.weight <= 120
        return valid_age and valid_height and valid_weight


class Slide:
    def __init__(
            self, name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validator = self.limitation_class(visitor)
        return validator.validate()

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.protected = "_" + name

    def __get__(self, instance: Any, owner: Type[Any]) -> Any:
        return getattr(instance, self.protected)

    def __set__(self, instance: Any, value: int) -> None:
        setattr(instance, self.protected, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def validate(self) -> None:
        if not (4 <= self.age <= 14):
            raise ValueError(
                "Age should be between 4 and 14 for children."
            )
        if not (80 <= self.height <= 120):
            raise ValueError(
                "Height should be between 80 and 120 for children."
            )
        if not (20 <= self.weight <= 50):
            raise ValueError(
                "Weight should be between 20 and 50 for children."
            )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def validate(self) -> None:
        if not (14 <= self.age <= 60):
            raise ValueError(
                "Age should be between 14 and 60 for adults."
            )
        if not (120 <= self.height <= 220):
            raise ValueError(
                "Height should be between 120 and 220 for adults."
            )
        if not (50 <= self.weight <= 120):
            raise ValueError(
                "Weight should be between 50 and 120 for adults."
            )


class Slide:
    def __init__(self, name: str,
                 limitation_class: Type[SlideLimitationValidator]
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
            return True
        except ValueError:
            return False

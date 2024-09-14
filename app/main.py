from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: Any, owner: Any) -> Any:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: int) -> Any:
        if not isinstance(value, int):
            raise TypeError(f"{self.protected_name} must be an integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"{self.protected_name} "
                f"must be between {self.min_amount} "
                f"and {self.max_amount}")
        setattr(instance, self.protected_name, value)

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name = "_" + name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
        self,
        name: str,
        limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class.age = visitor.age
            self.limitation_class.height = visitor.height
            self.limitation_class.weight = visitor.weight
        except (TypeError, ValueError):
            return False
        return True

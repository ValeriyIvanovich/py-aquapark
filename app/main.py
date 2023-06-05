from abc import ABC
from typing import Type


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: Type[SlideLimitationValidator],
            name: str
    ) -> None:
        self.private_name = "_" + name

    def __get__(
            self,
            instance: Type[SlideLimitationValidator],
            owner: Type[SlideLimitationValidator]
    ) -> int:
        value = getattr(instance, self.private_name)
        return value

    def __set__(
            self,
            instance: Type[SlideLimitationValidator],
            value: int
    ) -> None:
        if not isinstance(value, int | float):
            raise TypeError("Quantity should be int or float.")

        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Quantity should not be less than {self.min_amount}"
                f"and greater than {self.max_amount}.")
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


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
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except ValueError:
            return False
        return True

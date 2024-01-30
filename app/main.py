from __future__ import annotations
from abc import ABC


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: any, owner: any) -> object:
        return getattr(instance, self.protected_name)

    def __set_name__(self, owner: any, name: any) -> None:
        self.protected_name = "_" + name

    def __set__(self, instance: any, value: any) -> object:
        if not isinstance(value, int):
            raise TypeError("Value must be integer!")
        if self.min_amount <= value <= self.max_amount:
            return setattr(instance, self.protected_name, value)
        else:
            raise ValueError(f"Incorrect value! {value} must be in range "
                             f"of {self.min_amount}..{self.max_amount}")


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


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:

    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except ValueError or TypeError:
            return False
        else:
            return True

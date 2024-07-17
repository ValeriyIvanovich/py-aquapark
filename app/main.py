from typing import Type, Any

from abc import ABC


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type, name: str) -> None:
        self._protected_name = "_" + name

    def __get__(
            self,
            instance: Any,
            owner: Type) -> None:
        return getattr(instance, self._protected_name)

    def __set__(self, instance: Any, value: int) -> int:
        if self.min_amount <= value <= self.max_amount:
            value = setattr(instance, self._protected_name, value)
            return value
        raise ValueError(
            f"Quantity should not be less than {self.min_amount} and "
            f"greater than {self.max_amount}.")


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
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

    def __init__(self, name: str,
                 limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visistor: Visitor) -> bool:
        try:
            self.limitation_class(
                visistor.age,
                visistor.weight,
                visistor.height)
            return True
        except ValueError:
            return False

from __future__ import annotations

from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: Slide, owner: Type[Slide]) -> IntegerRange:
        return getattr(instance, self._name)

    def __set__(self, instance: Slide, value: int) -> None:
        if value > self.max_amount or value < self.min_amount:
            raise ValueError(
                f"Value {value} is out of range."
            )
        setattr(instance, self._name, value)

    def __set_name__(self, owner: Type[Slide], name: str) -> None:
        self._name = name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age_range = age
        self.weight_range = weight
        self.height_range = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age_range = IntegerRange(4, 14)
    weight_range = IntegerRange(20, 50)
    height_range = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age_range = IntegerRange(14, 60)
    weight_range = IntegerRange(50, 120)
    height_range = IntegerRange(120, 220)


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

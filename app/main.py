from __future__ import annotations

from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: IntegerRange, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: IntegerRange, owner: IntegerRange) -> str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: IntegerRange, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int) -> None:
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
                 limitation_class:
                 ChildrenSlideLimitationValidator
                 | AdultSlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, instance: Visitor) -> bool:
        age_lims = self.limitation_class.__dict__["age"].__dict__
        height_lims = self.limitation_class.__dict__["height"].__dict__
        weight_lims = self.limitation_class.__dict__["weight"].__dict__
        if (instance.age < age_lims["min_amount"]
                or instance.age > age_lims["max_amount"]):
            return False
        if (instance.height < height_lims["min_amount"]
                or instance.height > height_lims["max_amount"]):
            return False
        if (instance.weight < weight_lims["min_amount"]
                or instance.weight > weight_lims["max_amount"]):
            return False
        return True

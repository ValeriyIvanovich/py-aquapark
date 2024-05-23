from __future__ import annotations

from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, obj: object, objtype: type = None) -> IntegerRange:
        return self

    def __set__(self, obj: object, value: int) -> None:
        raise AttributeError("Cannot assign to an IntegerRange directly")


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    age = IntegerRange(min_amount=0, max_amount=0)
    height = IntegerRange(min_amount=0, max_amount=0)
    weight = IntegerRange(min_amount=0, max_amount=0)

    def validate(self, visitor: Visitor) -> bool:
        valid_age = (
            self.age.min_amount <= visitor.age <= self.age.max_amount)
        valid_height = (
            self.height.min_amount <= visitor.height <= self.height.max_amount)
        valid_weight = (
            self.weight.min_amount <= visitor.weight <= self.weight.max_amount)
        return valid_age and valid_height and valid_weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(min_amount=80, max_amount=120)
    weight = IntegerRange(min_amount=20, max_amount=50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(min_amount=120, max_amount=220)
    weight = IntegerRange(min_amount=50, max_amount=120)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)

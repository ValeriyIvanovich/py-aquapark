from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Visitor, name: str) -> None:
        self.name = "_" + name

    def __get__(
            self,
            instance: SlideLimitationValidator,
            owner: Visitor
    ) -> Visitor:
        return getattr(instance, self.name)

    def __set__(self, instance: SlideLimitationValidator, value: int) -> None:
        if value not in range(self.min_amount, self.max_amount + 1):
            value = False
            setattr(instance, self.name, value)
        else:
            value = True
            setattr(instance, self.name, value)


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
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type
    ) -> None:
        self.name = name
        self.limitation = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        limitation_class_instance = self.limitation(
            visitor.age,
            visitor.weight,
            visitor.height
        )

        if False in [
            limitation_class_instance.age,
            limitation_class_instance.weight,
            limitation_class_instance.height
        ]:
            return False
        return True

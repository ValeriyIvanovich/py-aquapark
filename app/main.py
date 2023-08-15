from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: Any = None) -> None:
        getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if self.min_amount > value or self.max_amount < value:
            raise ValueError(f"Quantity should not be "
                             f"less than {self.min_amount} "
                             f"and greater than {self.max_amount}.")

        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: float,
            height: float
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: float, height: float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    # def validate(self) -> bool:
    #     return True if (
    #             4 <= self.age <= 14
    #             and 80 <= self.height <= 120
    #             and 20 <= self.weight <= 50
    #     ) else False
    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(min_amount=80, max_amount=120)
    weight = IntegerRange(min_amount=20, max_amount=50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    # def validate(self) -> bool:
    #     return True if (
    #             14 <= self.age <= 60
    #             and 120 <= self.height <= 220
    #             and 50 <= self.weight <= 120
    #     ) else False
    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(min_amount=120, max_amount=220)
    weight = IntegerRange(min_amount=50, max_amount=120)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
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
        except ValueError:
            return False
        return True

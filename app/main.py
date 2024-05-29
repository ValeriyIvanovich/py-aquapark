from abc import ABC, abstractmethod
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.param_name = "_" + name

    def __get__(self, instance: object, owner: Type) -> int:
        return getattr(instance, self.param_name)

    def __set__(self, instance: object, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_amount} and greater "
                             f"than {self.max_amount}.")
        setattr(instance, self.param_name, value)


class Visitor:
    age = IntegerRange(min_amount=0, max_amount=120)
    height = IntegerRange(min_amount=50, max_amount=250)
    weight = IntegerRange(min_amount=10, max_amount=300)

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, visitor: Visitor) -> None:
        self.visitor = visitor

    @abstractmethod
    def validate(self) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def validate(self) -> bool:
        valid_age = 4 <= self.visitor.age <= 14
        valid_height = 80 <= self.visitor.height <= 120
        valid_weight = 20 <= self.visitor.weight <= 50
        return valid_age and valid_height and valid_weight


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def validate(self) -> bool:
        valid_age = 14 <= self.visitor.age <= 60
        valid_height = 120 <= self.visitor.height <= 220
        valid_weight = 50 <= self.visitor.weight <= 120
        return valid_age and valid_height and valid_weight


class Slide:
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class(visitor).validate()

from abc import ABC, abstractmethod
from typing import Any, Type, Tuple


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: Any, owner: Type) -> Tuple[int, int]:
        if instance is None:
            return self.min_amount, self.max_amount
        return self.min_amount, self.max_amount

    def __set__(self, instance: Any, value: int) -> None:
        raise AttributeError("Cannot set value")


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def validate(self, visitor: "Visitor") -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def validate(self, visitor: Visitor) -> bool:
        return all([
            self.age[0] <= visitor.age <= self.age[1],
            self.height[0] <= visitor.height <= self.height[1],
            self.weight[0] <= visitor.weight <= self.weight[1],
        ])


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def validate(self, visitor: Visitor) -> bool:
        return all([
            self.age[0] <= visitor.age <= self.age[1],
            self.height[0] <= visitor.height <= self.height[1],
            self.weight[0] <= visitor.weight <= self.weight[1],
        ])


class Slide:
    def __init__(
        self, name: str, limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation.validate(visitor)

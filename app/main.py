from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type, name: str) -> None:
        self.private_name = f"_{name}"

    def __get__(self, instance: object, owner: Type) -> int:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.private_name, value)
        else:
            raise ValueError(f"{self.private_name}"
                             f" must be between {self.min_amount}"
                             f" and {self.max_amount}")


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: IntegerRange,
                 height: IntegerRange, weight: IntegerRange) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(IntegerRange(4, 14),
                         IntegerRange(80, 120),
                         IntegerRange(20, 50)
                         )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(IntegerRange(14, 60),
                         IntegerRange(120, 220),
                         IntegerRange(50, 120)
                         )


class Slide:
    def __init__(self, name: str,
                 limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return (
            self.limitation_class.age.min_amount <= visitor.age
            <= self.limitation_class.age.max_amount
            and self.limitation_class.height.min_amount <= visitor.height
            <= self.limitation_class.height.max_amount
            and self.limitation_class.weight.min_amount <= visitor.weight
            <= self.limitation_class.weight.max_amount
        )

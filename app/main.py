from abc import ABC
from typing import Any, Type


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: Any) -> None:
        self.name = name

    def __get__(self, instance: Any, owner: Any) -> None:
        return getattr(instance, self.name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value must be between "
                f"{self.min_amount} and {self.max_amount}"
            )
        setattr(instance, self.name, value)


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
            age: IntegerRange,
            weight: IntegerRange,
            height: IntegerRange
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(4, 14),
            weight=IntegerRange(20, 50),
            height=IntegerRange(80, 120)
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):

    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(14, 60),
            weight=IntegerRange(50, 120),
            height=IntegerRange(120, 220)
        )


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        try:
            limitation_validator = self.limitation_class
            return all([
                limitation_validator.age.min_amount <= visitor.age
                <= limitation_validator.age.max_amount,
                limitation_validator.weight.min_amount <= visitor.weight
                <= limitation_validator.weight.max_amount,
                limitation_validator.height.min_amount <= visitor.height
                <= limitation_validator.height.max_amount
            ])
        except ValueError:
            return False

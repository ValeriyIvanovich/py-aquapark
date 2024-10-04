from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: object, owner: type) -> IntegerRange:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.protected_name} must be an integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"{self.protected_name} must be between "
                f"{self.min_amount} and {self.max_amount}"
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self) -> None:
        self.age_range = IntegerRange(4, 60)
        self.weight_range = IntegerRange(20, 120)
        self.height_range = IntegerRange(80, 220)

    def validate_visitor(self, visitor: Visitor) -> bool:
        return all((
            self.age_range.min_amount <= visitor.age
            <= self.age_range.max_amount,
            self.weight_range.min_amount <= visitor.weight
            <= self.weight_range.max_amount,
            self.height_range.min_amount <= visitor.height
            <= self.height_range.max_amount
        ))


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__()
        self.age_range = IntegerRange(4, 14)
        self.weight_range = IntegerRange(20, 50)
        self.height_range = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__()
        self.age_range = IntegerRange(14, 60)
        self.weight_range = IntegerRange(50, 120)
        self.height_range = IntegerRange(120, 220)


class Slide:
    def __init__(
            self, name: str, limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.validator.validate_visitor(visitor)

from __future__ import annotations

from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: Slide, owner: type(Slide)) -> IntegerRange:
        return getattr(instance, self._name)

    def __set__(self, instance: Slide, value: int) -> None:
        if value > self.max_amount or value < self.min_amount:
            raise ValueError(
                f"Value {value} is out of range."
            )
        setattr(instance, self._name, value)

    def __set_name__(self, owner: type(Slide), name: str) -> None:
        self._name = name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
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
        self.age_range = age
        self.weight_range = weight
        self.height_range = height

    def validate(self, visitor: Visitor) -> bool:
        return (
            (
                self.age_range.min_amount
                <= visitor.age
                <= self.age_range.max_amount
            )
            and (
                self.weight_range.min_amount
                <= visitor.weight
                <= self.weight_range.max_amount
            )
            and (
                self.height_range.min_amount
                <= visitor.height
                <= self.height_range.max_amount
            )
        )


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age_range = IntegerRange(4, 14)
        weight_range = IntegerRange(20, 50)
        height_range = IntegerRange(80, 120)
        super().__init__(age_range, weight_range, height_range)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age_range = IntegerRange(14, 60)
        weight_range = IntegerRange(50, 120)
        height_range = IntegerRange(120, 220)
        super().__init__(age_range, weight_range, height_range)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)

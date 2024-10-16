from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: SlideLimitationValidator,
            name: str
    ) -> None:
        self.protected_name = "_" + name

    def __get__(
            self: IntegerRange,
            instance: SlideLimitationValidator,
            owner: SlideLimitationValidator
    ) -> int:
        return getattr(instance, self.protected_name)

    def __set__(
            self: IntegerRange,
            instance: SlideLimitationValidator,
            value: int
    ) -> None:
        try:
            if not self.min_amount <= value <= self.max_amount:
                raise ValueError
        except ValueError:
            instance.result = False


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.result = True
        self.age = age
        self.weight = weight
        self.height = height

    def checking(self) -> bool:
        return self.result


class ChildrenSlideLimitationValidator(
    SlideLimitationValidator
):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(
    SlideLimitationValidator
):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class(
            visitor.age,
            visitor.weight,
            visitor.height
        ).checking()

from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, name: str) -> None:
        self.name = name

    def __get__(self) -> tuple:
        return self.min_amount, self.max_amount

    def __set__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: int,
                 weight: int,
                 height: int
                 ) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(4, 14),
            IntegerRange(20, 50),
            IntegerRange(80, 120))

    def validate(self, visitor: Visitor) -> bool:
        return (self.age.min_amount <= visitor.age
                and visitor.age <= self.age.max_amount
                and self.weight.min_amount <= visitor.weight
                and visitor.weight <= self.weight.max_amount
                and self.height.min_amount <= visitor.height
                and visitor.height <= self.height.max_amount)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(14, 60),
            IntegerRange(50, 120),
            IntegerRange(120, 220))

    def validate(self, visitor: Visitor) -> bool:
        return (self.age.min_amount <= visitor.age
                and visitor.age <= self.age.max_amount
                and self.weight.min_amount <= visitor.weight
                and visitor.weight <= self.weight.max_amount
                and self.height.min_amount <= visitor.height
                and visitor.height <= self.height.max_amount)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)

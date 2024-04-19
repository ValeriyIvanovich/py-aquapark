from abc import ABC


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
                 age: IntegerRange,
                 weight: IntegerRange,
                 height: IntegerRange
                 ) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    def validate(self, visitor: Visitor) -> bool:
        return (self.age.min_amount <= visitor.age
                and visitor.age <= self.age.max_amount
                and self.weight.min_amount <= visitor.weight
                and visitor.weight <= self.weight.max_amount
                and self.height.min_amount <= visitor.height
                and visitor.height <= self.height.max_amount)


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(4, 14)
        weight = IntegerRange(20, 50)
        height = IntegerRange(80, 120)
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(14, 60)
        weight = IntegerRange(50, 120)
        height = IntegerRange(120, 220)
        super().__init__(age, weight, height)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)

from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def validate(self, value: int) -> None:
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(
                f"Value {value} is out of range"
                f" ({self.min_amount}, {self.max_amount})"
            )


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            min_age: int,
            max_age: int,
            min_height: int,
            max_height: int,
            min_weight: int,
            max_weight: int
    ) -> None:
        self.age_range = IntegerRange(min_age, max_age)
        self.height_range = IntegerRange(min_height, max_height)
        self.weight_range = IntegerRange(min_weight, max_weight)

    @abstractmethod
    def can_access(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(4, 14, 80, 120, 20, 50)

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.age_range.validate(visitor.age)
            self.height_range.validate(visitor.height)
            self.weight_range.validate(visitor.weight)
            return True
        except ValueError:
            return False


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(14, 60, 120, 220, 50, 120)

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.age_range.validate(visitor.age)
            self.height_range.validate(visitor.height)
            self.weight_range.validate(visitor.weight)
            return True
        except ValueError:
            return False


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validator = self.limitation_class()
        return validator.can_access(visitor)

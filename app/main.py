from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: Any, owner: Any) -> bool:
        if self.name == "age":
            if not self.min_amount <= instance.age <= self.max_amount:
                raise ValueError(f"age {instance.age} out of range")
        if self.name == "weight":
            if not self.min_amount <= instance.weight <= self.max_amount:
                raise ValueError(f"weight {instance.weight} out of range")
        if self.name == "height":
            if not self.min_amount <= instance.height <= self.max_amount:
                raise ValueError(f"height {instance.height} out of height")
        return True

    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = name.split("_")[0]

    def __set__(self, instance: Any, value: int) -> None:
        if self.name == "age":
            if self.min_amount <= value <= self.max_amount:
                instance.age = value
        if self.name == "weight":
            if self.min_amount <= value <= self.max_amount:
                instance.weight = value
        if self.name == "height":
            if self.min_amount <= value <= self.max_amount:
                instance.height = value


class SlideLimitationValidator(ABC):
    age_range: IntegerRange
    weight_range: IntegerRange
    height_range: IntegerRange

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age_range = IntegerRange(4, 14)
    height_range = IntegerRange(80, 120)
    weight_range = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age_range = IntegerRange(14, 60)
    height_range = IntegerRange(120, 220)
    weight_range = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class Visitor:

    def __init__(self, name: int, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        self.limitation_class = (
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        )
        try:
            self.limitation_class.age_range
            self.limitation_class.height_range
            self.limitation_class.weight_range
        except ValueError as message_error:
            print(f"Sorry, {visitor.name} "
                  f"{message_error} for a slide '{self.name}'")
            return False
        return True

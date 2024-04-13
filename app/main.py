from abc import ABC, abstractmethod
from typing import Any, Type


class Range:
    def __init__(self, min_val: int, max_val: int) -> None:
        self.min = min_val
        self.max = max_val

    def __set_name__(self, owner: Type, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: Type) -> int:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: int) -> None:
        if not (self.min <= value <= self.max):
            raise ValueError(
                f"Value {value} out of range ({self.min}-{self.max})"
            )
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self) -> None:
        self.age = Range(0, 100)
        self.height = Range(0, 300)
        self.weight = Range(0, 200)

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__()
        self.age = Range(4, 14)
        self.height = Range(80, 120)
        self.weight = Range(20, 50)

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age.min <= visitor.age <= self.age.max
            and self.height.min <= visitor.height <= self.height.max
            and self.weight.min <= visitor.weight <= self.weight.max
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__()
        self.age = Range(14, 60)
        self.height = Range(120, 220)
        self.weight = Range(50, 120)

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age.min <= visitor.age <= self.age.max
            and self.height.min <= visitor.height <= self.height.max
            and self.weight.min <= visitor.weight <= self.weight.max
        )


class Slide:
    def __init__(
        self, name: str, limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation.validate(visitor)

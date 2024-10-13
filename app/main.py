from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, instance: object, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: object, owner: object) -> str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int | str) -> None:
        if not self.min_value <= value <= self.max_value:
            raise ValueError(f"Value must be in range from "
                             f"{self.min_value} to {self.max_value}")
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validator(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def validator(self) -> bool:
        if (4 <= self.age <= 14
                and 80 <= self.height <= 120
                and 20 <= self.weight <= 50):
            return True
        return False


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def validator(self) -> bool:
        if (14 <= self.age <= 60
                and 120 <= self.height <= 220
                and 50 <= self.weight <= 120):
            return True
        return False


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validator = self.limitation_class(visitor.age,
                                          visitor.weight,
                                          visitor.height)
        return validator.validator()

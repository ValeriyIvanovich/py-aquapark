from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if value in range(instance):
            setattr(instance, self.protected_name, value)

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age_range: tuple,
            weight_range: tuple,
            height_range: tuple
    ) -> None:
        self.age_range = age_range
        self.weight_range = weight_range
        self.height_range = height_range

    def validate(self, visitor: Visitor) -> None:
        if not (self.age_range[0] <= visitor.age <= self.age_range[1]):
            raise ValueError("Age out of range")
        if not (self.weight_range[0] <= visitor.weight
                <= self.weight_range[1]):
            raise ValueError("Weight out of range")
        if not (self.height_range[0] <= visitor.height
                <= self.height_range[1]):
            raise ValueError("Height out of range")


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__((4, 14), (20, 50), (80, 120))


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__((14, 60), (50, 120), (120, 220))


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation.validate(visitor)
        except (TypeError, ValueError):
            return False
        return True

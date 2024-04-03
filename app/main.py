from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: type) -> "IntegerRange":
        return self

    def __set__(self, instance: object, value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Value must be between {self.min_amount} "
                f"and {self.max_amount}")
        setattr(instance, self.name, value)

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name


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


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange = IntegerRange(4, 14)
    height: IntegerRange = IntegerRange(80, 120)
    weight: IntegerRange = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange = IntegerRange(14, 60)
    height: IntegerRange = IntegerRange(120, 220)
    weight: IntegerRange = IntegerRange(50, 120)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: type[SlideLimitationValidator]
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        if isinstance(visitor, Visitor):
            limitation = self.limitation_class
            if (limitation.age.min_amount <= visitor.age
                    <= limitation.age.max_amount
                    and limitation.height.min_amount
                    <= visitor.height <= limitation.height.max_amount
                    and limitation.weight.min_amount
                    <= visitor.weight <= limitation.weight.max_amount):
                return True
        return False

from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: str, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: str, owner: str) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: str, value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError
        setattr(instance, self.protected_name, value)


class SlideLimitationValidator(ABC):

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Visitor:

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class Slide:
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        if (self.limitation_class.__name__
                == "AdultSlideLimitationValidator"):
            try:
                AdultSlideLimitationValidator(visitor.age,
                                              visitor.weight,
                                              visitor.height)
            except ValueError:
                return False
            else:
                return True
        if (self.limitation_class.__name__
                == "ChildrenSlideLimitationValidator"):
            try:
                ChildrenSlideLimitationValidator(visitor.age,
                                                 visitor.weight,
                                                 visitor.height)
            except ValueError:
                return False
            else:
                return True

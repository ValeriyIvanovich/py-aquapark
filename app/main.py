from abc import ABC


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"Value should be from {self.min_amount} to {self.max_amount}")
        setattr(instance, self.private_name, value)


class Visitor:

    def __init__(
           self,
           name: str,
           age: int,
           weight: int,
           height: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)
        self.age = age
        self.height = height
        self.weight = weight


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)
        self.age = age
        self.height = height
        self.weight = weight


class Slide:

    def __init__(self, name: str, limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        if self.limitation_class == ChildrenSlideLimitationValidator:
            try:
                ChildrenSlideLimitationValidator(visitor.age, visitor.weight, visitor.height)
            except ValueError:
                return False
        else:
            try:
                AdultSlideLimitationValidator(visitor.age, visitor.weight, visitor.height)
            except ValueError:
                return False

        return True

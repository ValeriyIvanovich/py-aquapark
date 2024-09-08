from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: any, name: any) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: any, objtype: any = None) -> None:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: any, value: int) -> None:
        self.validate(value)
        setattr(obj, self.protected_name, value)

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Expected value to be an int")

        if value < self.min_amount or value > self.max_amount:
            raise ValueError("Value error !!!")


class Visitor:
    def __init__(self, name: int, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(min_amount=80, max_amount=120)
    weight = IntegerRange(min_amount=20, max_amount=50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(min_amount=120, max_amount=220)
    weight = IntegerRange(min_amount=50, max_amount=120)


class Slide:
    def __init__(
        self,
        name: str,
        limitation_class: ChildrenSlideLimitationValidator
            | AdultSlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> None:
        has_access = False
        if visitor.age <= 60 and visitor.age >= 14:
            if self.limitation_class is None:
                self.limitation_class = AdultSlideLimitationValidator

        if visitor.age <= 14 and visitor.age >= 4:
            if self.limitation_class is None:
                self.limitation_class = ChildrenSlideLimitationValidator

        if self.limitation_class is not None:
            try:
                self.limitation_class(
                    visitor.age,
                    visitor.height,
                    visitor.weight
                )
            except ValueError:
                has_access = False
            else:
                has_access = True

        return has_access

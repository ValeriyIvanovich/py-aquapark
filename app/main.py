from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self._name: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, instance: object, owner: type) -> int:
        return instance.__dict__.get(self._name)

    def __set__(self, instance: object, value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"{self._name.capitalize()} "
                             f"must be between {self.min_amount} and "
                             f"{self.max_amount}.")
        instance.__dict__[self._name] = value


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    age: IntegerRange
    weight: IntegerRange
    height: IntegerRange

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def is_valid(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(self) -> None:
        super().__init__(4, 50, 120)

    def is_valid(self, visitor: Visitor) -> bool:
        try:
            self.age = visitor.age
            self.weight = visitor.weight
            self.height = visitor.height
            return True
        except ValueError:
            return False


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(self) -> None:
        super().__init__(14, 120, 220)

    def is_valid(self, visitor: Visitor) -> bool:
        try:
            self.age = visitor.age
            self.weight = visitor.weight
            self.height = visitor.height
            return True
        except ValueError:
            return False


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.is_valid(visitor)

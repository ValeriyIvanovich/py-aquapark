from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self._name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError()
        if self.max_amount < value or value < self.min_amount:
            raise ValueError()
        setattr(instance, self._name, value)

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = f"_{name}"


class Visitor:
    def __init__(
        self,
        name: str,
        age: int,
        weight: int,
        height: int,
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


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age, height=visitor.height, weight=visitor.weight
            )
        except (ValueError, TypeError):
            return False
        else:
            return True

from abc import ABC


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: SlideLimitationValidator, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: SlideLimitationValidator, owner: None) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: SlideLimitationValidator, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Grade should be integer")

        if value not in range(self.min_amount, self.max_amount + 1):
            raise ValueError(
                f"Grade should not be less than "
                f"{self.min_amount} "
                f"and greater than {self.max_amount}"
            )

        setattr(instance, self.protected_name, value)


class Visitor:

    def __init__(
        self,
        name: str,
        age: int,
        weight: (int, float),
        height: (int, float)
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, height: int, weight: int) -> None:
        super().__init__(age, height, weight)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, height: int, weight: int) -> None:
        super().__init__(age, height, weight)


class Slide:

    def __init__(
        self,
        name: str,
        limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age, height=visitor.height, weight=visitor.weight
            )
        except (ValueError, TypeError):
            return False
        return True

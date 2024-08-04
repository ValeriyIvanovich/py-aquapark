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
        if self.min_amount <= value <= self.max_amount:
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


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        class_visit = None
        valid_adult = AdultSlideLimitationValidator(visitor.age,
                                                    visitor.weight,
                                                    visitor.height
                                                    )
        valid_children = ChildrenSlideLimitationValidator(visitor.age,
                                                          visitor.weight,
                                                          visitor.height
                                                          )
        if len(valid_adult.__dict__) == len(valid_children.__dict__) == 3:
            return True
        if len(valid_adult.__dict__) == 3:
            class_visit = type(valid_adult)
        if len(valid_children.__dict__) == 3:
            class_visit = type(valid_children)
        if self.limitation_class == class_visit:
            return True
        return False

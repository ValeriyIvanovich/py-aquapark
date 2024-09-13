from abc import ABC


class IntegerRange:
    def __init__(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"{self.name} must be between {self.min_amount} and {self.max_amount}")
        instance.__dict__[self.name] = value


class Visitor:
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age_range, weight_range, height_range):
        self.age = IntegerRange(*age_range)
        self.weight = IntegerRange(*weight_range)
        self.height = IntegerRange(*height_range)


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self):
        super().__init__((4, 14), (20, 50), (80, 120))


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self):
        super().__init__((14, 60), (50, 120), (120, 220))


class Slide:
    def __init__(self, name, limitation_class):
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor):
        try:
            self.limitation_class.age.__set__(visitor, visitor.age)
            self.limitation_class.weight.__set__(visitor, visitor.weight)
            self.limitation_class.height.__set__(visitor, visitor.height)
            return True
        except ValueError:
            return False

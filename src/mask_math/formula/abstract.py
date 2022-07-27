
class Singleton(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class NumberType(Singleton):
    pass


class ElementType(Singleton):
    pass


class CalculationType(Singleton):
    pass


class Element(object):
    def __init__(self):
        """
        どの集合に属するかを示す。
        実務的には複数の集合に属す。
        例えば、1は整数であり有理数であり実数であり複素数である
        """
        self.number_type: set[NumberType] = set()
        self.calc_type: set[CalculationType] = set()
        self.element_type: set[ElementType] = set()


class Operator(Element):
    pass








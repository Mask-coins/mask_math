from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Union
import math


class Formula(object):
    def __neg__(self):
        return Neg(self).eval()

    def __add__(self, other: Union[Formula, int]):
        return Add(self, other).eval()

    def __iadd__(self, other: Union[Formula, int]):
        return Add(self, other).eval()

    def __sub__(self, other: Union[Formula, int]):
        return Sub(self, other).eval()

    def __isub__(self, other: Union[Formula, int]):
        return Sub(self, other).eval()

    def __mul__(self, other: Union[Formula, int]):
        return Mul(self, other).eval()

    def __truediv__(self, other: Formula):
        return Div(self, other).eval()

    def __pow__(self, other: Formula):
        return Pow(self, other).eval()

    @abstractmethod
    def __eq__(self, other: Formula):
        pass


class MonoOperator(Formula, metaclass=ABCMeta):
    name = ""

    def __init__(self, value: Union[Formula, int]):
        self.value: Union[Formula, int] = value
        if isinstance(value, int):
            self.value = Z(value)

    @abstractmethod
    def eval(self):
        pass

    def __eq__(self, other):
        if type(self)==type(other):
            return self.value.__eq__(other.value)
        else:
            return False

    def __str__(self):
        return "(" + self.name + str(self.value) + ")"


class Neg(MonoOperator):
    name = "-"

    def __init__(self, value):
        super().__init__(value)

    def eval(self):
        return Mul(Z(-1),self.value).eval()


class BinOperator(Formula, metaclass=ABCMeta):
    name = ""

    def __init__(self, left: Union[Formula, int], right: Union[Formula, int]):
        self.left: Union[Formula, int] = left
        self.right: Union[Formula, int] = right
        if isinstance(left, int):
            self.left = Z(left)
        if isinstance(right, int):
            self.right = Z(right)

    @abstractmethod
    def eval(self):
        pass

    def __eq__(self, other):
        if type(self)==type(other):
            return self.left.__eq__(other.left) and self.right.__eq__(other.right)
        else:
            return False

    def __str__(self):
        return "(" + str(self.left) + self.name + str(self.right) +")"


class Add(BinOperator):
    name = "+"

    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        if isinstance(self.left,Z) and isinstance(self.right,Z):
            return Z(self.left.value+self.right.value)
        if isinstance(self.left,Div) and isinstance(self.right,Z):
            return Div(
                Add(self.left.left,
                    Mul(self.left.right,self.right).eval()).eval(),
                self.left.right).reduction()
        if isinstance(self.left,Z) and isinstance(self.right,Div):
            return Div(
                Add(self.right.left,
                    Mul(self.right.right,self.left).eval()).eval(),
                self.right.right).reduction()
        if isinstance(self.left,Div) and isinstance(self.right,Div):
            return Div(
                Add(
                    Mul(self.left.left,self.right.right).eval(),
                    Mul(self.left.right,self.right.left).eval()).eval(),
                Mul(self.left.right,self.right.right).eval()
            ).reduction()
        return Add(self.left, self.right)


class Sub(BinOperator):
    name = "-"

    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        #print(type(self.left),self.left,type(self.right),self.right)
        if isinstance(self.left,Z) and isinstance(self.right,Z):
            return Z(self.left.value-self.right.value)
        if isinstance(self.left,Div) and isinstance(self.right,Z):
            return Div(
                Sub(self.left.left,
                    Mul(self.left.right,self.right).eval()).eval(),
                self.left.right).reduction()
        if isinstance(self.left,Z) and isinstance(self.right,Div):
            return Div(
                Sub(Mul(self.right.right,self.left).eval(),self.right.left).eval(),
                self.right.right).reduction()
        if isinstance(self.left,Div) and isinstance(self.right,Div):
            return Div(
                Sub(
                    Mul(self.left.left,self.right.right).eval(),
                    Mul(self.left.right,self.right.left).eval()).eval(),
                Mul(self.left.right,self.right.right).eval()
            ).reduction()
        return Sub(self.left, self.right)


class Mul(BinOperator):
    name = "*"

    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        if isinstance(self.left,Z) and isinstance(self.right,Z):
            return Z(self.left.value*self.right.value)
        numerator = None
        denominator = None
        if isinstance(self.left,Div) and isinstance(self.right,Z):
            numerator = Mul(self.left.left,self.right).eval()
            denominator = self.left.right
        if isinstance(self.left,Z) and isinstance(self.right,Div):
            numerator = Mul(self.left,self.right.left).eval()
            denominator = self.right.right
        if isinstance(self.left,Div) and isinstance(self.right,Div):
            numerator = Mul(self.left.left,self.right.left).eval()
            denominator = Mul(self.left.right,self.right.right).eval()
        if numerator is not None and denominator is not None:
            return Div(numerator, denominator).reduction()
        return Mul(self.left, self.right)


class Div(BinOperator):
    name = "/"

    def __init__(self, left, right):
        numerator = left
        denominator = right
        if (isinstance(denominator,int) and denominator < 0
        ) or (isinstance(denominator,Z) and denominator.value < 0):
            numerator = -numerator
            denominator = -denominator
        super().__init__(numerator, denominator)

    def eval(self):
        #print(type(self.left),self.left,type(self.right),self.right)
        numerator = self.left
        denominator = self.right
        if isinstance(self.left,Div) and isinstance(self.right,Z):
            numerator = self.left.left
            denominator = Mul(self.left.right,self.right).eval()
        if isinstance(self.left,Z) and isinstance(self.right,Div):
            numerator = Mul(self.left,self.right.right).eval()
            denominator = self.right.left
        if isinstance(self.left,Div) and isinstance(self.right,Div):
            numerator = Mul(self.left.left,self.right.right).eval()
            denominator = Mul(self.left.right,self.right.left).eval()
        return Div(numerator, denominator).reduction()

    def reduction(self):
        if isinstance(self.left,Z) and isinstance(self.right,Z):
            if self.right.value < 0:
                self.left = Mul(Z(-1),self.left).eval()
                self.right = Mul(Z(-1),self.right).eval()
            g = math.gcd(self.left.value, self.right.value)
            self.left = Z(self.left.value//g)
            self.right = Z(self.right.value//g)
            if self.right.value == 1 or self.right.value == 0:
                return self.left
        return Div(self.left, self.right)


class Pow(BinOperator):
    name = "^"

    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        if isinstance(self.right,Z):
            if self.right.value == 0:
                return Z(0)
            if self.right.value < 0:
                x = Z(1)
                for i in range(-self.right.value):
                    x = Div(x,self.left).eval()
                return x
            else:
                x = Z(1)
                for i in range(self.right.value):
                    x =Mul(x,self.left).eval()
                return x
        return Pow(self.left, self.right)


class Number(Formula, metaclass=ABCMeta):
    @abstractmethod
    def __str__(self):
        pass


class Z(Number):
    def __init__(self, value: int):
        self.value: int = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if type(self)==type(other):
            return self.value.__eq__(other.value)
        else:
            return False


class Var(Number):
    def __init__(self,value):
        self.value: int = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if type(self)==type(other):
            return self.value.__eq__(other.value)
        else:
            return False


class Equation(object):
    def __init__(self, left: Formula, right: Formula):
        self.left: Formula = left
        self.right: Formula = right


if __name__ == '__main__':
    a = Div(2,-3)
    x = Var("x")
    y = Var("x")
    print(a)
    b = Z(3)
    c = Z(-3)
    print(x==y)












from __future__ import annotations
from abc import ABCMeta, abstractmethod, ABC
from typing import Union
import math
from src.mask_math import abstract_law
from src.mask_math import abstract_number


class Formula(object):
    def __init__(self):
        self._type = abstract_number.Number
        self.number_type_reset()

    def number_type(self):
        return self._type

    def number_type_reset(self):
        self._type = abstract_number.Number

    def number_type_set(self, t: type):
        self._type = t

    def __neg__(self):
        return Neg(self)

    def __add__(self, other: Union[Formula, int]):
        return Add(self, other)

    def __iadd__(self, other: Union[Formula, int]):
        return Add(self, other)

    def __sub__(self, other: Union[Formula, int]):
        return Sub(self, other)

    def __isub__(self, other: Union[Formula, int]):
        return Sub(self, other)

    def __mul__(self, other: Union[Formula, int]):
        return Mul(self, other)

    def __truediv__(self, other: Formula):
        return Div(self, other)

    def __pow__(self, other: Formula):
        return Pow(self, other)

    @abstractmethod
    def eval(self):
        return self

    @abstractmethod
    def __eq__(self, other: Formula):
        pass


class MonoOperator(Formula, metaclass=ABCMeta):
    name = ""

    def __init__(self, value: Union[Formula, int]):
        self.value: Union[Formula, int] = value
        if isinstance(value, int):
            self.value = Z(value)
        super().__init__()
        self.number_type_set(self.value.number_type())

    @abstractmethod
    def eval(self):
        pass

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value.__eq__(other.value)
        else:
            return False

    def __str__(self):
        return "(" + self.name + str(self.value) + ")"


class Neg(MonoOperator):
    name = "~"

    def __init__(self, value):
        super().__init__(value)

    def eval(self):
        value = self.value.eval()
        if isinstance(value, Z):
            return Z(-value.value).eval()
        if isinstance(value, Q):
            return Q(-value.numerator,value.denominator).eval()
        if isinstance(value, Neg):
            return value.value.eval()
        return Mul(Z(-1),value).eval()


class BinOperator(Formula, abstract_law.AbstractBinOperator, metaclass=ABCMeta):
    name = ""

    def __init__(self, left: Union[Formula, int], right: Union[Formula, int]):
        l: Union[Formula, int] = left
        r: Union[Formula, int] = right
        if isinstance(left, int):
            l = Z(left)
        if isinstance(right, int):
            r = Z(right)
        self.left = l
        self.right = r
        super().__init__()
        c = abstract_number.supset_eq(l.number_type(),r.number_type(),set(),set())
        self.number_type_set(c)
        #if issubclass(l.number_type(), r.number_type()):
        #    self.number_type_set(r.number_type())
        #if issubclass(r.number_type(), l.number_type()):
        #    self.number_type_set(r.number_type())

    @abstractmethod
    def eval(self):
        pass

    def __eq__(self, other):
        return self.number_type().eq(self, other)

    def __str__(self):
        return "(" + str(self.left) + self.name + str(self.right) +")"


class Add(BinOperator, abstract_law.AbstractAdd):
    name = "+"

    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        op = self
        # 整数演算
        op = Z.add(op)
        op = Q.add(op)
        if isinstance(op, (Z,Q,Var)):
            return op
        left: Formula = self.left.eval()
        right: Formula = self.right.eval()
        # 3*x + 4*x のようなパターン
        if issubclass(self.number_type(), abstract_number.CommutativeRing):
            a = left
            b =  right
            if isinstance(self.left, abstract_number.Variable):
                a = Z(1)*left
            if isinstance(self.right, abstract_number.Variable):
                b = Z(1)*left
            if self.number_type().var_add_check(a+b):
                return self.number_type().var_add(a+b)
        numerator = None
        denominator = None
        if isinstance(left,Q):
            numerator: Formula = (Z(left.denominator)*right + Z(left.numerator)).eval()
            denominator: Z = Z(left.denominator).eval()
        if isinstance(right,Q):
            numerator: Formula = (Z(right.denominator)*left + Z(right.numerator)).eval()
            denominator: Z = Z(right.denominator).eval()
        if isinstance(right,Z) and right < Z(0):
            numerator: Formula = (-left).eval()
            denominator: Z = (-right).eval()
        if isinstance(left,Div):
            numerator: Formula = (left.left + left.right*right).eval()
            denominator: Formula = left.right.eval()
        if isinstance(right,Div):
            numerator: Formula = (right.right*left + right.left).eval()
            denominator: Formula = right.right.eval()
        if numerator is not None and denominator is not None:
            return Div(numerator,denominator).eval()
        return left+right


class Sub(BinOperator):
    name = "-"

    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        left: Formula = self.left.eval()
        right: Formula = self.right.eval()
        return (left+(-right).eval()).eval()


class Mul(BinOperator, abstract_law.AbstractMul):
    name = "*"

    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        op = self
        op = Z.mul(op)
        op = Q.mul(op)
        if isinstance(op, (Z,Q)):
            return op
        left: Formula = op.left.eval()
        right: Formula = op.right.eval()
        if isinstance(right,Q):
            temp_left: Formula = Mul(left,Z(right.denominator)).eval()
            temp_right: Z = Z(right.numerator).eval()
            left: Formula = temp_left
            right: Z = temp_right
        if isinstance(right,Z) and right < Z(0):
            temp_left: Formula =(-left).eval()
            temp_right: Z =(-right).eval()
            left: Formula = temp_left
            right: Z = temp_right
        if isinstance(left,Div):
            numerator: Formula = (left.left * right).eval()
            denominator: Formula = left.right.eval()
            return (numerator/denominator).eval()
        if isinstance(right,Div):
            numerator: Formula = (right.right * left).eval()
            denominator: Formula = right.left.eval()
            return (numerator/denominator).eval()
        return left * right


class Div(BinOperator):
    name = "/"

    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        op = self
        op = Z.div(op)
        op = Q.div(op)
        if isinstance(op, (Z,Q)):
            return op
        left: Formula = op.left.eval()
        right: Formula = op.right.eval()
        if isinstance(right, (Q,Div)):
            return (left * right.swap()).eval()
        if isinstance(right,Z) and right < Z(0):
            temp_left: Formula = (-left).eval()
            temp_right: Z = (-right).eval()
            left: Formula = temp_left
            right: Z = temp_right
        numerator = left
        denominator = right
        if isinstance(left,Div):
            numerator: Formula = left.left
            denominator: Formula = (left.right * right).eval()
        return numerator/denominator

    def swap(self):
        return Div(self.right, self.left)


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


class LineOperator(Formula):
    def __init__(self):
        super().__init__()
        self.values: list[Formula] = []

    @abstractmethod
    def eval(self):
        if len(self.values) == 0:
            return None
        if len(self.values) == 1:
            return self.values.pop()
        x = self.values.pop()
        y = self.values.pop()
        while y:
            x += y
            y = self.values.pop()

    def __eq__(self, other):
        return self.number_type().eq(self, other)

    def __str__(self):
        return ""

    def push(self,value:Formula):
        self.values.append(value)




class R(Formula):
    '''
    原則として無理数を扱うが、事実上のfloat
    '''
    def __init__(self, value: float):
        super().__init__()
        self.value: float = value
        self.number_type_reset()

    def number_type_reset(self):
        self._type = abstract_number.RealNumber

    @abstractmethod
    def __str__(self):
        pass

    def eval(self):
        return self




class Q(Formula, abstract_number.RationalNumber):
    def __init__(self, numerator: int, denominator: int):
        self.numerator: int = numerator
        self.denominator: int = denominator
        super().__init__()

    def number_type_reset(self):
        self._type = abstract_number.RationalNumber

    def __str__(self):
        return "(" + str(self.numerator) + "/" + str(self.denominator) +")"

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.numerator == other.numerator and self.denominator == other.denominator
        else:
            return False

    def eval(self):
        numerator = self.numerator
        denominator = self.denominator
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        g = math.gcd(numerator, denominator)
        numerator = numerator//g
        denominator = denominator//g
        if denominator == 1:
            return Z(numerator)
        return Q(numerator,denominator)

    def R(self):
        return R(self.numerator/self.denominator)

    def Q(self):
        return self

    def swap(self):
        return Q(self.denominator,self.numerator)

    @classmethod
    def treat_type(cls, left, right):
        return isinstance(left, (Z,Q)) and isinstance(right, (Z,Q))

    @classmethod
    def add(cls, op: abstract_law.AbstractAdd):
        if isinstance(op, abstract_law.AbstractAdd):
            if isinstance(op.left, (Z,Q)) and isinstance(op.right, (Z,Q)):
                x: Q = op.left
                y: Q = op.right
                if isinstance(x,Z):
                    x = op.left.Q()
                if isinstance(y,Z):
                    y = op.right.Q()
                numerator = x.numerator * y.denominator + x.denominator * y.numerator
                denominator = x.denominator * y.denominator
                return Q(numerator,denominator).eval()
        return op

    @classmethod
    def mul(cls, op: abstract_law.AbstractMul):
        if isinstance(op, abstract_law.AbstractMul):
            if isinstance(op.left, (Z,Q)) and isinstance(op.right, (Z,Q)):
                x: Q = op.left
                y: Q = op.right
                if isinstance(x,Z):
                    x = op.left.Q()
                if isinstance(y,Z):
                    y = op.right.Q()
                numerator = x.numerator * y.numerator
                denominator = x.denominator * y.denominator
                return Q(numerator,denominator).eval()
        return op

    @classmethod
    def div(cls, op: Div):
        if isinstance(op, Div):
            if isinstance(op.left, (Z,Q)) and isinstance(op.right, (Z,Q)):
                x: Q = op.left
                y: Q = op.right
                if isinstance(x,Z):
                    x = op.left.Q()
                if isinstance(y,Z):
                    y = op.right.Q()
                numerator = x.numerator * y.denominator
                denominator = x.denominator * y.numerator
                return Q(numerator,denominator).eval()
        return op


class Z(Formula):
    def __init__(self, value: int):
        self.value: int = value
        super().__init__()

    class Zero(abstract_number.Zero):
        pass

    def number_type_reset(self):
        self._type = abstract_number.Integer

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value == other.value
        else:
            return False

    def R(self):
        return R(float(self.value))

    def Q(self):
        return Q(self.value,1)

    def CZ(self):
        return CZ(self.value,0)

    def supset_type(self):
        return (Q, CZ)

    def add_inv(self):
        Z(-self.value)

    def mul_inv(self):
        pass

    @classmethod
    def treat_type(cls, left, right):
        return cls==type(left) and cls==type(right)

    @classmethod
    def zero(cls):
        return Z(0)

    @classmethod
    def one(cls):
        return Z(1)

    @classmethod
    def zero_eval(cls, op: Union[Add,Mul]):
        if op.left == Z(0):
            op.left = op.number_type().zero()
        if op.right == Z(0):
            op.right = op.number_type().zero()
        op = op.number_type().zero_eval(op)
        if isinstance(op,op.number_type().Zero):
            op = Z(0)
        return op

    @classmethod
    def one_eval(cls, op: Add):
        if op.left == Z(0):
            op.left == op.number_type().one()
        if op.right == Z(0):
            op.right == op.number_type().one()
        op = op.number_type().zero_eval(op)
        if isinstance(op,op.number_type().ONE):
            op = Z(1)
        return op

    @classmethod
    def add(cls, op: Add):
        op = cls.zero_eval(op)
        op = op.number_type().one_eval(op)
        if type(op) == op.number_type().zero():
            op = cls.zero()
        if type(op) == op.number_type().one():
            op = cls.one()
        if isinstance(op, abstract_law.AbstractAdd):
            if isinstance(op.left,Z) and isinstance(op.right,Z):
                return Z(op.left.value + op.right.value)
        return op

    @classmethod
    def mul(cls, op: abstract_law.AbstractMul):
        if isinstance(op, abstract_law.AbstractMul):
            if isinstance(op.left,Z) and isinstance(op.right,Z):
                return Z(op.left.value * op.right.value)
        return op

    @classmethod
    def div(cls, op: Div):
        if isinstance(op, Div):
            if isinstance(op.left,Z) and isinstance(op.right,Z):
                return Q(op.left.value,op.right.value).eval()
        return op


class CZ(Formula):
    def __init__(self, real: Union[int, Z], imag: Union[int, Z]):
        super().__init__()
        self.real: Z = real
        self.imag: Z = imag
        if isinstance(real, int):
            self.real = Z(real)
        if isinstance(real, int):
            self.imag = Z(imag)

    def number_type_reset(self):
        self._type = abstract_number.CommutativeRing

    def __str__(self):
        return str(complex(self.real.value,self.imag.value))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.real == other.real and self.imag == other.imag
        else:
            return False

    def eval(self):
        if self.imag == Z(0):
            return self.real
        return self

    def conjugate(self):
        return CZ(self.real,(-self.imag).eval())

    def supset_type(self):
        return (C,)


class C(Formula):
    def __init__(self, real: Union[int, float, Z, R], imag: Union[int, float, Z, R]):
        super().__init__()
        self.real: Z = real
        self.imag: Z = imag
        if isinstance(real, float):
            self.real = R(float(real))
        if isinstance(imag, float):
            self.imag = R(float(imag))
        if isinstance(real, int):
            self.real = Z(real)
        if isinstance(imag, int):
            self.imag = Z(imag)

    def number_type_reset(self):
        self._type = abstract_number.ComplexNumber

    def __str__(self):
        pass

    def eval(self):
        if isinstance(self.real, Z) and isinstance(self.imag, Z):
            return CZ(self.real, self.imag)
        return self


class Var(Formula, abstract_number.Variable):
    def __init__(self, value, value_type=abstract_number.RealNumber):
        self.value: int = value
        self.value_type = value_type
        super().__init__()

    def number_type_reset(self):
        self._type = self.value_type

    def eval(self):
        return self

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value == other.value
        else:
            return False


class Equation(object):
    def __init__(self, left: Formula, right: Formula):
        self.left: Formula = left
        self.right: Formula = right

    def eval(self,var_name):
        pass


if __name__ == "__main__":
    x = Var("x")
    a = x + x
    print(a)
    print(a.eval())
    print((Z(1)+Z(1)).eval())










from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Union
import math


class Law(object):
    '''
    各種法則の親クラス
    '''
    pass


class AssociativeLaw(Law):
    '''
    結合法則
    '''
    pass


class AssociativeLawAdd(AssociativeLaw):
    pass


class AssociativeLawMul(AssociativeLaw):
    pass


class IdentityElementExistance(Law):
    '''
    単位元の存在
    '''
    pass


class IdentityElementExistanceAdd(IdentityElementExistance):
    pass


class IdentityElementExistanceMul(IdentityElementExistance):
    pass


class InverseElementExistance(Law):
    '''
    逆元の存在
    '''
    pass


class InverseElementExistanceAdd(InverseElementExistance):
    pass


class InverseElementExistanceMul(InverseElementExistance):
    pass


class CommutativeLaw(Law):
    '''
    交換法則
    '''
    @staticmethod
    def eq(left,right):
        return (left==left and right==right) or (left==right and right==left)


class CommutativeLawAdd(Law):
    pass


class CommutativeLawMul(Law):
    pass


class GroupAdd(
    AssociativeLawAdd,
    IdentityElementExistanceAdd,
    InverseElementExistanceAdd):
    pass


class GroupMul(
    AssociativeLawMul,
    IdentityElementExistanceMul,
    InverseElementExistanceMul):
    pass


class AbelianGroupAdd(GroupAdd,CommutativeLawAdd):
    pass


class AbelianGroupMul(GroupMul,CommutativeLawMul):
    pass


class DistributiveLaw(Law):
    '''
    分配法則
    '''
    pass


class Formula(object):
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
        if  isinstance(other,type(self)):
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
        left: Formula = self.left.eval()
        right: Formula = self.right.eval()
        numerator = None
        denominator = None
        if isinstance(left,Z) and isinstance(right,Z):
            return Z(left.value + right.value).eval()
        if isinstance(left,(Z,Q)) and isinstance(right,(Z,Q)):
            left: Q = left.Q()
            right: Q = right.Q()
            return Q(left.numerator * right.denominator + left.denominator * right.numerator, left.denominator * right.denominator).eval()
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

    def __eq__(self, other):
        if not isinstance(other,type(self)):
            return False
        if not(isinstance(self.left,CommutativeLawAdd) and isinstance(self.right,CommutativeLawAdd)):
            return self.left.__eq__(other.left) and self.right.__eq__(other.right)
        return CommutativeLaw.eq(self.left,self.right)


class Sub(BinOperator):
    name = "-"

    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        left: Formula = self.left.eval()
        right: Formula = self.right.eval()
        return (left+(-right).eval()).eval()


class Mul(BinOperator):
    name = "*"

    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        left: Formula = self.left.eval()
        right: Formula = self.right.eval()
        if isinstance(left,Z) and isinstance(right,Z):
            return Z(left.value * right.value).eval()
        if isinstance(left,(Z,Q)) and isinstance(right,(Z,Q)):
            left: Q = left.Q()
            right: Q = right.Q()
            return Q(left.numerator * right.numerator, left.denominator * right.denominator).eval()
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

    def __eq__(self, other):
        if not isinstance(other,type(self)):
            return False
        if not(isinstance(self.left,CommutativeLawMul) and isinstance(self.right,CommutativeLawMul)):
            return self.left.__eq__(other.left) and self.right.__eq__(other.right)
        return CommutativeLaw.eq(self.left,self.right)


class Div(BinOperator):
    name = "/"

    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        left: Formula = self.left.eval()
        right: Formula = self.right.eval()
        if isinstance(right, (Q,Div)):
            return (left * right.swap()).eval()
        if isinstance(left,Z) and isinstance(right,Z):
            return Q(left.value,right.value).eval()
        if isinstance(left,(Z,Q)) and isinstance(right,(Z,Q)):
            left: Q = left.Q()
            right: Q = right.Q()
            return Q(left.numerator * right.denominator, left.denominator * right.numerator).eval()
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


class Number(Formula, metaclass=ABCMeta):
    @abstractmethod
    def __str__(self):
        pass

    def eval(self):
        return self


class RealNumber(Number, CommutativeLawAdd, CommutativeLawMul):
    '''
    実数について扱う。
    整数・有理数・無理数・変数のサブクラスを持つ
    '''
    @abstractmethod
    def __str__(self):
        pass


class R(RealNumber):
    '''
    原則として無理数を扱うが、事実上のfloat
    '''
    def __init__(self, value: float):
        self.value: float = value

    @abstractmethod
    def __str__(self):
        pass

    def eval(self):
        return self


class Q(RealNumber):
    def __init__(self, numerator: int, denominator: int):
        self.numerator: int = numerator
        self.denominator: int = denominator

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

    def Q(self):
        return self

    def cast_float(self):
        return R(self.numerator/self.denominator)

    def swap(self):
        return Q(self.denominator,self.numerator)


class Z(RealNumber):
    def __init__(self, value: int):
        self.value: int = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value == other.value
        else:
            return False

    def Q(self):
        return Q(self.value,1)

    def cast_float(self):
        return R(float(self.value))


class CZ(Number):
    def __init__(self, real: Union[int,Z], imag: Union[int,Z]):
        self.real: Z = real
        self.imag: Z = imag
        if isinstance(real, int):
            self.real = Z(real)
        if isinstance(real, int):
            self.imag = Z(imag)

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


class C(Number):
    def __init__(self, real: Union[int, float, Z, R], imag: Union[int, float, Z, R]):
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

    def __str__(self):
        pass

    def eval(self):
        if isinstance(self.real, Z) and isinstance(self.imag, Z):
            return CZ(self.real, self.imag)
        return self




class Var(RealNumber):
    def __init__(self,value):
        self.value: int = value

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
    y = Var("y")
    z = Var("z")
    v = Var("v")
    a = (x/y)*(z/v)
    a = a.eval()
    print(a)










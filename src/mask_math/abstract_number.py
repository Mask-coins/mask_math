from src.mask_math.abstract_law import *


#まだ不完全
def supset_eq(x: Number, y: Number, self_set: set, other_set: set) -> Union[Number,None]:
    self_set.add(x)
    other_set.add(y)
    c = self_set & other_set
    if len(c)>0:
        return c.pop()
    r = set()
    for xt in x.supset_type():
        for yt in y.supset_type():
            r.add(supset_eq(xt,yt,self_set,other_set))
    return r.pop()


class Ring(Number):
    '''
    環
    ・加法：アーベル群
    ・乗法：モノイド（単位的半群）
    ・分配法則
    '''

    class Zero(IdentityElement):
        @classmethod
        def eval(cls, op: AbstractAdd):
            if not isinstance(op, AbstractAdd):
                return op
            if isinstance(op.left,cls) and isinstance(op.right,cls):
                return cls()
            if isinstance(op.left,cls):
                return op.right
            if isinstance(op.right,cls):
                return op.left

    class One(IdentityElement):
        @classmethod
        def eval(cls, op: AbstractMul):
            if not isinstance(op, AbstractMul):
                return op
            if isinstance(op.left,cls) and isinstance(op.right,cls):
                return cls()
            if isinstance(op.left,cls):
                return op.right
            if isinstance(op.right,cls):
                return op.left


    @classmethod
    def eq(cls, left, right):
        if isinstance(left, AbstractAdd) and isinstance(right, AbstractAdd):
            return cls.add_type().eq(left,right)
        if isinstance(left, AbstractMul) and isinstance(right, AbstractMul):
            return cls.mul_type().eq(left,right)
        if isinstance(left, AbstractBinOperator) and isinstance(right, AbstractBinOperator):
            return left.left==right.left and left.right==left.right
        return False

    @classmethod
    def add_type(cls):
        return AbelianGroup

    @classmethod
    def mul_type(cls):
        return Monoid

    @classmethod
    def one(cls):
        return None

    @classmethod
    def zero(cls):
        return None

    @classmethod
    def supset_type(cls):
        return (Number,)


class CommutativeRing(Ring, CommutativeLaw):
    """
    可換環
    ・加法：アーベル群
    ・乗法：可換モノイド
    ・分配法則
    すなわち整数的な演算である
    """

    @classmethod
    def mul_type(cls):
        return CommutativeMonoid

    @classmethod
    def supset_type(cls):
        return Ring,

    @classmethod
    def var_add_check(cls,value):
        return DistributiveLaw.var_add_check(value)

    @classmethod
    def var_add(cls,value):
        if isinstance(value,AbstractAdd):
            return DistributiveLaw.var_add(value)
        return value


class CommutativeField(CommutativeRing):
    """
    体(Field)
    ・加法：アーベル群
    ・乗法：可換モノイド、0 以外の元がアーベル群
    ・分配法則
    """
    @classmethod
    def supset_type(cls):
        return CommutativeRing,


class ComplexNumber(CommutativeField):
    """
    複素数：（可換）体
    """
    @classmethod
    def supset_type(cls):
        return CommutativeField,


class RealNumber(CommutativeField):
    '''
    実数：（可換）体
    '''

    @classmethod
    def supset_type(cls):
        return CommutativeField,


class RationalNumber(CommutativeField):
    '''
    有理数：（可換）体
    '''

    @classmethod
    def supset_type(cls):
        return RealNumber,


class Integer(CommutativeRing):
    '''
    整数：可換環
    '''

    @classmethod
    def supset_type(cls):
        return RationalNumber,


class GaussianInteger(CommutativeRing):
    '''
    ガウス整数（複素整数）：可換環
    '''

    @classmethod
    def supset_type(cls):
        return ComplexNumber,


class ModuleOverARing(Number):
    def __init__(self):
        super().__init__()
        self._ring = Ring

    def ring_type(self):
        return self._ring












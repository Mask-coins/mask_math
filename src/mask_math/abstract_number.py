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


class Zero(Law):
    value = None
    @classmethod
    def eval(cls, op: AbstractAdd):
        # 加法に対して単位元
        if isinstance(op, AbstractAdd):
            if op.left == cls.value and op.right == cls.value:
                return cls.value
            if op.left == cls.value:
                return op.right
            if op.right == cls.value:
                return op.left
        # 乗法に対して吸収元
        if isinstance(op, AbstractMul):
            if op.left == cls.value or op.right == cls.value:
                return cls.value
        return op




class Ring(Number):
    '''
    環
    ・加法：アーベル群
    ・乗法：モノイド（単位的半群）
    ・分配法則
    '''

    class Zero(IdentityElement):
        """
        零元とは、乗法に対して吸収元であり、加法に対して単位元である
        """
        @classmethod
        def eval(cls, op: AbstractAdd):
            # 加法に対して単位元
            if isinstance(op, AbstractAdd):
                if isinstance(op.left,cls) and isinstance(op.right,cls):
                    return cls()
                if isinstance(op.left,cls):
                    return op.right
                if isinstance(op.right,cls):
                    return op.left
            # 乗法に対して吸収元
            if isinstance(op, AbstractMul):
                if isinstance(op.left,cls) or isinstance(op.right,cls):
                    return cls()
            return op

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
    def supset_type(cls):
        return (Number,)

    @classmethod
    def is_zero(cls,x):
        return isinstance(x,type(cls.zero()))

    @classmethod
    def is_one(cls,x):
        return isinstance(x,type(cls.one()))

    @classmethod
    def zero(cls):
        return cls.Zero()

    @classmethod
    def one(cls):
        return cls.One()

    @classmethod
    def zero_eval(cls, op: Union[AbstractAdd,AbstractMul]):
        if not issubclass(op.number_type(),cls):
            return op
        # 加法に対して単位元
        if isinstance(op, AbstractAdd):
            if cls.is_zero(op.left) and cls.is_zero(op.right):
                return cls.zero()
            if cls.is_zero(op.left):
                return op.right
            if cls.is_zero(op.right):
                return op.left
        # 乗法に対して吸収元
        if isinstance(op, AbstractMul):
            if cls.is_zero(op.left) or cls.is_zero(op.right):
                return cls.zero()
        return op

    @classmethod
    def one_eval(cls, op: AbstractMul):
        if not issubclass(op.number_type(),cls):
            return op
        if not isinstance(op, AbstractMul):
            return op
        if cls.is_one(op.left) and cls.is_one(op.right):
            return cls.one()
        if cls.is_one(op.left):
            return op.right
        if cls.is_one(op.right):
            return op.left


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

    def mul_inv(self):
        pass


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
    '''
    環上の加群
    '''
    def __init__(self):
        super().__init__()
        self._scalar = Ring

    def scalar_type(self):
        return self._scalar


class Matrix(Number):
    '''
    行列
    '''
    def __init__(self):
        super().__init__()


















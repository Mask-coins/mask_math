from typing import Union


class Law(object):
    '''
    各種法則の親クラス
    '''
    pass


class Number(object):
    def __init__(self):
        self._type = type(self)

    @classmethod
    def supset_type(cls):
        return None

    @classmethod
    def eq(cls, left, right):
        return left==right


class Variable(Number):
    pass


class AbstractBinOperator(Number):
    '''
    二項演算を表す抽象概念
    '''
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right


class AssociativeLaw(Law):
    '''
    結合法則
    '''
    pass


class IdentityElement(object):
    '''
    単位元
    '''
    pass

class IdentityElementExistence(Law):
    '''
    単位元の存在
    '''
    pass


class InverseElementExistence(Law):
    '''
    逆元の存在
    '''
    pass


class CommutativeLaw(Law):
    '''
    交換法則
    '''
    @classmethod
    def eq(cls, left: Union[Number,AbstractBinOperator],right: Union[Number,AbstractBinOperator]):
        if isinstance(left, AbstractBinOperator) and isinstance(right, AbstractBinOperator):
            if left.number_type()==right.number_type():
                a = (left.left == right.left and left.right == right.right)
                b = (left.left == right.right and left.left == right.right)
                return a or b
        if isinstance(left, AbstractBinOperator) or isinstance(right, AbstractBinOperator):
            # 片方だけが二項演算子なら同一ではない
            return False
        return left == right


class AbstractAdd(AbstractBinOperator):
    '''
    加法の抽象概念
    '''
    pass


class AbstractMul(AbstractBinOperator):
    '''
    乗法の抽象概念
    '''
    pass


class DistributiveLaw(Law):
    '''
    分配法則
    '''
    @classmethod
    def eval(cls,value):
        if isinstance(value,AbstractMul):
            if isinstance(value.right,AbstractMul):
                # when a*(b+c)
                a = value.left
                b = value.right.left
                c = value.right.right
                ans = a*b + a*c
                return ans.eval()
            if isinstance(value.left,AbstractMul):
                # when a*(b+c)
                a = value.left.left
                b = value.left.right
                c = value.right
                ans = a*c + b*c
                return ans.eval()

    @classmethod
    def var_add_check(cls, value: AbstractAdd):
        if not isinstance(value, AbstractAdd):
            return False
        if isinstance(value.left, AbstractMul) and isinstance(value.right, AbstractMul):
            l = value.left
            r = value.right
            if isinstance(l.left,Variable) and not isinstance(l.right,Variable) and isinstance(r.left,Variable) and not isinstance(r.right,Variable):
                if l.left==r.left:
                    return True
            if isinstance(l.left,Variable) and not isinstance(l.right,Variable) and not isinstance(r.left,Variable) and isinstance(r.right,Variable):
                if l.left==r.right:
                    return True
            if not isinstance(l.right,Variable) and isinstance(l.right,Variable) and isinstance(r.left,Variable) and not isinstance(r.right,Variable):
                if l.right==r.left:
                    return True
            if not isinstance(l.left,Variable) and isinstance(l.right,Variable) and not isinstance(r.left,Variable) and isinstance(r.right,Variable):
                if l.right==r.right:
                    return True
        return False

    @classmethod
    def var_add(cls, value: AbstractAdd):
        if isinstance(value.left, AbstractMul) and isinstance(value.right, AbstractMul):
            l = value.left
            r = value.right
            if isinstance(l.left,Variable) and not isinstance(l.right,Variable) and isinstance(r.left,Variable) and not isinstance(r.right,Variable):
                if l.left==r.left:
                    return ((l.right+r.right).eval()*l.left)
            if isinstance(l.left,Variable) and not isinstance(l.right,Variable) and not isinstance(r.left,Variable) and isinstance(r.right,Variable):
                if l.left==r.right:
                    return ((l.right+r.left).eval()*l.left)
            if not isinstance(l.right,Variable) and isinstance(l.right,Variable) and isinstance(r.left,Variable) and not isinstance(r.right,Variable):
                if l.right==r.left:
                    return ((l.left+r.right).eval()*l.right)
            if not isinstance(l.left,Variable) and isinstance(l.right,Variable) and not isinstance(r.left,Variable) and isinstance(r.right,Variable):
                if l.right==r.right:
                    return ((l.left+r.left).eval()*l.right)
        return value


class Monoid(Law):
    @classmethod
    def eq(cls, left: AbstractBinOperator,right: AbstractBinOperator):
        return (left.left == right.left and left.right == right.right)

    @classmethod
    def has_identity_element(cls):
        return True

    @classmethod
    def has_inverse(cls):
        return False


class CommutativeMonoid(Law):
    @classmethod
    def eq(cls, left,right):
        return CommutativeLaw.eq(left,right)


class Group(Law):
    @classmethod
    def has_inverse(cls):
        return True

    @classmethod
    def has_identity_element(cls):
        return True



class AbelianGroup(Group):
    @classmethod
    def eq(cls,left,right):
        return CommutativeLaw.eq(left,right)















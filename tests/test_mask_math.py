from src.mask_math.formula import *
from src.mask_math.abstract_number import Integer

def test_z():
    a = Z(3)
    b = Z(-5)
    c = (a+b).eval()
    assert c == Z(-2)
    c = (a-b).eval()
    assert c == Z(8)
    c = (a*b).eval()
    assert c == Z(-15)
    c = (a/b).eval()
    assert c == Q(-3,5)
    a = Z(0)
    x = Var("x", Integer)
    c = (a+x).eval()
    print(c)
    assert c == Var("x", Integer)


def test_q():
    a = Q(3,1)
    a = a.eval()
    assert a == Z(3)
    a = Q(3,4)
    b = Q(5,-6)
    c = (a+b).eval()
    assert c == Q(-1,12)
    c = (a-b).eval()
    assert c == Q(19,12)
    c = (a*b).eval()
    assert c == Q(-5,8)
    c = (a/b).eval()
    assert c == Q(-9,10)


def test_z_q():
    a = Z(2)
    b = Q(3,4)
    c = (a+b).eval()
    assert c == Q(11,4)
    c = (a-b).eval()
    assert c == Q(5,4)
    c = (a*b).eval()
    assert c == Q(3,2)
    c = (a/b).eval()
    assert c == Q(8,3)


def test_q_z():
    a = Q(3,-4)
    b = Z(2)
    c = (a+b).eval()
    assert c == Q(5,4)
    c = (a-b).eval()
    assert c == Q(-11,4)
    c = (a*b).eval()
    assert c == Q(-3,2)
    c = (a/b).eval()
    assert c == Q(-3,8)


def test_Neg():
    a = Q(2,3)
    a = ---a
    a = a.eval()
    assert a == Q(-2,3)


def test_CZ():
    a = CZ(2,3)


def test_var_xx():
    x = Var("x")
    y = Var("x")
    b = x==y
    assert b==True


def test_var_xy():
    x = Var("x")
    y = Var("y")
    b = x==y
    assert b==False
    z = x*y
    z = z.eval()
    assert z==Mul(Var("x"),Var("y"))
    assert z==Mul(Var("y"),Var("x"))
    z = Var("z")
    a = (x*y/z).eval()
    b = Div(Mul(Var("x"),Var("y")),Var("z"))
    assert a==b
    v = Var("v")
    a = (x/y)*(z/v)
    assert a==Mul(Div(Var("x"),Var("y")),Div(Var("z"),Var("v")))
    assert a==Mul(Div(Var("z"),Var("v")),Div(Var("x"),Var("y")))
    a = a.eval()
    assert a==Div(Mul(Var("x"),Var("v")),Mul(Var("y"),Var("z")))
    assert a==Div(Mul(Var("v"),Var("x")),Mul(Var("z"),Var("y")))


def test_var_add():
    x = Var("x")
    a = x+x
    assert a==Add(Var("x"),Var("x"))
    a = a.eval()
    assert a==Add(Z(2),Var("x"))





from src.mask_math.formula import *
from src.mask_math.abstract_number import RealNumber

def test_div_z_z():
    a = Q(2,-3)
    assert a.numerator == 2
    assert a.denominator == -3
    a = a.eval()
    assert a.numerator == -2
    assert a.denominator == 3


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





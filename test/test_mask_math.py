from src.mask_math.formula import *


def test_div_z_z():
    a = Q(2,-3)
    assert a.numerator == 2
    assert a.denominator == -3
    a = a.eval()
    assert a.numerator == -2
    assert a.denominator == 3


def test_Neg():
    a = Div(2,3)
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
    z = Var("z")
    a = (x*y/z).eval()
    assert a==Div(Mul(Var("x"),Var("y")),Var("z"))
    v = Var("v")
    a = (x/y)*(z/v)
    assert a==Mul(Div(Var("x"),Var("y")),Div(Var("z"),Var("v")))
    a = a.eval()
    assert a==Div(Mul(Var("x"),Var("v")),Mul(Var("y"),Var("z")))







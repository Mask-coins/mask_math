from src.mask_math.formula import *


def test_div_z_z():
    a = Div(2,-3)
    assert a.left == Z(-2)
    assert a.right == Z(3)


def test_var_x_x():
    x = Var("x")
    y = Var("x")
    assert (x==y)==True






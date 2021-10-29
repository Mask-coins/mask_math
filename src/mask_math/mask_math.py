import numpy as np


def collatz_calc(n:int):
    if n % 2 == 0:
        return n//2
    return 3*n+1


def collatz_count(num:int):
    n = num
    count = 0
    while n > 1:
        count += 1
        n = collatz_calc(n)
    return count


def complex_plane(
        width=100,
        height=100,
        center_real=0,
        center_imag=0,
        zoom=1,
        symmetric=True,
        zeros=False) -> np.ndarray:
    start_real = 0
    start_imag = 0
    if symmetric:
        start_real = -width
        start_imag = -height
    if zeros:
        return np.zeros((height-start_imag+1,width-start_real+1), dtype=complex)
    axis_r = np.arange(start=start_real,stop=width+1,step=1).reshape((1,-1))
    axis_i = -1.j*np.arange(start=start_imag,stop=height+1,step=1).T.reshape((-1,1))
    return (axis_i+axis_r)/zoom+center_real+center_imag*1.j




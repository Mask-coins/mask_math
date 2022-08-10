
# mask_math

今のところ3つのモジュールから成ってます

* mask_math : 私がよく使いまわす数学・アルゴリズムを集めたものです。（思いついたら逐次追加）
* formula : 近似的な計算をしないまま、できるだけ数式的な計算をするものです。（実装中）
* fractal : マンデルブロ集合とかを表示させるものです

# Requirement

numpy
setuptools
opencv-python
Pillow
matplotlib

# Installation


```bash
pip install git+https://github.com/Mask-coins/mask_math
```

# Usage

## formula

整数を定義
```bash
from mask_math import formula

a = Z(4)
```

変数・文字を定義
```bash
from mask_math import formula

x = Var("x")
```
分数を定義（a,bともに同じ結果になります）
```bash
from mask_math import formula

a = Q(1,-2)
a = a.eval()
b = Z(-1)/Z(2)
b = b.eval()
```




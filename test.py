from funciones import replaceExpressions

# Num -> Dig*
# Dig -> o|1|2..|9
# Exp -> Exp2*Exp3
# Exp2 -> a
# 
from pprint import pprint


def test(arr):
    ret = replaceExpressions(arr)
    return ret


if __name__ == '__main__':
    arr = []
    arr.append("Num -> Dig*")
    arr.append("Dig -> o|1|2..|9")
    arr.append("Exp -> Exp2*Exp3")
    arr.append("Exp2 -> a")
    pprint(arr)
    pprint(test(arr))
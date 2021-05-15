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
    arr.append("EXP4 -> c")
    arr.append("EXP3 -> b|EXP4")
    arr.append("NUM -> DIG*")
    arr.append("EXP1 -> EXP2*EXP3")
    arr.append("EXP2 -> a")
    arr.append("DIG -> 0|1|2|3|4|5|6|7|8|9|EXP1|EXP2")

    arr = []
    arr.append('C -> D')
    arr.append('F -> 01+')
    arr.append('A -> B')
    arr.append('B -> C')
    arr.append('D -> E')
    arr.append('E -> F')

    for exp in arr: print(exp)
    print()

    for exp in test(arr): print(exp)
    print()

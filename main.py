from automata import NFA, DFA
from funciones import add_concat_op, conv_rangos, regex_to_nfa, nfa_to_dfa, replaceExpressions

alpha = input('Alfabeto: ')
n = int(input('Número de definiciones regulares: '))
print()

print('Ingrese las %d definiciones regulares.' % n)
defs_regs = [ input() for i in range(n) ]
defs_regs = replaceExpressions(defs_regs)

regexs = []
for def_reg in defs_regs:
    nombre = def_reg[:(def_reg.index('->') - 1)]
    regex = def_reg[(def_reg.index('->') + 3):]
    regex = conv_rangos(regex)
    regex = add_concat_op(regex, alpha)
    regexs.append({
        'nombre': nombre,
        'regex': regex,
        'dfa': nfa_to_dfa(regex_to_nfa(regex))
    })
print()

cadena = input('Ingrese la cadena a analizar:\n')
print()
for lexema in cadena.split():
    match = False
    for regex in regexs:
        if regex['dfa'].test(lexema):
            match = True
            print(lexema + ' -> ' + regex['nombre'])
            break
    if not match:
        print(lexema + ' -> ??')
print()

regexs[0]['dfa'].print()

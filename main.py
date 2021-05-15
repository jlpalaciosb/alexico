from automata import NFA, DFA
from funciones import add_concat_op, conv_rangos, regex_to_nfa, nfa_to_dfa


alpha = input('Alfabeto: ')
n = int(input('Número de definiciones regulares: '))
print()


regexs = []
print('Ingrese las %d definiciones regulares.' % n)
for i in range(n):
    def_reg = input()
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


cadena = input('Ingrese la cadena.\n')
print()
for lexema in cadena.split():
    match = False
    for regex in regexs:
        if regex['dfa'].test(lexema):
            match = True
            print(lexema + ' -> ' + regex['nombre'], end='\n\n')
            break
    if not match:
        print(lexema + ' → <<unknown>>', end='\n\n')

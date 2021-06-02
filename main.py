from funciones import regex_to_nfa, nfa_to_dfa, add_concat_op, conv_rangos, replaceExpressions


# input del usuario
alpha = input('Alfabeto: ')
n = int(input('Número de definiciones regulares: '))
print()
print('Ingrese las %d definiciones regulares.' % n)
defs_regs = [ input() for i in range(n) ]


# preprocesamientos y construcción de los nfas y dfas
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
        'nfa': regex_to_nfa(regex),
        'dfa': nfa_to_dfa(regex_to_nfa(regex))
    })
print()


# construir dfa final
nfa_final = None
for regex in regexs:
    if nfa_final is None:
        nfa_final = regex['nfa']
    else:
        nfa_final = nfa_final.orr(regex['nfa'])
dfa_final = nfa_to_dfa(nfa_final)
print('<< DFA FINAL >>')
dfa_final.print()
print()


# análisis léxico
cadena = input('Ingrese la cadena a analizar:\n')
print()
print('<< TABLA DE SÍMBOLOS >>')
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

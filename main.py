from automata import NFA, DFA, regex_to_nfa, add_concat_op, conv_rangos

alpha = input('Alfabeto: ')
n = int(input('Número de regexs: '))
print()

regexs = []
for i in range(n):
    nombre = input('Nombre regex %d: ' % (i + 1))
    regex = input('Definición regex %d: ' % (i + 1))
    regex = conv_rangos(regex)
    regex = add_concat_op(regex, alpha)
    print()
    regexs.append({
        'nombre': nombre,
        'regex': regex,
        'dfa': regex_to_nfa(regex).to_dfa()
    })

cadena = input('CADENA: ')
print()

for lexema in cadena.split():
    flag = False
    for regex in regexs:
        if regex['dfa'].test(lexema):
            flag = True
            print(lexema + ' → ' + regex['nombre'], end='\n\n')
            break
    if not flag:
        print(lexema + ' → <<unknown>>', end='\n\n')

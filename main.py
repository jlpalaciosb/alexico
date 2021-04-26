alpha = input('Alfabeto: ')
n = int(input('Número de regexs: ')); print()

regexs = []
for i in range(n):
    nombre = input('Nombre regex %d: ' % (i + 1))
    regex = input('Definición regex %d: ' % (i + 1)); print()
    regexs.append({'nombre': nombre, 'regex': regex})

cadena = input('CADENA: '); print()

def match(regex, lexema):
    return False

for lexema in cadena.split():
    flag = False
    for regex in regexs:
        if match(regex['regex'], lexema):
            flag = True
            print(lexema + ' → ' + regex['nombre'], end='\n\n')
            break
    if not flag:
        print(lexema + ' → <<unknown>>', '\n\n')

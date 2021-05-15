from automata import NFA, DFA


def add_concat_op(regex, alpha):
    ret = regex[0]
    for i in range(1, len(regex)):
        prev = regex[i - 1]
        curr = regex[i]
        if (curr in alpha or curr == '(' or curr == 'E') and (prev != '(' and prev != '|'):
            ret += '.'
        ret += curr
    return ret


def conv_rangos(regex):
    ret = ''
    i = 0
    while i < len(regex):
        ch = regex[i]
        if ch == '[':
            ch1 = regex[i+1]
            ch2 = regex[i+3]
            ret += '('
            ret += ch1
            for j in range(ord(ch1) + 1, ord(ch2) + 1):
                ret += '|'+chr(j)
            ret += ')'
            i += 5
        else:
            ret += ch
            i += 1
    return ret


def elim_parent(regex):
    if regex[0] == '(':
        c = 1
        i = 1
        while i < len(regex):
            if regex[i] == '(':
                c += 1
            elif regex[i] == ')':
                c -= 1
            if c == 0:
                break
            i += 1
        if i == (len(regex) - 1):
            return regex[1:-1]
        else:
            return regex
    else:
        return regex


def char_split(regex, char):
    poss = []

    c = 0
    for i in range(len(regex)):
        ch = regex[i]
        if ch == '(':
            c += 1
        elif ch == ')':
            c -= 1
        elif ch == char and c == 0:
            poss.append(i)
    
    ret = []
    r = ''
    for i in range(len(regex)):
        if i in poss:
            ret.append(r)
            r = ''
        else:
            r += regex[i]
    ret.append(r)
    
    return ret
    

def regex_to_nfa(regex):
    while regex != elim_parent(regex):
        regex = elim_parent(regex)

    if len(regex) == 1:
        return NFA.char(regex)
    
    or_split = char_split(regex, '|')
    if len(or_split) > 1:
        nfa = regex_to_nfa(or_split[0])
        for r in or_split[1:]:
            nfa = nfa.orr(regex_to_nfa(r))
        return nfa

    concat_split = char_split(regex, '.')
    if len(concat_split) > 1:
        nfa = regex_to_nfa(concat_split[0])
        for r in concat_split[1:]:
            nfa = nfa.concat(regex_to_nfa(r))
        return nfa

    if regex[-1] == '?':
        nfa = regex_to_nfa(regex[:-1])
        return nfa.opt()
    
    if regex[-1] == '*':
        nfa = regex_to_nfa(regex[:-1])
        return nfa.kleene()
    
    if regex[-1] == '+':
        nfa = regex_to_nfa(regex[:-1])
        return nfa.plus()
    
    raise Exception('nfa to regex error')


# agregar 0' ---E---> 0
def extra_initial_state(nfa):
    ret = NFA()
    ret.symbols = list(nfa.symbols)
    ret.num_states = nfa.num_states + 1
    for s in nfa.accepting_states:
        ret.accepting_states.append(s + 1)
    ret.transition_functions.append([0, 'E', 1])
    for tf in nfa.transition_functions:
        ret.transition_functions.append([tf[0] + 1, tf[1], tf[2] + 1])
    return ret


def nfa_to_dfa(nfa):
    nfa = extra_initial_state(nfa) # asegura un solo init_state y init_state=0
    dfa = DFA()
    dfa.symbols = list(nfa.symbols)

    d_estados = [nfa.e_cerradura([0])]
    i = 0
    while i < len(d_estados):
        t = d_estados[i]
        for a in nfa.symbols:
            u = nfa.e_cerradura(nfa.mover(t, a))
            if u == []: continue
            if u not in d_estados:
                d_estados.append(u)
            j = d_estados.index(u)
            dfa.transition_functions.append([i, a, j])
        i += 1

    dfa.num_states = len(d_estados)
    for ds in d_estados:
        if list(set(ds) & set(nfa.accepting_states)) != []:
            dfa.accepting_states.append(d_estados.index(ds))
    return dfa


def replaceExpressions(arr_exp):
    arr_exp = list(map(leftStrip,arr_exp))
    arr_exp = list(map(rightStrip,arr_exp))
    output_list = list(map(saveToDic, arr_exp))   
    search_and_replace(output_list)
    ret = search_and_replace(output_list)  
    return list(map(formatExp,ret))   


def formatExp(dic):
    return '--'.join('{} -> {}'.format(key, value) for key, value in dic.items())


def saveToDic(str_exp):
    arr_items = str_exp.split(' ')
    dic_exp = {}
    dic_exp[arr_items[0]] = arr_items[2]
    return dic_exp


def leftStrip(exp):
    return exp.lstrip()


def rightStrip(exp):
    return exp.rstrip()


def search_and_replace(arr_exp):
    for val in arr_exp:
        for val_in in arr_exp:
            aux_1 = list(val.keys())[0]
            aux_2 = list(val_in.keys())[0]
            if aux_1!=aux_2:
                if str(list(val.keys())[0]) in str(list(val_in.values())[0]):
                    aux = str(list(val_in.values())[0]).replace(
                        str(list(val.keys())[0]),
                        '('+str(list(val.values())[0])+')'
                    )                    
                    val_in[str(list(val_in.keys())[0])]=aux
    return arr_exp

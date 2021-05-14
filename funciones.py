from automata import NFA

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

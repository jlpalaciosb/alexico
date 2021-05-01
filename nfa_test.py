from automata import NFA

# nfa = NFA()

# nfa.symbols = ['a', 'b']
# nfa.num_states = 11
# nfa.accepting_states = [10]
# nfa.transition_functions.append([0, 'E', 1])
# nfa.transition_functions.append([0, 'E', 7])
# nfa.transition_functions.append([1, 'E', 2])
# nfa.transition_functions.append([1, 'E', 4])
# nfa.transition_functions.append([2, 'a', 3])
# nfa.transition_functions.append([3, 'E', 6])
# nfa.transition_functions.append([4, 'b', 5])
# nfa.transition_functions.append([5, 'E', 6])
# nfa.transition_functions.append([6, 'E', 1])
# nfa.transition_functions.append([6, 'E', 7])
# nfa.transition_functions.append([7, 'a', 8])
# nfa.transition_functions.append([8, 'b', 9])
# nfa.transition_functions.append([9, 'b', 10])
# nfa.print()

# nfa1=NFA()
# nfa1.num_states=3
# nfa1.symbols=['a']
# nfa1.transition_functions=[[0,'E',1],[0,'a',2]]
# nfa1.accepting_states=[2]
# nfa1.print()

# nfa2=NFA()
# nfa2.num_states=3
# nfa2.symbols=['b']
# nfa2.transition_functions=[[0,'b',1],[0,'b',2],[2,'b',1]]
# nfa2.accepting_states=[1]
# nfa2.print()

# nfa_concat = nfa1.concat(nfa2)
# nfa_concat.print()

# nfa_or=nfa1.orr(nfa2)
# nfa_or.print()

# nfa_or.kleene().print()

#nfa = NFA.char('a').concat(NFA.char('c').orr(NFA.char('d').kleene()))
# nfa = NFA.char('E').concat(NFA.char('a')).concat(NFA.char('E')).concat(NFA.char('E')).concat(NFA.char('c').kleene().concat(NFA.char('c'))).concat(NFA.char('E'))

# a ( [ a-e ]* a )?
nfa = NFA.char('a').concat(
    (
        (
            NFA.char('a').orr(NFA.char('b')).orr(NFA.char('c')).orr(NFA.char('d')).orr(NFA.char('e'))
        ).kleene().concat(NFA.char('a'))
    ).orr(NFA.char('E'))
)

dfa = nfa.to_dfa()
dfa.print()
print(dfa.test('a'))

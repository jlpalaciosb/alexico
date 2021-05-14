class NFA:
    def __init__(self):
        self.symbols = []
        self.num_states = 0 # Ej.: 3 then 0, 1, 2; start state is always 0
        self.accepting_states = []
        self.transition_functions = []
    
    @staticmethod
    def char(c):
        ret = NFA()
        if c != 'E':
            ret.symbols = [c]
        ret.num_states = 2
        ret.accepting_states = [1]
        ret.transition_functions = [[0, c, 1]]
        return ret
    
    def e_cerradura(self, t):
        ret = []
        for s in t: ret.append(s)
        i = 0
        while i < len(ret):
            s = ret[i]
            for tf in self.transition_functions:
                if tf[0] == s and tf[1] == 'E' and tf[2] not in ret:
                    ret.append(tf[2])
            i += 1
        return ret
    
    def mover(self, t, a):
        ret = []
        for tf in self.transition_functions:
            if tf[0] in t and tf[1] == a and tf[2] not in ret:
                ret.append(tf[2])
        return ret
    
    def concat(self, nfa2):
        nfa1 = self
        ret = NFA()
        ret.symbols = list(set(nfa1.symbols) | set(nfa2.symbols))
        ret.num_states = nfa1.num_states + nfa2.num_states
        for tf in nfa1.transition_functions:
            ret.transition_functions.append(tf)
        for tf in nfa2.transition_functions:
            ret.transition_functions.append([tf[0] + nfa1.num_states, tf[1], tf[2] + nfa1.num_states])
        for s in nfa1.accepting_states:
            ret.transition_functions.append([s, 'E', 0 + nfa1.num_states])
        for s in nfa2.accepting_states:
            ret.accepting_states.append(s + nfa1.num_states)
        return ret
    
    def orr(self, nfa2):
        nfa1 = self
        ret = NFA()
        ret.symbols = list(set(nfa1.symbols) | set(nfa2.symbols))
        ret.num_states = nfa1.num_states + nfa2.num_states + 2
        ret.accepting_states = [ret.num_states - 1]
        ret.transition_functions.append([0, 'E', 0 + 1])
        ret.transition_functions.append([0, 'E', 0 + nfa1.num_states + 1])
        for tf in nfa1.transition_functions:
            ret.transition_functions.append([tf[0] + 1, tf[1], tf[2] + 1])
        for tf in nfa2.transition_functions:
            ret.transition_functions.append([tf[0] + nfa1.num_states + 1, tf[1], tf[2] + nfa1.num_states + 1])
        for s in nfa1.accepting_states:
            ret.transition_functions.append([s + 1, 'E', ret.num_states - 1])
        for s in nfa2.accepting_states:
            ret.transition_functions.append([s + nfa1.num_states + 1, 'E', ret.num_states - 1])
        return ret
    
    def kleene(self):
        ret = NFA()
        ret.symbols = list(self.symbols)
        ret.num_states = self.num_states + 2
        ret.accepting_states = [ret.num_states - 1]
        ret.transition_functions.append([0, 'E', 0 + 1])
        ret.transition_functions.append([0, 'E', ret.num_states - 1])
        for s in self.accepting_states:
            ret.transition_functions.append([s + 1, 'E', 0 + 1])
            ret.transition_functions.append([s + 1, 'E', ret.num_states - 1])
        for tf in self.transition_functions:
            ret.transition_functions.append([tf[0] + 1, tf[1], tf[2] + 1])
        return ret
    
    def opt(self):
        return self.orr(NFA.char('E'))
    
    def plus(self):
        return self.concat(self.kleene())
    
    # agregar 0' ---E---> 0
    def extra_initial_state(self):
        ret = NFA()
        ret.symbols = list(self.symbols)
        ret.num_states = self.num_states + 1
        for s in self.accepting_states:
            ret.accepting_states.append(s + 1)
        ret.transition_functions.append([0, 'E', 1])
        for tf in self.transition_functions:
            ret.transition_functions.append([tf[0] + 1, tf[1], tf[2] + 1])
        return ret
    
    def to_dfa(self):
        nfa = self.extra_initial_state() # asegura un solo init_state y init_state=0
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

    def print(self):
        print('Symbols → ' + str(self.symbols))
        print('States → ' + str(list(range(self.num_states))))
        print('StartState → ' + str(0))
        print('AcceptingStates → ' + str(self.accepting_states))
        print('TransitionFunctions → ' + str(self.transition_functions))


# igual a NFA por que un DFA es tambien un NFA
class DFA:
    def __init__(self):
        self.symbols = []
        self.num_states = 0 # Ej.: 3 then 0, 1, 2; start state is always 0
        self.accepting_states = []
        self.transition_functions = []
    
    def test(self, str):
        s = 0
        i = 0
        while i < len(str) and s is not None:
            a = str[i]
            next_s = None
            for tf in self.transition_functions:
                if tf[0] == s and tf[1] == a:
                    next_s = tf[2]
                    break
            s = next_s
            i += 1
        return s in self.accepting_states
    
    def print(self):
        print('Symbols → ' + str(self.symbols))
        print('States → ' + str(list(range(self.num_states))))
        print('StartState → ' + str(0))
        print('AcceptingStates → ' + str(self.accepting_states))
        print('TransitionFunctions → ' + str(self.transition_functions))

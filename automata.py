class NFA:
    def __init__(self):
        self.symbols = []
        self.num_states = 0 # Ej.: 3 then 0, 1, 2; start state is always 0
        self.accepting_states = []
        self.transition_functions = []

    def print(self):
        print('Symbols → ' + str(self.symbols))
        print('States → ' + str(list(range(self.num_states))))
        print('StartState → ' + str(0))
        print('AcceptingStates → ' + str(self.accepting_states))
        print('TransitionFunctions → ' + str(self.transition_functions))
    
    @staticmethod
    def char(c):
        ret = NFA()
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


class DFA:
    def __init__(self):
        self.num_states = 0
        self.symbols = []
        self.num_accepting_states = 0
        self.accepting_states = []
        self.start_state = 0
        self.transition_functions = []
        self.q = []
    
    
    def convert_from_nfa(self, nfa):
        self.symbols = nfa.symbols
        self.start_state = nfa.start_state

        nfa_transition_dict = {}
        dfa_transition_dict = {}
        
        # Combine NFA transitions
        for transition in nfa.transition_functions:
            starting_state = transition[0]
            transition_symbol = transition[1]
            ending_state = transition[2]
            
            if (starting_state, transition_symbol) in nfa_transition_dict:
                nfa_transition_dict[(starting_state, transition_symbol)].append(ending_state)
            else:
                nfa_transition_dict[(starting_state, transition_symbol)] = [ending_state]

        self.q.append((0,))
        
        # Convert NFA transitions to DFA transitions
        for dfa_state in self.q:
            for symbol in nfa.symbols:
                if len(dfa_state) == 1 and (dfa_state[0], symbol) in nfa_transition_dict:
                    dfa_transition_dict[(dfa_state, symbol)] = nfa_transition_dict[(dfa_state[0], symbol)]
                    
                    if tuple(dfa_transition_dict[(dfa_state, symbol)]) not in self.q:
                        self.q.append(tuple(dfa_transition_dict[(dfa_state, symbol)]))
                else:
                    destinations = []
                    final_destination = []
                    
                    for nfa_state in dfa_state:
                        if (nfa_state, symbol) in nfa_transition_dict and nfa_transition_dict[(nfa_state, symbol)] not in destinations:
                            destinations.append(nfa_transition_dict[(nfa_state, symbol)])
                    
                    if not destinations:
                        final_destination.append(None)
                    else:  
                        for destination in destinations:
                            for value in destination:
                                if value not in final_destination:
                                    final_destination.append(value)
                        
                    dfa_transition_dict[(dfa_state, symbol)] = final_destination
                        
                    if tuple(final_destination) not in self.q:
                        self.q.append(tuple(final_destination))

        # Convert NFA states to DFA states            
        for key in dfa_transition_dict:
            self.transition_functions.append((self.q.index(tuple(key[0])), key[1], self.q.index(tuple(dfa_transition_dict[key]))))
        
        for q_state in self.q:
            for nfa_accepting_state in nfa.accepting_states:
                if nfa_accepting_state in q_state:
                    self.accepting_states.append(self.q.index(q_state))
                    self.num_accepting_states += 1


    def print_dfa(self):
        print(len(self.q))
        print("".join(self.symbols))
        print(str(self.num_accepting_states) + " " + " ".join(str(accepting_state) for accepting_state in self.accepting_states))
        print(self.start_state)
        
        for transition in sorted(self.transition_functions):
            print(" ".join(str(value) for value in transition))

import random

from table import Table

class EpsilonGreedy():
    def __init__(self,epsilon):
        self.epsilon=epsilon
        
    def select_action(self,state,table:Table):
        if random.random()>self.epsilon:
            #random
            return random.choice(table.get_all_actions())
        else:
            #greedy
            return table.get_optimal_action(state=state)
        pass

class QWeightedGreedy():
    def select_action(self,state,table:Table):
        actions,values=zip(*table.get_q_values_with_state(state=state))
        
        min_value=min(values)
        non_negative_values=[value-min_value for value in values]
        sum_non_negative_values=sum(non_negative_values)
        action_probs=[value/sum_non_negative_values for value in values]
        
        return random.choices(actions,weights=action_probs)
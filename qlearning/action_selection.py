import random

from table import Table

class EpsilonGreedy():
    """This class implements the common way for balance between exploration and exploitation. Choose an epsilon value, smaller gives more randomized decisions."""

    def __init__(self,epsilon):
        self.epsilon=epsilon
        
    def select_action(self,state,table:Table,possible_actions):
        """This method makes a decision with implemented Epsilon-Greedy, with some probability it makes randomly choose an action from given possible_actions and with some probability it gives the most optimal action with respect to given Table object table. State is used for choosing corresponding best action."""
        if random.random()>self.epsilon:
            #random
            return random.choice(possible_actions)
        else:
            #greedy
            return table.get_optimal_action(state=state)
        pass

#Not implemented.
class QWeightedGreedy():
    def select_action(self,state,table:Table):
        actions,values=zip(*table.get_q_values_with_state(state=state))
        
        min_value=min(values)
        non_negative_values=[value-min_value for value in values]
        sum_non_negative_values=sum(non_negative_values)
        action_probs=[value/sum_non_negative_values for value in values]
        
        return random.choices(actions,weights=action_probs)
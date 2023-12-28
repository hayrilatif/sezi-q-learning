import json

class Table():
    """This class can be used for store Q values of reinforcement learning tasks with discrete observation and action space.
    Access values with object:Table[*state*,*action*]. You can access values directly with passing states and actions itself. The Table will automatically create an state to id mapping and use it for value indexing. Fast an easy way for accessing q values."""


    def __init__(self):
        """Constructer-like method for creating Table object."""
        self.__table_dictionary={}
        self.__state_id_pairs=[]
        self.__action_id_pairs=[]
    
    def save_table(self,path:str):
        """This is a method for saving this table as json text. Give it a path:str to save."""

        file=open(path,"w+")
        file.write(json.dumps({"__table_dictionary":self.__table_dictionary,
                               "__state_id_pairs":self.__state_id_pairs,
                               "__action_id_pairs":self.__action_id_pairs}))
        file.close()
        
    def load_table(self,path:str):
        """This is a method for loading Table object from the given path:str."""

        file=open(path,"r+")
        obj=json.loads(file.read())
        
        self.__table_dictionary=obj["__table_dictionary"]
        self.__state_id_pairs=obj["__state_id_pairs"]
        self.__action_id_pairs=obj["__action_id_pairs"]

    def build_table(self,observation_space,action_space):
        """Use this method before the required table access before setting values. observation_space:|The iterable of any kind. It is representing the probable observations|, action_space:|The iterable of any kind. It is representing the probable actions.|"""

        for observation in observation_space:
            for action in action_space:
                self[observation,action]=0
    
    def get_q_values_with_state(self,state):
        """Use this method for access all Q values that linked to given state. You will get all actions Qs with given state. state:|Any kind of object.|"""

        keys,values=zip(*self.__filter_value_wrt_action_or_state(state=state))
        actions=list(map(self.__action_id_pairs[lambda x:int(x.split("-")[0])],keys))
        return zip(actions,values)

    def get_optimal_action(self,state):
        """Use this method for find the most rewarding action. state:|Any kind of object.|"""
        
        keys,values=list(zip(*self.__filter_value_wrt_action_or_state(state=state)))
        
        return self.__action_id_pairs[int(keys[values.index(max(values))].split("-")[0])]

    def get_all_actions(self):
        """Use this method to get all possible actions from the table."""

        return self.__action_id_pairs
    
    def get_all_states(self):
        """Use this method to get all possible states from the table."""

        return self.__state_id_pairs
    
    def get_minimum_wrt_action_or_state(self,**kwargs):
        """Use this method to get minimum value with given action or state. Use *state* or *action* only."""

        return min(list(zip(*self.__filter_value_wrt_action_or_state(**kwargs)))[-1])
    
    def get_maximum_wrt_action_or_state(self,**kwargs):
        """Use this method to get maximum value with given action or state. Use *state* or *action* only."""
        
        return max(list(zip(*self.__filter_value_wrt_action_or_state(**kwargs)))[-1])
    
    #Not implemented.
    def __repr__(self) -> str:
        t="     "
        for action in self.__action_id_pairs:
            for state in self.__state_id_pairs:
                t+=str(self[state,action])+"\n"
        
        return t

    #Filter the values with given state or action. For example if we have state "a", this method gives q values across all actions corresponded to state "a". 
    def __filter_value_wrt_action_or_state(self,**kwargs)->list:
        value_list=[]
        
        if "action" in kwargs.keys():
            search_id=self.__get_action_id(kwargs["action"])
            
            for key in self.__table_dictionary.keys():
                action_id,state_id=key.split("-")
                if search_id == int(action_id): value_list.append((key,self.__table_dictionary[key]))
                
            pass
        elif "state" in kwargs.keys():
            search_id=self.__get_state_id(kwargs["state"])
            
            for key in self.__table_dictionary.keys():
                action_id,state_id=key.split("-")
                if search_id == int(state_id): value_list.append((key,self.__table_dictionary[key]))
            
            pass
        return value_list
    
    #Returns id of the state.
    def __get_state_id(self,state)->int:
        
        if state in self.__state_id_pairs:
            return self.__state_id_pairs.index(state)
        else:
            self.__state_id_pairs.append(state)
            return self.__get_state_id(state)
        
    #Returns id of the action.
    def __get_action_id(self,action)->int:
        if action in self.__action_id_pairs:
            return self.__action_id_pairs.index(action)
        else:
            self.__action_id_pairs.append(action)
            return self.__get_action_id(action)
        
    #Class direct accessor.    
    def __getitem__(self,items):
        state,action=items
        path=f"{self.__get_action_id(action)}-{self.__get_state_id(state)}"
        if path not in self.__table_dictionary.keys():self.__table_dictionary[path]=0
        return self.__table_dictionary.get(path)
    
    #Class direct accessor.
    def __setitem__(self,items,new):
        state,action=items
        path=f"{self.__get_action_id(action)}-{self.__get_state_id(state)}"
        self.__table_dictionary[path]=new
        
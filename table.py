import json

class Table():
    def __init__(self):
        self.__table_dictionary={}
        self.__state_id_pairs=[]
        self.__action_id_pairs=[]
    
    #Not implemented.
    def __repr__(self) -> str:
        t="     "
        for action in self.__action_id_pairs:
            for state in self.__state_id_pairs:
                t+=str(self[state,action])+"\n"
        
        return t
    
    def save_table(self,path:str):
        file=open(path,"w+")
        file.write(json.dumps({"__table_dictionary":self.__table_dictionary,
                               "__state_id_pairs":self.__state_id_pairs,
                               "__action_id_pairs":self.__action_id_pairs}))
        file.close()
        
    def load_table(self,path:str):
        file=open(path,"r+")
        obj=json.loads(file.read())
        
        self.__table_dictionary=obj["__table_dictionary"]
        self.__state_id_pairs=obj["__state_id_pairs"]
        self.__action_id_pairs=obj["__action_id_pairs"]
    
    def build_table(self,observattion_space,action_space):
        for observation in observattion_space:
            for action in action_space:
                self[observation,action]=0
    
    def get_q_values_with_state(self,state):
        keys,values=zip(*self.__filter_value_wrt_action_or_state(state=state))
        actions=list(map(self.__action_id_pairs[lambda x:int(x.split("-")[0])],keys))
        return zip(actions,values)
        
    def get_optimal_action(self,state):
        keys,values=list(zip(*self.__filter_value_wrt_action_or_state(state=state)))
        
        return self.__action_id_pairs[int(keys[values.index(max(values))].split("-")[0])]
    
    def get_all_actions(self):
        return self.__action_id_pairs
    
    def get_all_states(self):
        return self.__state_id_pairs
    
    def get_minimum_wrt_action_or_state(self,**kwargs):
        return min(list(zip(*self.__filter_value_wrt_action_or_state(**kwargs)))[-1])
    
    def get_maximum_wrt_action_or_state(self,**kwargs):
        return max(list(zip(*self.__filter_value_wrt_action_or_state(**kwargs)))[-1])
    
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
    
        """_summary_
        action=[action] for get (key, cumulative rewward) across same action but different states.
        or state=[state]
        """
    
    def __get_state_id(self,state)->int:
        
        if state in self.__state_id_pairs:
            return self.__state_id_pairs.index(state)
        else:
            self.__state_id_pairs.append(state)
            return self.__get_state_id(state)
        
    def __get_action_id(self,action)->int:
        if action in self.__action_id_pairs:
            return self.__action_id_pairs.index(action)
        else:
            self.__action_id_pairs.append(action)
            return self.__get_action_id(action)
        
    def __getitem__(self,items):
        state,action=items
        path=f"{self.__get_action_id(action)}-{self.__get_state_id(state)}"
        if path not in self.__table_dictionary.keys():self.__table_dictionary[path]=0
        return self.__table_dictionary.get(path)
    
    def __setitem(self,items,new):
        state,action=items
        path=f"{self.__get_action_id(action)}-{self.__get_state_id(state)}"
        self.__table_dictionary[path]=new
        
    def __setitem__(self,items,new):
        self.__setitem(items,new)
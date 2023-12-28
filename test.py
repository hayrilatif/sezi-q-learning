import gymnasium as gym
import tqdm

from table import Table
from optimizer import calculate_new_q_value
from action_selection import EpsilonGreedy

#Creating test environment.
env=gym.make("Taxi-v3",render_mode="none")

#Creating table and building it.
table=Table()
table.build_table(list(range(500)),list(range(6)))

#Creating action decision maker class.
greedy=EpsilonGreedy(0.1)


print("---Training---")
for i in range(5000):
    #We gradually increasing the epsilon value. Making it more deterministic and optimal.
    greedy.epsilon=i/5000

    #Getting first state from the environment.
    state, info=env.reset()
    
    #rews for store rewards of every step.
    rews=[]
    for _ in range(201):
        action=greedy.select_action(state,table,[0,1,2,3,4,5])
        #env.render()
        n_state,reward,terminated,truncated,info=env.step(action)
        
        if terminated or truncated:
            break
        
        table[state,action]=calculate_new_q_value(table[state,action],0.01,0.99,reward,table.get_maximum_wrt_action_or_state(state=n_state))
        state=n_state
        
        rews.append(reward)
    
    print(i," ",sum(rews))

#Saves the table.
table.save_table("test_table.json")

#Loads the table.
table.load_table("test_table.json")

print("---Test---")

#Making decision strategy deterministic.
greedy.epsilon=1

for i in range(1000):
    state, info=env.reset()
    rews=[]
    for _ in range(201):
        action=greedy.select_action(state,table,[0,1,2,3,4,5])
        #env.render()
        n_state,reward,terminated,truncated,info=env.step(action)
        
        if terminated or truncated:
            break
        
        table[state,action]=calculate_new_q_value(table[state,action],0.1,0.9,reward,table.get_maximum_wrt_action_or_state(state=n_state))
        state=n_state
        
        rews.append(reward)
    
    print(f"Epoch:{i}, Sum Of Rewards: {sum(rews)}")
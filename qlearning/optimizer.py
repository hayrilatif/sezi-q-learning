def calculate_new_q_value(old_q,learning_rate,discount_factor,reward,new_state_max_q)->float:
    return (old_q*learning_rate)+(1-learning_rate)*(reward+new_state_max_q*discount_factor)
# tag::run_alphago[]
from dlgo.agent import load_prediction_agent, load_policy_agent, AlphaGoMCTS
from dlgo.rl import load_value_agent
import h5py

def main():
    fast_policy = load_prediction_agent(h5py.File('alphago_sl_policy_four_twenty.h5 ', 'r'))
    strong_policy = load_policy_agent(h5py.File('alphago_rl_policy_four_twenty_ten.h5', 'r'))
    value = load_value_agent(h5py.File('alphago_value_four_twenty_ten.h5', 'r'))

    alphago = AlphaGoMCTS(strong_policy, fast_policy, value)
# end::run_alphago[]

if __name__=='__main__':
    main()
# TODO: register in frontend

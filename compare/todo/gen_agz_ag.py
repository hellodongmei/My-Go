#!/usr/bin/env python
# coding=utf-8

import os,sys
import shutil

def write_logfile(filename, content):
    stdout_backup = sys.stdout
    log_file = open(filename, 'a+')
    log_file.close()
    log_file = open(filename, 'a+')
    sys.stdout = log_file
    print(content)
    log_file.close()
    sys.stdout = stdout_backup


num_games_onecpu = 10    # -a parameter
rounds_move = 50 # -c parameter

score_path = '/home/users/l/liudong1/scratch/compare/score/ag_agz' # -d parameter
if not os.path.exists(score_path):
    os.makedirs(score_path)
#     -d parameter 

strong_policy = '/home/users/l/liudong1/scratch/compare/agents/rl_policy_12.h5'
fast_policy = '/home/users/l/liudong1/scratch/compare/agents/ag_fast.h5'
value_net = '/home/users/l/liudong1/scratch/compare/agents/valphago_value_1.h5' 

agent = '/home/users/l/liudong1/scratch/compare/agents/agent_zero_11.h5' # last parameter 

agent_path = '/home/users/l/liudong1/scratch/compare/agents'

# how many cpu cores we ask  (total number of games = num_cpus_request *  num_games_onecpu)
num_cpus_request = 10  

# where the error information of the cpu cores to be stored
err_path = '/home/users/l/liudong1/scratch/compare/stderr/err_ag_12_search_agz' 
if not os.path.exists(err_path):
    os.makedirs(err_path)

# where the print information of the cpu cores to be stored
out_path = '/home/users/l/liudong1/scratch/compare/stdout/out_ag_12_search_agz' 
if not os.path.exists(out_path):
    os.makedirs(out_path)

# where do we store the shell scripts, the number of shell scripts = num_cpus_request
# after generating the shell scripts, we will submit all of them to baobab.
# the template of the shell scripts is shown below
shell_path = '/home/users/l/liudong1/scratch/compare/shells/score_ag_agz'
if not os.path.exists(shell_path):
    os.makedirs(shell_path)


env_path = '/home/users/l/liudong1/workspace/compare/set_env.sh'
python_path = '/home/users/l/liudong1/workspace/compare/b_v_b_ag_agz_search.py'

if os.path.exists(agent_path):

    print('Start to generate %d shell scripts:' % num_cpus_request)

    for i in range(0, num_cpus_request):

        print('\tNo.%d' % (i+1))

        duplicate_agent = agent.replace('.h5', '_agmcts_%d.h5' % (i+1) )
        if not os.path.exists(duplicate_agent):
            shutil.copyfile(agent, duplicate_agent)

        duplicate_strong = strong_policy.replace('.h5', '_agz_%d.h5' % (i+1) )
        if not os.path.exists(duplicate_strong):
            shutil.copyfile(strong_policy, duplicate_strong)

        duplicate_fast = fast_policy.replace('.h5', '_agz_%d.h5' % (i+1) )
        if not os.path.exists(duplicate_fast):
            shutil.copyfile(fast_policy, duplicate_fast)

        duplicate_value = value_net.replace('.h5', '_agz_%d.h5' % (i+1) )
        if not os.path.exists(duplicate_value):
            shutil.copyfile(value_net, duplicate_value)


        shell_name =  '%s/run_ag_agz_compare_%d.sh' % (shell_path, i+1)

        if os.path.exists(shell_name):
            os.remove(shell_name)

        write_logfile(shell_name, '#!/bin/sh\n')

        write_logfile(shell_name, '#SBATCH --cpus-per-task=1')
        write_logfile(shell_name, '#SBATCH --job-name=ag_agz')
        write_logfile(shell_name, '#SBATCH --time=12:00:00')
        write_logfile(shell_name, '#SBATCH --mem=10000')
        write_logfile(shell_name, '#SBATCH --gpus=1')
        write_logfile(shell_name, '##SBATCH --constraint="V5|V6"')
        write_logfile(shell_name, '#SBATCH --partition=shared-gpu\n')

        err_name = '%s/run_ag_agz_%d.err' % (err_path, i+1)
        out_name = '%s/run_ag_agz_%d.out' % (out_path, i+1)
        write_logfile(shell_name, '#SBATCH --error=%s' % err_name)
        write_logfile(shell_name, '#SBATCH --output=%s' % out_name)

        write_logfile(shell_name, '\nsrun echo "Loading libraries."')
        write_logfile(shell_name, 'srun source %s\n' % env_path)
        write_logfile(shell_name, 'srun export PYTHONPATH="/home/users/l/liudong1/workspace/compare:$PYTHONPATH"\n')

        write_logfile(shell_name, 'current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
        write_logfile(shell_name, 'srun echo "Running python scripts on $current_date_time."')
        running_comand = 'srun python %s -a %d -b %d -c %d -d %s %s %s %s %s' % (python_path, num_games_onecpu,  i+1, rounds_move, score_path, duplicate_strong, duplicate_fast, duplicate_value, duplicate_agent)
        write_logfile(shell_name, running_comand)

        write_logfile(shell_name, '\ncurrent_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
        write_logfile(shell_name, 'srun echo "Finished on $current_date_time."')

    print('All generated.')

else:
    print('"%s" is not existing, please double check.' % agent_path)


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


# num_games_onecpu = 10    # -a parameter
# rounds_move = 500 # -c parameter

# score_path = '/home/users/l/liudong1/scratch/compare/score/agagz_ag0' # -d parameter
# if not os.path.exists(score_path):
#     os.makedirs(score_path)
# #     -d parameter 

# strong_policy = '/home/users/l/liudong1/scratch/compare/agents/ag_rl_policy_0.h5'
# fast_policy = '/home/users/l/liudong1/scratch/compare/agents/ag_fast_0.h5'
# value_net = '/home/users/l/liudong1/scratch/compare/agents/valphago_value_1.h5' 

# agent = '/home/users/l/liudong1/scratch/compare/agents/ag_agz.h5' # last parameter 

agent_path = '/home/users/l/liudong1/scratch/compare/agents'

# # how many cpu cores we ask  (total number of games = num_cpus_request *  num_games_onecpu)
# num_cpus_request = 10  

# where the error information of the cpu cores to be stored
err_path = '/home/users/l/liudong1/scratch/compare/stderr/err_ag0_agagz_bot' 
if not os.path.exists(err_path):
    os.makedirs(err_path)

# where the print information of the cpu cores to be stored
out_path = '/home/users/l/liudong1/scratch/compare/stdout/out_ag0_agagz_bot' 
if not os.path.exists(out_path):
    os.makedirs(out_path)

# where do we store the shell scripts, the number of shell scripts = num_cpus_request
# after generating the shell scripts, we will submit all of them to baobab.
# the template of the shell scripts is shown below
shell_path = '/home/users/l/liudong1/scratch/compare/shells/score_agagz_ag0_bot'
if not os.path.exists(shell_path):
    os.makedirs(shell_path)

env_path = '/home/users/l/liudong1/workspace/compare/set_env.sh'
python_path = '/home/users/l/liudong1/workspace/compare/bot_v_bot_test.py'

if os.path.exists(agent_path):

    print('Start to generate shell scripts:')
    
    shell_name =  '%s/run_agagz_ag0_compare_1.sh' % shell_path

    if os.path.exists(shell_name):
        os.remove(shell_name)

    write_logfile(shell_name, '#!/bin/sh\n')

    write_logfile(shell_name, '#SBATCH --cpus-per-task=1')
    write_logfile(shell_name, '#SBATCH --job-name=ag0agagz')
    write_logfile(shell_name, '#SBATCH --time=12:00:00')
    write_logfile(shell_name, '#SBATCH --mem=10000')
    write_logfile(shell_name, '#SBATCH --gpus=1')
    write_logfile(shell_name, '##SBATCH --constraint="V5|V6"')
    write_logfile(shell_name, '#SBATCH --partition=shared-gpu\n')

    err_name = '%s/run_agz_bl1_1.err' % err_path
    out_name = '%s/run_agz_bl1_1.out' % out_path
    write_logfile(shell_name, '#SBATCH --error=%s' % err_name)
    write_logfile(shell_name, '#SBATCH --output=%s' % out_name)

    write_logfile(shell_name, '\nsrun echo "Loading libraries."')
    write_logfile(shell_name, 'srun source %s\n' % env_path)
    write_logfile(shell_name, 'srun export PYTHONPATH="/home/users/l/liudong1/workspace/compare:$PYTHONPATH"\n')

    write_logfile(shell_name, 'current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
    write_logfile(shell_name, 'srun echo "Running python scripts on $current_date_time."')
    running_comand = 'srun python %s ' % python_path
    write_logfile(shell_name, running_comand)

    write_logfile(shell_name, '\ncurrent_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
    write_logfile(shell_name, 'srun echo "Finished on $current_date_time."')

    # for i in range(0, num_cpus_request):

    #     print('\tNo.%d' % (i+1))

    #     duplicate_agent = agent.replace('.h5', '_agmcts0_%d.h5' % (i+1) )
    #     if not os.path.exists(duplicate_agent):
    #         shutil.copyfile(agent, duplicate_agent)

    #     duplicate_strong = strong_policy.replace('.h5', '_agagz_%d.h5' % (i+1) )
    #     if not os.path.exists(duplicate_strong):
    #         shutil.copyfile(strong_policy, duplicate_strong)

    #     duplicate_fast = fast_policy.replace('.h5', '_agagz_%d.h5' % (i+1) )
    #     if not os.path.exists(duplicate_fast):
    #         shutil.copyfile(fast_policy, duplicate_fast)

    #     duplicate_value = value_net.replace('.h5', '_agagz_%d.h5' % (i+1) )
    #     if not os.path.exists(duplicate_value):
    #         shutil.copyfile(value_net, duplicate_value)


    #     shell_name =  '%s/run_agagz_ag0_compare_%d.sh' % (shell_path, i+1)

    #     if os.path.exists(shell_name):
    #         os.remove(shell_name)

    #     write_logfile(shell_name, '#!/bin/sh\n')

    #     write_logfile(shell_name, '#SBATCH --cpus-per-task=1')
    #     write_logfile(shell_name, '#SBATCH --job-name=ag0agagz')
    #     write_logfile(shell_name, '#SBATCH --time=12:00:00')
    #     write_logfile(shell_name, '#SBATCH --mem=10000')
    #     write_logfile(shell_name, '#SBATCH --gpus=1')
    #     write_logfile(shell_name, '##SBATCH --constraint="V5|V6"')
    #     write_logfile(shell_name, '#SBATCH --partition=shared-gpu\n')

    #     err_name = '%s/run_agz_bl1_%d.err' % (err_path, i+1)
    #     out_name = '%s/run_agz_bl1_%d.out' % (out_path, i+1)
    #     write_logfile(shell_name, '#SBATCH --error=%s' % err_name)
    #     write_logfile(shell_name, '#SBATCH --output=%s' % out_name)

    #     write_logfile(shell_name, '\nsrun echo "Loading libraries."')
    #     write_logfile(shell_name, 'srun source %s\n' % env_path)
    #     write_logfile(shell_name, 'srun export PYTHONPATH="/home/users/l/liudong1/workspace/compare:$PYTHONPATH"\n')

    #     write_logfile(shell_name, 'current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
    #     write_logfile(shell_name, 'srun echo "Running python scripts on $current_date_time."')
    #     running_comand = 'srun python %s -a %d -b %d -c %d -d %s -e %s -f %s -g %s %s' % (python_path, num_games_onecpu,  i+1, rounds_move, score_path, duplicate_strong, duplicate_fast, duplicate_value, duplicate_agent)
    #     write_logfile(shell_name, running_comand)

    #     write_logfile(shell_name, '\ncurrent_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
    #     write_logfile(shell_name, 'srun echo "Finished on $current_date_time."')

    # print('All generated.')

else:
    print('"%s" is not existing, please double check.' % agent_path)


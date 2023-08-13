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

agent_generation = 10     # latest generation of the agents
num_games_onecpu = 500    # -g parameter
num_games_boards = 9      # -b parameter

score_path = '/home/users/l/liudong1/scratch/AG/score'
agent_path = '/home/users/l/liudong1/scratch/AG/agents'

# where the error and output information of the gpu cores to be stored
std_path = '/home/users/l/liudong1/scratch/AG/std_elo'
if not os.path.exists(std_path):
    os.makedirs(std_path)

# where do we store the shell scripts, the number of shell scripts = agent_generation
# after generating the shell scripts, we will submit all of them to baobab.
# the template of the shell scripts is shown below
shell_path = '/home/users/l/liudong1/scratch/AG/shells/elo'

"""
#!/bin/sh

#SBATCH --cpus-per-task=1
#SBATCH --job-name=agelo
#SBATCH --time=12:00:00
#SBATCH --gpus=1
##SBATCH --constraint="V5|V6"
##SBATCH --constraint="COMPUTE_CAPABILITY_6_0|COMPUTE_CAPABILITY_6_1|COMPUTE_CAPABILITY_7_5"
#SBATCH --partition=shared-gpu

#SBATCH --error=/home/users/l/liudong1/scratch/AG/std_elo/run_agz_elo_1.err
#SBATCH --output=/home/users/l/liudong1/scratch/AG/std_elo/run_agz_elo_1.out

srun echo "Loading libraries."
srun source /home/users/l/liudong1/workspace/AG_hpc/set_env.sh
srun export PYTHONPATH="/home/users/l/liudong1/workspace/AG_hpc:$PYTHONPATH"

current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Running python scripts on $current_date_time."
srun python /home/users/l/liudong1/workspace/AG_hpc/calc_elo_ratings.py -g 100 -b 9 /home/users/l/liudong1/scratch/AGZ/agents/agent_zero_1.h5 /home/users/l/liudong1/scratch/AGZ/agents/agent_zero_0.h5 

current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Finished on $current_date_time."
"""

env_path = '/home/users/l/liudong1/workspace/AG_hpc/set_env.sh'
python_path = '/home/users/l/liudong1/workspace/AG_hpc/calc_elo_ratings.py'

if os.path.exists(agent_path):

    print('Start to generate %d shell scripts:' % agent_generation)

    for i in range(0, agent_generation):

        print('\tNo.%d' % (i+1))

        agent_zero_0 = '%s/sl_policy_%d.h5' % (agent_path, 0)
        agent_zero_x = '%s/rl_policy_%d.h5' % (agent_path, i+1)
        agent_id = i+1

        agent_zero_0x =  '%s/sl_policy_%d_%d.h5' % (agent_path, 0, i+1)

        if not os.path.exists(agent_zero_0x):
            shutil.copyfile(agent_zero_0, agent_zero_0x)

        shell_name =  '%s/run_agz_elo_%d.sh' % (shell_path, i+1)

        if os.path.exists(shell_name):
            os.remove(shell_name)

        write_logfile(shell_name, '#!/bin/sh\n')

        write_logfile(shell_name, '#SBATCH --cpus-per-task=1')
        write_logfile(shell_name, '#SBATCH --job-name=agelo')
        write_logfile(shell_name, '#SBATCH --time=12:00:00')
        write_logfile(shell_name, '#SBATCH --gpus=1')
        write_logfile(shell_name, '##SBATCH --constraint="V5|V6"')
        write_logfile(shell_name, '##SBATCH --constraint="COMPUTE_CAPABILITY_6_0|COMPUTE_CAPABILITY_6_1|COMPUTE_CAPABILITY_7_5"')
        write_logfile(shell_name, '#SBATCH --partition=shared-gpu\n')

        err_name = '%s/run_agz_elo_%d.err' % (std_path, i+1)
        out_name = '%s/run_agz_elo_%d.out' % (std_path, i+1)
        write_logfile(shell_name, '#SBATCH --error=%s' % err_name)
        write_logfile(shell_name, '#SBATCH --output=%s' % out_name)

        write_logfile(shell_name, '\nsrun echo "Loading libraries."')
        write_logfile(shell_name, 'srun source %s\n' % env_path)
        write_logfile(shell_name, 'srun export PYTHONPATH="/home/users/l/liudong1/workspace/AG_hpc:$PYTHONPATH"\n')

        write_logfile(shell_name, 'current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
        write_logfile(shell_name, 'srun echo "Running python scripts on $current_date_time."')
        running_comand = 'srun python %s -g %d -b %d -c %d -d %s %s %s' % (python_path, num_games_onecpu, num_games_boards, agent_id, score_path, agent_zero_x, agent_zero_0x)
        write_logfile(shell_name, running_comand)

        write_logfile(shell_name, '\ncurrent_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
        write_logfile(shell_name, 'srun echo "Finished on $current_date_time."')

    print('All generated.')

else:
    print('"%s" is not existing, please double check.' % agent_path)
    

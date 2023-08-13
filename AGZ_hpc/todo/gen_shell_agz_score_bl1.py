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

num_games_onecpu = 20    # -a parameter
num_steps_search = 100  # -c parameter
# agent_generation = 1     # -d parameter
#                          -c parameter
score_path = '/home/users/l/liudong1/scratch/AGZ/score' 
if not os.path.exists(score_path):
    os.makedirs(score_path)
#                     -d parameter 

agent_path = '/home/users/l/liudong1/scratch/AGZ/agents_score' 

# how many cpu cores we ask  (total number of games = num_cpus_request *  num_games_onecpu)
num_cpus_request = 25  

# where the error information of the cpu cores to be stored
err_path = '/home/users/l/liudong1/scratch/AGZ/stderr/err_score' 
if not os.path.exists(err_path):
    os.makedirs(err_path)

# where the print information of the cpu cores to be stored
out_path = '/home/users/l/liudong1/scratch/AGZ/stdout/out_score' 
if not os.path.exists(out_path):
    os.makedirs(out_path)

# where do we store the shell scripts, the number of shell scripts = num_cpus_request
# after generating the shell scripts, we will submit all of them to baobab.
# the template of the shell scripts is shown below
shell_path = '/home/users/l/liudong1/scratch/AGZ/shells/score'

"""
#!/bin/sh

#SBATCH --cpus-per-task=1
#SBATCH --job-name=agzbl1
#SBATCH --time=12:00:00
#SBATCH --gpus=1
##SBATCH --constraint="V5|V6"
#SBATCH --partition=shared-gpu

#SBATCH --error=/home/users/l/liudong1/scratch/AGZ/stderr/err_1/run_agz_bl1_1.err 
#SBATCH --output=/home/users/l/liudong1/scratch/AGZ/stdout/out_1/run_agz_bl1_1.out

srun echo "Loading libraries."
srun source /home/users/l/liudong1/workspace/AGZ_hpc/set_env.sh

current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Running python scripts on $current_date_time."
srun python /home/users/l/liudong1/workspace/AGZ_hpc/agz_bl1.py -a 10 -b 1000 -c /home/users/l/liudong1/scratch/AGZ/exp/exp_1 -d 1 /home/users/l/liudong1/scratch/AGZ/agents/agent_zero_0.h5 /home/users/l/liudong1/scratch/AGZ/agents/agent_zero_0.h5

current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Finished on $current_date_time."
"""

env_path = '/home/users/l/liudong1/workspace/AGZ_hpc/set_env.sh'
python_path = '/home/users/l/liudong1/workspace/AGZ_hpc/score_agz_bl1.py'

if os.path.exists(agent_path):

    print('Start to generate %d shell scripts:' % num_cpus_request)

    for i in range(0, num_cpus_request):

        print('\tNo.%d' % (i+1))


        duplicate_agents = agent_path.replace('score', 'score_%d' % (i+1) )

        if not os.path.exists(duplicate_agents):
            shutil.copytree(agent_path, duplicate_agents)

        shell_name =  '%s/run_agz_score_bl1_%d.sh' % (shell_path, i+1)

        write_logfile(shell_name, '#!/bin/sh\n')

        write_logfile(shell_name, '#SBATCH --cpus-per-task=1')
        write_logfile(shell_name, '#SBATCH --job-name=agzscorebl1')
        write_logfile(shell_name, '#SBATCH --time=12:00:00')
        write_logfile(shell_name, '#SBATCH --gpus=1')
        write_logfile(shell_name, '##SBATCH --constraint="V5|V6"')
        write_logfile(shell_name, '#SBATCH --partition=shared-gpu\n')

        err_name = '%s/run_agz_bl1_%d.err' % (err_path, i+1)
        out_name = '%s/run_agz_bl1_%d.out' % (out_path, i+1)
        write_logfile(shell_name, '#SBATCH --error=%s' % err_name)
        write_logfile(shell_name, '#SBATCH --output=%s' % out_name)

        write_logfile(shell_name, '\nsrun echo "Loading libraries."')
        write_logfile(shell_name, 'srun source %s\n' % env_path)

        write_logfile(shell_name, 'current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
        write_logfile(shell_name, 'srun echo "Running python scripts on $current_date_time."')
        running_comand = 'srun python %s -a %d -b %d -c %d -d %s -e %s' % (python_path, num_games_onecpu,  i+1, num_steps_search, score_path, duplicate_agents)
        write_logfile(shell_name, running_comand)

        write_logfile(shell_name, '\ncurrent_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
        write_logfile(shell_name, 'srun echo "Finished on $current_date_time."')

    print('All generated.')

else:
    print('"%s" is not existing, please double check.' % agent_path)

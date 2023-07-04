#!/usr/bin/env python
# coding=utf-8

import os,sys

def write_logfile(filename, content):
    stdout_backup = sys.stdout
    log_file = open(filename, 'a+')
    log_file.close()
    log_file = open(filename, 'a+')
    sys.stdout = log_file
    print(content)
    log_file.close()
    sys.stdout = stdout_backup

agent_generation = 1     # -d parameter
agent_path = '/home/users/l/liudong1/scratch/AGZ/agents'                       # -c parameter
exp_path = '/home/users/l/liudong1/scratch/AGZ/exp/exp_%d' % agent_generation   # -b parameter
past_agent = '/home/users/l/liudong1/scratch/AGZ/agents/agent_zero_%d.h5' % (agent_generation - 1) # last parameter

# where the error information of the cpu cores to be stored
err_path = '/home/users/l/liudong1/scratch/AGZ/stderr'

# where the print information of the cpu cores to be stored
out_path = '/home/users/l/liudong1/scratch/AGZ/stdout'

# where do we store the shell scripts
shell_path = '/home/users/l/liudong1/scratch/AGZ/shells/bl2'

"""
#!/bin/sh

#SBATCH --cpus-per-task=1
#SBATCH --job-name=agzbl2
#SBATCH --time=12:00:00
#SBATCH --gpus=1
##SBATCH --constraint="V5|V6"
#SBATCH --partition=shared-gpu

#SBATCH --error=/home/users/l/liudong1/scratch/AGZ/stderr/run_agz_bl2_1.err 
#SBATCH --output=/home/users/l/liudong1/scratch/AGZ/stdout/run_agz_bl2_1.out

srun echo "Loading libraries."
srun source /home/users/l/liudong1/workspace/AGZ_hpc/set_env.sh

current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Running python scripts on $current_date_time."
srun python /home/users/l/liudong1/workspace/AGZ_hpc/agz_bl2.py -b /home/users/l/liudong1/scratch/AGZ/exp/exp_1 -c /home/users/l/liudong1/scratch/AGZ/agents -d 1 /home/users/l/liudong1/scratch/AGZ/agents/agent_zero_0.h5

current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Finished on $current_date_time."
"""

env_path = '/home/users/l/liudong1/workspace/AGZ_hpc/set_env.sh'
python_path = '/home/users/l/liudong1/workspace/AGZ_hpc/agz_bl2.py'


shell_name =  '%s/run_agz_bl2_%d.sh' % (shell_path, agent_generation)

print('Start to generate bl2 shell scripts for generation %d' % agent_generation)

write_logfile(shell_name, '#!/bin/sh\n')

write_logfile(shell_name, '#SBATCH --cpus-per-task=1')
write_logfile(shell_name, '#SBATCH --job-name=agzbl2')
write_logfile(shell_name, '#SBATCH --time=12:00:00')
write_logfile(shell_name, '#SBATCH --gpus=1')
write_logfile(shell_name, '##SBATCH --constraint="V5|V6"')
write_logfile(shell_name, '#SBATCH --partition=shared-gpu\n')

err_name = '%s/run_agz_bl2_%d.err' % (err_path, agent_generation)
out_name = '%s/run_agz_bl2_%d.out' % (out_path, agent_generation)
write_logfile(shell_name, '#SBATCH --error=%s' % err_name)
write_logfile(shell_name, '#SBATCH --output=%s' % out_name)

write_logfile(shell_name, '\nsrun echo "Loading libraries."')
write_logfile(shell_name, 'srun source %s\n' % env_path)

write_logfile(shell_name, 'current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
write_logfile(shell_name, 'srun echo "Running python scripts on $current_date_time."')

running_comand = 'srun python %s -b %s -c %s -d %d %s' % (python_path, exp_path, agent_path, agent_generation, past_agent)
write_logfile(shell_name, running_comand)

write_logfile(shell_name, '\ncurrent_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
write_logfile(shell_name, 'srun echo "Finished on $current_date_time."')

print('Shell generated.')

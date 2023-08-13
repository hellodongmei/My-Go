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

score_path = '/home/users/l/liudong1/scratch/AGZ/score'       # -a parameter
#num_gants = 11     # -b parameter
agent_path = '/home/users/l/liudong1/scratch/AGZ/agents_score' 

# where the error information of the cpu cores to be stored
err_path = '/home/users/l/liudong1/scratch/AGZ/stderr/err_score'

# where the print information of the cpu cores to be stored
out_path = '/home/users/l/liudong1/scratch/AGZ/stdout/out_score'

# where do we store the shell scripts
shell_path = '/home/users/l/liudong1/scratch/AGZ/shells/score'

"""
#!/bin/sh

#SBATCH --cpus-per-task=1
#SBATCH --job-name=agzscorebl2
#SBATCH --time=12:00:00
#SBATCH --gpus=1
##SBATCH --constraint="V5|V6"
#SBATCH --partition=shared-gpu

#SBATCH --error=//home/users/l/liudong1/scratch/AGZ/stderr/err_score/run_agz_score_bl2.err 
#SBATCH --output=/home/users/l/liudong1/scratch/AGZ/out_score/run_agz_score_bl2.out

srun echo "Loading libraries."
srun source /home/users/l/liudong1/workspace/AGZ_hpc/set_env.sh
srun export PYTHONPATH="/home/users/l/liudong1/workspace/AGZ_hpc:$PYTHONPATH"

current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Running python scripts on $current_date_time."
srun python /home/users/l/liudong1/workspace/AGZ_hpc/agz_bl2.py -a /home/users/l/liudong1/scratch/AGZ/score -b 11 


current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Finished on $current_date_time."
"""

env_path = '/home/users/l/liudong1/workspace/AGZ_hpc/set_env.sh'
python_path = '/home/users/l/liudong1/workspace/AGZ_hpc/score_agz_bl2.py'


shell_name =  '%s/run_agz_score_bl2.sh' % shell_path

if os.path.exists(shell_name):
    os.remove(shell_name)
            
print('Start to generate bl2 shell scripts for agz score bl2' )

write_logfile(shell_name, '#!/bin/sh\n')

write_logfile(shell_name, '#SBATCH --cpus-per-task=1')
write_logfile(shell_name, '#SBATCH --job-name=agzscorebl2')
write_logfile(shell_name, '#SBATCH --time=12:00:00')
write_logfile(shell_name, '#SBATCH --mem=10000')
write_logfile(shell_name, '#SBATCH --gpus=1')
write_logfile(shell_name, '##SBATCH --constraint="V5|V6"')
write_logfile(shell_name, '#SBATCH --partition=shared-gpu\n')

err_name = '%s/run_agz_score_bl2.err' % err_path
out_name = '%s/run_agz_score_bl2.out' % out_path
write_logfile(shell_name, '#SBATCH --error=%s' % err_name)
write_logfile(shell_name, '#SBATCH --output=%s' % out_name)

write_logfile(shell_name, '\nsrun echo "Loading libraries."')
write_logfile(shell_name, 'srun source %s\n' % env_path)
write_logfile(shell_name, 'srun export PYTHONPATH="/home/users/l/liudong1/workspace/AGZ_hpc:$PYTHONPATH"\n')

write_logfile(shell_name, 'current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
write_logfile(shell_name, 'srun echo "Running python scripts on $current_date_time."')

running_comand = 'srun python %s -a %s -b %s ' % (python_path, score_path, agent_path)
write_logfile(shell_name, running_comand)

write_logfile(shell_name, '\ncurrent_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
write_logfile(shell_name, 'srun echo "Finished on $current_date_time."')

print('Shell generated.')

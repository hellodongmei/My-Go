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

num_of_records = 6570     # -a parameter
# num_of_records = 4000

# where the error information of the cpu cores to be stored
err_path = '/home/users/l/liudong1/scratch/AG_AGZ/stderr/sl_bl1'

# where the print information of the cpu cores to be stored
out_path = '/home/users/l/liudong1/scratch/AG_AGZ/stdout/sl_bl1'

# where do we store the shell scripts
shell_path = '/home/users/l/liudong1/scratch/AG_AGZ/shells/sl_bl1'

"""
#!/bin/sh

#SBATCH --cpus-per-task=1
#SBATCH --job-name=agagz_slbl1
#SBATCH --time=12:00:00
#SBATCH --gpus=1
##SBATCH --constraint="V5|V6"
#SBATCH --partition=shared-gpu

#SBATCH --error=/home/users/l/liudong1/scratch/AG_AGZ/stderr/sl_bl1/run_ag_sl_bl1.err 
#SBATCH --output=/home/users/l/liudong1/scratch/AG_AGZ/stdout/sl_bl1/run_ag_sl_bl1.out

srun echo "Loading libraries."
srun source /home/users/l/liudong1/workspace/AG_AGZ/set_env.sh
srun export PYTHONPATH="/home/users/l/liudong1/workspace/AG_AGZ:$PYTHONPATH"

current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Running python scripts on $current_date_time."

srun cd /home/users/l/liudong1/workspace/AG_MCTS
srun python /home/users/l/liudong1/workspace/AG_AGZ/agagz_sl_bl1.py -a 6570

current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Finished on $current_date_time."
"""

env_path = '/home/users/l/liudong1/workspace/AG_AGZ/set_env.sh'
python_path = '/home/users/l/liudong1/workspace/AG_AGZ/agagz_sl_bl1.py'

shell_name =  '%s/run_ag_sl_bl1.sh' % shell_path

if os.path.exists(shell_name):
    os.remove(shell_name)
            
print('Start to generate ag sl bl1 shell scripts.')

write_logfile(shell_name, '#!/bin/sh\n')

write_logfile(shell_name, '#SBATCH --cpus-per-task=1')
write_logfile(shell_name, '#SBATCH --job-name=agagz_slbl1')
write_logfile(shell_name, '#SBATCH --time=12:00:00')
write_logfile(shell_name, '#SBATCH --gpus=1')
write_logfile(shell_name, '##SBATCH --constraint="V5|V6"')
write_logfile(shell_name, '#SBATCH --partition=shared-gpu\n')

err_name = '%s/run_ag_sl_bl1.err' % err_path
out_name = '%s/run_ag_sl_bl1.out' % out_path
write_logfile(shell_name, '#SBATCH --error=%s' % err_name)
write_logfile(shell_name, '#SBATCH --output=%s' % out_name)

write_logfile(shell_name, '\nsrun echo "Loading libraries."')
write_logfile(shell_name, 'srun source %s\n' % env_path)
write_logfile(shell_name, 'srun export PYTHONPATH="/home/users/l/liudong1/workspace/AG_AGZ:$PYTHONPATH"\n')

write_logfile(shell_name, 'current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
write_logfile(shell_name, 'srun echo "Running python scripts on $current_date_time."')

running_comand = 'srun python %s -a %d' % (python_path, num_of_records)
write_logfile(shell_name, running_comand)

write_logfile(shell_name, '\ncurrent_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
write_logfile(shell_name, 'srun echo "Finished on $current_date_time."')

print('Shell generated.')

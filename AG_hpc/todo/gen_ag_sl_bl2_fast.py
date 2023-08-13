#!/usr/bin/env python
# coding=utf-8

import os,sys
import shutil
import numpy as np

def write_logfile(filename, content):
    stdout_backup = sys.stdout
    log_file = open(filename, 'a+')
    log_file.close()
    log_file = open(filename, 'a+')
    sys.stdout = log_file
    print(content)
    log_file.close()
    sys.stdout = stdout_backup

num_of_bins_lr = 50
num_of_bins_bs = 4

agent_path = '/home/users/l/liudong1/scratch/AG/agents/fast'  # -c parameter
history_path = '/home/users/l/liudong1/scratch/AG/history/fast'      # -d parameter

# where the error information of the cpu cores to be stored
err_path = '/home/users/l/liudong1/scratch/AG/stderr/fast'
if not os.path.exists(err_path):
    os.makedirs(err_path)

# where the print information of the cpu cores to be stored
out_path = '/home/users/l/liudong1/scratch/AG/stdout/fast'
if not os.path.exists(out_path):
    os.makedirs(out_path)

# where do we store the shell scripts, the number of shell scripts = num_cpus_request
# after generating the shell scripts, we will submit all of them to baobab.
# the template of the shell scripts is shown below
shell_path = '/home/users/l/liudong1/scratch/AG/shells/fast'

"""
#!/bin/sh

#SBATCH --cpus-per-task=1
#SBATCH --mem=10000 # in MB => 10 G
#SBATCH --job-name=agslbl2
#SBATCH --time=12:00:00
#SBATCH --gpus=1
##SBATCH --constraint="V5|V6"
##SBATCH --constraint="COMPUTE_CAPABILITY_6_0|COMPUTE_CAPABILITY_6_1|COMPUTE_CAPABILITY_7_5"
#SBATCH --partition=shared-gpu

#SBATCH --error=/home/users/l/liudong1/scratch/AG/stderr/sl_bl2/run_ag_sl_bl2_lr_bs.err 
#SBATCH --output=/home/users/l/liudong1/scratch/AG/stdout/sl_bl2/run_ag_sl_bl2_lr_bs.out

srun echo "Loading libraries."
srun source /home/users/l/liudong1/workspace/AG_hpc/set_env.sh
srun export PYTHONPATH="/home/users/l/liudong1/workspace/AG_hpc:$PYTHONPATH"

current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Running python scripts on $current_date_time."
srun python /home/users/l/liudong1/workspace/AG_hpc/ag_sl_bl2.py -b 0.1 -c /home/users/l/liudong1/scratch/AG/agents/sl_bl2 -d /home/users/l/liudong1/scratch/AG/history -e 16
current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
srun echo "Finished on $current_date_time."
"""

env_path = '/home/users/l/liudong1/workspace/AG_hpc/set_env.sh'
python_path = '/home/users/l/liudong1/workspace/AG_hpc/ag_sl_bl2_fast.py'

lr_array = np.logspace(-4, -1.6, num=num_of_bins_lr, endpoint=True)

bs_array = np.array([16, 32, 64, 128])


print('Start to generate %d shell scripts:' % (num_of_bins_lr * num_of_bins_bs ))
#pprint('Start to generate %d shell scripts:' % num_of_bins_lr)


num_of_shells = 0

for i in range(0, num_of_bins_lr):
    for j in range(0, num_of_bins_bs):

        num_of_shells += 1

        print('\tNo.%d, i=%d, j=%d' % (num_of_shells, i+1, j+1))

        shell_name =  '%s/run_ag_sl_bl2_%.8f_%d.sh' % (shell_path, lr_array[i], bs_array[j])

        if os.path.exists(shell_name):
            os.remove(shell_name)

        write_logfile(shell_name, '#!/bin/sh\n')

        write_logfile(shell_name, '#SBATCH --cpus-per-task=1')
        write_logfile(shell_name, '#SBATCH --mem=10000 # in MB => 10 G')
        write_logfile(shell_name, '#SBATCH --job-name=agslbl2')
        write_logfile(shell_name, '#SBATCH --time=12:00:00')
        write_logfile(shell_name, '#SBATCH --gpus=1')
        write_logfile(shell_name, '##SBATCH --constraint="V5|V6"')
        write_logfile(shell_name, '##SBATCH --constraint="COMPUTE_CAPABILITY_6_0|COMPUTE_CAPABILITY_6_1|COMPUTE_CAPABILITY_7_5"')
        write_logfile(shell_name, '#SBATCH --partition=shared-gpu\n')

        err_name = '%s/run_ag_sl_bl2_%.8f_%d.err' % (err_path, lr_array[i], bs_array[j])
        out_name = '%s/run_ag_sl_bl2_%.8f_%d.out' % (out_path, lr_array[i], bs_array[j])
        write_logfile(shell_name, '#SBATCH --error=%s' % err_name)
        write_logfile(shell_name, '#SBATCH --output=%s' % out_name)

        write_logfile(shell_name, '\nsrun echo "Loading libraries."')
        write_logfile(shell_name, 'srun source %s\n' % env_path)
        write_logfile(shell_name, 'srun export PYTHONPATH="/home/users/l/liudong1/workspace/AG_hpc:$PYTHONPATH"\n')

        write_logfile(shell_name, 'current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
        write_logfile(shell_name, 'srun echo "Running python scripts on $current_date_time."')
        running_comand = 'srun python %s -b %.8f -c %s -d %s -e %d' % (python_path, lr_array[i], agent_path, history_path, bs_array[j])
        write_logfile(shell_name, running_comand)

        write_logfile(shell_name, '\ncurrent_date_time="`date "+%Y-%m-%d %H:%M:%S"`"')
        write_logfile(shell_name, 'srun echo "Finished on $current_date_time."')

print('All generated.')


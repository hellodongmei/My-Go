#!/usr/bin/env python
# coding=utf-8

import os,sys
import shutil
import subprocess as sub
import numpy as np

def ask_shell(command):
    p = sub.Popen(command, shell=True, stdout=sub.PIPE)
    stdoutput,erroutput=p.communicate()
    iferror=str(type(erroutput))
    if ('None' not in iferror):
        print ("\t\trun %s got errors: " % command, erroutput)
    return stdoutput

shell_path = '/home/users/l/liudong1/scratch/AG_AGZ/shells/sl_bl2'
history_path = '/home/users/l/liudong1/scratch/AG_AGZ/history/hist_minus4to1' 

list_shells = os.listdir(shell_path)

print('Submitting %d jobs now:' % len(list_shells))

num_of_bins_lr = 50
num_of_bins_bs = 4
lr_array = np.logspace(-4, -1, num=num_of_bins_lr, endpoint=True)
bs_array = np.array([16, 32, 64, 128])

num_finished = 0
num_resubmit = 0
for i in range(0, num_of_bins_lr):
    for j in range(0, num_of_bins_bs):
        hist_name = '%s/train_hist_%.8f_%d.npy' % (history_path, lr_array[i], bs_array[j])
        if os.path.exists(hist_name): 
            num_finished += 1
            continue
        shell_name =  '%s/run_ag_sl_bl2_%.8f_%d.sh' % (shell_path, lr_array[i], bs_array[j])
        print('\tNo.%d %d:\n\t\t%s' % (i+1, j+1, shell_name))
        ask_shell('sbatch %s' % shell_name)
        num_resubmit += 1


print('All checked: \n\tNo.%d/200 jobs finished; \n\tNo.%d/200 jobs resubmitted.' % (num_finished, num_resubmit) )

#!/usr/bin/env python
# coding=utf-8

import os,sys
import shutil
import subprocess as sub
import time

def ask_shell(command):
    p = sub.Popen(command, shell=True, stdout=sub.PIPE)
    stdoutput,erroutput=p.communicate()
    iferror=str(type(erroutput))
    if ('None' not in iferror):
        print ("\t\trun %s got errors: " % command, erroutput)
    return stdoutput

shell_path = '/home/users/l/liudong1/scratch/AG/shells/fast'

list_shells = os.listdir(shell_path)

print('Submitting %d jobs now:' % len(list_shells))
time_wait = 1*40

for i in range(0, len(list_shells)):

    if i < 140 : continue
    print('\tNo.%d:\n\t\t%s' % (i+1, list_shells[i]))

    shell_name =  '%s/%s' % (shell_path, list_shells[i])

    ask_shell('sbatch %s' % shell_name)

    time.sleep(time_wait)

print('All done.')

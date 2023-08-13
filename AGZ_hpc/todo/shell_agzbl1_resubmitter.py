#!/usr/bin/env python
# coding=utf-8

import os,sys
import shutil
import subprocess as sub

def ask_shell(command):
    p = sub.Popen(command, shell=True, stdout=sub.PIPE)
    stdoutput,erroutput=p.communicate()
    iferror=str(type(erroutput))
    if ('None' not in iferror):
        print ("\t\trun %s got errors: " % command, erroutput)
    return stdoutput

shell_path = '/home/users/l/liudong1/scratch/AGZ/shells/bl1'

# how many cpu cores we ask  (total number of games = num_cpus_request *  num_games_onecpu)
num_cpus_request = 120  
agent_generation = 12

exp_path = '/home/users/l/liudong1/scratch/AGZ/exp/exp_%d' % agent_generation

# where the print information of the cpu cores to be stored
out_path = '/home/users/l/liudong1/scratch/AGZ/stdout/out_%d' % agent_generation


num_finished = 0
num_resubmit = 0


print('Checking %d jobs now:' % num_cpus_request)
for i in range(0, num_cpus_request):
    print('\tNo.%d' % (i+1))

    shell_name =  '%s/run_agz_bl1_%d.sh' % (shell_path, i+1)

    exp_file = '%s/exp_%d_1.h5' % (exp_path, i+1)
    if os.path.exists(exp_file):
        exp_existence = True
    else:
        exp_existence = False

#    out_name = '%s/run_agz_bl1_%d.out' % (out_path, i+1)

#    if os.path.exists(out_name):

#        num_of_games_str = str(ask_shell('cat %s | grep "Starting the game!"' % out_name))
#        num_of_games_list = num_of_games_str.split('\\n')

#        if len(num_of_games_list) - 1 == 30 or len(num_of_games_list) - 1 == 5:
#        if len(num_of_games_list) - 1 == 1:
#            game_finished = True

#        else:
#            exp_existence = False
#    else:
#        exp_existence = False

#    if not exp_existence or not game_finished:
    if not exp_existence:
        print('\t\tresubmitting %s' % shell_name)
        ask_shell('sbatch %s' % shell_name)
        num_resubmit += 1
    else:
        num_finished += 1

print('All checked: \n\tNo.%d/200 jobs finished; \n\tNo.%d/200 jobs resubmitted.' % (num_finished, num_resubmit) )


import os,sys
import subprocess as sub
import re

from bigtree import dict_to_tree, tree_to_dot

def ask_shell(command):
    p = sub.Popen(command, shell=True, stdout=sub.PIPE)
    stdoutput,erroutput=p.communicate()
    iferror=str(type(erroutput))
    if ('None' not in iferror):
        print ("\twhile running %s, errors happend: %s" % (command, erroutput))
        write_logfile("./jobs_submitter.log", "\twhile running %s, errors happend: %s" % (command, erroutput))
    return stdoutput


stdoutput_0 = ask_shell("wc -l chapter13/*.py")
stdoutput_1 = ask_shell("wc -l chapter13/*/*.py")
stdoutput_2 = ask_shell("wc -l chapter13/*/*/*.py")

lines_of_files_0 = str(stdoutput_0).split('\\n')[0:-2]
lines_of_files_1 = str(stdoutput_1).split('\\n')[0:-2]
lines_of_files_2 = str(stdoutput_2).split('\\n')[0:-2]

all_lines = lines_of_files_0 + lines_of_files_1 + lines_of_files_2

total_number_of_lines = 0

all_dict = {}

for i in range(0, len(all_lines)):

	number_of_lines = re.findall("\d+", all_lines[i])[0]

	file_name = all_lines[i][all_lines[i].find(number_of_lines)+len(number_of_lines)+1:]

	tmp_dict_1 = {}

	tmp_dict_1["NoL"] = number_of_lines 

	all_dict[file_name] = tmp_dict_1

	total_number_of_lines += int(number_of_lines)

tmp_dict_1 = {}

tmp_dict_1["NoL"] = str(total_number_of_lines)

all_dict['chapter13'] = tmp_dict_1

root = dict_to_tree(all_dict)
root.show(attr_list=["NoL"])

graph = tree_to_dot(root, node_colour="gold")
graph.write_png("plot_tree.png")

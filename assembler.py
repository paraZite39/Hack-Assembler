import sys, os, re
import binparser as bp
import bincode as bc

registers = {"SCREEN": "16384", "KBD": "24576"}         # initialize builtin symbols

for i in range(16):
    registers["R" + str(i)] = str(i)                    # insert R0-R15 into reg table
    
vars = {}                                               # initialize var table

def clean_file(file):                                   # remove whitespace, comments
    out_file_name = file.split(".")[0] + "_clear.asm"   # out file will have '_clear.asm' at the end
    
    in_file = open(file, "r")                           # open in file
    fin_file = open(out_file_name, "w")                 # open out file
    
    for line in in_file.readlines():                
        stripped_line = bp.comp(line)                   # remove comments & whitespaces from line
        if stripped_line.rstrip() != "":                # if line is not empty
            fin_file.write(stripped_line)               # write it in out file
            
    fin_file.close()
    in_file.close()
    
    return out_file_name

def add_labels(file):
    counter = 16                                      # first var will start from 16th register
    line_counter = 0                                  # start line counter from 0
    file_r = open(file, "r")
    for line in file_r.readlines():                   # first run - insert labels in register table
        line = line.rstrip()
        if bp.is_label(line):
            registers[line[1:-1]] = str(line_counter) # if it's a label, ignore that line and add it to registers
        elif bp.is_variable(line):
            if line[1:] in vars:
                line_counter += 1                     # if var is already in table, increment line and move on
                continue
            else:
                vars[line[1:]] = str(counter)         # if it isn't, add it to variable table, increment line and counter
                counter += 1
                line_counter += 1
        else:
            line_counter += 1                         # if it's not label or var, increment line
    file_r.close()

def replace_vl(file):
    out_file_name = file.split(".")[0] + "_final.asm"   # out file will have '_final.asm' at the end
    
    in_file = open(file, "r")                           # open in file
    out_file = open(out_file_name, "w")                 # open out file
    
    for line in in_file.readlines():                               # second run - replace label and var calls with their line number
        line_str = line.rstrip()                                   # remove \n
        if bp.is_label(line_str):                                  # 1.if line is a label declaration
            continue                                               # ignore
        elif bp.is_label_or_var_call(line_str, registers):         # 2.if line is a label call (@LOOP)
            label = line_str[1:]                                   # remove first character
            fin_line = re.sub(label, registers[label], line)       # replace label with its line number
        elif bp.is_label_or_var_call(line_str, vars):              # 3.if line is a var call (@i)
            var = line_str[1:]                                     # remove first character
            fin_line = re.sub(var, vars[var], line)                # replace var with its register count
        else:                                                      # if it's neither
            fin_line = line                                        # write line as is

        out_file.write(fin_line)                                   # write result to out_file

    in_file.close()
    out_file.close()

    return out_file_name

def main():
    in_file = sys.argv[1]                   # get instruction file
    clean_file_name = clean_file(in_file)   # clean instruction file
    add_labels(clean_file_name)             # add labels to reg table
    fin_file = replace_vl(clean_file_name)  # replace label and var calls with their addresses
    instr_file = open(fin_file, "r")        # open cleaned and unlabeled instruction file
    final_lines = [bc.codify(line) for line in instr_file.readlines()]  # get list of binary lines
    hack_file = open(in_file.split(".")[0] + ".hack", "w")              # open result file

    for line in [line for line in final_lines if line]:                 # write every non-null line into file
            hack_file.write(line + "\n")

    instr_file.close()
    hack_file.close()
    os.remove(clean_file_name)  # delete aux files
    os.remove(fin_file)

main()

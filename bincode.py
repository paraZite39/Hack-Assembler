import re
import binparser

binvalues = {"dest": {"null": "000", "M": "001", "D": "010", "MD": "011",           # destination bin values
                      "A": "100", "AM": "101", "AD": "110", "AMD": "111"},
             "comp": {"0": "101010", "1": "111111", "-1": "111010",                 # computation bin values
                      "D": "001100", "A": "110000", "!D": "001101",
                      "!A": "110001", "-D": "001111", "-A": "110011",
                      "D+1": "011111", "A+1": "110111", "D-1": "001110",
                      "A-1": "110010", "D+A": "000010", "D-A": "010011",
                      "A-D": "000111", "D&A": "000000", "D|A": "010101",
                      "M": "110000", "!M": "110001", "-M": "110011",
                      "M+1": "110111", "M-1": "110010", "D+M": "000010",
                      "D-M": "010011", "M-D": "000111", "D&M": "000000", "D|M": "010101"},
             "jmp": {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",       # jump bin values
                     "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}}

def assign_dcj(line):
    dest, comp, jmp = "null", "null", "null"
    is_dest = True if "=" in line else False        # check if line has a destination (value before a = sign)
    is_jmp = True if ";" in line else False         # check if line has a jump condition (value after a ; sign)

    if is_dest:                                                             # if line has a = sign (has a destination)
        lefteq, righteq = line.split("=")[0], line.split("=")[1]            # split line into values before and after =
        if is_jmp:                                                          # if line has a ; sign
            leftsc, rightsc = righteq.split(";")[0], righteq.split(";")[1]  # split value after = into what's before and after ;
            dest, comp, jmp = lefteq, leftsc, rightsc                       # assign dest, comp and jmp to value before =, before ; and after ;
        else:
            dest, comp = lefteq, righteq                                    # if it has an = but not a ;, assign dest and comp to before and after =
    else:
        if is_jmp:                                                          # if it has ; but not =
            leftsc, rightsc = line.split(";")[0], line.split(";")[1]        # split line in values before and after ;
            comp, jmp = leftsc, rightsc                                     # assign comp and jmp to value before and after ;
        else:
            comp = line                                                     # if no ; or =, computation is entire line
        
    return dest.rstrip(), comp.rstrip(), jmp.rstrip()                       # return dest, comp and jmp without any accidental \n

def codify(line):
    if binparser.is_a(line):                  # if instr starts with @, it's an A-instruction
        addr = bin(int(line[1:]))[2:]         # convert dec address into bin
        return addr.zfill(16)                 # return address with 0-padding until size of 16
    elif binparser.is_c(line):
        dest, comp, jmp = assign_dcj(line)    # if it's a C-address, assign dest, comp and jmp to their respective values
        
        fin_values = {"dest": "", "comp": "","jmp": ""}                   # final bin values to be returned

        for (key, value) in ("dest", dest), ("comp", comp), ("jmp", jmp):
            if value in binvalues[key]:                                   # if portion is in bin value dictionary
                fin_values[key] = binvalues[key][value]                   # assign binvalue to each component
                print(key, value, fin_values[key], binvalues[key][value])
            else:
                print(key, value, "not found")                            # if value is not in reg table, announce that it was not found

        a_bit = "1" if "M" in comp else "0"                               # if there is an M in the computation, set A bit to 1, else to 0
        
        fin_dest, fin_comp, fin_jmp = fin_values["dest"], fin_values["comp"], fin_values["jmp"]    # assign final values
        return "111" + a_bit + fin_comp + fin_dest + fin_jmp                                       # and return the result

if __name__ == "__main__":                                                                         # tests
    d1, c1, j1 = assign_dcj("A=A+1")
    print(d1, c1, j1)
    d2, c2, j2 = assign_dcj("D;JMP")
    print(d2, c2, j2)
    d3, c3, j3 = assign_dcj("D=M+1;JMP")
    print(d3, c3, j3)

    code1 = codify("@12")
    print(code1)

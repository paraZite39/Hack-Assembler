import re

def comp(line):
    print("called comp on", line)
    line = re.sub("\/\/.*", "", line) # remove everything after //
    line = re.sub(" ", "", line)      # remove spaces
    print("result is", line)
    return line

def is_label(line):
    return True if line[0] == "(" and line[-1] == ")" \     # line is label if it's surrounded by parantheses
                and line[1:-1] == line[1:-1].upper() \      # and value inside is all-caps
                else False 

def is_a(line):
    return True if line[0] == "@" else False                # line is an A-instruction if it starts with an @                        

def is_label_or_var_call(line, table):
    return True if is_a(line) \             # line is a label or var call if it's an A-instr
           and line[1:] in table \          # with a name present in the table
           else False                      

def is_c(line):
    return True if "=" in line or ";" in line else False    # line is an A-instr if it has a = or ; sign

def is_variable(line):
    return True if is_a(line) \                             # line is a variable call if it's an A-instruction
                and line[1].isalpha() \                     # followed by a character
                and line[1:] == line[1:].lower() \          # that's lowercase
                else False

if __name__ == "__main__":                                  # test lines
    a = comp("@163 // goto 163\n")
    b = comp("A = M ; JMP\n")
    c = comp("M = A + 1\n")
    d = comp("A = A+M\n")
    print("".join([a,b,c,d]))

    a2 = is_label("(LOOP)")
    b2 = is_label("@HEY")
    c2 = is_label("A = M")
    print(a2, b2, c2)

    a3 = is_a("@i")
    b3 = is_c("A=M+1;JGT")
    c3 = is_variable("@index")
    print(a3, b3, c3)

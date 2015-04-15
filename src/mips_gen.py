from sys import argv
import mips_code as mips_code

from parser import mips_parser

def gen_code(inputFile):
    program = open(inputFile).read()
    ST, TAC = mips_parser(program)    
    MC = mips_code.mips_code(ST, TAC)
    
    count = 0
    MC.make_label()
    for function_name in TAC.code:
        MC.add_function(function_name)

        if (function_name == 'main'):
            MC.add_code(['subu', '$sp', '$sp', '8'])
            MC.add_code(['sw', '$fp', '8($sp)', ''])
            MC.add_code(['sw', '$ra', '4($sp)', ''])
            MC.add_code(['addiu', '$fp', '$sp', '8'])

            MC.add_code(['subu', '$sp', '$sp', ST.get_function_attribute(function_name,'width')])
            
        else:
            MC.add_code(['subu', '$sp', '$sp', '8'])
            MC.add_code(['sw', '$fp', '8($sp)', ''])
            MC.add_code(['sw', '$ra', '4($sp)', ''])
            MC.add_code(['addiu', '$fp', '$sp', '8'])

            MC.add_code(['subu', '$sp', '$sp', ST.get_function_attribute(function_name,'width')])

            for x in range(1,ST.get_function_attribute(function_name, 'arguments')):
                MC.add_code(['lw','$a' + str(x), str(4*x) + '($sp)', ''])

        for line in TAC.code[function_name]:
            if line[3] == 'JUMP_LABEL':
                MC.add_code(['jal', line[2], '', ''])
                MC.add_code(['move', '$sp' ,'$fp', ''])
                MC.add_code(['lw', '$ra' ,'-4($fp)', ''])
                MC.add_code(['lw', '$fp' ,'0($fp)', ''])

            elif line[3] == 'JUMPBACK_TO_CALLEE':
                MC.add_code(['jr', '$ra' ,'', ''])

            elif line[3] == 'PUSHPARAM':
                reg = MC.get_reg(line[0])
                MC.add_code(['move', '$a'+str(counter), reg,''])
                counter = counter +1 ;

            elif line[3] == '=':
                reg1 = MC.get_reg(line[0])
                reg2 = MC.get_reg(line[1])
                MC.add_code(['move', reg1, reg2, ''])

            elif line[3] == '=i':
                reg = MC.get_reg(line[0])
                MC.add_code(['li', reg, line[1], ''])

            elif line[3] == '=s':
                reg = MC.get_reg(line[0])
                MC.add_code(['la', reg, 'string' + str(count), ''])
                count += 1

            elif line[3] == 'unary-':
                reg1 = MC.get_reg(line[0])
                reg2 = MC.get_reg(line[1])
                MC.add_code(['sub', reg1, '$zero', reg2])
 
            elif line[3] == '+':
                reg1 = MC.get_reg(line[0])
                reg2 = MC.get_reg(line[1])
                reg3 = MC.get_reg(line[2])
                MC.add_code(['add', reg1, reg2, reg3])
               
            elif line[3] == '-':
                reg1 = MC.get_reg(line[0])
                reg2 = MC.get_reg(line[1])
                reg3 = MC.get_reg(line[2])
                MC.add_code(['sub', reg1, reg2, reg3])
                
            elif line[3] == '*':
                reg1 = MC.get_reg(line[1])
                reg2 = MC.get_reg(line[2])
                reg3 = MC.get_reg(line[0])
                MC.add_code(['mult', reg1, reg2,''])
                MC.add_code(['mflo', reg3,'',''])
               
            elif line[3] == '/':
                reg1 = MC.get_reg(line[1])
                reg2 = MC.get_reg(line[2])
                reg3 = MC.get_reg(line[0])
                MC.add_code(['div', reg1, reg2, ''])
                MC.add_code(['mflo', reg3, '', ''])
               
            elif line[3] == '%':
                reg1 = MC.get_reg(line[1])
                reg2 = MC.get_reg(line[2])
                reg3 = MC.get_reg(line[0])
                MC.add_code(['div', reg1, reg2, ''])
                MC.add_code(['mfhi', reg3, '', ''])
              
            elif line[3] == '<':
                reg1 = MC.get_reg(line[0])
                reg2 = MC.get_reg(line[1])
                reg3 = MC.get_reg(line[2])
                MC.add_code(['slt', reg1, reg2, reg3])
           
            elif line[3] == '>':
                reg1 = MC.get_reg(line[0])
                reg2 = MC.get_reg(line[1])
                reg3 = MC.get_reg(line[2])
                MC.add_code(['sgt', reg1, reg2, reg3])
               
            elif line[3] == '<=':
                reg1 = MC.get_reg(line[0])
                reg2 = MC.get_reg(line[1])
                reg3 = MC.get_reg(line[2])
                MC.add_code(['sle', reg1, reg2, reg3])
           
            elif line[3] == '>=':
                reg1 = MC.get_reg(line[0])
                reg2 = MC.get_reg(line[1])
                reg3 = MC.get_reg(line[2])
                MC.add_code(['sge', reg1, reg2, reg3])
                
            elif line[3] == '==':
                reg1 = MC.get_reg(line[0])
                reg2 = MC.get_reg(line[1])
                reg3 = MC.get_reg(line[2])
                MC.add_code(['seq', reg1, reg2, reg3])
            
            elif line[3] == '!=':
                reg1 = MC.get_reg(line[0])
                reg2 = MC.get_reg(line[1])
                reg3 = MC.get_reg(line[2])
                MC.add_code(['sne', reg1, reg2, reg3])
             
            elif line[3] == 'COND_GOTO_Z':
                reg1 = MC.get_reg(line[0])
                MC.add_code(['beq', reg1, '$zero', line[2]])

            elif line[3] == 'GOTO':
                MC.add_code(['b', line[2], '', ''])

            elif line[3] == 'FUNCTION_RETURN':
                reg1 = MC.get_reg(line[0])
                MC.add_code(['move', reg1, '$v0', ''])

            elif line[3] == 'RETURN':
                reg1 = MC.get_reg(line[0])
                MC.add_code(['move', '$v0', reg1, ''])
                MC.add_code(['move', '$sp', '$fp', ''])
                MC.add_code(['lw', '$ra', '-4($fp)', ''])
                MC.add_code(['lw', '$fp', '0($fp)', ''])

            elif line[3] == 'INPUT':
                if line[2] == 'NUMBER':
                    MC.add_code(['li', '$v0', '5', ''])
                    MC.add_code(['syscall', '', '', ''])
                    reg = MC.get_reg(line[0])
                    MC.add_code(['move', reg, '$v0', ''])
                else:
                    MC.add_code(['li', '$v0', '8', ''])
                    MC.add_code(['la', '$a0', 'String', ''])
                    MC.add_code(['li', '$a1', '64', ''])
                    MC.add_code(['syscall', '', '', ''])
                    reg = MC.get_reg(line[0])
                    MC.add_code(['move', reg, '$a0', ''])

            elif line[3] == 'HALT':
                MC.add_code(['li', '$v0', '10', ''])
                MC.add_code(['syscall', '', '', ''])

            elif line[3] == 'printcall':
                if line[2] == 'NUMBER':
                    reg = MC.get_reg(line[0])
                    MC.add_code(['move', '$a0', reg, ''])
                    MC.add_code(['li', '$v0', 1, ''])
                    MC.add_code(['syscall', '', '', ''])
                elif line[2] == 'STRING' or line[2] == 'PSEUDO_STRING':
                    reg = MC.get_reg(line[0])
                    MC.add_code(['move', '$a0', reg, ''])
                    MC.add_code(['li', '$v0', 4, ''])
                    MC.add_code(['syscall', '', '', ''])

            else:
                MC.add_code(line)
    MC.print_mips_code()

if __name__ == '__main__':
    filename, inputFile = argv
    gen_code(inputFile)

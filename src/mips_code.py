class mips_code:
    def __init__(self, ST, TAC):
        self.code = {}
        self.ST = ST
        self.TAC = TAC
        self.current_function = ''
        self.label_no = 0
        self.label_name = 'label'

        self.register_descriptor = {
                '$t0' : None,
                '$t1' : None,
                '$t2' : None,
                '$t3' : None,
                '$t4' : None,
                '$t5' : None,
                '$t6' : None,
                '$t7' : None,
                '$t8' : None,
                '$t9' : None,
                '$s0' : None,
                '$s1' : None,
                '$s2' : None,
                '$s3' : None,
                '$s4' : None,
                '$s5' : None,
                '$s6' : None,
                '$s7' : None
                }
    	self.free_reg= []
        for reg in self.register_descriptor.keys():
        	self.free_reg.append(reg)
        self.used_reg= []

    def add_code(self, code):
        self.code[self.current_function].append(code)

    def add_function(self, function):
        self.current_function = function
        self.code[function] = []

    def print_mips_code(self):
            f = open( 'result.s', 'w')
            f.write('.data\n')
            
            f.write('String:\n\t.space 64\n')
            count = 0
            for function_name in self.TAC.code:
                for string in self.ST.symboltable[function_name]['string']:
                    f.write('%s:\t.asciiz\t"%s"\n' %('string'+str(count), string))
                    count += 1
            f.write('.text\n')
            for function_name in self.code.keys():
                f.write("%s:\n" %function_name)
                for i in range(len(self.code[function_name])):
                    code_line = self.code[function_name][i]
                    if code_line[0] == 'LABEL':
                        f.write("%s:\n" %code_line[1])
                    elif code_line[1] == '':
                        f.write("\t%s\n" %code_line[0])
                    elif code_line[2] == '':
                        f.write("\t%s\t\t%s\n" %(code_line[0], code_line[1]))
                    elif code_line[3] == '':
                        f.write("\t%s\t%s,\t%s\n" %(code_line[0], code_line[1], code_line[2]))
                    else:
                        f.write("\t%s\t%s,\t%s,\t%s\n" %(code_line[0], code_line[1], code_line[2], code_line[3]))

            f.close()


    def get_reg(self, temp_name):
        if temp_name in self.register_descriptor.values():
            reg = self.ST.address_descriptor[temp_name]['register']
        else:
            if len(self.free_reg) == 0:
                reg = self.used_reg.pop(0)
                temp_name1 = self.register_descriptor[reg]
                self.ST.address_descriptor[temp_name1]['register'] = None
                self.register_descriptor[reg] = temp_name 
                self.ST.address_descriptor[temp_name]['register'] = reg
            	self.used_reg.append(reg)     
            else:
                reg = self.free_reg.pop()
                self.register_descriptor[reg] = temp_name
            	self.ST.address_descriptor[temp_name]['register'] = reg
            	self.used_reg.append(reg)
        return reg

    def free_reg(self, reg):
            self.register_descriptor[reg] = None
            self.free_reg.append(reg)
            self.used_reg.pop(self.used_reg.index(reg))

    def create_labelname(self):
    	final_label = self.label_name + str(self.label_no)
        self.label_no += 1
        return final_label
    
    def make_label(self):
        for function_name in self.TAC.code:
            label_set = {}
            for code in self.TAC.code[function_name]:
                if code[3] in ['COND_GOTO_Z', 'GOTO']:
                    if label_set.has_key(code[2]):
                        label = label_set[code[2]]
                    else:
                        label = self.create_labelname()
                        label_set[code[2]] = label

                    code[2] = label

            line_no = 0
            count = 0
            for code in range(len(self.TAC.code[function_name])):
                if line_no in label_set.keys():
                    self.TAC.code[function_name].insert(line_no + count, ['LABEL', label_set[line_no], '', ''])
                    count += 1
                    del label_set[line_no]
                line_no += 1
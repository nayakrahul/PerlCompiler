from parsetree import *
import sys
import ply.yacc as yacc
import symbol_table as symbol_table
import three_address_code as three_address_code

# Get the token map from the lexer.  This is required.
from plexer import tokens, lexer

# from helpers import symbol_table as symbol_table
# from helpers import three_address_code as three_address_code
globvar = -2
var = 0;

def p_start(p):
	'''start : segments'''
	print "start"
	TAC.emit('', '' , -1, 'HALT')
	p[0] = {}


def p_segments(p):
	'''segments : statements_subroutine segments
				| statements_subroutine M_segments'''
	p[0] = {}
	p[0]['end_list'] = TAC.merge(p[1].get('end_list', []), p[2].get('end_list', []))
	p[0]['begin_list'] = TAC.merge(p[1].get('begin_list', []), p[2].get('begin_list', []))

	#p[0] = treeNode('segments', output, p)	

def p_program(p):
    '''statements_subroutine : statements 
    						| subroutine '''
   
    #p[0] = treeNode('statements_subroutine', output, p)
    p[0] = {}
    next_list = p[1].get('next_list', [])
    p[0]['end_list'] = p[1].get('end_list', [])
    p[0]['begin_list'] = p[1].get('begin_list', [])
    
       
def p_M_SEGMENTS(p):
	'M_segments : epsilon'

	p[0] = {}	

def p_block(p):
    '''block : BLOCK_BEGIN statements BLOCK_END'''	
    #p[0] = treeNode('block', output, p)
    p[0] = {}

    p[0]['end_list'] = p[2].get('end_list', [])
    p[0]['begin_list'] = p[2].get('begin_list', [])

def p_statments(p):
    '''statements : statement statements
    				| statement M_STATEMENTS'''

    p[0] = {}
    p[0]['end_list'] = TAC.merge(p[1].get('end_list', []), p[2].get('end_list', []))
    p[0]['begin_list'] = TAC.merge(p[1].get('begin_list', []), p[2].get('begin_list', []))
    #p[0] = treeNode('statements', output, p)		


				  
def p_statement(p):
	'''statement : assignment M_QUAD
				| declaration M_QUAD
				| function_call M_QUAD
				| break M_QUAD
				| continue M_QUAD
				| print M_QUAD
				| return M_QUAD
				| die M_QUAD
				| chomp M_QUAD
				| expression M_QUAD SEMICOLON
				| use M_QUAD
				| while_statement M_QUAD
				| do_while_statement M_QUAD
				| for_statement M_QUAD
				| switch_statement M_QUAD
				| if_statement M_QUAD
				| ifelse_statement M_QUAD
				'''

	#p[0] = treeNode('statement', output, p)
 	p[0] = {}
 	next_list = p[1].get('next_list', [])
 	TAC.back_patch(next_list, p[2]['quad'])
 	
 	p[0]['end_list'] = p[1].get('end_list', [])
 	p[0]['begin_list'] = p[1].get('begin_list', [])

def p_use(p):
	'''use : USE STRICT SEMICOLON
			| USE WARNINGS SEMICOLON'''

	#p[0] = treeNode('use', output, p)
	p[0] = {}

   

def p_statementList(p):
	'''block_or_statement : block 
						| statement
						| SEMICOLON'''

	#p[0] = treeNode('block_or_statement', output, p)
	p[0] = {}
	p[0]['end_list'] = p[1].get('end_list', [])
	p[0]['begin_list'] = p[1].get('begin_list', [])

	
def p_statement_if(p):
	'''if_statement : IF LPAR expression RPAR M_if block_or_statement '''

	p[0] = {}
	p[0]['next_list']=[]
	p[0]['type'] = 'VOID'
	if p[3]['type'] == 'BOOLEAN':
		p[0]['next_list'] = TAC.merge(p[6].get('end_list', []), p[6].get('next_list', []))
    	p[0]['next_list'] = TAC.merge(p[5].get('false_list', []), p[0].get('next_list', []))
    	

	#p[0] = treeNode('statement', output, p)

def p_m_ifBranch(p):
   	'M_if : epsilon'

   	p[0] = {}
   	p[0]['false_list'] = [TAC.getnext_quad()]
   	TAC.emit(p[-2]['temp_name'], '', -1, 'COND_GOTO_Z')


def p_statement_if_else(p):
	'''ifelse_statement : IF LPAR expression RPAR M_if block_or_statement ELSE M_else block_or_statement'''
	
	p[0] = {}
	TAC.back_patch(p[5]['false_list'], p[8]['quad'])
	p[0]['next_list'] = p[8]['next_list']
	p[0]['end_list'] = TAC.merge(p[9].get('end_list', []), p[6].get('end_list', []))
	p[0]['begin_list'] = TAC.merge(p[9].get('begin_list', []), p[6].get('begin_list', []))




def p_statement_elsif(p):
	'''elsif_statement : IF expression RPAR M_if block_or_statement elsif_statements ELSE M_else block_or_statement'''

	p[0] = {}
	TAC.back_patch(p[4]['false_list'], p[8]['quad'])
	p[0]['next_list'] = p[8]['next_list']
	p[0]['end_list'] = TAC.merge(p[9].get('end_list', []), p[5].get('end_list', []))
	p[0]['begin_list'] = TAC.merge(p[9].get('begin_list', []), p[5].get('begin_list', []))
	#p[0] = treeNode('statement', output, p)

def p_elsif_statements(p):
	'''elsif_statements : M_elsif ELSIF expression RPAR block_or_statement M_elsif elsif_statements 
						| M_elsif ELSIF expression RPAR block_or_statement'''

	#p[0] = treeNode('elsif_statements', output, p)
	p[0] = {}
	TAC.back_patch(p[1]['false_list'], p[6]['quad'])
	p[0]['next_list'] = p[6]['next_list']					
	p[0]['end_list'] = p[5].get('end_list', [])
	p[0]['begin_list'] = p[5].get('begin_list', [])

def p_m_elsif(p):
	'''M_elsif : epsilon'''
	p[0] = {}
	p[0]['next_list'] = [TAC.getnext_quad()]
	p[0]['quad'] = TAC.getnext_quad()

def p_m_elseBranch(p):
    'M_else : epsilon'

    p[0] = {}
    p[0]['next_list'] = [TAC.getnext_quad()]
    TAC.emit('', '', -1, 'GOTO')

    p[0]['quad'] = TAC.getnext_quad()


def p_while_statement(p):
		'''while_statement : WHILE M_QUAD LPAR expression RPAR  M_whileBranch block_or_statement
					'''
		p[0] = {}
		p[0]['next_list']=[]
		p[0]['type'] = 'VOID'
		if p[4]['type'] == 'BOOLEAN':
	        	TAC.back_patch(p[7]['begin_list'], p[2]['quad'])
	        	p[0]['next_list'] = TAC.merge(p[7].get('end_list', []), p[7].get('next_list', []))
	        	p[0]['next_list'] = TAC.merge(p[6].get('false_list', []), p[0].get('next_list', []))

	        	TAC.emit('', '', p[2]['quad'], 'GOTO')



def p_m_whileBranch(p):
    'M_whileBranch : epsilon'

    p[0] = {}
    p[0]['false_list'] = [TAC.getnext_quad()]
    TAC.emit(p[-2]['temp_name'], '', -1, 'COND_GOTO_Z')


def p_m_for(p):
    'M_for : epsilon'

    p[0] = {}
    p[0]['false_list'] = [TAC.getnext_quad()]
    TAC.emit(p[-2]['temp_name'], '', -1, 'COND_GOTO_Z')


def p_do_while(p):
		'''do_while_statement : DO M_QUAD block WHILE LPAR expression RPAR M_whileBranch SEMICOLON '''
		p[0] = {}
		p[0]['next_list']=[]
		p[0]['type'] = 'VOID'
		if p[6]['type'] == 'BOOLEAN':
	        	TAC.back_patch(p[3]['begin_list'], p[2]['quad'])
	        	p[0]['next_list'] = TAC.merge(p[3].get('end_list', []), p[3].get('next_list', []))
	        	p[0]['next_list'] = TAC.merge(p[8].get('false_list', []), p[0].get('next_list', []))

	        	TAC.emit('', '', p[2]['quad'], 'GOTO')


					
def p_for_statement(p):
		'''for_statement : FOR  LPAR assignment M_QUAD expression SEMICOLON M_for expression RPAR  block_or_statement
					| FOR LPAR assignment M_QUAD expression SEMICOLON M_for expression RPAR  SEMICOLON
					'''

		p[0] = {}
		p[0]['next_list']=[]
		p[0]['type'] = 'VOID'
		if p[5]['type'] == 'BOOLEAN':
	        	TAC.back_patch(p[10]['begin_list'], p[4]['quad'])
	        	p[0]['next_list'] = TAC.merge(p[10].get('end_list', []), p[10].get('next_list', []))
	        	p[0]['next_list'] = TAC.merge(p[7].get('false_list', []), p[0].get('next_list', []))

	        	TAC.emit('', '', p[4]['quad'], 'GOTO')
		#p[0] = treeNode('statement', output, p)

def p_multi_expression(p):
	'''multi_expression : expression expressionlist'''

	#p[0] = treeNode('multi_expression', output, p)	

def p_expressionlist(p):
	'''expressionlist : COMMA expression expressionlist
							| epsilon'''

	#p[0] = treeNode('expressionlist', output, p)								

def p_multi_assignment(p):
	'''multi_assignment	: SCALAR_VARIABLE ASSIGNMENT expression assignmentlist
						| SEMICOLON''' 

	#p[0] = treeNode('multi_assignment', output, p)	

def p_assignmentlist(p):
	'''assignmentlist : COMMA SCALAR_VARIABLE ASSIGNMENT expression assignmentlist 
					  | SEMICOLON'''

	#p[0] = treeNode('assignmentlist', output, p)					

def p_keys_or_values(p):
	'''keys_or_values : KEYS 
					| VALUES'''

	#p[0] = treeNode('keys_or_values', output, p)

def p_foreach_statement(p):
				'''statement : FOREACH SCALAR_VARIABLE LPAR ARRAY_VARIABLE RPAR block_or_statement
							| FOREACH SCALAR_VARIABLE LPAR keys_or_values HASH_VARIABLE RPAR block_or_statement
							| FOREACH SCALAR_VARIABLE LPAR keys_or_values HASH_VARIABLE RPAR SEMICOLON
							| FOREACH LPAR INTEGER DOUBLE_DOT INTEGER RPAR block_or_statement
							'''

				#p[0] = treeNode('statement', output, p)

def p_switch(p):
			'''switch_statement : SWITCH LPAR SCALAR_VARIABLE RPAR BLOCK_BEGIN cases BLOCK_END'''
			p[0] = {}
			global globvar
			globvar = -2

			
			#p[0] = treeNode('statement', output, p)

def p_cases(p):
			'''cases : case_block M_QUAD cases 
					| case_block M_QUAD
					| ELSE block M_QUAD'''
			p[0] = {}
			
			if(p[1] != 'else') :
			 	next_list = p[1].get('next_list', [])
			 	TAC.back_patch(next_list, p[2]['quad'])
		 	


def p_case_block(p):
	'case_block : CASE switch_expression M_switch block'
	p[0] = {}
	p[0]['next_list'] = []
	p[0]['next_list'] = TAC.merge(p[4].get('end_list', []), p[4].get('next_list', []))
	p[0]['next_list'] = TAC.merge(p[3].get('false_list', []), p[0].get('next_list', []))
	

def p_switch_expression(p):
	'switch_expression : expression'
	p[0] = {}
	global globvar
	globvar += 2
	TAC.emit(ST.make_temp(),ST.lookup(p[-4-globvar],0)['temporary_name'],p[1]['temp_name'],'==')


def p_m_switch(p):
	'M_switch : epsilon'
	p[0] = {}
	p[0]['false_list'] = [TAC.getnext_quad()]
	TAC.emit('', '', -1, 'COND_GOTO_Z')

def p_assignment2(p):
	'''assignment :  MY ARRAY_VARIABLE ASSIGNMENT array SEMICOLON
					| MY ARRAY_VARIABLE ASSIGNMENT LPAR INTEGER DOUBLE_DOT INTEGER RPAR SEMICOLON
					| MY ARRAY_VARIABLE ASSIGNMENT KEYS HASH_VARIABLE SEMICOLON
					| MY ARRAY_VARIABLE ASSIGNMENT VALUES HASH_VARIABLE SEMICOLON'''

	p[0] = {}
	identifier = {}
	identifier['name'] = p[2]
	identifier['type'] = 'UNDEFINED'
	global globvar
	global var
	globvar = -2
	var = 0

	ST.add_symbol(p[2],'UNDEFINED',0) 

def p_assignment1(p):	
	''' assignment :  MY SCALAR_VARIABLE ASSIGNMENT expression SEMICOLON 
					| MY HASH_VARIABLE ASSIGNMENT LPAR hashList RPAR SEMICOLON
					| MY SCALAR_VARIABLE ASSIGNMENT function_call SEMICOLON
					'''

	p[0] = {}
	identifier = {}
	identifier['name'] = p[2]
	identifier['type'] = p[4]['type']
	identifier['temp_name'] = p[4]['temp_name']
	if (ST.is_identifier_exist(identifier['name'],1) == False):
		ST.add_symbol(identifier['name'], identifier['type'],0)
		ST.add_attribute(identifier['name'], 'temporary_name', identifier['temp_name'])
		ST.add_attribute(p[2], 'type', p[4]['type'])
	if(p[4].has_key('name') == False):
		temp_name = ST.make_temp(variable=p[2])
		TAC.emit(temp_name, p[4]['temp_name'], '', '=') 
		

def p_f_assignment(p):
	'''assignment : SCALAR_VARIABLE ASSIGNMENT function_call
					| SCALAR_VARIABLE SIMULT_ASSIGNMENT function_call'''
	p[0] = {}
	identifier = {}
	identifier['name'] = p[1]
	identifier['type'] = p[3]['type']
	identifier['temp_name'] = p[3]['temp_name']
	if (ST.is_identifier_exist(identifier['name'],0) == False):
		ST.add_symbol(identifier['name'], identifier['type'],1)
		ST.add_attribute(p[1], 'type', p[3]['type'])
		temp_name = ST.make_temp(variable=p[1])
		ST.add_attribute(identifier['name'],'temporary_name', temp_name)
		TAC.emit(temp_name, p[3]['temp_name'], '', '=')          
	else:
		TAC.emit(ST.lookup(identifier['name'],0)['temporary_name'], p[3]['temp_name'], '', '=') 

def p_s_assignment(p):
	'''assignment : SCALAR_VARIABLE ASSIGNMENT expression SEMICOLON'''
	p[0] = {}
	identifier = {}
	identifier['name'] = p[1]
	identifier['type'] = p[3]['type']
	identifier['temp_name'] = p[3]['temp_name']
	if (ST.is_identifier_exist(identifier['name'],0) == False):
		ST.add_symbol(identifier['name'], identifier['type'],1)
		ST.add_attribute(p[1], 'type', p[3]['type'])
		temp_name = ST.make_temp(variable=p[1])
		ST.add_attribute(identifier['name'],'temporary_name', temp_name)
		TAC.emit(temp_name, p[3]['temp_name'], '', '=')          
	else:
		TAC.emit(ST.lookup(identifier['name'],0)['temporary_name'], p[3]['temp_name'], '', '=') 

def p_assignment(p):
	''' assignment :  ARRAY_VARIABLE ASSIGNMENT  array  SEMICOLON 
					| HASH_VARIABLE ASSIGNMENT LPAR hashList RPAR SEMICOLON
					| ARRAY_VARIABLE ASSIGNMENT KEYS HASH_VARIABLE SEMICOLON
					| ARRAY_VARIABLE ASSIGNMENT VALUES HASH_VARIABLE SEMICOLON
					| ARRAY_VARIABLE ASSIGNMENT LPAR INTEGER DOUBLE_DOT INTEGER RPAR SEMICOLON'''
			

	#p[0] = treeNode('assignment', output, p)
	p[0] = {}
	identifier = {}
	identifier['name'] = p[1]
	identifier['type'] = 'UNDEFINED'
	global globvar
	global var
	globvar = -2
	var = 0
	#ST.add_symbol(p[1], 'UNDEFINED',1)
	ST.add_symbol(p[1],'UNDEFINED',1) 


def p_array1(p):
	'''array : ARRAY_VARIABLE'''
	p[0] = {}


	

def p_array(p):
	'''array : LPAR arrayList RPAR'''
	p[0] = {}

def p_arrayList(p):
    '''arrayList : array_expression COMMA arrayList
    				| array_expression'''
    p[0] = {}

def p_array_expression(p):
	'''array_expression : expression'''

	global globvar
	global var
	globvar += 2
	a = ST.make_temp()
	TAC.emit(a, var, '','=i')
	var += 1
	b = ST.make_temp()
	TAC.emit(b,a,'4','*')
	c = ST.make_temp()
	arr_var = '$'+str(p[-3-globvar])[1:]+'['+ str(var-1) +']'
	ST.add_symbol(arr_var, 'UNDEFINED',1)
	ST.add_attribute(arr_var,'temporary_name', c)
	TAC.emit(c,b,'base','+')
	TAC.emit('*'+c,p[1]['temp_name'],'','=i')
     
def p_arrayList2(p):
    '''arrayList : epsilon'''

    #p[0] = treeNode('arrayList', output, p)
    p[0] = {'value': [], 'type': 'UNDEFINED'}



def p_hashList(p):
    '''hashList : expression COMMA expression COMMA hashList 
    			| expression COMMA expression'''

    #p[0] = treeNode('hashList', output, p)	
					
def p_declaration(p):
		'''declaration : MY SCALAR_VARIABLE SEMICOLON 
						| MY ARRAY_VARIABLE SEMICOLON'''

		#p[0] = treeNode('declaration', output, p)
		

           


def p_function_call(p):
	'''function_call : function_name LPAR argumentList RPAR SEMICOLON '''

	p[0] = {}
	no_of_argument = p[3]['arguments']
	ST.set_function_attribute(p[1]['name'],'arguments',no_of_argument)
	TAC.emit('', '', p[1]['name'], 'JUMP_LABEL')
	if(ST.get_function_attribute(p[1]['name'], 'return_type') != None) :
		temp = ST.make_temp()
		TAC.emit(temp, '', p[1]['name'], 'FUNCTION_RETURN')
		p[0]['temp_name'] = temp
		p[0]['type'] = ST.get_function_attribute(p[1]['name'], 'return_type')


def p_function_name(p):
	'''function_name : IDENTIFIER '''

	p[0] = {}
	p[0]['name'] = p[1]
	if not ST.is_function_exist(p[1]):
		print "ERROR : funtion not declared"
		sys.exit(0)
	
	
	#p[0] = treeNode('function_call', output, p)

def p_argumentList1(p):
	'''argumentList : epsilon'''
	p[0] = {}
	p[0]['arguments'] = 0
	

def p_argumentList(p):
	'''argumentList : expression arguments 
					'''

	#p[0] = treeNode('argumentList', output, p)
	p[0] = {}
	p[0]['arguments'] = p[2]['arguments'] + 1

	TAC.emit('','',p[1]['temp_name'],'PUSHPARAM')

def p_arguments(p):
		'''arguments : COMMA expression arguments'''

		#p[0] = treeNode('arguments', output, p)
		p[0] = {}
		p[0]['arguments'] = p[3]['arguments'] + 1

		TAC.emit('','',p[2]['temp_name'],'PUSHPARAM')

def p_arguments1(p):
	'''arguments : epsilon'''
	p[0] = {}	
	p[0]['arguments'] = 0	

def p_return(p):
		'return : RETURN expression SEMICOLON'

		#p[0] = treeNode('return', output, p)
		p[0] = {}
		ST.set_function_attribute(ST.get_current_scope(),'return_type',p[2]['type'])
		TAC.emit(p[2]['temp_name'], p[2]['type'] ,'', 'RETURN')

def  p_break(p):
	'break : BREAK SEMICOLON'

	p[0] = {}
	p[0]['end_list'] = [TAC.getnext_quad()]
	TAC.emit('', '', -1, 'GOTO')

	
def p_continue(p):
	'continue : CONTINUE SEMICOLON'

	p[0] = {}
	p[0]['begin_list'] = [TAC.getnext_quad()]
	TAC.emit('', '', -1, 'GOTO')
		#p[0] = treeNode('continue', output, p)


def p_chomp(p):
	'chomp : CHOMP expression SEMICOLON' 	

	#p[0] = treeNode('chomp', output, p)

def p_subroutine(p):
	'''subroutine : SUB marker identifier M_sub block marker1'''		
	#p[0] = treeNode('subroutine', output, p)

	p[0] = {}
	p[0]['next_list']=[]
	p[0]['type'] = 'VOID'
	p[0]['next_list'] = TAC.merge(p[5].get('end_list', []), p[5].get('next_list', []))
	p[0]['next_list'] = TAC.merge(p[4].get('false_list', []), p[0].get('next_list', []))
	

def p_sub(p):
	'''M_sub : epsilon'''
	p[0] = {}
   	p[0]['false_list'] = [TAC.getnext_quad()]
  


def p_identifier(p):
	'''identifier : IDENTIFIER'''
	p[0] = {}
	ST.add_function(p[1])
	TAC.new_function(p[1])


def p_marker(p):
	'''marker : epsilon'''
	p[0] = {}
	ST.change_in_function()

def p_marker1(p):
	'''marker1 : epsilon'''
	p[0] = {}
	TAC.emit('', '', '', 'JUMPBACK_TO_CALLEE')
	ST.change_in_function()
	

############PRINT#############		
def p_print(p):
		'''print : PRINT printlist SEMICOLON '''
		p[0] = {}
		
		if p[2]['type'] == 'NUMBER':
			TAC.emit(p[2]['temp_name'], '', p[2]['type'], 'printcall')
		else:
			TAC.emit(p[2]['temp_name'], '', p[2]['type'], 'printcall')
		#p[0] = treeNode('print', output, p)
		
def p_die(p):
		'''die : DIE printlist SEMICOLON '''

		#p[0] = treeNode('die', output, p)		
		
def p_printlist(p):    # baad me karege
#gayle ne 215 
		'''printlist : expression'''
		p[0] = {}
		p[0]['type'] = p[1]['type']
		p[0]['temp_name'] = p[1]['temp_name']
		#p[0] = treeNode('printlist', output, p)
		
		
	
	
########################################
############## EXPRESSIONS #############


precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQUAL', 'NOT_EQUAL'),
        ('left', 'OP_LESS_THAN', 'OP_GREATER_THAN', 'OP_LESS_THAN_E', 'OP_GREATER_THAN_E'),
        ('right','EXPONENT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE', 'MODULUS'),
        ('right', 'MINUS', 'NOT'),
        )

######## UNARY EXPRESSIONS ############

def p_expression_unary(p):
    '''expression : MINUS expression 
    			| INCREAMENT expression 
    			| expression INCREAMENT 
    			| DCREAMENT expression 
    			| expression DCREAMENT''' 

    #p[0] = treeNode('expression', output, p)    
    p[0] = {}
    p[0]['temp_name'] = ST.make_temp()
    if p[1] == '++':
    	p[0]['type'] = p[2]['type']
    	temp = ST.make_temp()
    	TAC.emit(temp, '1', '', '=i')
        TAC.emit(p[2]['temp_name'], p[2]['temp_name'] , temp , '+')
    if p[1] == '--':
    	p[0]['type'] = p[2]['type']
    	temp = ST.make_temp()
    	TAC.emit(temp, '1', '', '=i')
        TAC.emit(p[2]['temp_name'], p[2]['temp_name'] , temp , '-')
    if p[2] == '++':
    	p[0]['type'] = p[1]['type']
    	temp = ST.make_temp()
    	TAC.emit(temp, '1', '', '=i')
       	TAC.emit(p[1]['temp_name'], p[1]['temp_name'] , temp , '+')
    if p[2] == '--':
    	p[0]['type'] = p[1]['type']
    	temp = ST.make_temp()
    	TAC.emit(temp, '1', '', '=i')
       	TAC.emit(p[1]['temp_name'], p[1]['temp_name'] , temp , '-')
    if p[1] == '-':
    	p[0]['type'] = p[2]['type']
        TAC.emit(p[0]['temp_name'], p[2]['temp_name'] , temp , 'unary-')

######## BINARY EXPRESSIONS ############

def p_expression_binop(p):
	'''expression : expression PLUS expression
	              | expression MINUS expression
	              | expression MULTIPLY expression
	              | expression DIVIDE expression
	              | expression MODULUS expression
	              | expression EXPONENT expression'''


	#p[0] = treeNode('expression', output, p) 
	# To store information
	p[0] = {}
	p[0]['temp_name'] = ST.make_temp()
	if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
		p[0]['type'] = 'NUMBER'
		

	if p[2] == '+':
		TAC.emit(p[0]['temp_name'], p[1]['temp_name'] , p[3]['temp_name'] , '+')
	if p[2] == '-':
	   TAC.emit(p[0]['temp_name'], p[1]['temp_name'] , p[3]['temp_name'] , '-')
	if p[2] == '*':
	  	TAC.emit(p[0]['temp_name'], p[1]['temp_name'] , p[3]['temp_name'] , '*')
	if p[2] == '/':
	   TAC.emit(p[0]['temp_name'], p[1]['temp_name'] , p[3]['temp_name'] , '/')
	if p[2] == '%':
	   TAC.emit(p[0]['temp_name'], p[1]['temp_name'] , p[3]['temp_name'] , '%')
	if p[2] == '**':
	   TAC.emit(p[0]['temp_name'], p[1]['temp_name'] , p[3]['temp_name'] , '**')


def p_ternary(p):
	'''expression : expression Q_MARK M_QMARK expression COLON M_COLON expression '''  

	#p[0] = treeNode('expression', output, p) 	     
	p[0] = {}

	p[0]['temp_name'] = ST.make_temp()
	TAC.back_patch(p[5]['false_list'], p[8]['quad'])
	p[0]['next_list'] = p[8]['next_list']
	p[0]['end_list'] = TAC.merge(p[7].get('end_list', []), p[4].get('end_list', []))
	p[0]['begin_list'] = TAC.merge(p[7].get('begin_list', []), p[4].get('begin_list', []))

def p_M_QMARK(p):
    'M_QMARK : epsilon'

    p[0] = {}
    p[0]['false_list'] = [TAC.getnext_quad()]
    TAC.emit(p[-2]['temp_name'], '', -1, '')

def p_M_COLON(p):
    'M_COLON : epsilon'

    p[0] = {}
    p[0]['next_list'] = [TAC.getnext_quad()]
    TAC.emit('', '', -1, 'GOTO')

    p[0]['quad'] = TAC.getnext_quad()
######## RELATIONAL EXPRESSION ############

def p_expression_relational(p):
    '''expression : expression OP_GREATER_THAN expression
                  | expression OP_GREATER_THAN_E expression
                  | expression OP_LESS_THAN expression
                  | expression OP_LESS_THAN_E expression
                  | expression EQUAL expression
                  | expression NOT_EQUAL expression
                  | expression STRING_CMP expression'''

    #p[0] = treeNode('expression', output, p)   
    # print "d"
    p[0] = {} 
    p[0]['temp_name'] = ST.make_temp()
    p[0]['type'] = 'BOOLEAN'
    # Emit code
    TAC.emit(p[0]['temp_name'], p[1]['temp_name'], p[3]['temp_name'], p[2])


######## LOGICAL EXPRESSION ##############

def p_expression_logical_and(p):
    'expression : expression AND expression'        

    #p[0] = treeNode('expression', output, p)    
    p[0] = {}
    p[0]['temp_name'] = ST.make_temp()
    p[0]['type'] = 'BOOLEAN'
    TAC.emit(p[0]['temp_name'], p[1]['temp_name'], p[4]['temp_name'] , p[2])

def p_expression_logical_or(p):
    'expression : expression OR expression'        

    #p[0] = treeNode('expression', output, p)    
    p[0] = {}
    p[0]['temp_name'] = ST.make_temp()
    p[0]['type'] = 'BOOLEAN'
    TAC.emit(p[0]['temp_name'], p[1]['temp_name'], p[4]['temp_name'] , p[2])

def p_expression_logical_not(p):
    'expression : NOT expression'

    #p[0] = treeNode('expression', output, p)
    p[0] = {}
    p[0]['temp_name'] = ST.make_temp()
    p[0]['type'] = 'BOOLEAN'
    TAC.emit(p[0]['temp_name'], p[2]['temp_name'], '' , p[1])    

######## GROUP EXPRESSION ##############

def p_expression_group(p):
    'expression : LPAR expression RPAR'

    #p[0] = treeNode('expression', output, p)    
    p[0] = {}

    # emit code
    p[0]['temp_name'] = p[2]['temp_name']
    p[0]['type'] = p[2]['type']
    p[0]['true_list'] = p[2].get('true_list', [])
    p[0]['false_list'] = p[2].get('false_list', [])

######## IDENTIFIER EXPRESSION ###########

def p_expression_identifier(p):
    '''expression : SCALAR_VARIABLE'''

    #p[0] = treeNode('expression', output, p)    
    p[0] = {}

    if ST.is_identifier_exist(p[1],0):
    	p[0]['type'] = ST.get_attribute(p[1], 'type')
        p[0]['temp_name'] = ST.get_attribute(p[1], 'temporary_name')
    else :
    	p[0]['temp_name'] = ST.make_temp(variable=p[1])
    	print "variable not declared"
        sys.exit(0)



def p_constant(p):
	'''expression : constant'''

	#p[0] = treeNode('expression', output, p)
	p[0] = { 'type' : p[1]['type'] }
	p[0]['name'] = 'constant'
	p[0]['temp_name'] = ST.make_temp()
	
	if(p[1]['type'] != 'STRING' and p[1]['type'] != 'PSEUDO_STRING'):
		TAC.emit(p[0]['temp_name'], p[1]['value'], '', '=i')
	else :
		TAC.emit(p[0]['temp_name'], p[1]['value'], '', '=s')
	

def p_INTEGER(p):
	'constant : INTEGER'

	p[0] = { 'type' : 'NUMBER', 'value' : p[1] }

def p_float(p):
	'constant : FLOAT'

	p[0] = { 'type' : 'NUMBER', 'value' : p[1] }

def p_hexadecimal(p):
	'constant : HEXADECIMAL'

	p[0] = { 'type' : 'HEXADECIMAL', 'value' : p[1] }

def p_octal(p):
	'constant : OCTAL'

	p[0] = { 'type' : 'OCTAL', 'value' : p[1] }

def p_binary(p):
	'constant : BINARY'

	p[0] = { 'type' : 'BINARY', 'value' : p[1] }

def p_exponantial(p):
	'constant : EXPONANTIAL'

	p[0] = { 'type' : 'NUMBER', 'value' : p[1] }

def p_string(p):
	'constant : STRING'

	p[0] = { 'type' : 'STRING', 'value' : p[1] }
	ST.add_string(p[1])

def p_psuedo_string(p):
	'constant : PSEUDO_STRING'

	p[0] = { 'type' : 'PSEUDO_STRING', 'value' : p[1] }
	ST.add_string(p[1])

def p_expression_input_no(p):
	'''expression : INPUT'''
  
	#p[0] = treeNode('expression', output, p)    
	p[0] = {}
	p[0]['temp_name'] = ST.make_temp()
	p[0]['type'] = 'NUMBER'
	TAC.emit(p[0]['temp_name'] , '', 'NUMBER', 'INPUT')


def p_expression_input_string(p):
	'''expression : S_INPUT'''
  
	#p[0] = treeNode('expression', output, p)    
	p[0] = {}
	p[0]['temp_name'] = ST.make_temp()
	p[0]['type'] = 'STRING'
	TAC.emit(p[0]['temp_name'], '', 'STRING', 'INPUT')


def p_M_QUAD(p):
	'M_QUAD : epsilon'

	p[0] = { 'quad' : TAC.getnext_quad()}

def p_M_STATEMENTS(p):
	'M_STATEMENTS : epsilon'

	p[0] = {}	

def p_epsilon(p):
	'epsilon :'

	#p[0] = treeNode('epsilon', output, p)     
	p[0] = {}

def p_error(p):
	print "Syntax error in input!"
	sys.exit(0)
	
parser = yacc.yacc()
ST = symbol_table.symbol_table()
TAC = three_address_code.three_address_code(ST)
parser = yacc.yacc()

#######################################
def mips_parser(program):
    result = parser.parse(program)
    return ST, TAC


def testYacc(inputFile):
    program = open(inputFile).read()
    result = parser.parse(program)
    TAC.pprint() 
    ST.print_symbol()
	
 
if __name__ == "__main__":
    from sys import argv
    filename, inputFile = argv

    testYacc(inputFile)	
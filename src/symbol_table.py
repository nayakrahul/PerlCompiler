import pprint

class symbol_table:
	def __init__(self):
		self.symboltable = {
							'main' : {
									'name':'main',
									'return_type':None,
									'in_function': False,
									'width': 0,
									'string': [],
									'arguments' : 0
									}
							}
		self.count = 0
		self.variable_name = "t"
		self.scope = [self.symboltable['main']]
		self.address_descriptor = {}


	def add_symbol(self,symbol,symbol_type,flag):
		if flag == 1 :
				self.symboltable['main'][symbol] = {
					'type' : symbol_type,
					'name' : symbol, 
					'width' : 'UNDEFINED'
				}
		else :
			if self.symboltable['main']['in_function'] == False :
				self.symboltable['main'][symbol] = {
					'type' : symbol_type,
					'name' : symbol, 
					'width' : 'UNDEFINED'
				}
			else :	
				current_scope = self.scope[len(self.scope)-1]
				self.symboltable[current_scope['name']][symbol] = {
												'type' : symbol_type,
												'name' : symbol, 
												'width' : 'UNDEFINED'
											}

	def lookup(self,symbol,flag):
		if (self.symboltable['main']['in_function'] == False):
			if self.symboltable['main'].has_key(symbol):
				return self.symboltable['main'][symbol]
			else :
				return None

		else :
			current_scope = self.scope[len(self.scope)-1]
			if(self.symboltable[current_scope['name']].has_key(symbol)):
				return current_scope[symbol]
			elif(self.scope[0].has_key(symbol)) :
				if(flag == 0):
					return self.scope[0][symbol]
				else :
					return None;
			else :
				return None

	def print_symbol(self):
		pprint.pprint(self.symboltable)

	def make_temp(self,variable=''):
		create_new = self.variable_name + str(self.count)
		self.count+=1
		self.address_descriptor[create_new] = { 'memory': None , 
                                                'register': None, 
                                                'store': False, 
                                                'dirty': False,
                                                'scope': self.get_current_scope(),
                                                'variable': variable}
		if (self.symboltable['main']['in_function'] == False):
			self.symboltable['main']['width'] += 4
		else:
			current_scope = self.scope[len(self.scope)-1]
			self.symboltable[current_scope['name']]['width'] += 4
		return create_new

	def add_attribute(self,symbol,name,value):
		self.lookup(symbol,0)[name] = value;

	def get_attribute(self,symbol,attribute_name):
		if self.lookup(symbol,0).has_key(attribute_name):
			return self.lookup(symbol,0)[attribute_name]
	

	def is_identifier_exist(self,symbol,flag):
		if (self.lookup(symbol,flag)!= None) :
			return True
		else :
			return False

	def get_current_scope(self) :
		if (self.symboltable['main']['in_function'] == False):
			return self.scope[0]['name']
		else :	
			return self.scope[len(self.scope) - 1]['name']

	def add_function(self,function_name):
		self.symboltable[function_name] = {
                'name': function_name, 
                'return_type':None,
                'width':0,
                'string': [],
                'arguments': 0
                }
   		self.scope.append(self.symboltable[function_name])

	def change_in_function(self):
		self.symboltable['main']['in_function'] = not(self.symboltable['main']['in_function'])


	def is_function_exist(self,function_name):
		if (self.symboltable.has_key(function_name)) :
			return True
		else :
			return False


	def get_function_attribute(self,function_name,attribute_name):
		if (self.symboltable.has_key(function_name)) :
			return self.symboltable[function_name][attribute_name]
		else :
			return None

	def add_string(self,string_value):
		if (self.symboltable['main']['in_function'] == False):
			self.symboltable['main']['string'].append(string_value)
		else:
			current_scope = self.scope[len(self.scope)-1]
			self.symboltable[current_scope['name']]['string'].append(string_value)

	def set_function_attribute(self,function_name,attribute_name,attribute_value):
		if (self.symboltable.has_key(function_name)) :
			self.symboltable[function_name][attribute_name] = attribute_value
		else :
			print "Function with this name don't exits"



	
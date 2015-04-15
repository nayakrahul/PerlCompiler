class three_address_code:
	def __init__(self,ST):
		self.code = {'main' : []}
		self.quad = {'main' : -1}
		self.nextquad = {'main' : 0}
		
		self.ST = ST

	def new_function(self,function_name):
		self.code[function_name] = []
		self.quad[function_name] = -1
		self.nextquad[function_name] = 0


		
	def increment_quad(self):
		if (self.ST.symboltable['main']['in_function'] == True):
			current_function = self.ST.get_current_scope()
			self.quad[current_function] = self.nextquad[current_function]
			self.nextquad[current_function]+=1
		else :
			self.quad['main'] = self.nextquad['main']
			self.nextquad['main']+=1


	def getnext_quad(self):
		if (self.ST.symboltable['main']['in_function'] == True):
			current_function = self.ST.get_current_scope()
			return self.nextquad[current_function]
		else:
			return self.nextquad['main']

	def emit(self,destination,source1,source2,operator):
		self.increment_quad()
		if (self.ST.symboltable['main']['in_function'] == True):
			current_function = self.ST.get_current_scope()
			self.code[current_function].append([destination,source1,source2,operator])
		else :
			self.code['main'].append([destination,source1,source2,operator])


	def merge(self,list1,list2):
		list3 = list(list1)
		list3.extend(list2)
		return list3


	def back_patch(self,lists,location):
		if (self.ST.symboltable['main']['in_function'] == True):
			current_function = self.ST.get_current_scope()
			for positon in lists:
				self.code[current_function][positon][2] = location

		else :
			for positon in lists:
				self.code['main'][positon][2] = location

	def pprint(self):
		print "\n\n----------------------------------------------\n"
		for funtion in self.code.keys():
			print "\n%s: "%funtion
		
			for i in range(len(self.code[funtion])):
				
				code = self.code[funtion][i]
				if code[3] == "=i":
					print "%5d: \t%s = %s" %(i,code[0],code[1])

				elif code[3] == "=s":
					print "%5d: \t%s = %s" %(i,code[0],code[1])
					
			 	elif code[3] == '=':
					print "%5d: \t%s %s %s" % (i,code[0],code[3],code[1])
					
				elif (code[3] == 'COND_GOTO_Z' or code[3] == 'printcall' or code[3] == 'GOTO' ):
					print "%5d: \t%s %s %s %s" % (i,code[0],code[1],code[3],code[2])
						
				else:
					print "%5d: \t%s = %s %s %s" % (i,code[0],code[1],code[3],code[2])	
				
		
import os
import sys

from dumbo_parser import dumbo_parser

# Dictionnary that stores the variables.
# Key is the current depth that we're in (for imbricated for loops)
# Value is a dictionnary containing the variable names as keys, and values as values.
variables = {}

# Current depth that we're computing at
current_depth = 0

def dumbo_interpreter(datapath, templatepath, outputpath):
	read_data(datapath)
	output = apply_template(templatepath)
	outputfile=open(outputpath, 'w')
	outputfile.write(output)
	outputfile.close()

# Reads data from the data file, to initialize the variables
def read_data(datapath):
	global variables
	datafile = open(datapath, 'r')
	data = dumbo_parser.parse(datafile.read()) 
	variables[current_depth] = {}
	for elem in data:
		if type(elem) is tuple: #https://www.geeksforgeeks.org/python-check-if-variable-is-tuple/
			if elem[0] == "assign":
				variables[current_depth][elem[1]] = elem[2]
			else:
				raise Exception
	datafile.close()
	return

# Applies the template from the template file to the variables
def apply_template(templatepath):
	out = ""
	templatefile = open(templatepath, 'r')
	template = dumbo_parser.parse(templatefile.read())
	if template == "":
		return ""

	for elem in template:
		if type(elem) is str:
			out += elem
		elif type(elem) is tuple:
			out += apply_function(elem) 

	templatefile.close()
	return out

# Applies a dumbo function given a parsed tuple
# -assign
# -concatenate
# -for
# -if
# -print
# -arithmetic operations (+,-,*,/)
# -comparators (<,>,=,!=)
# -logical operations (or, and)
def apply_function(function):
	name = function[0]
	
	if name == "assign":
		function_assign(function[1], function[2])
		return ""

	elif name == "concatenate":
		return function_concatenate(function[1], function[2])

	elif name == "for":
		return for_loop(function[1], function[2], function[3])

	elif name == "if":
		if len(function) == 3:
			return if_condition(function[1], function[2])
		else:
			return if_condition(function[1], function[2], function[3])
	elif name == "print":
		return function_print(function[1])
	elif name in arithmetic_ops:
		if name=="-" and len==2:
			return arithmetic_ops[name](0, find_variable(function[1])) # Unary minus
		else:
			return arithmetic_ops[name](find_variable(function[1]), find_variable(function[2]))
	elif name in comparators_ops:
		return comparators_ops[name](find_variable(function[1]), find_variable(function[2]))
	elif name in logical_ops:
		if type(function[1]) is tuple:
			function[1] = apply_function(function[1])
		if type(function[2]) is tuple:
			function[2] = apply_function(function[2])

		return logical_ops[name](function[1], function[2])
	else:
		raise Exception

# Function dor assigning a value to a variable
def function_assign(variable, value):
	# Checks if the value has to be computed first
	if type(value) is tuple:
		value = apply_function(value)

	#Checks if we replace an already declared variable at a higher depth
	for i in range(current_depth, -1, -1):
		if variable in variables[i]:
			variables[i][variable]=value
			return ""
	# Else we assign it to a new variable at current depth
	variables[current_depth][variable]=value


# Function for concatenating two strings 
def function_concatenate(elem1, elem2):
	if type(elem2) is str:
		return find_variable(elem1) + find_variable(elem2)
	elif type(elem2) is tuple:
		return find_variable(elem1) + apply_function(elem2)

# Function for printing
def function_print(elem):
	if type(elem) is str:
		return str(find_variable(elem))
	elif type(elem) is tuple:
		return apply_function(elem)

# Function that manages for loops (for elem in listname do body endfor)
def for_loop(elem, listname, body):
	global current_depth

	# Increment current depth since we enter a new loop
	current_depth += 1
	# Initialize the new variables dictionnary at this depth
	variables[current_depth] = {}

	# Search for the list name in lower depth variables
	for i in range(current_depth-1, -1, -1):
		if listname in variables[i]:
			for_list = variables[i][listname]
			break

	output = ""

	for i in range(len(for_list)):
		variables[current_depth][elem] = for_list[i]
		for instruction in body:
			output += apply_function(instruction)

	# Clear all the variables at that depth
	variables[current_depth].clear()

	# Decrement the current depth since we exit a loop
	current_depth -=1

	return output

# Function that manages if conditions (if condition then body else body_else endif)
def if_condition(condition, body):
	if type(condition) is tuple:
		condition = apply_function(condition)

	output = ""

	if condition:
		for instruction in body:
			output += apply_function(instruction)

	return output

# Find a variable given it's name, returns a string if the variable is not defined
# Priority is given to most deeply defined value
def find_variable(string):
	for i in range(current_depth, -1, -1):
		if string in variables[i]:
			return variables[i][string]
	return string

arithmetic_ops = {
    "+": lambda x, y: str(float(x)+float(y)),
    "-": lambda x, y: str(float(x)-float(y)),
    "*": lambda x, y: str(float(x)*float(y)),
    "/": lambda x, y: str(float(x)/float(y)), 
}

comparators_ops = {
	"<": lambda x, y: float(x) < float(y),
    ">": lambda x, y: float(x) > float(y),
    "=": lambda x, y: float(x) == float(y),
    "!=": lambda x, y: float(x) != float(y),
}

logical_ops = {
	"and": lambda x, y: x and y,
    "or": lambda x, y: x or y,
}


if __name__ == "__main__":
	if len(sys.argv) == 4:
		dumbo_interpreter(sys.argv[1],sys.argv[2],sys.argv[3])
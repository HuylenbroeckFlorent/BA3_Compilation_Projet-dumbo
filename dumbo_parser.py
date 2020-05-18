import ply.lex as lex
import ply.yacc as yacc
from dumbo_lex import tokens

#<programme> -> <txt>|<txt><programme>
def p_programme_TO_txt_OR_txt_programme(p):
	''' programme 	: TXT 
					| TXT programme'''
	if len(p) == 2:
		p[0] = [p[1]] #TXT
	elif len(p) == 3:
		p[0] = [p[1]] + p[2] #TXT programme

#<programme> -> <dumbo_block> | <dumbo_block><programme>
def p_programme_TO_dblock_OR_dblock_programme(p):
	''' programme 	: DUMBO_BLOCK 
					| DUMBO_BLOCK programme'''
	if len(p) == 2: 
		p[0] = p[1] #DBLOCK
	elif len(p) == 3:
		p[0] = p[1] + p[2] #DBLOCK programme

#<txt> -> [a-zA-Z0-9;&<>"_=.\/ \n\s:,"-]+

#<dumbo_bloc> -> {{<expression_list>}}
def p_dumbo_block_TO_open_expression_list_close(p):
	'''DUMBO_BLOCK : DUMBO_BLOCK_START expression_list DUMBO_BLOCK_END'''
	p[0]=p[2]

##<dumbo_bloc> -> {{ }} ##Thanks template3 for pointing that out
def p_dumbo_block_TO_open_close(p):
	'''DUMBO_BLOCK : DUMBO_BLOCK_START DUMBO_BLOCK_END'''
	p[0]=[]

#<expression_list> -> <expression> ; <expression_list>
def p_expression_list_TO_expression_semicolon_expression_list(p):
	'''expression_list : expression SEMICOLON expression_list'''
	p[0] = [p[1]] + p[3]

#<expression_list> -> <expression>
def p_expression_list_TO_expression_semicolon(p):
	'''expression_list : expression SEMICOLON'''
	p[0] = [p[1]]

#<expression> -> print<string_expression>
def p_expression_TO_print_string_expression(p):
	'''expression : PRINT string_expression'''
	p[0] = ("print", p[2])

#<expression> -> for <variable> in <string_list> do <expression_list> endfor
#<expression> -> for <variable> in <variable> do <expression_list> endfor
def p_expression_TO_for_variable_in_string_list_do_expression_list_endfor(p):
	'''expression : FOR VARIABLE IN string_list DO expression_list ENDFOR
				  | FOR VARIABLE IN VARIABLE DO expression_list ENDFOR'''
	p[0] = ("for", p[2], p[4], p[6])


#<expression> -> <variable> := <string_expression>
#<expression> -> <variable> := <string_list>
def p_expression_TO_assign_string_or_variable(p):
	'''expression 	: VARIABLE ASSIGN string_expression
					| VARIABLE ASSIGN string_list'''
	p[0] = ("assign", p[1], p[3])

#<string_expression> -> <string>
#<string_expression> -> <variable>
def p_string_expression_TO_string_or_variable(p):
	'''string_expression 	: STRING 
							| comparable_expression''' ###DLC
	p[0]=p[1]

#<string_expression> -> <string_expression>.<string_expression>
def p_string_expression_TO_string_expression_dot_string_expression(p):
	'''string_expression : string_expression DOT string_expression'''
	p[0] = ("concatenate", p[1],p[3])

#<string_list> -> (<string_list_interior>)
def p_string_list_TO_lparen_string_list_interior_rparen(p):
	'''string_list : LPAREN string_list_interior RPAREN'''
	p[0] = p[2]

#<string_list_interior> -> <string> | <string>,<string_list_interior>
def p_string_list_interior(p):
	'''string_list_interior : STRING 
							| STRING COMMA string_list_interior'''
	if len(p) == 2:
		p[0] = [p[1]]
	elif len(p) == 4:
		p[0] = [p[1]] + p[3]

def p_error(p):
    print("Syntax error in line "+str(p.lineno))
    print(str(p))


########################### DLC ###########################

#<comparable_expression> -> VARIABLE | <number_expression>
def p_comparable_expression_TO_variable_OR_number_expression(p):
	'''comparable_expression 	: VARIABLE
								| number_expression'''
	p[0] = p[1]

#<expression> -> IF <boolean_expression> DO <expression_list> ENDIF
def p_expression_if(p):
	'''expression : IF boolean_expression DO expression_list ENDIF'''
	p[0] = ("if", p[2], p[4])

#<boolean_expression> -> <boolean>
def p_boolean_expression_TO_boolean(p):
	'''boolean_expression : boolean'''
	p[0] = p[1]

#<boolean_expression> -> <boolean> AND/OR <boolean_expression>
def p_boolean_expression_TO_boolean_AND_OR_boolean_expression(p):
	'''boolean_expression 	: boolean AND boolean_expression
							| boolean OR boolean_expression'''
	p[0] = (p[2], p[1], p[3])

#<number_expression> -> <number>
def p_number_expression_TO_number_or_variable(p):
	'''number_expression 	: NUMBER'''
	p[0] = p[1]

#<number_expression> -> <number_expression> + <number_expression>
#<number_expression> -> <number_expression> - <number_expression>
#<number_expression> -> <number_expression> * <number_expression>
#<number_expression> -> <number_expression> / <number_expression>
def p_number_expression_TO_number_expression_op_number_expression(p):
	'''number_expression 	: comparable_expression PLUS comparable_expression
							| comparable_expression MINUS comparable_expression
							| comparable_expression MULT comparable_expression
							| comparable_expression DIV comparable_expression'''
	p[0] = (p[2], p[1], p[3])

#<number_expression> -> -<number_expression>
def p_number_expression_TO_unary_minus_number_expression(p):
	'''number_expression : UNARY_MINUS number_expression'''
	p[0] = -p[2]

#<boolean> -> TRUE | FALSE
def p_boolean_TO_true_or_false(p):
	'''boolean 	: TRUE
				| FALSE'''
	p[0]=p[1]

#<boolean> -> <number_expression> COMPARATOR <number_expression>
def p_boolean_TO_expression_comparator_expression(p):
	'''boolean 	: comparable_expression COMPARATOR comparable_expression'''
	p[0] = (p[2], p[1], p[3])

precedence = (("left", "PLUS", "MINUS"), ("left", "MULT", "DIV"), ("right", "UNARY_MINUS"))

dumbo_parser = yacc.yacc(outputdir="output")
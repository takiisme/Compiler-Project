// Name: Thái Tài
// ID: 2052246

grammar MT22;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    token = self.type
    if token == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif token == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif token == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// Fragment
fragment Digit: [0-9];
fragment Lowercase: [a-z];
fragment Uppercase: [A-Z];
fragment Underscore: [_];
fragment Letter: Lowercase | Uppercase;
fragment Decimal: [.] Digit*;
fragment Exponent: [eE][+-]? Digit+;
fragment Escape_seq: '\\' [bfnrt'"\\];
fragment Character: ~[\f\r\n'"\\] | Escape_seq;
fragment Not_escape: '\\' ~[bfnrt'"\\];

program : (variable_declaration | function_declaration) program_body EOF;
program_body: (variable_declaration | function_declaration) program_body | ;

// Parser (Syntax Analysis)

// Declaration
variable_declaration : id_list COLON variable_type_without_void SEMI | variable_declaration_without_semi SEMI;
variable_declaration_without_semi: IDENTIFIER COLON variable_type_without_void ASSIGN expression | IDENTIFIER COMMA variable_declaration_without_semi COMMA expression;
id_list: IDENTIFIER id_list_body | IDENTIFIER;
id_list_body: COMMA IDENTIFIER id_list_body | ;

function_declaration: IDENTIFIER COLON FUNCTION variable_type LB nullable_parameter_list RB (INHERIT IDENTIFIER | ) block_statement;
parameter_one: (INHERIT | ) (OUT | ) IDENTIFIER COLON variable_type_without_void;
nullable_parameter_list: parameter_one parameter_list_body | ;
parameter_list: parameter_one parameter_list_body | parameter_one;
parameter_list_body: COMMA parameter_one parameter_list_body | ;

// Statement
assign_statement:           (IDENTIFIER | index_operation) ASSIGN expression SEMI;
if_statement:               IF LB expression RB statement (ELSE statement | );
for_statement:              FOR LB (IDENTIFIER | index_operation) ASSIGN expression COMMA expression COMMA expression RB statement;
while_statement:            WHILE LB expression RB statement;
do_while_statement:         DO block_statement WHILE LB expression RB SEMI; // block_statement -> statement
break_statement:            BREAK SEMI;
continue_statement:         CONTINUE SEMI;
return_statement:           RETURN (expression | ) SEMI;
call_statement:             IDENTIFIER LB nullable_expression_list RB SEMI;
block_statement:            LCB block_statement_body RCB;
block_statement_body:       (statement | variable_declaration) block_statement_body | ;

statement:  assign_statement | if_statement | for_statement | 
            while_statement | do_while_statement | return_statement | 
            call_statement | block_statement | break_statement | continue_statement;

// Expression
expression:                 relational_expression CONCATENATE relational_expression | relational_expression;
relational_expression:      logical_expression (EQUAL | NOT_EQUAL | SMALL | LARGE | SMALL_EQUAL | LARGE_EQUAL) logical_expression | logical_expression;
logical_expression:         logical_expression (AND | OR) additive_expression | additive_expression;
additive_expression:        additive_expression (ADD | SUBTRACT) multiplicative_expression | multiplicative_expression;
multiplicative_expression:  multiplicative_expression (MULTIPLY | DIVIDE | MODULO) not_expression | not_expression;
not_expression:             NOT not_expression | sign_expression;
sign_expression:            SUBTRACT sign_expression | index_expression;
index_expression:           index_operation | operand;
operand:                    primitive_lit | function_call | IDENTIFIER | arraylit | LB expression RB;

nullable_expression_list: expression expression_list_body | ;
expression_list: expression expression_list_body | expression;
expression_list_body: COMMA expression expression_list_body | ;

index_operation: IDENTIFIER LSB expression_list RSB;
function_call: IDENTIFIER LB nullable_expression_list RB;

// Lexer (Lexical Analysis)

// Literals
INTEGER_LIT:        ([0] | [1-9](Digit* | (Digit* Underscore Digit+)*)) {self.text = self.text.replace('_','')};
FLOAT_LIT:          (INTEGER_LIT Decimal | INTEGER_LIT Exponent | INTEGER_LIT Decimal Exponent | Decimal Exponent) {self.text = self.text.replace('_','')};
BOOLEAN_LIT:        TRUE | FALSE;
STRING_LIT:         '"' Character* '"' { self.text = self.text[1:-1]};
primitive_lit:      INTEGER_LIT | FLOAT_LIT | BOOLEAN_LIT | STRING_LIT;
arraylit:           LCB nullable_expression_list RCB;

array_type:         ARRAY LSB intlit_list RSB OF (INTEGER | BOOLEAN | FLOAT | STRING);
intlit_list:        INTEGER_LIT intlit_list_body | INTEGER_LIT;
intlit_list_body:   COMMA INTEGER_LIT intlit_list_body | ;

variable_type_without_void:     INTEGER | BOOLEAN | FLOAT | STRING | array_type | AUTO;
variable_type:                  variable_type_without_void | VOID;

// Keywords
AUTO:       'auto';
BREAK:      'break';
BOOLEAN:    'boolean';
DO:         'do';
ELSE:       'else';
FALSE:      'false';
FLOAT:      'float';
FOR:        'for';
FUNCTION:   'function';
IF:         'if';
INTEGER:    'integer';
RETURN:     'return';
STRING:     'string';
TRUE:       'true';
WHILE:      'while';
VOID:       'void';
OUT:        'out';
CONTINUE:   'continue';
OF:         'of';
INHERIT:    'inherit';
ARRAY:      'array';

// Identifiers
IDENTIFIER: (Letter | Underscore) (Letter | Digit | Underscore)*;

// Operators:
ADD:        '+';
SUBTRACT:   '-';
MULTIPLY:   '*';
DIVIDE:     '/';
MODULO:     '%';

AND:        '&&';
OR:         '||';
EQUAL:      '==';
NOT_EQUAL:  '!=';
SMALL_EQUAL: '<=';
LARGE_EQUAL: '>=';
SMALL:      '<';
LARGE:      '>';
CONCATENATE: '::';
NOT:        '!';

// Separators:
LB:         '(';
RB:         ')';
LSB:        '[';
RSB:        ']';
LCB:        '{';
RCB:        '}';
SEMI:       [;];
COMMA:      [,];
ASSIGN:     '=';
COLON:      [:];
DOT:        [.];

// Ignore characters
WHITESPACE: [ \t\b\f\r\n]+ -> skip;	// Skip white space
LINE_COMMENT: '//' (~[\r\f\n])* -> skip; // Skip line comment
BLOCK_COMMENT: '/' '*' .*? '*' '/' -> skip; // Skip block comment by non-greedy algorithm

// Error raising
ERROR_CHAR: .{
	raise ErrorToken(self.text)
};

UNCLOSE_STRING: '"' Character* ([\n\r\f] | EOF) {
	if(str(self.text)[-1] in ['\n', '\r', '\f']):
		raise UncloseString(str(self.text)[1:-1])
	else:
		raise UncloseString(str(self.text)[1:])
};

ILLEGAL_ESCAPE: '"' Character* Not_escape {
	raise IllegalEscape(str(self.text)[1:])
};

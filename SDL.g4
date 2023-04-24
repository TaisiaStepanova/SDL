grammar SDL;


program
 : block EOF
 ;

block
 : name_func* stat*
 ;

stat
 : assignment
 | control_structure
 | call_func
 ;
 
 name_func:
    'function' ID '(' (TYPE'*'ID (',' TYPE '*'ID)*)? ')' stat_block
    ;

    
call_func
    : ID '('(('&')? op_func (',' ('&')? op_func)*)? ')'
    ;
    
op_func
    : (ID|call_func|expr)
    ;
    
control_structure
    : if_stat
    | while_stat
    | until_stat
    | for_stat
    | switch_stat
    ;
    
assignment
 : ID '=' expr
 | TYPE ID ('=' expr)?
 ;
 
 for_stat
 : FOR assignment ',' comp_expr ',' assignment stat_block;
 
 switch_stat
 : SWITCH ID '{' (CASE  INTEGER stat_block )+ '}';

if_stat
 : IF comp_expr stat_block (ELIF comp_expr stat_block)*
 (ELSE stat_block)?
 ;

until_stat
 : REPEATE stat_block UNTIL comp_expr;


stat_block
 : '{' block '}'
 ;

while_stat
 : WHILE comp_expr stat_block
 ;
 
comp_expr
    : expr ('<=' | '>=' | '<' | '>') expr
    | expr ('==' | '!=') expr             
    | comp_expr AND comp_expr
    | comp_expr OR comp_expr
    ;

expr
 : expr '^' expr                        
 | '-' expr                             
 | expr ('*' | '/' | '%' | '//') expr
 | expr ('+' | '-') expr              
 | atom                                 
 ;

atom
 : '(' expr ')'   
 | INTEGER
 | FLOAT
 | BOOL              
 | ID             
 ;

OR : '||';
AND : '&&';
EQ : '==';
NEQ : '!=';
GT : '>';
LT : '<';
GTEQ : '>=';
LTEQ : '<=';
PLUS : '+';
MINUS : '-';
MULT : '*';
DIV : '/';
DOUBLEDIV : '//';
MOD : '%';
POW : '^';
NOT : '!';
AMPERSAND   : '&' ;
COMMA : ',';


ASSIGN : '=';
OPAR : '(';
CPAR : ')';
OBRACE : '{';
CBRACE : '}';

ELIF : 'elif';
IF : 'if';
ELSE : 'else';
WHILE : 'while';
REPEATE : 'repeate';
UNTIL : 'until';
FOR : 'for';
SWITCH   : 'switch' ;
CASE     : 'case' ;
FUNCTION : 'function' ;



TYPE            : 'int' | 'float' | 'bool';
INTEGER         : '-'? DIGIT+ ;
FLOAT           : '-'? DIGIT+ ([.,] DIGIT+) ;
BOOL            :	'True' | 'False' ;


ID              :  [a-zA-Z][a-zA-Z_]*;
DIGIT           : [0-9] ;

COMMENT
 : '///' ~[\r\n]* -> skip
 ;

SPACE
 : [ \t\r\n] -> skip
 ;

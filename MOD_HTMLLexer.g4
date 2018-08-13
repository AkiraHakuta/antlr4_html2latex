// antlr4py3 MOD_HTMLLexer.g4 -o mod_gen

lexer grammar MOD_HTMLLexer;

// Default "mode": Everything OUTSIDE of a tag
COMMENT     :   '<!--' .*? '-->' ;
CDATA       :   '<![CDATA[' .*? ']]>' ;

DTD         :   '<!' .*? '>'            -> skip ; // <!DOCTYPE html>, ... 

XML_DeclOpen :   '<?xml' S              -> pushMode(INSIDE) ; 

SCRIPT  : '<script' .*? '>' .*? '</script>' -> skip;
SCRIPT2 : '<SCRIPT' .*? '>' .*? '</SCRIPT>' -> skip;
STYLE   : '<style'  .*? '>' .*? '</style>'  -> skip;
STYLE2  : '<STYLE'  .*? '>' .*? '</STYLE>'  -> skip;
SCRIPTLET  : '<?' .*? '?>'                  -> skip;
SCRIPTLET2 : '<%' .*? '%>'                  -> skip;


SP_TEXT     : '&' Name ';' 
			| '&#' DIGIT+ ';'
			| '&#x' HEXDIGIT+ ';'
			| '&'
			| '$'
			| '%'
			| '_'
			;

SEA_WS      :   (' '|'\t'|'\r'? '\n')+ ;
OPEN         :   '<'                    -> pushMode(INSIDE) ;
TEXT        :   ~[<&$%_]+ ;         // match any 16 bit char other than <, &, $, _


// ---------------------- Everything INSIDE of a tag --------------------------
mode INSIDE;

CLOSE       :   '>'                     -> popMode ;
SPECIAL_CLOSE:  '?>'                    -> popMode ; // close <?xml...?>
SLASH_CLOSE :   '/>'                    -> popMode ;

SLASH       :   '/' ;
TAG_EQUALS :[ ]* '=' -> pushMode(ATTVALUE) ;

OPTName  : 'li'|'dt'|'dd'|'p'|'rt'|'rp'|'optgroup'|'option'|'colgroup'|'caption'|
            'thead'|'tbody'|'tfoot'|'tr'|'td'|'th'; 
			// optional tags (except  'html'|'head'|'body'|)

SName       :'area'|'br'|'base'|'basefont'|'bgsound'|'col'|'embed'|'frame'|'hr'|
			'img'|'input'|'isindex'|'keygen'|'link'|'menuitem'|'meta'|'META'|'nextid'|
			'param'|'plaintext'|'source'|'spacer'|'track'|'wbr'; // single tags 

Name        :   NameStartChar NameChar* ;
S           :   [ \t\r\n]               ; //  -> skip ;

fragment  HEXDIGIT : [a-fA-F0-9] ;

fragment  DIGIT    : [0-9] ;

fragment  NameChar :   NameStartChar
					|'-' |'_' |'.' |DIGIT 
					|'\u00B7'| '\u0300'..'\u036F'|'\u203F'..'\u2040';

fragment  NameStartChar:  [:a-zA-Z]
					|'\u2070'..'\u218F'|'\u2C00'..'\u2FEF'|'\u3001'..'\uD7FF' 
					|'\uF900'..'\uFDCF'|'\uFDF0'..'\uFFFD';


// --------------------  Name = ATTVALUE_VALUE ------------------------
mode ATTVALUE;

ATTVALUE_VALUE : [ ]* ATTRIBUTE -> popMode ;

ATTRIBUTE : DOUBLE_QUOTE_STRING| SINGLE_QUOTE_STRING| HEXCHARS| HEXCHARS2| DECCHARS| ATTCHARS ;

fragment HEXCHARS:  '#' [0-9a-fA-F]+ ;
fragment HEXCHARS2: '&#'[0-9a-fA-F]+ ;

fragment DECCHARS: [0-9]+ '%'? ;

fragment ATTCHAR : '-'| '_'| '.'| '/'| '+'| ','| '?'| '='| ':'| ';'| '#'| '&'| '%'| [0-9a-zA-Z];

fragment ATTCHARS: ATTCHAR+ ;

fragment DOUBLE_QUOTE_STRING : '"' ~[<"]* '"' ;

fragment SINGLE_QUOTE_STRING : '\'' ~[<']* '\'';

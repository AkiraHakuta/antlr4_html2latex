// antlr4py3 HTMLLexer.g4 -o gen

lexer grammar HTMLLexer;

// Default "mode": Everything OUTSIDE of a tag
COMMENT     :   '<!--' .*? '-->' ;
CDATA       :   '<![CDATA[' .*? ']]>' ;
DTD         :   '<!' .*? '>'               -> skip ; // <!DOCTYPE html>, ... 

XML_DeclOpen :  '<?xml' S                  -> pushMode(INSIDE) ; 

SCRIPTLET   : '<?' .*? '?>' | '<%' .*? '%>' ;

SP_TEXT     : '&' Name ';' 
			| '&#' DIGIT+ ';'
			| '&#x' HEXDIGIT+ ';'
			| '&'
			| '$'
			;

SEA_WS      :   (' '|'\t'|'\r'? '\n')+ ;

SCRIPT_OPEN  : '<script' .*? '>'    ->pushMode(SCRIPT) ;
STYLE_OPEN   : '<style' .*? '>'     ->pushMode(STYLE)  ;
OPEN         :   '<'                -> pushMode(INSIDE);

TEXT        :   ~[<&$]+ ;        // match any 16 bit char other than < and & and $ 


// ---------------------- Everything INSIDE of a tag --------------------------
mode INSIDE;

CLOSE       :   '>'                     -> popMode ;
SPECIAL_CLOSE:  '?>'                    -> popMode ; // close <?xml...?>
SLASH_CLOSE :   '/>'                    -> popMode ;

SLASH       :   '/' ;
TAG_EQUALS : '=' -> pushMode(ATTVALUE) ;

SName       :'area'|'br'|'base'|'basefont'|'bgsound'|'col'|'embed'|'frame'|'hr'|
			'img'|'input'|'isindex'|'keygen'|'link'|'menuitem'|'meta'|'META'|'nextid'|
			'param'|'plaintext'|'source'|'spacer'|'track'|'wbr'; // single tags

Name        :   NameStartChar NameChar* ;
S           :   [ \t\r\n]                 -> skip ;

fragment
HEXDIGIT    :   [a-fA-F0-9] ;

fragment
DIGIT       :   [0-9] ;

fragment
NameChar    :   NameStartChar
            |   '-' | '_' | '.' | DIGIT 
            |   '\u00B7'|   '\u0300'..'\u036F'| '\u203F'..'\u2040';

fragment
NameStartChar:  [:a-zA-Z]
            |   '\u2070'..'\u218F' 
            |   '\u2C00'..'\u2FEF' 
            |   '\u3001'..'\uD7FF' 
            |   '\uF900'..'\uFDCF' 
            |   '\uFDF0'..'\uFFFD';


// -------------------- <script ...> ... </script>--------------------
mode SCRIPT;

SCRIPT_BODY  : .*? '</script>' -> popMode  ;
SCRIPT_SHORT_BODY  : .*? '</>' -> popMode  ;


// --------------------- <style ...> ... </style>----------------------
mode STYLE;

STYLE_BODY  : .*? '</style>' -> popMode  ;
STYLE_SHORT_BODY : .*? '</>' -> popMode  ;


// --------------------  Name = ATTVALUE_VALUE ------------------------
mode ATTVALUE;

ATTVALUE_VALUE : [ ]* ATTRIBUTE -> popMode ;

ATTRIBUTE : DOUBLE_QUOTE_STRING| SINGLE_QUOTE_STRING| HEXCHARS| HEXCHARS2| DECCHARS | ATTCHARS;

fragment HEXCHARS:  '#' [0-9a-fA-F]+ ;
fragment HEXCHARS2: '&#'[0-9a-fA-F]+ ;

fragment DECCHARS: [0-9]+ '%'? ;

fragment ATTCHAR : '-'| '_'| '.'| '/'| '+'| ','| '?'| '='| ':'| ';'| '#'| '&'| '%'| [0-9a-zA-Z];

fragment ATTCHARS: ATTCHAR+ ;

fragment DOUBLE_QUOTE_STRING : '"' ~[<"]* '"'  ;

fragment SINGLE_QUOTE_STRING : '\'' ~[<']* '\'';

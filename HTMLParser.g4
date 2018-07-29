// antlr4py3 HTMLParser.g4 -o gen -no-listener -visitor

parser grammar HTMLParser;
options { tokenVocab = HTMLLexer; }

document : misc* xml? (misc* element)* misc*;

xml      : xml_decl_open attribute* SPECIAL_CLOSE ;

content      : content_body* ;
content_body : element | CDATA | COMMENT | chardata ;

element     : '<' o_tag=Name attribute* Name? '>' content '<' '/' c_tag=Name '>'  # paired_tag
            | '<' SName attribute* Name? ('/>'| '>')                              # single_tag
			| '<' Name attribute* '/>'                                            # single_slash_tag
			| script                                                              # script_tag
			| style                                                               # style_tag
            ;

attribute   : Name+  TAG_EQUALS  ATTVALUE_VALUE ;

chardata    : TEXT | SP_TEXT | SEA_WS ;

misc        : COMMENT | SEA_WS | scriptlet;

scriptlet : SCRIPTLET ;
script: SCRIPT_OPEN ( SCRIPT_BODY | SCRIPT_SHORT_BODY );
style : STYLE_OPEN ( STYLE_BODY | STYLE_SHORT_BODY)   ;

xml_decl_open : XML_DeclOpen ;

// antlr4py3 MOD_HTMLParser.g4 -o mod_gen

parser grammar MOD_HTMLParser;
options { tokenVocab = MOD_HTMLLexer; }

document :  (misc | xml |element | CDATA | COMMENT |chardata)*;

xml      :   xml_decl_open attribute* SPECIAL_CLOSE ;

element     :   '<' OPTName (S+ attribute)* (S+ Name)? S* '>'        # opt_opening_tag
			|   '<' '/' OPTName  '>'                                 # opt_closing_tag
			|   '<' Name (S+ attribute)* (S+ Name)? S* '>'           # opening_tag
			|   '<' '/' Name '>'                                     # closing_tag
            |   '<' SName (S+ attribute)* (S+ Name)? S* ('/>'| '>')  # single_tag
			|   '<' Name (S+ attribute)* S* '/>'                     # single_slash_tag
            ;

attribute   :   (Name S*)+  TAG_EQUALS  ATTVALUE_VALUE ;

chardata    :   TEXT | SP_TEXT | SEA_WS ;

misc        :   COMMENT | SEA_WS ;

scriptlet : SCRIPTLET ;

xml_decl_open : XML_DeclOpen ;
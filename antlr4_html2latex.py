# python.exe antlr4_html2latex.py sample1.html
# python.exe antlr4_html2latex.py sample2.html -m MOD

from antlr4 import *

from gen.HTMLLexer import HTMLLexer
from gen.HTMLParser import HTMLParser
from gen.HTMLParserVisitor import HTMLParserVisitor

from mod_gen.MOD_HTMLLexer import MOD_HTMLLexer
from mod_gen.MOD_HTMLParser import MOD_HTMLParser
from mod_gen.MOD_HTMLParserListener import MOD_HTMLParserListener

from MyTokenStreamRewriter import MyTokenStreamRewriter
from Interval import Interval
DEFAULT_PROGRAM_NAME = MyTokenStreamRewriter.DEFAULT_PROGRAM_NAME

import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os, re, csv, argparse, copy


# from https://github.com/antlr/antlr4/blob/master/runtime/Python3/bin/pygrun
# this is a python version of TestRig
def beautify_lisp_string(in_string):
    indent_size = 3
    add_indent = ' '*indent_size
    out_string = in_string[0]  # no indent for 1st (
    indent = ''
    for i in range(1, len(in_string)):
        if in_string[i] == '(' and in_string[i+1] != ' ':
            indent += add_indent
            out_string += "\n" + indent + '('
        elif in_string[i] == ')':
            out_string += ')'
            if len(indent) > 0:
                indent = indent.replace(add_indent, '', 1)
        else:
            out_string += in_string[i]
    return out_string    

 
 
# convert HTML into LaTeX
    
    
class GetTableSize(HTMLParserVisitor):
    def __init__(self):
        super().__init__()
        self.data = {} 
        

    def visitDocument(self, ctx):
        result = ''
        for el in ctx.element():
            visit_el = self.visit(el)
            if visit_el != None:
                result += visit_el
        return result
        
    
    def visitContent_body(self, ctx):
        result = ''
        if ctx.element() != None:
            visit_element = self.visit(ctx.element())
            if visit_element != None:
                result += visit_element
        elif ctx.chardata() != None:
            if ctx.chardata().TEXT() != None:
                result += ctx.chardata().TEXT().getText()
        return result
        
        
    def visitContent(self, ctx):
        result = ''
        for cb in ctx.content_body():
            result += self.visit(cb)            
        return result     
        
        
    def visitPaired_tag(self, ctx):
        tag_name = ctx.Name(0).getText()
        if tag_name == 'table':            
            table_str = self.visit(ctx.content())
            #print(table_str)
            table_list = table_str.split('r')
            col_len = len(table_list[1])
            row_len = len(table_list) - 1
            self.data[ctx] = {'col_size':col_len, 'row_size':row_len, 
                        'table':[[0 for i in range(col_len)] for i in range(row_len)],
                        'colspan':[[0 for i in range(col_len)] for i in range(row_len)]}
        elif tag_name == 'td' or tag_name == 'th':
            i = 0
            colspan_num = 1
            while True:                
                attr=ctx.attribute(i)
                if attr != None:
                    if attr.Name(0).getText() == 'colspan':
                        colspan=attr.ATTVALUE_VALUE().getText()                        
                        colspan_num = getInt(colspan)
                    i += 1
                else:
                    break
            self.visit(ctx.content())
            return 'd' * colspan_num
        elif tag_name == 'tr':            
            result = 'r'+self.visit(ctx.content())
            return result
        elif tag_name == 'caption':
            return ''
        else:
            return self.visit(ctx.content())
            
            
    
class GetTableData(HTMLParserVisitor):
    def __init__(self, data, tag_dict):
        super().__init__()
        self.data = data
        self.data_stack = []
        self.pair_tag_dict = tag_dict['pair_tag_dict']
        self.sp_text_dict = tag_dict['sp_text_dict']
        self.data1 = None
        self.col=None
        self.row=None
        self.col_size = None        
        
    def visitDocument(self, ctx):
        result = ''
        for el in ctx.element():
            visit_el = self.visit(el)
            if visit_el != None:
                result += visit_el
        return result

     
    def visitContent_body(self, ctx):
        result = ''
        if ctx.element() != None:
            visit_element = self.visit(ctx.element())
            if visit_element != None:
                result += visit_element
        if ctx.chardata() != None:
            result += self.visit(ctx.chardata())
        return result
        
        
    def visitContent(self, ctx):
        result = ''
        for cb in ctx.content_body():
            result += self.visit(cb)            
        return result
        
        
    def visitPaired_tag(self, ctx): 
        tag_name = ctx.Name(0).getText()
        if  tag_name == 'table':
            self.data_stack.append(self.data1)
            self.data_stack.append(self.col)
            self.data_stack.append(self.row)
            self.data_stack.append(self.col_size)
            self.data1 = self.data[ctx]            
            self.col = 0
            self.row = 0
            self.col_size = self.data1['col_size']
            self.visit(ctx.content())
            self.data[ctx] = self.data1
            self.col_size = self.data_stack.pop()
            self.row = self.data_stack.pop()
            self.col = self.data_stack.pop()
            self.data1 = self.data_stack.pop()            
        elif tag_name == 'td' or tag_name == 'th':
            i = 0
            colspan_num = 1
            while True:                
                attr=ctx.attribute(i)
                if attr != None:
                    if attr.Name(0).getText() == 'colspan':
                        colspan=attr.ATTVALUE_VALUE().getText()
                        colspan_num = getInt(colspan)
                        self.data1['colspan'][self.row][self.col] = colspan_num
                    elif attr.Name(0).getText() == 'rowspan':
                        rowspan=attr.ATTVALUE_VALUE().getText()
                        self.rowspan_num = getInt(rowspan)
                        for y in range(self.row+1,self.row+self.rowspan_num):
                            for x in range(self.col,self.col+colspan_num):
                                self.data1['table'][y][x] = 1
                    i += 1
                else:
                    break
            self.col += colspan_num
            while self.col < self.col_size:
                if self.data1['table'][self.row][self.col] == 1:
                    self.col += 1
                else:
                    break
            result = 'd' + self.visit(ctx.content())
            return result
        elif tag_name == 'tr':            
            result = 'r'+self.visit(ctx.content())
            self.row += 1
            self.col = 0
            return result
        elif tag_name == 'caption':
            self.data1['caption'] = self.visit(ctx.content())
        else:
            return self.visit(ctx.content())
            
            
    def visitChardata(self, ctx):
        result = ''        
        if ctx.TEXT() != None:
            result += ctx.getText()
        elif ctx.SEA_WS() != None:
            result += ctx.getText()
        else:
            for st in self.sp_text_dict.keys():
                if ctx.SP_TEXT() != None and ctx.SP_TEXT().getText() == st:
                    result += self.sp_text_dict[st]
                    break
        return result   

        
def getInt(str1):
    str2 = str1.replace('\'', '').replace('"','')
    return int(str2)  
    
        

document_begin = '%\\documentclass[pdflatex,a4paper,10pt]{article}\n'+ \
                '%\\documentclass[a4paper,fleqn,10pt]{jsarticle}\n' + \
                '\\documentclass[pdflatex, a4paper, 10pt, jadriver=standard]{bxjsarticle}\n' + \
                '\\setlength{\\oddsidemargin}{-10mm}\n' + \
                '\\setlength{\\topmargin}{-19mm}\n' + \
                '\\setlength{\\textheight}{250mm}\n' + \
                '\\usepackage{graphicx}\n' + \
                '\\usepackage{hyperref}\n' + \
                '\\pagestyle{empty}\n'
document_end = '\n\\end{document}'
    
TABLE_FIT_SCALE = 0.85        
        
class LaTeXCode(HTMLParserVisitor):
    def __init__(self, table_data, tag_dict, args):
        super().__init__()
        self.title = ''
        self.table_data = table_data
        if args.t == 'TBL':
            self.table_sw = True
        else:
            self.table_sw = False
        self.a = args.a
        self.img = args.i    
        self.pair_tag_dict = tag_dict['pair_tag_dict']
        self.sp_text_dict = tag_dict['sp_text_dict']
        self.table_data_stack = []        
        self.col_size = None
        self.row_size = None
        self.table = None
        self.colspan = None
        self.col = None
        self.row = None
        self.cell_width_scale = 1.000 
    
                
    def visitDocument(self, ctx):
        result = document_begin+self.title+'\n\\begin{document}\n'
        for el in ctx.element():
            visit_el = self.visit(el)
            if visit_el != None:
                result += visit_el                
        result += document_end
        return result    
    
        
    def visitPaired_tag(self, ctx):
        #print(ctx.o_tag.text,ctx.c_tag.text)
        #if ctx.o_tag == None or ctx.c_tag == None:
        #    print('tag error:',ctx.o_tag,ctx.c_tag,ctx.start.line,ctx.start.column+1)
        tag_name = ctx.Name(0).getText()
        for key_name in self.pair_tag_dict.keys():
            if tag_name == key_name:
                return self.pair_tag_dict[tag_name][0]+self.visit(ctx.content())+self.pair_tag_dict[tag_name][1]
        if tag_name == 'html' or tag_name == 'head':
            return self.visit(ctx.content())
        elif tag_name == 'body':
            return self.visit(ctx.content())
        elif tag_name == 'title':
            result = ''
            result += '{\\Large Title: ' + self.visit(ctx.content()) + '}\\newline\\newline\n'
            return result
        elif tag_name == 'a':
            i = 0
            href = ''
            title = ''
            while True:
                attr=ctx.attribute(i)
                if attr != None:
                    if attr.Name(0).getText() == 'href':
                        href=attr.ATTVALUE_VALUE().getText()
                    elif attr.Name(0).getText() == 'title':
                        title=attr.ATTVALUE_VALUE().getText()
                    i += 1
                else:
                    break
            if self.a == 'A':
                result = '\\href{' + href[1:-1:].replace('%','\%').replace('&','\&') + '}{' + self.visit(ctx.content()) +'}\n'
            else:
                result = 'anchor: ' + self.visit(ctx.content()) + '\n'
            return result
        elif self.table_sw and tag_name == 'table': 
            self.table_data_stack.append(self.col_size)
            self.table_data_stack.append(self.row_size)
            self.table_data_stack.append(self.table)
            self.table_data_stack.append(self.colspan)
            self.table_data_stack.append(self.col)
            self.table_data_stack.append(self.row)
            self.table_data_stack.append(self.cell_width_scale)
            
            self.curr_table_data = self.table_data[ctx]
            self.col_size = self.curr_table_data['col_size']
            self.row_size = self.curr_table_data['row_size']
            self.table = self.curr_table_data['table']
            self.colspan = self.curr_table_data['colspan']
            self.col = 0
            self.row = 0
            tabular_col_head = '{'
            self.cell_width_scale = round(self.cell_width_scale/self.col_size,3)
            for i in range(self.col_size):
                tabular_col_head += '|p{'+str(self.cell_width_scale)+'\\textwidth}'
            tabular_col_head += '|}\\hline \n' 
            tabular_code = '%table code\n'
            if 'caption' in self.curr_table_data:
                tabular_code += self.curr_table_data['caption'] + '\\newline \n'              
            tabular_code += '\\begin{tabular}' + tabular_col_head \
                + self.visit(ctx.content())\
                + '\\end{tabular}\n'                
            self.cell_width_scale=self.table_data_stack.pop()
            self.row=self.table_data_stack.pop()
            self.col=self.table_data_stack.pop()                
            self.colspan=self.table_data_stack.pop()
            self.table=self.table_data_stack.pop()
            self.row_size=self.table_data_stack.pop()
            self.col_size=self.table_data_stack.pop()
            return tabular_code
        elif self.table_sw and ( tag_name == 'td' or tag_name == 'th' ):
            colspan = self.colspan[self.row][self.col]
            self.table_data_stack.append(self.cell_width_scale)
            if colspan == 0:
                self.cell_width_scale = round(self.cell_width_scale*TABLE_FIT_SCALE,3)
                tabular_code = self.visit(ctx.content())
                self.col += 1
            else:
                self.cell_width_scale = round(self.cell_width_scale*colspan*TABLE_FIT_SCALE,3)
                tabular_code = '\\multicolumn{'+ str(colspan) + '}{'+'|p{'+str(self.cell_width_scale)+'\\textwidth}|}{' \
                                + self.visit(ctx.content()) +'}'
                self.col += colspan            
            while (self.col < self.col_size):
                if self.table[self.row][self.col] == 1:
                    tabular_code += '&'
                    self.col += 1
                else:
                    break
            if self.col < self.col_size:
                tabular_code += '&'
            self.cell_width_scale=self.table_data_stack.pop()
            return tabular_code    
        elif self.table_sw and tag_name == 'tr':            
            tabular_code = ''
            while (self.col < self.col_size):
                if self.table[self.row][self.col] == 1:
                    tabular_code += '&'
                    self.col += 1
                else:
                    break
            tabular_code += self.visit(ctx.content()) + '\\\\\\hline '
            self.col = 0
            self.row += 1
            return tabular_code 
        elif tag_name == 'caption':
            return ''
        else:
            return self.visit(ctx.content())
            
            
    def visitContent_body(self, ctx):
        result = ''
        if ctx.element() != None:
            visit_element = self.visit(ctx.element())
            if visit_element != None:
                result += visit_element
        elif ctx.chardata() != None:
            result += self.visit(ctx.chardata())
        return result
        
        
    def visitContent(self, ctx):
        result = ''
        for cb in ctx.content_body():
            result += self.visit(cb)            
        return result
        
        
    def visitSingle_tag(self, ctx):
        tag_name = ctx.SName().getText()
        if tag_name == 'img':
            i = 0
            src = ''
            data_src = ''
            alt = ''
            while True:
                attr=ctx.attribute(i)
                if attr != None:
                    if attr.Name(0).getText() == 'src':
                        src=attr.ATTVALUE_VALUE().getText()
                    elif attr.Name(0).getText() == 'data-src':
                        data_src=attr.ATTVALUE_VALUE().getText()
                    elif attr.Name(0).getText() == 'alt':
                        alt=attr.ATTVALUE_VALUE().getText()
                    i += 1
                else:
                    break
            if src == '':
                src = data_src
            if self.img == 'IMG':
                result = '%img alt: ' + alt[1:-1:] + '\n\\includegraphics{'+ src[1:-1:].replace('%','\%').replace('&','\&') + '}\n'
            else:
                result = '%img alt: ' + alt[1:-1:] + '\n'
            return result
        elif tag_name == 'br':
            return '\\newline\n'
        else:
            return ''
            
            
    def visitSingle_slash_tag(self, ctx):
        if ctx.Name().getText() == 'p':
            return '\\par\n'        
        else:
            return ''
            
            
    def visitChardata(self, ctx):
        result = ''        
        if ctx.TEXT() != None:
            result += ctx.getText()
        elif ctx.SEA_WS() != None:
            result += ctx.getText()
        else:
            for st in self.sp_text_dict.keys():
                if ctx.SP_TEXT() != None and ctx.SP_TEXT().getText() == st:
                    result += self.sp_text_dict[st]
                    break
        return result     
            
                
 
def sq_str(str1):
    start = 0
    for i in range(len(str1)):
        if str1[i] == '[':
            start=i+1
            break
    end = 0
    for i in range(len(str1)):
        if str1[-i] == ']':
            end=i
            break
    end = len(str1) - end
    str2 = str1[start:end:]
    result = ''
    pos = 0
    max = len(str2)
    while pos < max:
        if (pos + 1 < max) and str2[pos:(pos+2):] == '\\\\':
            result += '\\'
            pos += 2
        elif (pos + 1 < max) and str2[pos:(pos+2):] == '\\n':
            result += '\n'
            pos += 2
        else:
            result += str2[pos]
            pos += 1    
    return result
 
    
def get_tag_dict():    
    pair_tag_dict ={}
    single_tag_dict = {}
    sp_text_dict ={}
    tagfile = 'html2latex.csv'
    f = open(tagfile, "r")
    tag_reader = csv.reader(f)
    for row in tag_reader:
        if row != []:
            if sq_str(row[0]) == 'pair_tag':
                pair_tag_dict[sq_str(row[1])] = [sq_str(row[2]),sq_str(row[3])]
            elif sq_str(row[0]) == 'single_tag':
                single_tag_dict[sq_str(row[1])] = sq_str(row[2])    
            elif sq_str(row[0]) == 'sp_text':
                sp_text_dict[sq_str(row[1])] = sq_str(row[2])
    f.close()
    return {'pair_tag_dict': pair_tag_dict, 'single_tag_dict': single_tag_dict, 'sp_text_dict': sp_text_dict}   



# modify HTML file (optional tags except p tag)
IN = 1
OUT = 0
EX_CL_TAG = 1
NO_CL_TAG = 0
class GetModData(MOD_HTMLParserListener):
    def __init__(self):
        super().__init__()
        self.insert_before = {}
        self.delete_list =[]
        self.opt_stack = []
        self.opt = {'oul':None, 'thd':None, 'thd_cl_tag':None, 'tr':None, 'dl':None, 'ruby':None, 'caption':None}
        self.pair_tag_name = {}
        
    
    def set_tag_data(self, sw, name):
        if name in self.pair_tag_name:
            if sw == 0:
                self.pair_tag_name[name][0] += 1
            else:
                self.pair_tag_name[name][1] += 1
        else:
            if sw == 0:
                self.pair_tag_name[name] = [1,0]
            else:
                self.pair_tag_name[name] = [0,1]
        if self.pair_tag_name[name][0] < self.pair_tag_name[name][1]:
            return -1
        else:
            return 1            
            
    
    def init_opt(self):
        for key in self.opt.keys():
            self.opt[key] = None
            
        
    def enterOpening_tag(self, ctx):        
        tag_name = ctx.Name(0).getText()
        self.set_tag_data(0, tag_name)
        #print('op=',self.insert_before)
        #print('op opt=',self.opt)
        self.opt_stack.append(copy.copy(self.opt))
        self.init_opt()
            
            
    def enterClosing_tag(self, ctx):
        tag_name = ctx.Name().getText()
        if self.set_tag_data(1, tag_name) == -1:
            self.delete_list.append(ctx)
            print('\npaired tag error. delete: line = {:d}, column = {:d}, </{:s}>'.format(ctx.start.line,ctx.start.column+1,tag_name))
            self.pair_tag_name[tag_name][1] += -1             
            return
        if tag_name == 'ol':
            if self.opt['oul'] == NO_CL_TAG:                
                self.insert_before[ctx] = '</li>\n'
        elif tag_name == 'ul':
            if self.opt['oul'] == NO_CL_TAG:                
                self.insert_before[ctx] = '</li>\n'
        elif tag_name == 'dl':
            if self.opt['dl'] != None:
                self.insert_before[ctx] = '</' + self.opt['dl'] + '>\n'
        elif tag_name == 'ruby':
            if self.opt['ruby'] != None:
                self.insert_before[ctx] = '</' + self.opt['ruby'] + '>\n'
            self.opt['ruby'] = None
        elif tag_name == 'table':            
            if self.opt['thd'] != None and self.opt['thd_cl_tag'] == NO_CL_TAG:
                self.set_insert_before(ctx, '</' + self.opt['thd'] + '>\n')
            if self.opt['tr'] == NO_CL_TAG:
                self.set_insert_before(ctx, '</tr>\n')                
        try:
            self.opt = self.opt_stack.pop()
        except:
            print('tag error! line = {:d}, column = {:d}, </{:s}>'.format(ctx.start.line,ctx.start.column+1,tag_name))
            pass     
        
            
    def enterOpt_opening_tag(self, ctx):
        opt_name = ctx.OPTName().getText() 
        #print('opop=',self.insert_before)
        #print('opop opt=',self.opt)     
        if  opt_name == 'li':
            if self.opt['oul'] == NO_CL_TAG:
                self.insert_before[ctx] = '</li>\n'                     
            self.opt['oul'] = NO_CL_TAG                     
        elif  opt_name == 'dd' or opt_name == 'dt':
            if self.opt['dl'] != None:
                self.insert_before[ctx] = '</' + self.opt['dl'] + '>\n'
            self.opt['dl'] = opt_name
        elif  opt_name == 'rp' or opt_name == 'rt':
   
            if self.opt['ruby'] != None:
                self.insert_before[ctx] = '</' + self.opt['ruby'] + '>\n'
            self.opt['ruby'] = opt_name
        elif  opt_name == 'th' or opt_name == 'td':            
            if self.opt['thd_cl_tag'] == NO_CL_TAG:
                self.insert_before[ctx] = '</' + self.opt['thd'] + '>\n'
            self.opt['thd'] = opt_name
            self.opt['thd_cl_tag'] = NO_CL_TAG            
        elif  opt_name == 'tr':
            if self.opt['caption'] == NO_CL_TAG:
                self.set_insert_before(ctx, '</caption>\n')
                self.opt['caption'] = EX_CL_TAG
            if self.opt['thd_cl_tag'] == NO_CL_TAG:
                self.set_insert_before(ctx, '</' + self.opt['thd'] + '>\n')
            if self.opt['tr'] == NO_CL_TAG:
                self.set_insert_before(ctx, '</tr>\n')
            self.opt['tr'] = NO_CL_TAG
            self.opt['thd_cl_tag'] = None            
        elif  opt_name == 'caption':
            self.opt['caption'] = NO_CL_TAG                
        elif opt_name == 'colgroup':
            self.delete_list.append(ctx)
        elif opt_name == 'optgroup':
            self.delete_list.append(ctx)
        elif opt_name == 'option':
            self.delete_list.append(ctx)
        elif opt_name == 'thead':
            self.delete_list.append(ctx) 
        elif opt_name == 'tbody':
            self.delete_list.append(ctx) 
        elif opt_name == 'tfoot':
            self.delete_list.append(ctx)             
            
                            
    def enterOpt_closing_tag(self, ctx):
        opt_name = ctx.OPTName().getText()
        #print('opt_cl_name',opt_name,ctx.start.line,ctx.stop.column+1)
        #print('opcl=',self.insert_before)
        #print('opcl opt=',self.opt)        
        if opt_name == 'li' :
            self.opt['oul'] = EX_CL_TAG
        elif  opt_name == 'dd' or opt_name == 'dt':
            self.opt['dl'] = None
        elif  opt_name == 'rp' or opt_name == 'rt':
            self.opt['ruby'] = None
        elif  opt_name == 'th' or opt_name == 'td':
            self.opt['thd'] = None
            self.opt['thd_cl_tag'] = EX_CL_TAG
        elif  opt_name == 'tr':
            if self.opt['thd_cl_tag'] == NO_CL_TAG:
                self.set_insert_before(ctx, '</' + self.opt['thd'] + '>\n')
            self.opt['tr'] = EX_CL_TAG
            self.opt['thd_cl_tag'] = None
        elif  opt_name == 'caption':
            self.opt['caption'] = EX_CL_TAG
        elif opt_name == 'colgroup':
            self.delete_list.append(ctx)
        elif opt_name == 'optgroup':
            self.delete_list.append(ctx)
        elif opt_name == 'option':
            self.delete_list.append(ctx) 
        elif opt_name == 'thead':
            self.delete_list.append(ctx) 
        elif opt_name == 'tbody':
            self.delete_list.append(ctx) 
        elif opt_name == 'tfoot':
            self.delete_list.append(ctx)      
               
        
    def set_insert_before(self, ctx, tag):
        if ctx in self.insert_before:
            self.insert_before[ctx] += tag
        else:
            self.insert_before[ctx] = tag
 
 

 # modify HTML file (p tag)
 
class GetModPData(MOD_HTMLParserListener):
    def __init__(self):
        super().__init__()
        self.insert_before = {}
        self.p_cl_tag = None
        self.p_cl_tag_added = None
        
     
    def enterOpt_opening_tag(self, ctx):
        opt_name = ctx.OPTName().getText()
        if self.p_cl_tag == NO_CL_TAG:
            self.insert_before[ctx] = '</p>\n'
            self.p_cl_tag_added = ctx
            self.p_cl_tag = EX_CL_TAG
        if opt_name == 'p':            
            self.p_cl_tag = NO_CL_TAG
            self.p_cl_tag_added = None
            
            
    def enterOpt_closing_tag(self, ctx):
        opt_name = ctx.OPTName().getText()
        if opt_name == 'p':
            if self.p_cl_tag_added != None:
                self.insert_before.pop(self.p_cl_tag_added)
                self.p_cl_tag_added = None
            self.p_cl_tag = EX_CL_TAG
            
    
    def enterOpening_tag(self, ctx):        
        tag_name = ctx.Name(0).getText()
        if self.p_cl_tag == NO_CL_TAG:
            self.insert_before[ctx] = '</p>\n'
            self.p_cl_tag_added = ctx
            self.p_cl_tag = None
            
    
    def enterClosing_tag(self, ctx):
        tag_name = ctx.Name().getText()        
        if self.p_cl_tag == NO_CL_TAG:
            self.insert_before[ctx] = '</p>\n'
            self.p_cl_tag = None


            
class GetModDeleteData(MOD_HTMLParserListener):
    def __init__(self,delete_paired_tag_list):
        super().__init__()
        self.delete_list =[]
        self.delete_paired_tag_list = delete_paired_tag_list
        
    def enterOpening_tag(self, ctx):        
        tag_name = ctx.Name(0).getText()
        for p_tag_name in self.delete_paired_tag_list:
            if tag_name == p_tag_name:
                self.delete_list.append(ctx)
            
            
    
    def enterClosing_tag(self, ctx):
        tag_name = ctx.Name().getText()        
        for p_tag_name in self.delete_paired_tag_list:
            if tag_name == p_tag_name:
                self.delete_list.append(ctx)
                 
            
def paired_tag_error(paired_tag_dict):
    result = {}
    for key, value in paired_tag_dict.items(): 
        if value[0] > value[1]:
            result[key] = value
    return result    

    
    
def mod_main(input_stream):
    lexer = MOD_HTMLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    #token_stream.fill()
    #print('tokens:')
    #for tk in token_stream.tokens:
    #    print(tk)
    parser = MOD_HTMLParser(token_stream)
    tree = parser.document()
    #lisp_tree_str = tree.toStringTree(recog=parser)
    #print(beautify_lisp_string(lisp_tree_str))
    
    walker = ParseTreeWalker()
    mod_data = GetModData()
    walker.walk(mod_data, tree)
    paired_tag_error_dict = paired_tag_error(mod_data.pair_tag_name)
    if paired_tag_error_dict != {}:
        print('\npaired tag error {\'name\':[number of opening tags, number of closing tags],...}\n',paired_tag_error_dict)
    rewriter = MyTokenStreamRewriter(token_stream)
    for ctx in mod_data.delete_list:
        rewriter.delete(DEFAULT_PROGRAM_NAME,ctx.start.tokenIndex, ctx.stop.tokenIndex) 
    
    if mod_data.insert_before == {}:
        print('\ninsert tags: None')
    else:
        print('\ninsert tags:')
        for key, value in mod_data.insert_before.items():
            print('line = {:d}, column = {:d}, {:s}'.format(key.start.line,key.start.column+1,value.replace('\n','')))
    for key, value in mod_data.insert_before.items():
        #print('value=',value)
        rewriter.insertBeforeIndex(key.start.tokenIndex, value) 
    interval = Interval(rewriter.tokens.tokens)
    result =rewriter.getText(DEFAULT_PROGRAM_NAME,interval).replace('\r\n','\n')
    return [result,list(paired_tag_error_dict.keys())]  
 
    
            
def mod_p_main(input_stream):
    lexer = MOD_HTMLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = MOD_HTMLParser(token_stream)
    tree = parser.document()
    walker = ParseTreeWalker()
    mod_p_data = GetModPData()
    walker.walk(mod_p_data, tree)    
    rewriter = MyTokenStreamRewriter(token_stream)     
    if mod_p_data.insert_before == {}:
        print('\ninsert p tag: None')
    else:
        print('\ninsert p tag:')
        for key, value in mod_p_data.insert_before.items():
            print('line = {:d}, column = {:d}, {:s}'.format(key.start.line,key.start.column+1,value.replace('\n','')))
    for key, value in mod_p_data.insert_before.items():
        rewriter.insertBeforeIndex(key.start.tokenIndex, value) 
    interval = Interval(rewriter.tokens.tokens)
    result =rewriter.getText(DEFAULT_PROGRAM_NAME,interval).replace('\r\n','\n')
    return result   



def mod_delete_main(input_stream, delete_paired_tag_list):
    lexer = MOD_HTMLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = MOD_HTMLParser(token_stream)
    tree = parser.document()
    walker = ParseTreeWalker()
    mod_delete_data = GetModDeleteData(delete_paired_tag_list)
    walker.walk(mod_delete_data, tree)    
    rewriter = MyTokenStreamRewriter(token_stream)     
    for ctx in mod_delete_data.delete_list:
        rewriter.delete(DEFAULT_PROGRAM_NAME,ctx.start.tokenIndex, ctx.stop.tokenIndex) 
    interval = Interval(rewriter.tokens.tokens)
    result =rewriter.getText(DEFAULT_PROGRAM_NAME,interval).replace('\r\n','\n')
    return result   
    
    
    
def main(filename, args, file_list):  
    path = file_list[0]
    sf_ext = file_list[1]
    file_name = path + sf_ext
    try:
        input_stream = FileStream(file_name, encoding= args.e, errors = 'ignore')
    except OSError:
        print('cannot open', file_name)
        sys.exit()
    if args.m == 'MOD':
        print('\nmodifying html file (insert \'optional tags\' except p tag) ....') 
        result = mod_main(input_stream) 
               
        #print('mod_main:\n', result[0])
        input_stream = InputStream(result[0].replace('\r\n','\n'))
        delete_paired_tag_list = result[1]
        
        print('\nmodifying html file (insert  p tag) ....') 
        result = mod_p_main(input_stream)        
        #print('mod_p_main:\n', result)
        input_stream = InputStream(result.replace('\r\n','\n'))
        if delete_paired_tag_list != []:
            print('\ndelete paired tags: ', delete_paired_tag_list)
        result = mod_delete_main(input_stream, delete_paired_tag_list)        
        #print('mod_delete_main:\n', result)
        input_stream = InputStream(result.replace('\r\n','\n'))
        
    lexer = HTMLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    token_stream.fill()
    #print('tokens:')
    #for tk in token_stream.tokens:
    #    print(tk)
    parser = HTMLParser(token_stream)
    tree = parser.document()
    #lisp_tree_str = tree.toStringTree(recog=parser)
    #print(beautify_lisp_string(lisp_tree_str))
    get_table_size = GetTableSize()
    get_table_size.visit(tree)
    tag_dict = get_tag_dict()
    get_data = GetTableData(get_table_size.data, tag_dict)
    get_data.visit(tree)
    #print(get_data.data)
    latexc = LaTeXCode(get_data.data, tag_dict, args)
    result=latexc.visit(tree)
    result1 = ''
    result_len = len(result)
    for i in range(result_len):
        if (i + 1 < result_len) and result[i] == '\n' and result[i+1] == '\n':# and result[i+2] == '\n':
            i += 1
        else:
            result1 += result[i]
    #print(result1)
    texfile = path + '.tex'
    f = open(texfile, 'w', encoding=args.e)
    f.write(result1)
    f.close()
    print('\nantlr4_html2latex creates \'{}\'.\n'.format(os.path.basename(texfile)))
    
    

version = '0.5'
if __name__ == '__main__':
    aparser = argparse.ArgumentParser()
    aparser.add_argument("filename", help="set filename, for example test.html")    
    aparser.add_argument('-v', version='%(prog)s version {}'.format(version), action='version')    
    aparser.add_argument('-e', metavar='ENCODING',help="-e ascii or -e euc-jp or ... ,default = utf-8 ", default = 'utf-8')
    aparser.add_argument('-t', metavar='NOTBL',help="converting table  to tabular ,default = TBL", default = 'TBL')
    aparser.add_argument('-m',metavar='MOD', help="modifying html codes (optional tags, ..), default = NOMOD ", default = 'NOMOD')
    aparser.add_argument('-a',metavar='NOA', help="converting anchor to href, default = A ", default = 'A')
    aparser.add_argument('-i',metavar='NOIMG', help="converting img to includegraphics, default = IMG ", default = 'IMG')
    
    args = aparser.parse_args()
    print('\nThis is antlr4_html2latex version {}.'.format(version))
    filename = args.filename
    path, sf_ext = os.path.splitext(filename)
    if sf_ext[1:].find('html') == -1:
        print('extension error')
        sys.exit()    
    main(filename, args, [path, sf_ext])
    
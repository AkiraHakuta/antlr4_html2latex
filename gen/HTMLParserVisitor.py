# Generated from HTMLParser.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .HTMLParser import HTMLParser
else:
    from HTMLParser import HTMLParser

# This class defines a complete generic visitor for a parse tree produced by HTMLParser.

class HTMLParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by HTMLParser#document.
    def visitDocument(self, ctx:HTMLParser.DocumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#xml.
    def visitXml(self, ctx:HTMLParser.XmlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#content.
    def visitContent(self, ctx:HTMLParser.ContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#content_body.
    def visitContent_body(self, ctx:HTMLParser.Content_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#paired_tag.
    def visitPaired_tag(self, ctx:HTMLParser.Paired_tagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#single_tag.
    def visitSingle_tag(self, ctx:HTMLParser.Single_tagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#single_slash_tag.
    def visitSingle_slash_tag(self, ctx:HTMLParser.Single_slash_tagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#script_tag.
    def visitScript_tag(self, ctx:HTMLParser.Script_tagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#style_tag.
    def visitStyle_tag(self, ctx:HTMLParser.Style_tagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#attribute.
    def visitAttribute(self, ctx:HTMLParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#chardata.
    def visitChardata(self, ctx:HTMLParser.ChardataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#misc.
    def visitMisc(self, ctx:HTMLParser.MiscContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#scriptlet.
    def visitScriptlet(self, ctx:HTMLParser.ScriptletContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#script.
    def visitScript(self, ctx:HTMLParser.ScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#style.
    def visitStyle(self, ctx:HTMLParser.StyleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HTMLParser#xml_decl_open.
    def visitXml_decl_open(self, ctx:HTMLParser.Xml_decl_openContext):
        return self.visitChildren(ctx)



del HTMLParser

from __future__ import annotations

import abc
import lcdoc
from lcdoc import SymbolTable, Symbol, Declaration, TypeAliasSymbol
from typing import Iterator, Tuple
import typing
from doc_utils import DocBlock
from lcdoc import MethodSymbol
import doc_utils
from lcdoc import ClassSymbol

import string_utils

import clang.cindex

def show_list_CursorKind() -> None :
    for k in clang.cindex.CursorKind.get_all_kinds():
        print(k)

def get_cursor_kind(name : str) -> clang.cindex.CursorKind :
    return typing.cast(clang.cindex.CursorKind, getattr(clang.cindex.CursorKind, name))

CK_NAMESPACE   = get_cursor_kind("NAMESPACE")
CK_STRUCT_DECL : clang.cindex.CursorKind = clang.cindex.CursorKind.STRUCT_DECL
CK_CLASS_DECL  : clang.cindex.CursorKind = clang.cindex.CursorKind.CLASS_DECL
CK_CXX_METHOD  : clang.cindex.CursorKind = clang.cindex.CursorKind.CXX_METHOD
CK_TYPE_ALIAS_DECL  : clang.cindex.CursorKind = clang.cindex.CursorKind.TYPE_ALIAS_DECL

TK_VOID  : clang.cindex.TypeKind = clang.cindex.TypeKind.VOID
TK_INT  : clang.cindex.TypeKind = clang.cindex.TypeKind.INT
TK_RVALUEREFERENCE  : clang.cindex.TypeKind = clang.cindex.TypeKind.RVALUEREFERENCE
TK_LVALUEREFERENCE  : clang.cindex.TypeKind = clang.cindex.TypeKind.LVALUEREFERENCE
TK_POINTER  : clang.cindex.TypeKind = clang.cindex.TypeKind.POINTER
TK_ELABORATED  : clang.cindex.TypeKind = clang.cindex.TypeKind.ELABORATED
TK_AUTO  : clang.cindex.TypeKind = clang.cindex.TypeKind.AUTO

def get_access_specifier(name : str) -> clang.cindex.AccessSpecifier :
    return typing.cast(clang.cindex.AccessSpecifier, getattr(clang.cindex.AccessSpecifier, name))

AS_INVALID   = get_access_specifier("INVALID")
AS_PUBLIC    = get_access_specifier("PUBLIC")
AS_PROTECTED = get_access_specifier("PROTECTED")
AS_PRIVATE   = get_access_specifier("PRIVATE")
AS_NONE      = get_access_specifier("NONE")

class Node(lcdoc.Node) :

    cursor : clang.cindex.Cursor

    def __init__(self, cursor : clang.cindex.Cursor) -> None:
        super().__init__()

        self.cursor = cursor
    
    def spelling(self) -> str :
        return self.cursor.spelling

    def displayname(self) -> str :
        return self.cursor.displayname

    def file(self) -> str :
        return typing.cast(clang.cindex.SourceLocation, self.cursor.location).file.name
        
class Type :

    const_qualified : bool = False

    def __init__(self) -> None:
        pass

    @abc.abstractclassmethod
    def __repr__(self) -> str :
        pass

    @abc.abstractclassmethod
    def to_html(self, context : Symbol | None = None) -> str :
        pass

    def get_html_const_prefix(self) -> str :
        if self.const_qualified :
            return "<code-keyword>const</code-keyword> "
        return ""

class BasicType(Type) :
    ty : str = ""

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return self.ty

    def to_html(self, context : Symbol | None = None) -> str :
        assert self.ty
        return self.get_html_const_prefix() + f"<code-keyword>{self.ty}</code-keyword>"

class RValueRefType(Type) :
    to : Type | None = None

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        if self.to :
            return self.to.__repr__() + "&&"
        return "ERROR &&"

    def to_html(self, context : Symbol | None = None) -> str :
        assert self.to
        return self.get_html_const_prefix() + f"{self.to.to_html(context)}&&"

class LValueRefType(Type) :
    to : Type | None = None

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        if self.to :
            return self.to.__repr__() + "&"
        return "ERROR &"

    def to_html(self, context : Symbol | None = None) -> str :
        assert self.to
        return self.get_html_const_prefix() + f"{self.to.to_html(context)}&"

class PointerType(Type) :
    to : Type | None = None

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        if self.to :
            return self.to.__repr__() + "*"
        return "ERROR *"

    def to_html(self, context : Symbol | None = None) -> str :
        assert self.to
        if self.const_qualified :
            return self.to.to_html(context) + " " + self.get_html_const_prefix() + "*"
        return f"{self.to.to_html(context)}*"

class ClassType(Type) :

    classSymbol : ClassSymbol | None = None

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        if self.classSymbol :
            return self.classSymbol.__repr__()
        return "ERROR"

    def to_html(self, context : Symbol | None = None) -> str :
        assert self.classSymbol
        return self.get_html_const_prefix() + f"{self.classSymbol.to_html_full(context)} &"

class TypeAliasType(Type) :

    aliasSymbol : lcdoc.TypeAliasSymbol | None = None

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        if self.aliasSymbol :
            return self.aliasSymbol.__repr__()
        return "ERROR"

    def to_html(self, context : Symbol | None = None) -> str :
        assert self.aliasSymbol
        return self.get_html_const_prefix() + self.aliasSymbol.to_html_full(context)

class AutoType(Type) :

    deduced : Symbol | None = None

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        if self.deduced :
            return self.deduced.__repr__()
        return "ERROR"

    def to_html(self, context : Symbol | None = None) -> str :
        assert self.deduced
        return self.get_html_const_prefix() + self.deduced.to_html_full(context)

class ParsedDocument :

    filePath : str = ""

    symbolTable : SymbolTable

    declarations : list[Declaration]

    def __init__(self) -> None:
        self.symbolTable = SymbolTable()
        self.declarations = []

class Definition :

    defName : str = ""
    defValue : str = ""

    def __init__(self) -> None:
        pass

class FileOptions :
    includeDirs : list[str]
    definitions : list[Definition]

    def __init__(self) -> None:
        self.includeDirs = []
        self.definitions = []

    def merge(self, child : FileOptions) -> FileOptions :
        result = FileOptions()

        for i in self.includeDirs :
            result.includeDirs.append(i)
        for i in child.includeDirs :
            result.includeDirs.append(i)

        for d in self.definitions :
            result.definitions.append(d)
        for d in child.definitions :
            result.definitions.append(d)

        return result

class DocumentParser :

    includes : list[str]
    inFileOnly : bool = False

    m_filePath : str
    m_currDoc : ParsedDocument

    def __init__(self) -> None:
        self.includes = []

    def parse(self, filePath : str) -> ParsedDocument :

        self.m_filePath = filePath

        # https://clang.llvm.org/docs/ClangCommandLineReference.html
        args : list[str] = []
        for include in self.includes :
            args.append("-I%s" % include)
        args.append("--std=c++20")

        index : clang.cindex.Index = clang.cindex.Index.create()
        tu : clang.cindex.TranslationUnit = index.parse(filePath, args)
        #for d in tu.diagnostics.tu.cursor.get_children() :
        #    print(typing.cast(clang.cindex.Cursor, d).spelling, type(d))

        # The document Abstract Syntax Tree (AST)
        AST : list[clang.cindex.Cursor] = []
        for node in tu.cursor.get_children() :
            AST.append(node)

        doc = ParsedDocument()
        self.m_currDoc = doc
        doc.filePath = filePath

        self.findDeclarations(doc, AST)
        
        return doc

    def findDeclarations(self, doc : ParsedDocument, AST : list[clang.cindex.Cursor]) -> None :
        doc.declarations.clear()
        self.findDeclarations_impl(doc, AST)

    def findDeclarations_impl(self, doc : ParsedDocument, nodes : Iterator[clang.cindex.Cursor] | list[clang.cindex.Cursor], parent : Symbol | None = None) -> None :

        for node in nodes :
            #print(node.kind, node.spelling)

            if not node.spelling :
                # this because sometime "Unknown template argument kind 280" ValueError
                # exception i thrown
                continue

            if self.inFileOnly :
                location = typing.cast(clang.cindex.SourceLocation, node.location)
                assert location.file
                if location.file.name != self.m_filePath :
                    continue
            
            if node.kind == CK_NAMESPACE :
                symbol = self.find_symbol_or_add(doc, node, lcdoc.NamespaceSymbol, parent)
                self.findDeclarations_impl(doc, node.get_children(), symbol)
                continue

            if node.kind == CK_STRUCT_DECL :
                self.find_symbol_and_decl_or_add(doc, node, lcdoc.StructDeclaration, lcdoc.StructSymbol, parent)
                continue

            if node.kind == CK_CLASS_DECL :
                self.find_symbol_and_decl_or_add(doc, node, lcdoc.ClassDeclaration, lcdoc.ClassSymbol, parent)
                continue

            if node.kind == CK_CXX_METHOD :
                symbol, decl = self.find_symbol_and_decl_or_add(doc, node, lcdoc.MethodDeclaration, lcdoc.MethodSymbol, parent)
                symbol = typing.cast(lcdoc.MethodSymbol, symbol)
                symbol.ret = FuncArg()
                #symbol.ret.strType = typing.cast(clang.cindex.Type, typing.cast(clang.cindex.Type, node.result_type).get_canonical()).spelling
                symbol.ret.strType = typing.cast(clang.cindex.Type, node.result_type).spelling
                symbol.ret.typ = self.clangType_to_Type(typing.cast(clang.cindex.Type, node.result_type))
                AS = typing.cast(clang.cindex.AccessSpecifier, node.access_specifier)
                if AS == AS_PRIVATE :
                    symbol.access_specifier = lcdoc.AccessSpecifier.PRIVATE
                if AS == AS_PROTECTED :
                    symbol.access_specifier = lcdoc.AccessSpecifier.PROTECTED
                if AS == AS_PUBLIC :
                    symbol.access_specifier = lcdoc.AccessSpecifier.PUBLIC
                if AS == AS_INVALID or AS == AS_NONE :
                    assert False
                symbol.const_qualified = node.is_const_method()
                for a in node.get_arguments() :
                    arg = FuncArg()
                    argument = typing.cast(clang.cindex.Cursor, a)
                    argType = typing.cast(clang.cindex.Type, argument.type)
                    arg.name = argument.spelling
                    #arg.strType = typing.cast(clang.cindex.Type, argType.get_canonical()).
                    arg.strType = argType.spelling
                    arg.typ = self.clangType_to_Type(argType)
                    symbol = typing.cast(lcdoc.MethodSymbol, symbol)
                    symbol.args.clear()
                    symbol.args.append(arg)
                continue

            if node.kind == CK_TYPE_ALIAS_DECL :
                symbol, decl = self.find_symbol_and_decl_or_add(doc, node, lcdoc.TypeAliasDeclaration, lcdoc.TypeAliasSymbol, parent)
                # TODO TO WHAT????
                continue

            self.findDeclarations_impl(doc, node.get_children(), parent)

    def find_symbol_or_add(self, doc : ParsedDocument, node : clang.cindex.Cursor, symbol_type : type, parent : Symbol | None) -> Symbol :
        symbol = doc.symbolTable.find(node.mangled_name if node.mangled_name else node.spelling, symbol_type, parent)
        symbol = typing.cast(lcdoc.Symbol, symbol)
        if symbol == None :
            symbol = symbol_type()
            symbol = typing.cast(lcdoc.Symbol, symbol)
            symbol.mangledName = node.mangled_name
            symbol.name = node.spelling
            if not symbol.mangledName :
                symbol.mangledName = symbol.name
            if parent != None :
                symbol.addToParent(parent)
            doc.symbolTable.add(symbol)
        return symbol

    def find_symbol_and_decl_or_add(self, doc : ParsedDocument, node : clang.cindex.Cursor, decl_type : type, symbol_type : type, parent : Symbol | None) -> Tuple[ Symbol, Declaration ] :
        symbol = self.find_symbol_or_add(doc, node, symbol_type, parent)
        decl : Declaration | None = None
        for d in doc.declarations :
            if d.symbol == symbol :
                decl = d
                break
        if decl == None :
            decl = typing.cast(Declaration, decl_type(Node(node)))
            decl.symbol = symbol
            doc.declarations.append(decl)
        symbol.declaration = decl
        symbol.definition = decl
        #symbol.documentationString.brief =  ("brief: " + str(node.brief_comment)) if node.brief_comment else ""
        #symbol.documentationString.docStr += ("raw: " + string_utils.trimCommentLines(str(node.raw_comment))) if node.raw_comment else "" + "\n"
        symbol.documentationString.brief =  str(node.brief_comment) if node.brief_comment else ""
        symbol.documentationString.docStr += string_utils.trimCommentLines(str(node.raw_comment)) if node.raw_comment else "" + "\n"
        self.findDeclarations_impl(doc, node.get_children(), symbol)

        return symbol, decl

    def clangType_to_Type(self, cType : clang.cindex.Type) -> Type | None :
        if cType.kind == TK_VOID :
            result = BasicType()
            result.ty = "void"
            return result
        
        if cType.kind == TK_INT :
            result = BasicType()
            result.ty = "int"
            result.const_qualified = cType.is_const_qualified()
            return result
        
        if cType.kind == TK_RVALUEREFERENCE :
            ref = RValueRefType()
            ref.to = self.clangType_to_Type(cType.get_pointee())
            ref.const_qualified = cType.is_const_qualified()
            return ref

        if cType.kind == TK_LVALUEREFERENCE :
            ref = LValueRefType()
            ref.to = self.clangType_to_Type(cType.get_pointee())
            ref.const_qualified = cType.is_const_qualified()
            return ref

        if cType.kind == TK_POINTER :
            ptr = PointerType()
            ptr.to = self.clangType_to_Type(cType.get_pointee())
            ptr.const_qualified = cType.is_const_qualified()
            return ptr

        if cType.kind == TK_ELABORATED :
            cl = TypeAliasType()
            symbol = self.findSybolByCursor(cType.get_declaration())
            assert symbol
            cl.aliasSymbol = typing.cast(TypeAliasSymbol, symbol)
            cl.const_qualified = cType.is_const_qualified()
            return cl

        if cType.kind == TK_AUTO :
            au = AutoType()
            au.deduced = self.findSybolByCursor(cType.get_declaration())
            au.const_qualified = cType.is_const_qualified()
            return au

        print("unknown kind: ", cType.kind)
        
        return None

    def findSybolByCursor(self, cursor : clang.cindex.Cursor) -> Symbol | None :
        for symbol in self.m_currDoc.symbolTable.symbols :
            if symbol.definition :
                if cursor == typing.cast(Node, symbol.definition.node).cursor :
                    return symbol
        return None



class FuncArg(lcdoc.FuncArg) :
    strType : str = ""
    typ : Type | None = None
    pass

    def to_html_full(self) -> str :
        assert self.typ
        return self.typ.to_html() + " " + self.name



class Generator :

    symbolTable : SymbolTable

    def __init__(self) -> None:
        self.symbolTable = SymbolTable()

        # TODO REMOVE
        symbolTable = self.symbolTable
        std = lcdoc.NamespaceSymbol()
        std.name = "std"
        stringSymbol = lcdoc.ClassSymbol()
        stringSymbol.name = "basic_string"
        stringSymbol.addToParent(std)
        symbolTable.add(std)
        symbolTable.add(stringSymbol)

    def html(self, doc : ParsedDocument) :

        # https://stackoverflow.com/questions/46003452/how-to-correctly-write-a-raw-multiline-string-in-python
        # https://stackoverflow.com/questions/10660435/pythonic-way-to-create-a-long-multi-line-string
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>

    <link rel="stylesheet" href="https://lucaciucci99.com/css/style.css">
    <link rel="stylesheet" href="./style.css">

    <script async src="https://cdn.jsdelivr.net/npm/tex-math@latest/dist/tex-math.js"></script>
</head>
<body>

    <lc-content>
        <section>
            <article>
        """

        for symbol in doc.symbolTable.symbols :
            if isinstance(symbol, lcdoc.ClassSymbol) :
                html += "<article-page>%s</article-page>" % self.class_to_html_page(symbol)

        if False :
            for symbol in doc.symbolTable.symbols :
                if isinstance(symbol, lcdoc.ClassSymbol) or isinstance(symbol, lcdoc.StructSymbol) :
                    html += """
    <article-page>
    %s
    </article-page>
                    """ % self.class_to_html(symbol)
                    html += "\n"
            
            html += """
                </article>
            </section>
        </lc-content>

    </body>
    </html>
            """

        return html

    def class_to_html_page(self, classSymbol : lcdoc.ClassSymbol) -> str :
        html : str = ""

        classDoc = doc_utils.DocBlock()
        classDoc.parse(classSymbol.documentationString.docStr)

        # title
        html += f"<h1>{classSymbol.name}</h1>"

        # brief description
        html += f"<h2>{classSymbol.to_html_name()}</h2><hr>"
        html += f"<p>{classDoc.brief}</p>"
        #html += f"<p>{classSymbol.getCompleteName()}</p>"
        html += f"<p>Full Symbol:<pre><code>{classSymbol.to_html_full()}</code></pre></p>"

        # methods
        html += "<h2>Methods</h2>"
        rows : str = ""
        for child in classSymbol.children :
            if isinstance(child, MethodSymbol) :
                method : MethodSymbol = typing.cast(MethodSymbol, child)
                assert method.declaration
                node = typing.cast(Node, method.declaration.node)
                cursor = node.cursor
                row : str = ""
                #row += self.html_table_data(f"{self.symbol_str_highlight_to_html(typing.cast(FuncArg, method.ret).strType)}", "return-type")
                row += self.html_table_data(f"<code>{typing.cast(FuncArg, method.ret).typ.to_html()}</code>", "return-type")
                args : str = ""
                for arg in method.args[:-1] :
                    arg2 = typing.cast(FuncArg, arg)
                    args += f"{self.type_to_html(arg2.typ)} <code-mvar>{arg2.name}</code-mvar>, "
                if len(method.args) > 0 :
                    arg = method.args[-1]
                    arg2 = typing.cast(FuncArg, arg)
                    args += f"{arg2.typ.to_html()} <code-mvar>{arg2.name}</code-mvar>"
                doc = doc_utils.DocBlock()
                doc.parse(method.documentationString.docStr)
                row += self.html_table_data(f"""
<code><code-function>{method.name}</code-function>({args}){" <code-keyword>const</code-keyword>" if cursor.is_const_method() else ""}</code><br>{self.method_doc_to_html_details(doc, method)}
                """)
                rows += self.html_table_row(row)
        html += self.html_table(rows, "basic-table")

        return html

    def method_doc_to_html_details(self, doc : doc_utils.DocBlock, methodSymbol : lcdoc.MethodSymbol) -> str :
        if not doc.long :
            return doc.brief

        return f"""
<details>
    <summary>{doc.brief}</summary>
    {doc.long}
    {self.args_html_table_section(methodSymbol.args, doc)}
</details>
            """

    def args_html_table_section(self, args : list[lcdoc.FuncArg], methodDoc : doc_utils.DocBlock) -> str :
        if len(args) <= 0 :
            return ""
        return f"""
<h4>Parameters</h4>
{self.args_to_html_table(args, methodDoc)}
        """

    def args_to_html_table(self, args : list[lcdoc.FuncArg], methodDoc : doc_utils.DocBlock) -> str :
        rows : str = ""
        for _arg in args :
            arg = typing.cast(FuncArg, _arg)
            row : str = ""
            #row += self.html_table_data(f"<code>{arg.strType}</code>", "type")
            row += self.html_table_data(f"<code>{arg.typ.to_html()}</code>", "type")
            tmp = ""
            paramDocBlock = methodDoc.findParam(arg.name)
            if paramDocBlock :
                doc = doc_utils.DocBlock()
                doc.parse(paramDocBlock.descr)
                tmp = f"<details><summary>{doc.brief}</summary>{doc.long}</details>"
            row += self.html_table_data(f"<code><code-mvar>{arg.name}</code-mvar></code>{tmp}")
            rows += self.html_table_row(row)
        return self.html_table(rows, "basic-table")

    def html_table(self, content : str, classes : str = "") -> str :
        return f"""
<table class="{classes}">
{content}
</table>
        """

    def html_table_row(self, content : str, classes : str = "") -> str :
        return f"""
<tr class="{classes}">
{content}
</tr>
        """

    def html_table_data(self, content : str, classes : str = "") -> str :
        return f"""
<td class="{classes}">
{content}
</td>
        """

    def symbol_str_highlight_to_html(self, src : str) -> str :
        html : str = ""
        pieces = src.split()
        for piece in pieces :
            # keywords
            if self.isKeyword(piece) :
                html += f"<code-keyword>{piece}</code-keyword> "
                continue

            # symbol
            ss = piece.split("::")
            tot : str = ""
            for i in range(len(ss)) :
                symbol = self.findSymbol("::".join(ss[:i+1]))
                if not symbol :
                    if tot :
                        tot += "::"
                    tot += "::".join(ss[i:])
                    break
                if tot :
                    tot += "::"
                tot += self.get_symbol_html_name(symbol)
            if tot :
                html += tot
                continue

            # everything else
            html += piece + " "
        return html

    # TODO in which context and global if starts with ::
    def findSymbol(self, src : str) -> Symbol | None :
        if src.find("::") >= 0 :
            pass
        for symbol in self.symbolTable.symbols :
            if symbol.getCompleteName() == src :
                return symbol
        return None

    def isKeyword(self, name : str) -> bool :
        if name == "true" :
            return True
        if name == "false" :
            return True
        if name == "void" :
            return True
        if name == "int" :
            return True
        if name == "unsigned" :
            return True
        if name == "long" :
            return True
        if name == "const" :
            return True
        return False




# https://stackoverflow.com/questions/19079070/retrieving-comments-using-python-libclang
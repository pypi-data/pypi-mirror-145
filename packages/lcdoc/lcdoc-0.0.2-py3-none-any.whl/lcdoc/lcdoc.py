"""LC_NOTICE_BEGIN
LC_NOTICE_END"""


from __future__ import annotations
import abc
from enum import Enum
from operator import contains

from typing import Iterator

class DocumentationString :
    brief : str = ""
    docStr : str = ""

class Symbol :
    declaration : Declaration | None = None
    definition : Declaration | None = None

    name : str = ""
    mangledName : str = ""

    documentationString : DocumentationString

    parent : Symbol | None = None
    children : list[Symbol]

    def __init__(self) -> None:
        self.children = []
        self.documentationString = DocumentationString()

    def addToParent(self, parent : Symbol) -> None :
        if not contains(parent.children, self) :
            parent.children.append(self)
        self.parent = parent

    def getCompleteName(self) -> str :
        if (self.parent) :
            return self.parent.getCompleteName() + "!!" + self.name
        return self.name

    @abc.abstractclassmethod
    def to_html_name(self) -> str :
        pass

    def to_html_full(self, context : Symbol | None = None) -> str :
        if self.parent :
            if context :
                if self.parent == context :
                    return self.to_html_name()
            return self.parent.to_html_full() + "::" + self.to_html_name()
        return self.to_html_name()

class NamespaceSymbol(Symbol) :

    def getCompleteName(self) -> str :
        if isinstance(self.parent, NamespaceSymbol) :
            return self.parent.getCompleteName() + "::" + self.name
        return self.name

    def __repr__(self) -> str:
        return "namespace " + self.getCompleteName()

    def to_html_name(self) -> str :
        return f"<code-namespace>{self.name}</code-namespace>"

# abstract
class TypeSymbol(Symbol) :
    pass

class StructSymbol(TypeSymbol) :

    def getCompleteName(self) -> str :
        if isinstance(self.parent, NamespaceSymbol) :
            return self.parent.getCompleteName() + "::" + self.name
        return self.name

    def __repr__(self) -> str:
        return "struct " + self.getCompleteName()

    def to_html_name(self) -> str :
        return f"<code-class>{self.name}</code-class>"

class ClassSymbol(TypeSymbol) :

    def getCompleteName(self) -> str :
        if isinstance(self.parent, NamespaceSymbol) :
            return self.parent.getCompleteName() + "::" + self.name
        return self.name

    def __repr__(self) -> str:
        return "class " + self.getCompleteName()

    def to_html_name(self) -> str :
        return f"<code-class>{self.name}</code-class>"

class FuncArg :
    name : str = ""

    @abc.abstractmethod
    def to_html_full(self, context : Symbol | None = None) -> str :
        return f"\"{self.name}\""

class AccessSpecifier(Enum) :
    PRIVATE   =  0
    PUBLIC    = 1
    PROTECTED = 2

class MethodSymbol(Symbol) :

    args : list[FuncArg]

    ret : FuncArg

    access_specifier : AccessSpecifier
    
    const_qualified : bool = False

    def __init__(self) -> None:
        super().__init__()
        self.args = []
        self.ret = FuncArg()
        self.access_specifier = AccessSpecifier(AccessSpecifier.PUBLIC)

    def getCompleteName(self) -> str :
        if isinstance(self.parent, NamespaceSymbol) :
            return self.parent.getCompleteName() + "::" + self.name
        return self.name

    def __repr__(self) -> str:
        return "method " + self.getCompleteName()

    def to_html_name(self) -> str :
        return f"<code-function>{self.name}</code-function>"

    def to_html_full(self, context : Symbol | None = None) -> str :
        r : str = self.ret.to_html_full()
        # TODO params
        if self.parent :
            if context :
                if self.parent == context :
                    return r + " " + self.to_html_name()
            return r + " " + self.parent.to_html_full() + "::" + self.to_html_name()
        return r + " " + self.to_html_name()

class TypeAliasSymbol(TypeSymbol) :
    to : TypeSymbol | None = None

    def getCompleteName(self) -> str :
        if self.parent :
            return self.parent.getCompleteName() + "::" + self.name
        return self.name

    def __repr__(self) -> str:
        return "alias " + self.getCompleteName() + " to " + (self.to.__repr__() if self.to else "ERROR")

    def to_html_name(self) -> str :
        return f"<code-class>{self.name}</code-class>"

class SymbolTable :
    symbols : list[Symbol]
    root_symbols : list[Symbol]

    def __init__(self) -> None:
        self.symbols = []
        self.root_symbols = []

    def add(self, symbol : Symbol) -> None :
        self.symbols.append(symbol)
        if (symbol.parent == None) :
            self.root_symbols.append(symbol)

    def find(self, mangledName : str, class_type : type, parent : Symbol | None = None) -> Symbol | None :
        for symbol in self.symbols :
            if mangledName == symbol.mangledName and isinstance(symbol, class_type) :
                if parent :
                    if symbol.parent == parent :
                        return symbol
                    else :
                        return None
                return symbol
        return None

class Node :

    @abc.abstractclassmethod
    def spelling(self) -> str :
        pass

    @abc.abstractclassmethod
    def displayname(self) -> str :
        pass

    @abc.abstractclassmethod
    def file(self) -> str :
        pass


class Declaration :
    ciao : str = "aa"
    node : Node

    symbol : Symbol | None = None

    def __init__(self, node : Node) -> None :
        self.node = node

    def spelling(self) -> str :
        return self.node.spelling()

    def __str__(self) -> str:
        return self.__repr__()
        #return str(self.node.kind) + " " + self.node.spelling()

    def __repr__(self) -> str:
        # see https://docs.python.org/3/reference/datamodel.html#object.__repr__
        #return self.node.displayname()
        return self.node.spelling()

class StructDeclaration(Declaration) :

    def __init__(self, node : Node) -> None :
        super().__init__(node)

class ClassDeclaration(Declaration) :

    def __init__(self, node : Node) -> None :
        super().__init__(node)

class MethodDeclaration(Declaration) :

    def __init__(self, node : Node) -> None :
        super().__init__(node)

class TypeAliasDeclaration(Declaration) :

    def __init__(self, node : Node) -> None:
        super().__init__(node)
